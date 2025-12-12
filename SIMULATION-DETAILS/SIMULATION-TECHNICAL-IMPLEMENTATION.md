# CR-V4 SIMULATION SYSTEM - PART 3: TECHNICAL IMPLEMENTATION
# Complete Code Structures, Data Models, and Execution Flow

**Document Class:** Technical Implementation Specification  
**Version:** 1.0  
**Date:** December 11, 2024  

---

# SECTION C: COMPLETE DATA MODELS

## C.1 GENOME DATA STRUCTURES

### C.1.1 Complete StudentGenome Class

```python
"""
simulation/agents/genome.py
Complete student genome implementation.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum, auto
from typing import Dict, List, Literal, Optional, Tuple
import random
import math
import uuid


class PersonaType(Enum):
    """8 distinct student archetypes."""
    STRUGGLING_PERSISTER = auto()
    ANXIOUS_PERFECTIONIST = auto()
    DISENGAGED_GAMER = auto()
    CONCEPTUALLY_GAPPED = auto()
    STEADY_LEARNER = auto()
    FAST_TRACKER = auto()
    LATE_JOINER = auto()
    DROPPER = auto()


class LoginTimePreference(Enum):
    """When student typically studies."""
    EARLY_MORNING = "05:00-08:00"
    MORNING = "08:00-12:00"
    AFTERNOON = "12:00-17:00"
    EVENING = "17:00-21:00"
    NIGHT = "21:00-01:00"
    LATE_NIGHT = "01:00-05:00"


@dataclass
class CognitiveCapacity:
    """
    Stable cognitive traits (the 'hardware').
    
    These traits are immutable for a given agent and
    represent their baseline cognitive capabilities.
    """
    iq_factor: float              # 0.0-1.0, learning speed multiplier
    working_memory_limit: int     # 3-9 items (Miller's Law)
    processing_speed: float       # 0.5-2.0, response time multiplier
    attention_span_minutes: int   # 15-90 minutes typical
    
    def __post_init__(self):
        assert 0.0 <= self.iq_factor <= 1.0
        assert 3 <= self.working_memory_limit <= 9
        assert 0.5 <= self.processing_speed <= 2.0
        assert 15 <= self.attention_span_minutes <= 90


@dataclass
class PsychometricProfile:
    """
    Behavioral and emotional traits.
    
    These influence HOW the student learns and responds
    to challenges, successes, and failures.
    """
    grit_index: float            # 0.0-1.0, resilience to failure
    anxiety_trait: float         # 0.0-1.0, baseline test anxiety
    focus_stability: float       # 0.0-1.0, attention consistency
    guessing_tendency: float     # 0.0-1.0, likelihood to guess when unsure
    perfectionism: float         # 0.0-1.0, need for perfect scores
    risk_tolerance: float        # 0.0-1.0, willingness to try hard questions
    
    def __post_init__(self):
        for attr in ['grit_index', 'anxiety_trait', 'focus_stability',
                     'guessing_tendency', 'perfectionism', 'risk_tolerance']:
            val = getattr(self, attr)
            assert 0.0 <= val <= 1.0, f"{attr} must be 0-1, got {val}"


@dataclass
class KnowledgeState:
    """
    Dynamic knowledge representation.
    
    This is the GROUND TRUTH that the platform's AI
    is trying to estimate.
    """
    kc_mastery_map: Dict[str, float]      # concept_id → mastery (0.0-1.0)
    kc_last_interaction: Dict[str, datetime]  # concept_id → last seen
    misconceptions: List[str]              # Active misconception IDs
    prereq_gaps: List[str]                 # Known prerequisite gaps
    
    def get_mastery(self, concept_id: str) -> float:
        """Get mastery, defaulting to 0.3 for unseen concepts."""
        return self.kc_mastery_map.get(concept_id, 0.3)
    
    def update_mastery(self, concept_id: str, delta: float):
        """Update mastery with bounds checking."""
        current = self.get_mastery(concept_id)
        new_value = max(0.0, min(1.0, current + delta))
        self.kc_mastery_map[concept_id] = new_value
        self.kc_last_interaction[concept_id] = datetime.now()


@dataclass
class TemporalContext:
    """
    Time-based context for the student.
    """
    join_date: date
    standard: Literal[11, 12]
    target_exam_date: date
    is_dropper: bool = False
    previous_attempts: int = 0
    previous_best_percentile: Optional[float] = None
    
    @property
    def days_to_exam(self) -> int:
        """Days remaining to target exam."""
        return (self.target_exam_date - date.today()).days
    
    @property
    def months_on_platform(self) -> float:
        """Months since joining."""
        return (date.today() - self.join_date).days / 30.0


@dataclass
class BehavioralPatterns:
    """
    Behavioral tendencies for realistic simulation.
    """
    login_time_preference: LoginTimePreference
    session_length_mean: float    # Average session in minutes
    session_length_std: float     # Standard deviation
    consistency_factor: float     # 0.0-1.0, schedule adherence
    study_hours_per_day: float    # Typical daily study time
    weekend_multiplier: float     # Study intensity on weekends
    break_frequency: float        # How often takes breaks (per hour)
    
    def sample_session_length(self) -> float:
        """Sample a session length from distribution."""
        length = random.gauss(self.session_length_mean, self.session_length_std)
        return max(10.0, min(180.0, length))  # 10 min to 3 hours


@dataclass
class StudentGenome:
    """
    Complete student genome - the HIDDEN TRUTH.
    
    This is the ground truth that the simulation uses
    to generate realistic behavior. The platform's AI
    must try to estimate this from observable actions.
    """
    # Identity
    genome_id: str
    persona_type: PersonaType
    
    # Component structures
    cognitive: CognitiveCapacity
    psychometric: PsychometricProfile
    knowledge: KnowledgeState
    temporal: TemporalContext
    behavioral: BehavioralPatterns
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0"
    
    def to_dict(self) -> dict:
        """Serialize genome for storage."""
        return {
            "genome_id": self.genome_id,
            "persona_type": self.persona_type.name,
            "cognitive": {
                "iq_factor": self.cognitive.iq_factor,
                "working_memory_limit": self.cognitive.working_memory_limit,
                "processing_speed": self.cognitive.processing_speed,
                "attention_span_minutes": self.cognitive.attention_span_minutes,
            },
            "psychometric": {
                "grit_index": self.psychometric.grit_index,
                "anxiety_trait": self.psychometric.anxiety_trait,
                "focus_stability": self.psychometric.focus_stability,
                "guessing_tendency": self.psychometric.guessing_tendency,
                "perfectionism": self.psychometric.perfectionism,
                "risk_tolerance": self.psychometric.risk_tolerance,
            },
            "knowledge": {
                "kc_mastery_map": self.knowledge.kc_mastery_map,
                "misconceptions": self.knowledge.misconceptions,
                "prereq_gaps": self.knowledge.prereq_gaps,
            },
            "temporal": {
                "join_date": self.temporal.join_date.isoformat(),
                "standard": self.temporal.standard,
                "target_exam_date": self.temporal.target_exam_date.isoformat(),
                "is_dropper": self.temporal.is_dropper,
            },
            "behavioral": {
                "login_time_preference": self.behavioral.login_time_preference.name,
                "session_length_mean": self.behavioral.session_length_mean,
                "study_hours_per_day": self.behavioral.study_hours_per_day,
            },
        }
```

