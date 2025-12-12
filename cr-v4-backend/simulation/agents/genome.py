"""
CR-V4 Student Genome Module

This module defines the complete student genome - the HIDDEN TRUTH
that represents the actual cognitive state of each simulated student.

COUNCIL DECISIONS IMPLEMENTED:
1. 8 persona types with realistic distributions
2. Cognitive capacity traits (stable)
3. Psychometric profile (behavioral)
4. Dynamic knowledge state per concept
5. Standard-aware temporal context
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Literal, Optional, Tuple
import random
import math
import uuid


# =============================================================================
# ENUMS
# =============================================================================

class PersonaType(Enum):
    """
    8 distinct student archetypes for simulation.
    
    Distribution (Council Approved):
        STRUGGLING_PERSISTER: 15%
        ANXIOUS_PERFECTIONIST: 12%
        DISENGAGED_GAMER: 10%
        CONCEPTUALLY_GAPPED: 15%
        STEADY_LEARNER: 28%
        FAST_TRACKER: 10%
        LATE_JOINER: 6%
        DROPPER: 4%
    """
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


# =============================================================================
# COMPONENT DATA CLASSES
# =============================================================================

@dataclass
class CognitiveCapacity:
    """
    Stable cognitive traits (the 'hardware').
    
    These traits are IMMUTABLE for a given agent and
    represent their baseline cognitive capabilities.
    """
    iq_factor: float              # 0.0-1.0, learning speed multiplier
    working_memory_limit: int     # 3-9 items (Miller's Law)
    processing_speed: float       # 0.5-2.0, response time multiplier
    attention_span_minutes: int   # 15-90 minutes typical
    
    def __post_init__(self):
        """Validate bounds."""
        self.iq_factor = max(0.0, min(1.0, self.iq_factor))
        self.working_memory_limit = max(3, min(9, self.working_memory_limit))
        self.processing_speed = max(0.5, min(2.0, self.processing_speed))
        self.attention_span_minutes = max(15, min(90, self.attention_span_minutes))


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
        """Validate all traits are 0-1."""
        for attr in ['grit_index', 'anxiety_trait', 'focus_stability',
                     'guessing_tendency', 'perfectionism', 'risk_tolerance']:
            val = getattr(self, attr)
            setattr(self, attr, max(0.0, min(1.0, val)))


@dataclass
class KnowledgeState:
    """
    Dynamic knowledge representation.
    
    This is the GROUND TRUTH that the platform's AI
    is trying to estimate. Each concept has a mastery value.
    """
    kc_mastery_map: Dict[str, float] = field(default_factory=dict)
    kc_last_interaction: Dict[str, datetime] = field(default_factory=dict)
    misconceptions: List[str] = field(default_factory=list)
    prereq_gaps: List[str] = field(default_factory=list)
    
    def get_mastery(self, concept_id: str, default: float = 0.3) -> float:
        """Get mastery, defaulting to 0.3 for unseen concepts."""
        return self.kc_mastery_map.get(concept_id, default)
    
    def set_mastery(self, concept_id: str, value: float):
        """Set mastery with bounds checking."""
        self.kc_mastery_map[concept_id] = max(0.0, min(1.0, value))
        self.kc_last_interaction[concept_id] = datetime.now()
    
    def update_mastery(self, concept_id: str, delta: float):
        """Update mastery by delta with bounds checking."""
        current = self.get_mastery(concept_id)
        self.set_mastery(concept_id, current + delta)


@dataclass
class TemporalContext:
    """
    Time-based context for the student.
    
    CRITICAL: This determines standard-wise content access.
    
    COUNCIL DECISION (Dec 12, 2024): Time Isolation
    - All time calculations use SIMULATION time, not real-world time
    - Methods accept sim_date parameter for complete isolation
    - Simulation can run ANY time period (past, present, future)
    """
    join_date: date
    standard: Literal[11, 12]
    target_exam_date: date
    is_dropper: bool = False
    previous_attempts: int = 0
    previous_best_percentile: Optional[float] = None
    
    # Internal tracking for simulation time (set by orchestrator)
    _sim_current_date: Optional[date] = None
    
    def set_sim_date(self, sim_date: date):
        """Set current simulation date for time calculations."""
        self._sim_current_date = sim_date
    
    def days_to_exam_from(self, sim_date: date) -> int:
        """Days remaining to target exam from given simulation date."""
        return max(0, (self.target_exam_date - sim_date).days)
    
    def days_on_platform_from(self, sim_date: date) -> int:
        """Days since joining from given simulation date."""
        return max(0, (sim_date - self.join_date).days)
    
    def months_on_platform_from(self, sim_date: date) -> float:
        """Months since joining from given simulation date."""
        return self.days_on_platform_from(sim_date) / 30.0
    
    @property
    def days_to_exam(self) -> int:
        """Days remaining to target exam (uses internal sim date if set)."""
        if self._sim_current_date is not None:
            return self.days_to_exam_from(self._sim_current_date)
        # Fallback to target exam date difference from join (for initialization)
        return max(0, (self.target_exam_date - self.join_date).days)
    
    @property
    def days_on_platform(self) -> int:
        """Days since joining (uses internal sim date if set)."""
        if self._sim_current_date is not None:
            return self.days_on_platform_from(self._sim_current_date)
        return 0  # Not yet started
    
    @property
    def months_on_platform(self) -> float:
        """Months since joining."""
        return self.days_on_platform / 30.0
    
    def has_passed_exam(self, current_date: date) -> bool:
        """Check if the target exam date has passed."""
        return current_date >= self.target_exam_date


@dataclass
class BehavioralPatterns:
    """
    Behavioral tendencies for realistic simulation.
    """
    login_time_preference: LoginTimePreference
    session_length_mean: float         # Average session in minutes
    session_length_std: float          # Standard deviation
    consistency_factor: float          # 0.0-1.0, schedule adherence
    study_hours_per_day: float         # Typical daily study time
    weekend_multiplier: float          # Study intensity on weekends
    break_frequency_per_hour: float    # How often takes breaks
    
    def sample_session_length(self) -> float:
        """Sample a session length from distribution."""
        length = random.gauss(self.session_length_mean, self.session_length_std)
        return max(10.0, min(180.0, length))  # 10 min to 3 hours


# =============================================================================
# MAIN GENOME CLASS
# =============================================================================

@dataclass
class StudentGenome:
    """
    Complete student genome - the HIDDEN TRUTH.
    
    This is the ground truth that the simulation uses
    to generate realistic behavior. The platform's AI
    must try to estimate this from observable actions.
    
    The genome contains:
    1. Identity (genome_id, persona_type)
    2. Cognitive capacity (stable traits)
    3. Psychometric profile (behavioral traits)
    4. Knowledge state (dynamic, per-concept)
    5. Temporal context (join date, standard, exam date)
    6. Behavioral patterns (login times, session length)
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
    
    # Runtime state (not part of genome, but tracked)
    is_active: bool = True
    has_graduated: bool = False
    churn_reason: Optional[str] = None
    
    @property
    def standard(self) -> Literal[11, 12]:
        """Convenience accessor for current standard."""
        return self.temporal.standard
    
    @property
    def is_dropper(self) -> bool:
        """Convenience accessor for dropper status."""
        return self.temporal.is_dropper
    
    def can_access_concept(self, concept_id: str) -> bool:
        """
        Check if this student can access a concept.
        
        CRITICAL VALIDATION: 11th students cannot access 12th content.
        """
        from ..config import CONTENT_RULES
        return CONTENT_RULES.is_concept_allowed(
            concept_id,
            self.temporal.standard,
            self.temporal.is_dropper
        )
    
    def mark_graduated(self, current_date: date):
        """Mark student as graduated (exam date passed)."""
        if self.temporal.has_passed_exam(current_date):
            self.has_graduated = True
            self.is_active = False
    
    def mark_churned(self, reason: str):
        """Mark student as churned (left platform)."""
        self.is_active = False
        self.churn_reason = reason
    
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
                "previous_attempts": self.temporal.previous_attempts,
            },
            "behavioral": {
                "login_time_preference": self.behavioral.login_time_preference.name,
                "session_length_mean": self.behavioral.session_length_mean,
                "study_hours_per_day": self.behavioral.study_hours_per_day,
                "consistency_factor": self.behavioral.consistency_factor,
            },
            "is_active": self.is_active,
            "has_graduated": self.has_graduated,
            "created_at": self.created_at.isoformat(),
        }


