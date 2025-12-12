"""
CR-V4 Cognitive Logic Core Module

This module implements the 'brain' of each simulated student,
generating realistic answers based on IRT and cognitive modeling.

COUNCIL DECISIONS IMPLEMENTED:
1. 3PL-IRT for answer generation
2. Fatigue and anxiety penalties
3. Slip and guess mechanics
4. Response time generation
5. Learning and forgetting dynamics
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Tuple
import math
import random

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from .genome import StudentGenome


# =============================================================================
# ENUMS
# =============================================================================

class AnswerOutcome(Enum):
    """Why the answer was correct/incorrect."""
    KNOWLEDGE_CORRECT = "knew_it"
    KNOWLEDGE_INCORRECT = "didnt_know"
    SLIP = "careless_error"
    LUCKY_GUESS = "guessed_right"
    SKIP = "skipped"
    TIMEOUT = "ran_out_of_time"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SessionState:
    """
    Dynamic state during a study session.
    
    This tracks the student's current condition
    which affects their performance.
    """
    session_start: datetime
    questions_attempted: int = 0
    questions_correct: int = 0
    current_fatigue: float = 0.0      # 0.0-1.0
    current_anxiety: float = 0.0       # 0.0-1.0
    current_frustration: float = 0.0   # 0.0-1.0
    breaks_taken: int = 0
    consecutive_wrong: int = 0
    consecutive_correct: int = 0
    total_time_minutes: float = 0.0
    
    @property
    def session_duration_minutes(self) -> float:
        """Minutes since session started."""
        return (datetime.now() - self.session_start).total_seconds() / 60
    
    @property
    def current_accuracy(self) -> float:
        """Session accuracy so far."""
        if self.questions_attempted == 0:
            return 0.5
        return self.questions_correct / self.questions_attempted


@dataclass
class QuestionContext:
    """Context about the question being attempted."""
    question_id: str
    concept_id: str
    subject: str
    difficulty_b: float      # IRT b parameter
    discrimination_a: float  # IRT a parameter
    guessing_c: float        # IRT c parameter
    is_high_stakes: bool     # Mock test vs practice
    time_limit_seconds: Optional[int] = None
    is_12th_content: bool = False  # For standard validation


@dataclass
class AnswerResult:
    """Result of an agent attempting a question."""
    is_correct: bool
    outcome: AnswerOutcome
    response_time_seconds: float
    theta_effective: float           # Ability used
    probability_correct: float       # P(correct) calculated
    fatigue_at_answer: float
    anxiety_at_answer: float
    confidence_self_report: float    # Agent's self-assessment (1-5)
    
    # Validation metadata
    standard_violation: bool = False  # True if 12th content given to 11th student


# =============================================================================
# COGNITIVE LOGIC CORE
# =============================================================================

class CognitiveLogicCore:
    """
    The 'brain' of the simulated student.
    
    Implements:
    - 3PL-IRT for answer generation
    - Fatigue and anxiety effects
    - Slip and guess mechanics
    - Response time generation
    - Learning and forgetting
    
    Council-approved constants are defined as class variables.
    """
    
    # === Council-approved constants ===
    FATIGUE_PENALTY_ALPHA: float = 0.15      # θ penalty per unit fatigue
    ANXIETY_PENALTY_BETA: float = 0.20       # θ penalty per unit anxiety
    BASE_SLIP_RATE: float = 0.02             # Base careless error rate
    FATIGUE_SLIP_MULTIPLIER: float = 0.08    # Additional slip from fatigue
    FATIGUE_GROWTH_PER_QUESTION: float = 0.01
    FATIGUE_GROWTH_PER_MINUTE: float = 0.005
    FATIGUE_DECAY_PER_BREAK: float = 0.20    # Fatigue reduction per break
    
    def __init__(self, genome: StudentGenome):
        """
        Initialize CLC with a student genome.
        
        Args:
            genome: The student's genome (hidden truth)
        """
        self.genome = genome
        self._session: Optional[SessionState] = None
    
    @property
    def session(self) -> Optional[SessionState]:
        """Get current session state."""
        return self._session
    
    def start_session(self) -> SessionState:
        """Start a new study session."""
        self._session = SessionState(session_start=datetime.now())
        return self._session
    
    def end_session(self):
        """End the current session."""
        self._session = None
    
    # =========================================================================
    # CORE IRT CALCULATIONS
    # =========================================================================
    
    def irt_probability(
        self,
        theta: float,
        a: float,
        b: float,
        c: float
    ) -> float:
        """
        Calculate 3PL IRT probability of correct answer.
        
        Formula: P(θ) = c + (1-c) × [1 / (1 + e^(-a(θ-b)))]
        
        Args:
            theta: Student ability (0-1 scale, mapped to IRT scale internally)
            a: Item discrimination (0.1-3.0)
            b: Item difficulty (-3 to +3)
            c: Guessing parameter (0-0.25 typically)
            
        Returns:
            Probability of correct answer (0-1)
        """
        # Map 0-1 theta to IRT scale (-3 to +3)
        theta_irt = (theta * 6) - 3
        
        # Guard against extreme values
        a = max(0.01, min(3.0, a))
        exponent = -a * (theta_irt - b)
        
        # Prevent overflow
        if exponent > 20:
            logistic = 0.0
        elif exponent < -20:
            logistic = 1.0
        else:
            logistic = 1.0 / (1.0 + math.exp(exponent))
        
        probability = c + (1.0 - c) * logistic
        return probability
    
    def calculate_effective_ability(
        self,
        concept_id: str,
        session_state: SessionState,
        question_context: QuestionContext
    ) -> float:
        """
        Calculate θ_effective accounting for fatigue and anxiety.
        
        Formula: θ_eff = θ_genome - (α × F) - (β × A)
        
        Args:
            concept_id: The concept being tested
            session_state: Current session state
            question_context: Context about the question
            
        Returns:
            Effective ability (0-1)
        """
        # Base ability from genome
        theta_genome = self.genome.knowledge.get_mastery(concept_id)
        
        # Current fatigue
        fatigue = session_state.current_fatigue
        
        # Calculate current anxiety
        base_anxiety = self.genome.psychometric.anxiety_trait
        stakes_multiplier = 1.5 if question_context.is_high_stakes else 1.0
        
        # Anxiety increases with consecutive failures
        failure_anxiety = min(0.2, session_state.consecutive_wrong * 0.04)
        
        anxiety = min(1.0, base_anxiety * stakes_multiplier + failure_anxiety)
        session_state.current_anxiety = anxiety
        
        # Apply penalties
        theta_effective = (
            theta_genome 
            - (self.FATIGUE_PENALTY_ALPHA * fatigue)
            - (self.ANXIETY_PENALTY_BETA * anxiety)
        )
        
        return max(0.0, min(1.0, theta_effective))
    
    def calculate_slip_probability(
        self,
        session_state: SessionState
    ) -> float:
        """
        Calculate probability of careless error.
        
        Slip increases with fatigue and cognitive load.
        
        Returns:
            Slip probability (0-0.20)
        """
        base_slip = self.BASE_SLIP_RATE
        fatigue_slip = self.FATIGUE_SLIP_MULTIPLIER * session_state.current_fatigue
        
        # Focus affects slip rate
        focus_factor = 1.5 - self.genome.psychometric.focus_stability
        
        total_slip = (base_slip + fatigue_slip) * focus_factor
        
        return min(0.20, total_slip)  # Cap at 20%
    
    # =========================================================================
    # ANSWER GENERATION
    # =========================================================================
    
    def generate_answer(
        self,
        question_context: QuestionContext,
        session_state: Optional[SessionState] = None
    ) -> AnswerResult:
        """
        Generate an answer based on agent's true state.
        
        This is the CORE simulation logic.
        
        Args:
            question_context: Information about the question
            session_state: Current session (uses internal if None)
            
        Returns:
            AnswerResult with all details
        """
        if session_state is None:
            if self._session is None:
                self.start_session()
            session_state = self._session
        
        # === CRITICAL: Standard validation ===
        standard_violation = False
        if question_context.is_12th_content and self.genome.standard == 11:
            if not self.genome.is_dropper:
                standard_violation = True
                # Log this as a CRITICAL violation
        
        # Step 1: Calculate effective ability
        theta_eff = self.calculate_effective_ability(
            question_context.concept_id,
            session_state,
            question_context
        )
        
        # Step 2: Get IRT probability
        prob_correct = self.irt_probability(
            theta=theta_eff,
            a=question_context.discrimination_a,
            b=question_context.difficulty_b,
            c=question_context.guessing_c
        )
        
        # Step 3: Determine if should guess (gamer behavior)
        should_guess = self._should_guess(theta_eff, session_state)
        
        # Step 4: Roll for answer
        roll = random.random()
        
        if should_guess:
            # Guessing: only c parameter matters
            is_correct = roll < question_context.guessing_c
            outcome = (AnswerOutcome.LUCKY_GUESS if is_correct 
                      else AnswerOutcome.KNOWLEDGE_INCORRECT)
            response_time = self._generate_guess_time()
        else:
            # Normal attempt
            if roll < prob_correct:
                # Would be correct, check for slip
                slip_prob = self.calculate_slip_probability(session_state)
                if random.random() < slip_prob:
                    is_correct = False
                    outcome = AnswerOutcome.SLIP
                else:
                    is_correct = True
                    outcome = AnswerOutcome.KNOWLEDGE_CORRECT
            else:
                # Incorrect attempt, check for lucky guess
                if random.random() < question_context.guessing_c:
                    is_correct = True
                    outcome = AnswerOutcome.LUCKY_GUESS
                else:
                    is_correct = False
                    outcome = AnswerOutcome.KNOWLEDGE_INCORRECT
            
            response_time = self._generate_response_time(
                theta_eff, 
                question_context.difficulty_b
            )
        
        # Step 5: Update session state
        self._update_session_state(session_state, is_correct)
        
        # Step 6: Generate self-reported confidence
        confidence = self._generate_confidence(theta_eff, is_correct)
        
        return AnswerResult(
            is_correct=is_correct,
            outcome=outcome,
            response_time_seconds=response_time,
            theta_effective=theta_eff,
            probability_correct=prob_correct,
            fatigue_at_answer=session_state.current_fatigue,
            anxiety_at_answer=session_state.current_anxiety,
            confidence_self_report=confidence,
            standard_violation=standard_violation,
        )
    
    def _should_guess(
        self,
        theta_effective: float,
        session_state: SessionState
    ) -> bool:
        """Determine if agent should guess rapidly."""
        # High guessing tendency + low ability = likely to guess
        guess_factor = self.genome.psychometric.guessing_tendency
        
        # More likely to guess when frustrated
        frustration_boost = session_state.current_frustration * 0.3
        
        # More likely to guess when ability is low for this question
        ability_factor = max(0, 0.5 - theta_effective)
        
        guess_probability = guess_factor * (0.3 + frustration_boost + ability_factor * 0.4)
        
        return random.random() < guess_probability
    
    def _generate_response_time(
        self,
        theta: float,
        difficulty: float
    ) -> float:
        """
        Generate realistic response time.
        
        Uses lognormal distribution for realistic variance.
        """
        # Map difficulty to 0-1 scale for comparison
        difficulty_normalized = (difficulty + 3) / 6
        gap = theta - difficulty_normalized
        
        # Base times by gap
        if gap > 0.3:
            base = 25.0  # Easy
            sigma = 0.3
        elif gap > 0:
            base = 50.0  # Moderate
            sigma = 0.4
        elif gap > -0.3:
            base = 90.0  # Hard
            sigma = 0.5
        else:
            base = 150.0  # Very hard
            sigma = 0.6
        
        # Apply processing speed
        base = base / self.genome.cognitive.processing_speed
        
        # Sample from lognormal
        if HAS_NUMPY:
            time = float(np.random.lognormal(np.log(base), sigma))
        else:
            time = math.exp(random.gauss(math.log(base), sigma))
        
        return min(300.0, max(5.0, time))
    
    def _generate_guess_time(self) -> float:
        """Generate fast guessing time (3-8 seconds)."""
        return random.uniform(3.0, 8.0)
    
    def _update_session_state(
        self,
        session_state: SessionState,
        is_correct: bool
    ):
        """Update session state after an answer."""
        session_state.questions_attempted += 1
        
        if is_correct:
            session_state.questions_correct += 1
            session_state.consecutive_correct += 1
            session_state.consecutive_wrong = 0
            session_state.current_frustration = max(
                0, session_state.current_frustration - 0.05
            )
        else:
            session_state.consecutive_wrong += 1
            session_state.consecutive_correct = 0
            session_state.current_frustration = min(
                1.0, session_state.current_frustration + 0.1
            )
        
        # Fatigue increases
        session_state.current_fatigue = min(
            1.0,
            session_state.current_fatigue + self.FATIGUE_GROWTH_PER_QUESTION
        )
    
    def _generate_confidence(
        self,
        theta: float,
        is_correct: bool
    ) -> float:
        """Generate self-reported confidence (1-5 scale)."""
        base_confidence = theta * 4 + 1  # Maps 0-1 to 1-5
        
        # Anxious students underreport
        if self.genome.psychometric.anxiety_trait > 0.6:
            base_confidence -= 0.5
        
        # Perfectionists are never fully confident
        if self.genome.psychometric.perfectionism > 0.7:
            base_confidence = min(4.0, base_confidence)
        
        # Add noise
        noise = random.gauss(0, 0.3)
        
        return max(1.0, min(5.0, base_confidence + noise))
    
    # =========================================================================
    # LEARNING AND FORGETTING
    # =========================================================================
    
    def apply_learning(
        self,
        concept_id: str,
        was_correct: bool,
        content_quality: float = 0.8
    ):
        """
        Update genome after learning interaction.
        
        Args:
            concept_id: The concept learned
            was_correct: If the interaction was successful
            content_quality: Quality of content (0-1)
        """
        iq = self.genome.cognitive.iq_factor
        
        if was_correct:
            # Positive reinforcement
            gain = 0.03 * iq * content_quality
            self.genome.knowledge.update_mastery(concept_id, gain)
        else:
            # Small negative effect (learning from mistakes)
            # But not as much gain as getting it right
            gain = 0.01 * iq * content_quality
            self.genome.knowledge.update_mastery(concept_id, gain)
    
    def apply_forgetting(
        self,
        concept_id: str,
        days_elapsed: float
    ):
        """
        Apply forgetting curve decay.
        
        Uses retention = exp(-t / (θ × 30 + 5))
        
        Higher mastery = slower forgetting.
        
        Args:
            concept_id: The concept to decay
            days_elapsed: Days since last interaction
        """
        current = self.genome.knowledge.get_mastery(concept_id)
        
        # Higher mastery = slower forgetting
        decay_rate = 30 * current + 5
        retention = math.exp(-days_elapsed / decay_rate)
        
        # Apply decay (never below 0.1)
        decayed = 0.1 + (current - 0.1) * retention
        
        self.genome.knowledge.set_mastery(concept_id, decayed)
    
    def take_break(self, session_state: SessionState, minutes: float = 10):
        """
        Simulate taking a break.
        
        Reduces fatigue based on break duration.
        
        Args:
            session_state: Current session
            minutes: Break duration
        """
        session_state.breaks_taken += 1
        
        # Fatigue reduction based on break length
        reduction = min(0.4, self.FATIGUE_DECAY_PER_BREAK * (minutes / 10))
        session_state.current_fatigue = max(0, session_state.current_fatigue - reduction)
        
        # Anxiety also reduces slightly
        session_state.current_anxiety = max(0, session_state.current_anxiety - 0.05)