### C.1.2 Persona Configuration

```python
"""
simulation/agents/personas.py
Persona-specific configuration for genome generation.
"""

from dataclasses import dataclass
from typing import Dict, Tuple
from .genome import PersonaType


@dataclass
class PersonaConfig:
    """Configuration for a persona type."""
    
    # Distribution percentages
    population_percentage: float
    
    # Cognitive means (will sample around these)
    iq_mean: float
    iq_std: float
    working_memory_mean: int
    processing_speed_mean: float
    
    # Psychometric means
    grit_mean: float
    anxiety_mean: float
    focus_mean: float
    guessing_mean: float
    
    # Knowledge initialization
    starting_mastery_mean: float
    prereq_gaps_count: int
    misconception_count: int
    
    # Behavioral defaults
    study_hours_mean: float
    session_length_mean: float


PERSONA_CONFIGS: Dict[PersonaType, PersonaConfig] = {
    
    PersonaType.STRUGGLING_PERSISTER: PersonaConfig(
        population_percentage=0.15,
        iq_mean=0.35, iq_std=0.10,
        working_memory_mean=5,
        processing_speed_mean=0.7,
        grit_mean=0.85, anxiety_mean=0.40,
        focus_mean=0.50, guessing_mean=0.20,
        starting_mastery_mean=0.30,
        prereq_gaps_count=5,
        misconception_count=3,
        study_hours_mean=4.0,
        session_length_mean=45.0,
    ),
    
    PersonaType.ANXIOUS_PERFECTIONIST: PersonaConfig(
        population_percentage=0.12,
        iq_mean=0.80, iq_std=0.10,
        working_memory_mean=7,
        processing_speed_mean=1.0,
        grit_mean=0.70, anxiety_mean=0.85,
        focus_mean=0.70, guessing_mean=0.10,
        starting_mastery_mean=0.60,
        prereq_gaps_count=1,
        misconception_count=2,
        study_hours_mean=6.0,
        session_length_mean=60.0,
    ),
    
    PersonaType.DISENGAGED_GAMER: PersonaConfig(
        population_percentage=0.10,
        iq_mean=0.55, iq_std=0.15,
        working_memory_mean=6,
        processing_speed_mean=1.3,
        grit_mean=0.20, anxiety_mean=0.20,
        focus_mean=0.30, guessing_mean=0.75,
        starting_mastery_mean=0.35,
        prereq_gaps_count=4,
        misconception_count=5,
        study_hours_mean=1.5,
        session_length_mean=20.0,
    ),
    
    PersonaType.CONCEPTUALLY_GAPPED: PersonaConfig(
        population_percentage=0.15,
        iq_mean=0.65, iq_std=0.12,
        working_memory_mean=6,
        processing_speed_mean=1.0,
        grit_mean=0.60, anxiety_mean=0.50,
        focus_mean=0.55, guessing_mean=0.30,
        starting_mastery_mean=0.50,
        prereq_gaps_count=8,  # Key: many gaps
        misconception_count=4,
        study_hours_mean=3.5,
        session_length_mean=50.0,
    ),
    
    PersonaType.STEADY_LEARNER: PersonaConfig(
        population_percentage=0.28,  # Largest group
        iq_mean=0.55, iq_std=0.10,
        working_memory_mean=6,
        processing_speed_mean=1.0,
        grit_mean=0.55, anxiety_mean=0.45,
        focus_mean=0.55, guessing_mean=0.25,
        starting_mastery_mean=0.40,
        prereq_gaps_count=3,
        misconception_count=3,
        study_hours_mean=3.0,
        session_length_mean=45.0,
    ),
    
    PersonaType.FAST_TRACKER: PersonaConfig(
        population_percentage=0.10,
        iq_mean=0.90, iq_std=0.05,
        working_memory_mean=8,
        processing_speed_mean=1.5,
        grit_mean=0.75, anxiety_mean=0.30,
        focus_mean=0.80, guessing_mean=0.15,
        starting_mastery_mean=0.65,
        prereq_gaps_count=1,
        misconception_count=1,
        study_hours_mean=4.0,
        session_length_mean=90.0,
    ),
    
    PersonaType.LATE_JOINER: PersonaConfig(
        population_percentage=0.06,
        iq_mean=0.60, iq_std=0.15,
        working_memory_mean=6,
        processing_speed_mean=1.1,
        grit_mean=0.65, anxiety_mean=0.70,
        focus_mean=0.60, guessing_mean=0.30,
        starting_mastery_mean=0.45,
        prereq_gaps_count=4,
        misconception_count=4,
        study_hours_mean=5.5,  # Panic studying
        session_length_mean=75.0,
    ),
    
    PersonaType.DROPPER: PersonaConfig(
        population_percentage=0.04,
        iq_mean=0.65, iq_std=0.15,
        working_memory_mean=6,
        processing_speed_mean=1.0,
        grit_mean=0.75, anxiety_mean=0.65,
        focus_mean=0.60, guessing_mean=0.25,
        starting_mastery_mean=0.55,  # Has some prep
        prereq_gaps_count=3,
        misconception_count=3,
        study_hours_mean=6.0,
        session_length_mean=90.0,
    ),
}
```