# =============================================================================
# PERSONA CONFIGURATIONS
# =============================================================================

@dataclass
class PersonaConfig:
    """Configuration for generating a specific persona."""
    # Cognitive means (required)
    iq_mean: float
    iq_std: float
    working_memory_mean: int
    processing_speed_mean: float
    attention_span_mean: int
    
    # Psychometric means (required)
    grit_mean: float
    anxiety_mean: float
    focus_mean: float
    guessing_mean: float
    
    # Knowledge initialization (required)
    starting_mastery_mean: float
    prereq_gaps_count: int
    misconception_count: int
    
    # Behavioral defaults (required)
    study_hours_mean: float
    session_length_mean: float
    
    # Optional with defaults
    perfectionism_mean: float = 0.5
    risk_tolerance_mean: float = 0.5
    consistency_mean: float = 0.5



PERSONA_CONFIGS: Dict[PersonaType, PersonaConfig] = {
    
    PersonaType.STRUGGLING_PERSISTER: PersonaConfig(
        iq_mean=0.35, iq_std=0.10,
        working_memory_mean=5,
        processing_speed_mean=0.7,
        attention_span_mean=35,
        grit_mean=0.85, anxiety_mean=0.40,
        focus_mean=0.50, guessing_mean=0.20,
        perfectionism_mean=0.30, risk_tolerance_mean=0.40,
        starting_mastery_mean=0.30,
        prereq_gaps_count=5,
        misconception_count=3,
        study_hours_mean=4.0,
        session_length_mean=45.0,
        consistency_mean=0.70,
    ),
    
    PersonaType.ANXIOUS_PERFECTIONIST: PersonaConfig(
        iq_mean=0.80, iq_std=0.10,
        working_memory_mean=7,
        processing_speed_mean=1.0,
        attention_span_mean=55,
        grit_mean=0.70, anxiety_mean=0.85,
        focus_mean=0.70, guessing_mean=0.10,
        perfectionism_mean=0.90, risk_tolerance_mean=0.30,
        starting_mastery_mean=0.60,
        prereq_gaps_count=1,
        misconception_count=2,
        study_hours_mean=6.0,
        session_length_mean=60.0,
        consistency_mean=0.85,
    ),
    
    PersonaType.DISENGAGED_GAMER: PersonaConfig(
        iq_mean=0.55, iq_std=0.15,
        working_memory_mean=6,
        processing_speed_mean=1.3,
        attention_span_mean=20,
        grit_mean=0.20, anxiety_mean=0.20,
        focus_mean=0.30, guessing_mean=0.75,
        perfectionism_mean=0.10, risk_tolerance_mean=0.80,
        starting_mastery_mean=0.35,
        prereq_gaps_count=4,
        misconception_count=5,
        study_hours_mean=1.5,
        session_length_mean=20.0,
        consistency_mean=0.25,
    ),
    
    PersonaType.CONCEPTUALLY_GAPPED: PersonaConfig(
        iq_mean=0.65, iq_std=0.12,
        working_memory_mean=6,
        processing_speed_mean=1.0,
        attention_span_mean=45,
        grit_mean=0.60, anxiety_mean=0.50,
        focus_mean=0.55, guessing_mean=0.30,
        perfectionism_mean=0.50, risk_tolerance_mean=0.50,
        starting_mastery_mean=0.50,
        prereq_gaps_count=8,  # Key: many gaps
        misconception_count=4,
        study_hours_mean=3.5,
        session_length_mean=50.0,
        consistency_mean=0.55,
    ),
    
    PersonaType.STEADY_LEARNER: PersonaConfig(
        iq_mean=0.55, iq_std=0.10,
        working_memory_mean=6,
        processing_speed_mean=1.0,
        attention_span_mean=45,
        grit_mean=0.55, anxiety_mean=0.45,
        focus_mean=0.55, guessing_mean=0.25,
        perfectionism_mean=0.50, risk_tolerance_mean=0.50,
        starting_mastery_mean=0.40,
        prereq_gaps_count=3,
        misconception_count=3,
        study_hours_mean=3.0,
        session_length_mean=45.0,
        consistency_mean=0.60,
    ),
    
    PersonaType.FAST_TRACKER: PersonaConfig(
        iq_mean=0.90, iq_std=0.05,
        working_memory_mean=8,
        processing_speed_mean=1.5,
        attention_span_mean=70,
        grit_mean=0.75, anxiety_mean=0.30,
        focus_mean=0.80, guessing_mean=0.15,
        perfectionism_mean=0.60, risk_tolerance_mean=0.70,
        starting_mastery_mean=0.65,
        prereq_gaps_count=1,
        misconception_count=1,
        study_hours_mean=4.0,
        session_length_mean=90.0,
        consistency_mean=0.75,
    ),
    
    PersonaType.LATE_JOINER: PersonaConfig(
        iq_mean=0.60, iq_std=0.15,
        working_memory_mean=6,
        processing_speed_mean=1.1,
        attention_span_mean=50,
        grit_mean=0.65, anxiety_mean=0.70,
        focus_mean=0.60, guessing_mean=0.30,
        perfectionism_mean=0.55, risk_tolerance_mean=0.55,
        starting_mastery_mean=0.45,
        prereq_gaps_count=4,
        misconception_count=4,
        study_hours_mean=5.5,  # Panic studying
        session_length_mean=75.0,
        consistency_mean=0.50,
    ),
    
    PersonaType.DROPPER: PersonaConfig(
        iq_mean=0.65, iq_std=0.15,
        working_memory_mean=6,
        processing_speed_mean=1.0,
        attention_span_mean=55,
        grit_mean=0.75, anxiety_mean=0.65,
        focus_mean=0.60, guessing_mean=0.25,
        perfectionism_mean=0.70, risk_tolerance_mean=0.45,
        starting_mastery_mean=0.55,  # Has some prep
        prereq_gaps_count=3,
        misconception_count=3,
        study_hours_mean=6.0,
        session_length_mean=90.0,
        consistency_mean=0.75,
    ),
}