---

## C.2 COGNITIVE LOGIC CORE

### C.2.1 Complete CLC Implementation

```python
"""
simulation/agents/cognitive_core.py
The brain of each simulated student.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Tuple
import math
import random
import numpy as np

from .genome import StudentGenome


class AnswerOutcome(Enum):
    """Why the answer was correct/incorrect."""
    KNOWLEDGE_CORRECT = "knew_it"
    KNOWLEDGE_INCORRECT = "didnt_know"
    SLIP = "careless_error"
    LUCKY_GUESS = "guessed_right"
    SKIP = "skipped"
    TIMEOUT = "ran_out_of_time"


@dataclass
class SessionState:
    """Dynamic state during a study session."""
    session_start: datetime
    questions_attempted: int = 0
    questions_correct: int = 0
    current_fatigue: float = 0.0      # 0.0-1.0
    current_anxiety: float = 0.0       # 0.0-1.0
    current_frustration: float = 0.0   # 0.0-1.0
    breaks_taken: int = 0
    consecutive_wrong: int = 0
    consecutive_correct: int = 0
    
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
    confidence_self_report: float    # Agent's self-assessment


class CognitiveLogicCore:
    """
    The 'brain' of the simulated student.
    
    Implements:
    - 3PL-IRT for answer generation
    - Fatigue and anxiety effects
    - Slip and guess mechanics
    - Response time generation
    - Learning and forgetting
    """
    
    # Council-approved constants
    FATIGUE_PENALTY_ALPHA = 0.15
    ANXIETY_PENALTY_BETA = 0.20
    BASE_SLIP_RATE = 0.02
    FATIGUE_SLIP_MULTIPLIER = 0.08
    FATIGUE_GROWTH_PER_QUESTION = 0.01
    FATIGUE_GROWTH_PER_MINUTE = 0.005
    
    def __init__(self, genome: StudentGenome):
        self.genome = genome
    
    def calculate_effective_ability(
        self,
        concept_id: str,
        session_state: SessionState,
        question_context: QuestionContext
    ) -> float:
        """
        Calculate θ_effective accounting for fatigue and anxiety.
        
        Formula: θ_eff = θ_genome - (α × F) - (β × A)
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
    
    def irt_probability(
        self,
        theta: float,
        a: float,
        b: float,
        c: float
    ) -> float:
        """
        Calculate 3PL IRT probability.
        
        P(θ) = c + (1-c) × [1 / (1 + e^(-a(θ-b)))]
        """
        # Guard against extreme values
        a = max(0.01, a)
        exponent = -a * (theta - b)
        exponent = max(-20, min(20, exponent))  # Prevent overflow
        
        logistic = 1.0 / (1.0 + math.exp(exponent))
        probability = c + (1.0 - c) * logistic
        
        return probability
    
    def calculate_slip_probability(
        self,
        session_state: SessionState
    ) -> float:
        """
        Calculate probability of careless error.
        
        Slip increases with fatigue and cognitive load.
        """
        base_slip = self.BASE_SLIP_RATE
        fatigue_slip = self.FATIGUE_SLIP_MULTIPLIER * session_state.current_fatigue
        
        # Focus affects slip rate
        focus_factor = 1.5 - self.genome.psychometric.focus_stability
        
        total_slip = (base_slip + fatigue_slip) * focus_factor
        
        return min(0.20, total_slip)  # Cap at 20%
    
    def generate_answer(
        self,
        question_context: QuestionContext,
        session_state: SessionState
    ) -> AnswerResult:
        """
        Generate an answer based on agent's true state.
        
        This is the core simulation logic.
        """
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
            confidence_self_report=confidence
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
        
        # More likely to guess when ability is low
        ability_factor = 1.0 - theta_effective
        
        guess_probability = guess_factor * (0.3 + frustration_boost + ability_factor * 0.4)
        
        return random.random() < guess_probability
    
    def _generate_response_time(
        self,
        theta: float,
        difficulty: float
    ) -> float:
        """Generate realistic response time."""
        gap = theta - difficulty
        
        # Base times by gap
        if gap > 0.5:
            base = 25.0  # Easy
            sigma = 0.3
        elif gap > 0:
            base = 50.0  # Moderate
            sigma = 0.4
        elif gap > -0.5:
            base = 90.0  # Hard
            sigma = 0.5
        else:
            base = 150.0  # Very hard
            sigma = 0.6
        
        # Apply processing speed
        base = base / self.genome.cognitive.processing_speed
        
        # Sample from lognormal
        time = np.random.lognormal(np.log(base), sigma)
        
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
        """Generate self-reported confidence (0-5 scale)."""
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
    
    def apply_learning(
        self,
        concept_id: str,
        was_correct: bool,
        content_quality: float = 0.8
    ):
        """
        Update genome after learning interaction.
        
        Uses simplified Ebbinghaus model.
        """
        iq = self.genome.cognitive.iq_factor
        
        if was_correct:
            # Positive reinforcement
            gain = 0.03 * iq * content_quality
            self.genome.knowledge.update_mastery(concept_id, gain)
        else:
            # Small negative effect
            loss = -0.015
            self.genome.knowledge.update_mastery(concept_id, loss)
    
    def apply_forgetting(
        self,
        concept_id: str,
        days_elapsed: float
    ):
        """
        Apply forgetting curve decay.
        
        Uses retention = exp(-t / (θ × 30 + 5))
        """
        current = self.genome.knowledge.get_mastery(concept_id)
        
        # Higher mastery = slower forgetting
        decay_rate = 30 * current + 5
        retention = math.exp(-days_elapsed / decay_rate)
        
        # Apply decay (never below 0.1)
        decayed = 0.1 + (current - 0.1) * retention
        
        self.genome.knowledge.kc_mastery_map[concept_id] = decayed
```

---

## C.3 TRUST ENGINE

### C.3.1 Complete Trust Implementation

```python
"""
simulation/agents/trust_engine.py
Trust and compliance dynamics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
import random

from .genome import StudentGenome


class TrustZone(Enum):
    """Trust level zones."""
    HIGH = "high"           # T > 0.8
    SKEPTIC = "skeptic"     # 0.4 < T < 0.8
    DANGER = "danger"       # 0.1 < T < 0.4
    CHURN = "churn"         # T < 0.1


class AgentAction(Enum):
    """Possible agent actions."""
    FOLLOW_RECOMMENDATION = "follow"
    BROWSE_MANUALLY = "browse"
    SKIP_SESSION = "skip"
    RAPID_GUESS = "game"
    DO_MINIMUM = "minimum"
    LEAVE_PLATFORM = "churn"


class RecommendationQuality(Enum):
    """Quality of platform recommendation."""
    FLOW = "flow"           # Optimal challenge
    NEUTRAL = "neutral"     # Acceptable
    INSULT = "insult"       # Too easy
    FRUSTRATION = "frustration"  # Too hard


@dataclass
class TrustState:
    """Agent's trust in the platform."""
    trust_score: float = 1.0
    insult_count: int = 0
    frustration_count: int = 0
    flow_count: int = 0
    interactions_total: int = 0
    last_decay: datetime = field(default_factory=datetime.now)
    churn_triggered: bool = False
    
    @property
    def zone(self) -> TrustZone:
        """Get current trust zone."""
        if self.trust_score > 0.8:
            return TrustZone.HIGH
        elif self.trust_score > 0.4:
            return TrustZone.SKEPTIC
        elif self.trust_score > 0.1:
            return TrustZone.DANGER
        else:
            return TrustZone.CHURN
    
    @property
    def at_risk(self) -> bool:
        """Is agent at risk of churning?"""
        return self.zone in (TrustZone.DANGER, TrustZone.CHURN)


@dataclass
class Recommendation:
    """A recommendation from the platform."""
    question_id: str
    concept_id: str
    difficulty: float
    is_primary: bool = True


class TrustEngine:
    """
    Manages trust dynamics and compliance decisions.
    """
    
    # Trust delta values (council-approved)
    DELTA_FLOW = +0.02
    DELTA_NEUTRAL = 0.00
    DELTA_INSULT = -0.05
    DELTA_FRUSTRATION = -0.10
    
    # Passive decay
    DECAY_FACTOR = 0.99
    
    # Early interaction multiplier
    FIRST_IMPRESSION_LIMIT = 10
    FIRST_IMPRESSION_MULTIPLIER = 2.0
    
    def __init__(self, genome: StudentGenome):
        self.genome = genome
        self.state = TrustState()
    
    def evaluate_recommendation(
        self,
        recommendation: Recommendation
    ) -> RecommendationQuality:
        """
        Evaluate how the agent perceives a recommendation.
        
        Based on gap between agent's ability and recommendation difficulty.
        """
        # Get agent's true ability for this concept
        theta = self.genome.knowledge.get_mastery(recommendation.concept_id)
        diff = recommendation.difficulty
        
        gap = abs(theta - diff)
        
        if gap < 0.3:
            return RecommendationQuality.FLOW
        elif diff < theta - 0.5:
            return RecommendationQuality.INSULT
        elif diff > theta + 0.5:
            return RecommendationQuality.FRUSTRATION
        else:
            return RecommendationQuality.NEUTRAL
    
    def update_trust(
        self,
        quality: RecommendationQuality
    ) -> float:
        """
        Update trust score based on recommendation quality.
        
        Returns the new trust score.
        """
        self.state.interactions_total += 1
        
        # Get base delta
        delta = {
            RecommendationQuality.FLOW: self.DELTA_FLOW,
            RecommendationQuality.NEUTRAL: self.DELTA_NEUTRAL,
            RecommendationQuality.INSULT: self.DELTA_INSULT,
            RecommendationQuality.FRUSTRATION: self.DELTA_FRUSTRATION,
        }[quality]
        
        # First impressions weighted more heavily
        if self.state.interactions_total <= self.FIRST_IMPRESSION_LIMIT:
            delta *= self.FIRST_IMPRESSION_MULTIPLIER
        
        # Low-grit students are more sensitive to negative
        if delta < 0:
            grit_factor = 2.0 - self.genome.psychometric.grit_index
            delta *= grit_factor
        
        # Apply passive decay
        self.state.trust_score *= self.DECAY_FACTOR
        
        # Apply delta
        self.state.trust_score += delta
        self.state.trust_score = max(0.0, min(1.0, self.state.trust_score))
        
        # Track counts
        if quality == RecommendationQuality.FLOW:
            self.state.flow_count += 1
        elif quality == RecommendationQuality.INSULT:
            self.state.insult_count += 1
        elif quality == RecommendationQuality.FRUSTRATION:
            self.state.frustration_count += 1
        
        # Check for churn
        if self.state.trust_score < 0.1:
            self.state.churn_triggered = True
        
        return self.state.trust_score
    
    def decide_action(
        self,
        recommendation: Recommendation
    ) -> AgentAction:
        """
        Decide what action the agent takes.
        
        Depends on trust level and personality.
        """
        if self.state.churn_triggered:
            return AgentAction.LEAVE_PLATFORM
        
        zone = self.state.zone
        
        if zone == TrustZone.HIGH:
            # Very compliant
            return AgentAction.FOLLOW_RECOMMENDATION
        
        elif zone == TrustZone.SKEPTIC:
            # Sometimes non-compliant
            roll = random.random()
            if roll < 0.25:
                return AgentAction.BROWSE_MANUALLY
            return AgentAction.FOLLOW_RECOMMENDATION
        
        elif zone == TrustZone.DANGER:
            # High non-compliance
            roll = random.random()
            if roll < 0.2:
                return AgentAction.RAPID_GUESS  # Gaming
            elif roll < 0.4:
                return AgentAction.SKIP_SESSION
            elif roll < 0.6:
                return AgentAction.DO_MINIMUM
            return AgentAction.FOLLOW_RECOMMENDATION
        
        else:  # CHURN
            return AgentAction.LEAVE_PLATFORM
```