# =============================================================================
# GENOME GENERATOR
# =============================================================================

def _sample_bounded_normal(mean: float, std: float, 
                           min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Sample from normal distribution with bounds."""
    value = random.gauss(mean, std)
    return max(min_val, min(max_val, value))


def _sample_login_preference(persona: PersonaType) -> LoginTimePreference:
    """Sample login time preference based on persona."""
    if persona == PersonaType.DISENGAGED_GAMER:
        return random.choice([LoginTimePreference.NIGHT, LoginTimePreference.LATE_NIGHT])
    elif persona == PersonaType.ANXIOUS_PERFECTIONIST:
        return random.choice([LoginTimePreference.EARLY_MORNING, LoginTimePreference.MORNING])
    else:
        return random.choice(list(LoginTimePreference))


def generate_genome(
    persona_type: PersonaType,
    standard: Literal[11, 12],
    join_date: date,
    target_exam_date: date,
    is_dropper: bool = False,
    available_concepts: Optional[List[str]] = None
) -> StudentGenome:
    """
    Generate a single student genome.
    
    Args:
        persona_type: The persona archetype
        standard: 11 or 12
        join_date: When student joined
        target_exam_date: JEE exam date
        is_dropper: If this is a repeat attempt
        available_concepts: List of concept IDs to initialize mastery for
        
    Returns:
        StudentGenome with all components initialized
    """
    config = PERSONA_CONFIGS[persona_type]
    
    # Generate cognitive capacity
    cognitive = CognitiveCapacity(
        iq_factor=_sample_bounded_normal(config.iq_mean, config.iq_std),
        working_memory_limit=round(_sample_bounded_normal(
            config.working_memory_mean, 1, 3, 9
        )),
        processing_speed=_sample_bounded_normal(
            config.processing_speed_mean, 0.2, 0.5, 2.0
        ),
        attention_span_minutes=round(_sample_bounded_normal(
            config.attention_span_mean, 10, 15, 90
        )),
    )
    
    # Generate psychometric profile
    psychometric = PsychometricProfile(
        grit_index=_sample_bounded_normal(config.grit_mean, 0.15),
        anxiety_trait=_sample_bounded_normal(config.anxiety_mean, 0.15),
        focus_stability=_sample_bounded_normal(config.focus_mean, 0.15),
        guessing_tendency=_sample_bounded_normal(config.guessing_mean, 0.15),
        perfectionism=_sample_bounded_normal(config.perfectionism_mean, 0.15),
        risk_tolerance=_sample_bounded_normal(config.risk_tolerance_mean, 0.15),
    )
    
    # Generate knowledge state
    kc_mastery = {}
    if available_concepts:
        for concept in available_concepts:
            # Check if concept is allowed for this standard
            is_12th = "_12_" in concept or concept.startswith("12_")
            if standard == 11 and is_12th and not is_dropper:
                continue  # Skip 12th concepts for 11th students
            
            # Generate mastery
            mastery = _sample_bounded_normal(
                config.starting_mastery_mean, 0.20, 0.05, 0.80
            )
            kc_mastery[concept] = mastery
    
    # Generate some prerequisite gaps
    prereq_gaps = []
    if available_concepts and config.prereq_gaps_count > 0:
        potential_gaps = [c for c in available_concepts if kc_mastery.get(c, 0) < 0.5]
        prereq_gaps = random.sample(
            potential_gaps, 
            min(config.prereq_gaps_count, len(potential_gaps))
        )
    
    knowledge = KnowledgeState(
        kc_mastery_map=kc_mastery,
        kc_last_interaction={},
        misconceptions=[],
        prereq_gaps=prereq_gaps,
    )
    
    # Generate temporal context
    temporal = TemporalContext(
        join_date=join_date,
        standard=standard,
        target_exam_date=target_exam_date,
        is_dropper=is_dropper,
        previous_attempts=1 if is_dropper else 0,
    )
    
    # Generate behavioral patterns
    behavioral = BehavioralPatterns(
        login_time_preference=_sample_login_preference(persona_type),
        session_length_mean=config.session_length_mean,
        session_length_std=config.session_length_mean * 0.3,
        consistency_factor=_sample_bounded_normal(config.consistency_mean, 0.15),
        study_hours_per_day=config.study_hours_mean,
        weekend_multiplier=_sample_bounded_normal(1.2, 0.2, 0.5, 2.0),
        break_frequency_per_hour=_sample_bounded_normal(1.5, 0.5, 0.5, 3.0),
    )
    
    return StudentGenome(
        genome_id=str(uuid.uuid4()),
        persona_type=persona_type,
        cognitive=cognitive,
        psychometric=psychometric,
        knowledge=knowledge,
        temporal=temporal,
        behavioral=behavioral,
    )


def generate_genome_pool(
    count: int = 1000,
    target_exam_date: date = date(2025, 1, 22),
    available_concepts: Optional[List[str]] = None,
    random_seed: Optional[int] = 42
) -> List[StudentGenome]:
    """
    Generate a pool of student genomes with realistic distribution.
    
    Args:
        count: Number of genomes to generate
        target_exam_date: JEE exam date
        available_concepts: Concepts to initialize
        random_seed: For reproducibility
        
    Returns:
        List of StudentGenome objects
    """
    if random_seed is not None:
        random.seed(random_seed)
    
    from ..config import AGENT_POOL_CONFIG
    genomes = []
    
    # Calculate counts per persona
    persona_counts = {
        PersonaType[name]: round(count * pct)
        for name, pct in AGENT_POOL_CONFIG.persona_distribution.items()
    }
    
    # Adjust for rounding errors
    total = sum(persona_counts.values())
    if total != count:
        diff = count - total
        # Add/subtract from largest group
        largest_persona = max(persona_counts, key=persona_counts.get)
        persona_counts[largest_persona] += diff
    
    for persona, persona_count in persona_counts.items():
        for i in range(persona_count):
            # Determine standard
            if persona == PersonaType.DROPPER:
                standard = 12
                is_dropper = True
            else:
                is_dropper = False
                # 45% 11th, 55% 12th
                standard = 11 if random.random() < 0.45 else 12
            
            # Determine join date based on persona
            if persona == PersonaType.LATE_JOINER:
                # 1-6 months before exam
                days_before = random.randint(30, 180)
            elif persona == PersonaType.DROPPER:
                # 10-14 months before (previous year)
                days_before = random.randint(300, 420)
            else:
                # 12-24 months before
                days_before = random.randint(360, 720)
            
            join_date = target_exam_date - timedelta(days=days_before)
            
            genome = generate_genome(
                persona_type=persona,
                standard=standard,
                join_date=join_date,
                target_exam_date=target_exam_date,
                is_dropper=is_dropper,
                available_concepts=available_concepts,
            )
            genomes.append(genome)
    
    return genomes