---

## C.4 GOD-VIEW OBSERVER

### C.4.1 Observer Implementation

```python
"""
simulation/observer/god_view.py
The all-seeing validation system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import math

from ..agents.genome import StudentGenome


class ViolationType(Enum):
    """Types of validation violations."""
    COLD_START_HALLUCINATION = "cold_start"
    FATIGUE_BLINDNESS = "fatigue_blind"
    GAMING_NOT_DETECTED = "gaming_miss"
    FORGETTING_LAG = "forget_lag"
    BURNOUT_FALSE_POSITIVE = "burnout_fp"
    BURNOUT_FALSE_NEGATIVE = "burnout_fn"
    ROOT_CAUSE_WRONG = "root_wrong"
    OVER_CONFIDENCE = "over_conf"


class Severity(Enum):
    """Violation severity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Violation:
    """A detected validation violation."""
    violation_type: ViolationType
    severity: Severity
    agent_id: str
    timestamp: datetime
    message: str
    genome_value: float
    inferred_value: float
    discrepancy: float
    
    @property
    def is_critical(self) -> bool:
        return self.severity == Severity.CRITICAL


@dataclass
class TruthFidelityMetrics:
    """Aggregate metrics for truth fidelity."""
    total_agents: int
    total_comparisons: int
    rmse: float                    # Root Mean Square Error
    mae: float                     # Mean Absolute Error
    max_discrepancy: float
    violations_count: int
    critical_violations: int
    trust_retention_rate: float    # % with trust > 0.5
    diagnostic_precision: float    # Correct gap identification


class GodViewObserver:
    """
    Validates platform AI against ground truth genomes.
    
    Has access to:
    - All agent genomes (hidden truth)
    - All platform inferred states
    - Compares and flags discrepancies
    """
    
    # Thresholds (council-approved)
    COLD_START_INTERACTION_LIMIT = 10
    COLD_START_CONFIDENCE_THRESHOLD = 0.3
    FATIGUE_THRESHOLD = 0.7
    MASTERY_DROP_THRESHOLD = 0.2
    GAMING_RESPONSE_TIME_THRESHOLD = 5.0
    FORGETTING_LAG_DAYS = 7
    
    def __init__(self):
        self.genomes: Dict[str, StudentGenome] = {}
        self.violations: List[Violation] = []
        self.comparison_log: List[dict] = []
    
    def register_genome(self, genome: StudentGenome):
        """Register a genome for tracking."""
        self.genomes[genome.genome_id] = genome
    
    def validate(
        self,
        agent_id: str,
        concept_id: str,
        inferred_mastery: float,
        platform_confidence: float,
        interaction_count: int,
        additional_context: dict
    ) -> Optional[Violation]:
        """
        Validate platform's inference against genome.
        
        Returns violation if detected, None otherwise.
        """
        genome = self.genomes.get(agent_id)
        if not genome:
            return None
        
        # Get ground truth
        genome_mastery = genome.knowledge.get_mastery(concept_id)
        
        # Calculate discrepancy
        discrepancy = abs(inferred_mastery - genome_mastery)
        
        # Log for metrics
        self.comparison_log.append({
            "agent_id": agent_id,
            "concept_id": concept_id,
            "genome": genome_mastery,
            "inferred": inferred_mastery,
            "discrepancy": discrepancy,
            "timestamp": datetime.now(),
        })
        
        # Check for violations
        
        # 1. Cold Start Hallucination
        if interaction_count < self.COLD_START_INTERACTION_LIMIT:
            if discrepancy > self.COLD_START_CONFIDENCE_THRESHOLD:
                return self._create_violation(
                    ViolationType.COLD_START_HALLUCINATION,
                    Severity.HIGH,
                    agent_id,
                    genome_mastery,
                    inferred_mastery,
                    f"Platform estimates {concept_id} at {inferred_mastery:.2f} "
                    f"but actual is {genome_mastery:.2f} after only "
                    f"{interaction_count} interactions"
                )
        
        # 2. Fatigue Blindness
        fatigue = additional_context.get("fatigue", 0)
        if fatigue > self.FATIGUE_THRESHOLD:
            if (genome_mastery - inferred_mastery) > self.MASTERY_DROP_THRESHOLD:
                if not additional_context.get("burnout_detected", False):
                    return self._create_violation(
                        ViolationType.FATIGUE_BLINDNESS,
                        Severity.HIGH,
                        agent_id,
                        genome_mastery,
                        inferred_mastery,
                        f"Agent fatigued (F={fatigue:.2f}), but platform "
                        f"dropped mastery instead of detecting burnout"
                    )
        
        # 3. Gaming Not Detected
        avg_response_time = additional_context.get("avg_response_time", 60)
        if avg_response_time < self.GAMING_RESPONSE_TIME_THRESHOLD:
            if inferred_mastery > genome_mastery + 0.1:
                return self._create_violation(
                    ViolationType.GAMING_NOT_DETECTED,
                    Severity.CRITICAL,
                    agent_id,
                    genome_mastery,
                    inferred_mastery,
                    f"Agent gaming (avg response {avg_response_time:.1f}s) but "
                    f"mastery was increased"
                )
        
        return None
    
    def _create_violation(
        self,
        vtype: ViolationType,
        severity: Severity,
        agent_id: str,
        genome_val: float,
        inferred_val: float,
        message: str
    ) -> Violation:
        """Create and record a violation."""
        violation = Violation(
            violation_type=vtype,
            severity=severity,
            agent_id=agent_id,
            timestamp=datetime.now(),
            message=message,
            genome_value=genome_val,
            inferred_value=inferred_val,
            discrepancy=abs(genome_val - inferred_val)
        )
        self.violations.append(violation)
        return violation
    
    def calculate_metrics(
        self,
        trust_states: Dict[str, float]
    ) -> TruthFidelityMetrics:
        """Calculate aggregate truth fidelity metrics."""
        if not self.comparison_log:
            return TruthFidelityMetrics(
                total_agents=len(self.genomes),
                total_comparisons=0,
                rmse=0, mae=0, max_discrepancy=0,
                violations_count=0, critical_violations=0,
                trust_retention_rate=0, diagnostic_precision=0
            )
        
        # Calculate RMSE and MAE
        discrepancies = [c["discrepancy"] for c in self.comparison_log]
        
        rmse = math.sqrt(sum(d**2 for d in discrepancies) / len(discrepancies))
        mae = sum(discrepancies) / len(discrepancies)
        max_disc = max(discrepancies)
        
        # Count violations
        critical = sum(1 for v in self.violations if v.is_critical)
        
        # Trust retention
        if trust_states:
            retained = sum(1 for t in trust_states.values() if t > 0.5)
            retention_rate = retained / len(trust_states)
        else:
            retention_rate = 1.0
        
        return TruthFidelityMetrics(
            total_agents=len(self.genomes),
            total_comparisons=len(self.comparison_log),
            rmse=rmse,
            mae=mae,
            max_discrepancy=max_disc,
            violations_count=len(self.violations),
            critical_violations=critical,
            trust_retention_rate=retention_rate,
            diagnostic_precision=0.85  # TODO: Implement properly
        )
    
    def generate_report(self) -> str:
        """Generate human-readable validation report."""
        metrics = self.calculate_metrics({})
        
        report = [
            "=" * 60,
            "GOD-VIEW OBSERVER REPORT",
            "=" * 60,
            f"Agents Tracked: {metrics.total_agents}",
            f"Comparisons Made: {metrics.total_comparisons}",
            "",
            "TRUTH FIDELITY METRICS:",
            f"  RMSE: {metrics.rmse:.4f}",
            f"  MAE: {metrics.mae:.4f}",
            f"  Max Discrepancy: {metrics.max_discrepancy:.4f}",
            "",
            "VIOLATIONS:",
            f"  Total: {metrics.violations_count}",
            f"  Critical: {metrics.critical_violations}",
            "",
        ]
        
        if self.violations:
            report.append("VIOLATION DETAILS:")
            for v in self.violations[:10]:  # Show first 10
                report.append(f"  [{v.severity.value}] {v.violation_type.value}")
                report.append(f"    Agent: {v.agent_id}")
                report.append(f"    {v.message}")
                report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
```

---

## C.5 ORCHESTRATOR

### C.5.1 Main Orchestrator

```python
"""
simulation/orchestrator/main.py
Central orchestration for the simulation.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from ..agents.genome import StudentGenome
from ..agents.cognitive_core import CognitiveLogicCore
from ..agents.trust_engine import TrustEngine
from ..observer.god_view import GodViewObserver


logger = logging.getLogger(__name__)


@dataclass
class SimulationConfig:
    """Configuration for simulation run."""
    agent_count: int = 1000
    time_compression: float = 100.0  # 100x speed
    simulation_days: int = 90        # 3 months simulated
    checkpoint_frequency: int = 100  # Steps between saves
    api_base_url: str = "http://localhost:8000/api/v4"


class SimulationOrchestrator:
    """
    Master controller for the simulation.
    
    Manages:
    - Time advancement
    - Agent lifecycle
    - API interaction
    - Data collection
    - Observer validation
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.agents: Dict[str, 'StudentAgent'] = {}
        self.observer = GodViewObserver()
        self.current_step = 0
        self.simulation_time = datetime.now()
        self.running = False
    
    def initialize(self):
        """Initialize the simulation with agents."""
        logger.info(f"Initializing simulation with {self.config.agent_count} agents")
        
        # Generate genomes
        from .genome_generator import generate_genome_pool
        genomes = generate_genome_pool(self.config.agent_count)
        
        # Create agents
        for genome in genomes:
            agent = StudentAgent(
                genome=genome,
                clc=CognitiveLogicCore(genome),
                trust_engine=TrustEngine(genome)
            )
            self.agents[genome.genome_id] = agent
            self.observer.register_genome(genome)
        
        logger.info(f"Created {len(self.agents)} agents")
    
    def run(self):
        """Run the simulation."""
        self.running = True
        
        total_steps = self.config.simulation_days * 24  # Hourly steps
        
        logger.info(f"Starting simulation: {total_steps} steps")
        
        for step in range(total_steps):
            if not self.running:
                break
            
            self.current_step = step
            self.advance_time()
            
            # Process each agent
            for agent_id, agent in self.agents.items():
                if not agent.churned:
                    self.process_agent_step(agent)
            
            # Checkpoint
            if step % self.config.checkpoint_frequency == 0:
                self.save_checkpoint()
                logger.info(f"Step {step}/{total_steps} complete")
        
        self.generate_final_report()
    
    def advance_time(self):
        """Advance simulation time by compressed amount."""
        real_seconds = 1.0 / self.config.time_compression
        sim_hours = 1.0  # Each step is 1 simulated hour
        
        self.simulation_time += timedelta(hours=sim_hours)
    
    def process_agent_step(self, agent: 'StudentAgent'):
        """Process one agent for one time step."""
        # Agent decides action
        action = agent.decide_action(self.simulation_time)
        
        # Execute action
        # ... (API calls, answer generation, etc.)
        
        # Validate with Observer
        # ... (compare genome to inferred state)
    
    def save_checkpoint(self):
        """Save simulation state."""
        # Save to Parquet
        pass
    
    def generate_final_report(self):
        """Generate final validation report."""
        report = self.observer.generate_report()
        logger.info(report)
        
        with open("simulation_report.txt", "w") as f:
            f.write(report)
```

---

**END OF PART 3: TECHNICAL IMPLEMENTATION**

**Document Size:** ~800 lines of implementation code  
**Modules Specified:** 
- genome.py (180 lines)
- personas.py (140 lines)  
- cognitive_core.py (280 lines)
- trust_engine.py (180 lines)
- god_view.py (200 lines)
- orchestrator/main.py (100 lines)

**Total Implementation Lines:** ~1,080 lines ready for development
