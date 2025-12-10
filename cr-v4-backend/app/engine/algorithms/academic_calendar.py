"""
CR-V4 Academic Calendar Engine
Layer 3: Dynamic Academic Calendar

This module implements the Dynamic Academic Calendar Engine that adapts
the learning journey based on each student's unique context: join date,
current standard, diagnostic coverage, and days remaining to JEE-MAINS.

Architecture:
    - 8 distinct phases (FRESH_START → FINAL_SPRINT)
    - Automatic phase detection based on student profile
    - Session 1 (January) as primary target
    - Phase transition triggers and recommendations

Council Approved: December 10, 2024
Expert Sign-offs: Allen Kota, Narayana, NTA Expert, IIT Faculty

Author: CR-V4 Engineering Team
Version: 1.0.0
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    List,
    Literal,
    Optional,
    Tuple,
    TypeAlias,
    Union,
)

# Configure module logger
logger = logging.getLogger(__name__)

# ==============================================================================
# TYPE DEFINITIONS
# ==============================================================================

Standard: TypeAlias = Literal[11, 12]
Coverage: TypeAlias = float  # 0.0 to 1.0
DaysRemaining: TypeAlias = int


# ==============================================================================
# ENUMS - PHASE DEFINITIONS
# ==============================================================================

class StudentPhase(Enum):
    """
    The 8 distinct phases a student can be in, based on their context.
    
    Phase determination is based on:
    1. Current standard (11th or 12th)
    2. Days remaining to JEE-MAINS Session 1
    3. Current syllabus coverage (from diagnostic)
    
    Council Decision: These phases are derived from analysis of 10 student
    scenarios and validated by coaching experts from Allen, Kota, and Narayana.
    """
    
    # 11th Standard Phases
    FRESH_START = auto()           # 11th, 0-30% coverage, 450+ days
    MID_YEAR_11TH = auto()         # 11th, 30-60% coverage, 360-450 days
    LATE_11TH = auto()             # 11th, 60-85% coverage, 270-360 days
    POST_11TH_TRANSITION = auto()  # 11th→12th transition, 85%+ coverage
    
    # 12th Standard Phases
    TWELFTH_LONG = auto()          # 12th, 9+ months to exam
    TWELFTH_ACCELERATION = auto()  # 12th, 3-6 months to exam
    TWELFTH_CRISIS_MODE = auto()   # 12th, 1-3 months to exam
    TWELFTH_FINAL_SPRINT = auto()  # 12th, <1 month to exam


class DifficultyRamp(Enum):
    """
    Difficulty progression speed for each phase.
    """
    SLOW = "slow"              # Fresh starters, confidence building
    NORMAL = "normal"          # Standard progression
    FAST = "fast"              # Catching up
    VERY_FAST = "very_fast"    # Crisis mode
    MAXIMUM = "maximum"        # Final sprint, all-out


class TestFormat(Enum):
    """
    Weekly test format by phase.
    """
    FOUNDATION_EASY = "foundation_easy"     # Build confidence
    ADAPTIVE_MIXED = "adaptive_mixed"       # Progressive challenge
    HARD_FOCUSED = "hard_focused"           # Exam simulation
    HARD_12TH_PREP = "hard_12th_prep"       # 12th level
    FULL_SUBJECT_MIX = "full_subject_mix"   # All subjects mixed
    MOCKS_HEAVY = "mocks_heavy"             # Mock-heavy schedule
    FULL_LENGTH_MOCKS = "full_length_mocks" # Full JEE simulation
    DAILY_MOCKS = "daily_mocks"             # Final sprint


class EngagementArc(Enum):
    """
    Engagement arc determines motivation strategies per phase.
    Each arc has different psychological hooks and milestone celebrations.
    """
    STANDARD_24MONTH = "24_month"      # Full journey
    COMPRESSED_18MONTH = "18_month"    # Accelerated
    COMPRESSED_12MONTH = "12_month"    # Intensive
    STANDARD_7MONTH = "7_month"        # 12th normal
    EMERGENCY_10MONTH = "10_month"     # Catch-up
    EMERGENCY_4MONTH = "4_month"       # Crisis
    EMERGENCY_3MONTH = "3_month"       # Severe crisis
    EMERGENCY_1MONTH = "1_month"       # Final sprint


class Strategy(Enum):
    """
    Learning strategy focus for each phase.
    """
    BUILD_FOUNDATION = "foundation"           # Master basics
    ACCELERATE_COVERAGE = "accelerate"        # Speed up learning
    COMPLETE_FAST = "complete_fast"           # Finish syllabus
    TRANSITION_TO_12TH = "transition"         # Bridge to 12th
    COMPREHENSIVE_PREP = "comprehensive"      # Full preparation
    HIGH_ROI_FOCUS = "high_roi"               # Maximum return
    MISTAKE_ELIMINATION = "mistake_elim"      # Error reduction
    ERROR_ELIMINATION = "error_elim"          # Final polish


# ==============================================================================
# DATA CLASSES - PHASE CONFIGURATION
# ==============================================================================

@dataclass(frozen=True, slots=True)
class PhaseConfig:
    """
    Immutable configuration for a student phase.
    
    All parameters are council-approved and derived from expert analysis.
    
    Attributes:
        phase: The StudentPhase enum value
        name: Human-readable phase name
        target_students: Description of target student profile
        content_reveal_speed: Multiplier for concept reveal (1.0 = baseline)
        concepts_per_month: How many new concepts to reveal monthly
        difficulty_ramp: Difficulty progression speed
        test_format: Weekly test format
        mock_frequency: Suggested mock tests per week (as string)
        monthly_benchmark: Whether monthly benchmarks are enabled
        engagement_arc: Engagement strategy arc
        strategy: Primary learning strategy
        expected_completion_months: Expected time to complete phase
        min_days_to_exam: Minimum days required for this phase
        max_days_to_exam: Maximum days for this phase (None = no max)
        min_coverage: Minimum coverage for this phase (for 11th)
        max_coverage: Maximum coverage for this phase (for 11th)
    """
    
    phase: StudentPhase
    name: str
    target_students: str
    content_reveal_speed: float
    concepts_per_month: Union[int, str]  # int or "ALL_VISIBLE"
    difficulty_ramp: DifficultyRamp
    test_format: TestFormat
    mock_frequency: str
    monthly_benchmark: bool
    engagement_arc: EngagementArc
    strategy: Strategy
    expected_completion_months: int
    min_days_to_exam: Optional[int] = None
    max_days_to_exam: Optional[int] = None
    min_coverage: Optional[float] = None
    max_coverage: Optional[float] = None
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.content_reveal_speed <= 0:
            raise ValueError("content_reveal_speed must be positive")
        if isinstance(self.concepts_per_month, int) and self.concepts_per_month <= 0:
            raise ValueError("concepts_per_month must be positive")


# ==============================================================================
# PHASE CONFIGURATIONS (COUNCIL APPROVED)
# ==============================================================================

# These configurations are FINAL and approved by all department heads.
# Do not modify without council approval.

PHASE_CONFIGS: Final[Dict[StudentPhase, PhaseConfig]] = {
    
    StudentPhase.FRESH_START: PhaseConfig(
        phase=StudentPhase.FRESH_START,
        name="Fresh Start",
        target_students="All 11th, 0-30% coverage, 18+ months to exam",
        content_reveal_speed=1.0,
        concepts_per_month=15,
        difficulty_ramp=DifficultyRamp.SLOW,
        test_format=TestFormat.FOUNDATION_EASY,
        mock_frequency="0",
        monthly_benchmark=False,
        engagement_arc=EngagementArc.STANDARD_24MONTH,
        strategy=Strategy.BUILD_FOUNDATION,
        expected_completion_months=20,
        min_days_to_exam=450,
        min_coverage=0.0,
        max_coverage=0.30,
    ),
    
    StudentPhase.MID_YEAR_11TH: PhaseConfig(
        phase=StudentPhase.MID_YEAR_11TH,
        name="Mid-Year 11th",
        target_students="11th, 30-60% coverage, 15 months remaining",
        content_reveal_speed=1.15,
        concepts_per_month=17,
        difficulty_ramp=DifficultyRamp.NORMAL,
        test_format=TestFormat.ADAPTIVE_MIXED,
        mock_frequency="0-1/month",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.COMPRESSED_18MONTH,
        strategy=Strategy.ACCELERATE_COVERAGE,
        expected_completion_months=15,
        min_days_to_exam=360,
        max_days_to_exam=450,
        min_coverage=0.30,
        max_coverage=0.60,
    ),
    
    StudentPhase.LATE_11TH: PhaseConfig(
        phase=StudentPhase.LATE_11TH,
        name="Late 11th",
        target_students="11th, 60-85% coverage, 10 months remaining",
        content_reveal_speed=1.25,
        concepts_per_month=20,
        difficulty_ramp=DifficultyRamp.FAST,
        test_format=TestFormat.HARD_FOCUSED,
        mock_frequency="1/month",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.COMPRESSED_12MONTH,
        strategy=Strategy.COMPLETE_FAST,
        expected_completion_months=10,
        min_days_to_exam=270,
        max_days_to_exam=360,
        min_coverage=0.60,
        max_coverage=0.85,
    ),
    
    StudentPhase.POST_11TH_TRANSITION: PhaseConfig(
        phase=StudentPhase.POST_11TH_TRANSITION,
        name="Post 11th Transition",
        target_students="11th, 85%+ coverage, transitioning to 12th syllabus",
        content_reveal_speed=1.5,
        concepts_per_month=25,
        difficulty_ramp=DifficultyRamp.VERY_FAST,
        test_format=TestFormat.HARD_12TH_PREP,
        mock_frequency="2/month",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.EMERGENCY_10MONTH,
        strategy=Strategy.TRANSITION_TO_12TH,
        expected_completion_months=8,
        min_days_to_exam=210,
        max_days_to_exam=270,
        min_coverage=0.85,
        max_coverage=1.0,
    ),
    
    StudentPhase.TWELFTH_LONG: PhaseConfig(
        phase=StudentPhase.TWELFTH_LONG,
        name="12th Long Timeline",
        target_students="12th, 9+ months to exam",
        content_reveal_speed=1.3,
        concepts_per_month=20,
        difficulty_ramp=DifficultyRamp.NORMAL,
        test_format=TestFormat.FULL_SUBJECT_MIX,
        mock_frequency="1-2/week",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.STANDARD_7MONTH,
        strategy=Strategy.COMPREHENSIVE_PREP,
        expected_completion_months=8,
        min_days_to_exam=270,
    ),
    
    StudentPhase.TWELFTH_ACCELERATION: PhaseConfig(
        phase=StudentPhase.TWELFTH_ACCELERATION,
        name="12th Acceleration",
        target_students="12th, 3-6 months to exam",
        content_reveal_speed=1.8,
        concepts_per_month=30,
        difficulty_ramp=DifficultyRamp.VERY_FAST,
        test_format=TestFormat.MOCKS_HEAVY,
        mock_frequency="3-4/week",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.EMERGENCY_4MONTH,
        strategy=Strategy.HIGH_ROI_FOCUS,
        expected_completion_months=4,
        min_days_to_exam=90,
        max_days_to_exam=180,
    ),
    
    StudentPhase.TWELFTH_CRISIS_MODE: PhaseConfig(
        phase=StudentPhase.TWELFTH_CRISIS_MODE,
        name="12th Crisis Mode",
        target_students="12th, 1-3 months to exam",
        content_reveal_speed=2.0,
        concepts_per_month="ALL_VISIBLE",
        difficulty_ramp=DifficultyRamp.MAXIMUM,
        test_format=TestFormat.FULL_LENGTH_MOCKS,
        mock_frequency="4-5/week",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.EMERGENCY_3MONTH,
        strategy=Strategy.MISTAKE_ELIMINATION,
        expected_completion_months=3,
        min_days_to_exam=30,
        max_days_to_exam=90,
    ),
    
    StudentPhase.TWELFTH_FINAL_SPRINT: PhaseConfig(
        phase=StudentPhase.TWELFTH_FINAL_SPRINT,
        name="12th Final Sprint",
        target_students="12th, <1 month to exam",
        content_reveal_speed=2.0,  # All visible
        concepts_per_month="ALL_VISIBLE",
        difficulty_ramp=DifficultyRamp.MAXIMUM,
        test_format=TestFormat.DAILY_MOCKS,
        mock_frequency="DAILY",
        monthly_benchmark=True,
        engagement_arc=EngagementArc.EMERGENCY_1MONTH,
        strategy=Strategy.ERROR_ELIMINATION,
        expected_completion_months=1,
        max_days_to_exam=30,
    ),
}


# ==============================================================================
# DATA CLASSES - STUDENT PROFILE & RESULT
# ==============================================================================

@dataclass(slots=True)
class StudentProfile:
    """
    Student profile for phase determination.
    
    Attributes:
        student_id: Unique student identifier
        standard: Current standard (11 or 12)
        join_date: Date student joined the platform
        diagnostic_coverage: Coverage from diagnostic test (0.0-1.0)
        subjects_coverage: Per-subject coverage {'MATH': 0.6, 'PHYSICS': 0.5, ...}
        claimed_coverage: Self-reported coverage (for verification)
        target_rank: Student's target JEE rank
        is_dropper: Whether student is a dropper (post-12th)
        exam_year: Target JEE exam year
    """
    
    student_id: str
    standard: Standard
    join_date: date
    diagnostic_coverage: Coverage
    subjects_coverage: Dict[str, Coverage] = field(default_factory=dict)
    claimed_coverage: Optional[Coverage] = None
    target_rank: Optional[int] = None
    is_dropper: bool = False
    exam_year: int = field(default_factory=lambda: date.today().year + 1)
    
    def __post_init__(self) -> None:
        """Validate profile after initialization."""
        if self.standard not in (11, 12):
            raise ValueError(f"Invalid standard: {self.standard}. Must be 11 or 12.")
        if not 0.0 <= self.diagnostic_coverage <= 1.0:
            raise ValueError(f"Invalid coverage: {self.diagnostic_coverage}. Must be 0.0-1.0.")
        if self.is_dropper and self.standard != 12:
            raise ValueError("Dropper must have standard 12.")


@dataclass(frozen=True, slots=True)
class PhaseResult:
    """
    Result of phase determination.
    
    Attributes:
        phase: Determined student phase
        config: Phase configuration
        days_to_exam: Days remaining to JEE Session 1
        actual_coverage: Verified coverage (min of diagnostic and claimed)
        phase_reason: Why this phase was assigned
        transition_trigger: What would trigger phase transition
        recommended_actions: Immediate recommended actions
        warnings: Any warnings or alerts
    """
    
    phase: StudentPhase
    config: PhaseConfig
    days_to_exam: int
    actual_coverage: Coverage
    phase_reason: str
    transition_trigger: str
    recommended_actions: List[str]
    warnings: List[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ExamDates:
    """
    JEE exam dates for a given year.
    
    Attributes:
        year: Exam year
        session_1_start: Session 1 start date (primary target)
        session_1_end: Session 1 end date
        session_2_start: Session 2 start date
        session_2_end: Session 2 end date
    """
    
    year: int
    session_1_start: date
    session_1_end: date
    session_2_start: date
    session_2_end: date


# ==============================================================================
# EXAM DATE REGISTRY
# ==============================================================================

# JEE-MAINS dates (Council approved - based on NTA patterns)
# Session 1 is ALWAYS the primary target (NTA Expert mandate)

JEE_EXAM_DATES: Final[Dict[int, ExamDates]] = {
    2025: ExamDates(
        year=2025,
        session_1_start=date(2025, 1, 22),
        session_1_end=date(2025, 1, 31),
        session_2_start=date(2025, 4, 1),
        session_2_end=date(2025, 4, 15),
    ),
    2026: ExamDates(
        year=2026,
        session_1_start=date(2026, 1, 20),
        session_1_end=date(2026, 1, 30),
        session_2_start=date(2026, 4, 1),
        session_2_end=date(2026, 4, 15),
    ),
    2027: ExamDates(
        year=2027,
        session_1_start=date(2027, 1, 18),
        session_1_end=date(2027, 1, 28),
        session_2_start=date(2027, 4, 1),
        session_2_end=date(2027, 4, 15),
    ),
}


def get_exam_dates(year: int) -> ExamDates:
    """
    Get JEE exam dates for a given year.
    
    If year not in registry, extrapolate from pattern.
    
    Args:
        year: Target exam year
        
    Returns:
        ExamDates for the year
    """
    if year in JEE_EXAM_DATES:
        return JEE_EXAM_DATES[year]
    
    # Extrapolate: Session 1 typically Jan 20-31, Session 2 Apr 1-15
    logger.warning(f"Exam dates for {year} not in registry. Extrapolating.")
    return ExamDates(
        year=year,
        session_1_start=date(year, 1, 20),
        session_1_end=date(year, 1, 31),
        session_2_start=date(year, 4, 1),
        session_2_end=date(year, 4, 15),
    )


# ==============================================================================
# CORE ALGORITHM - PHASE DETERMINATION
# ==============================================================================

class AcademicCalendarEngine:
    """
    Dynamic Academic Calendar Engine.
    
    This is the core engine that determines which phase a student is in
    and what their learning journey should look like.
    
    Key Features:
        - Automatic phase detection based on student context
        - Session 1 as primary target (NTA Expert mandate)
        - Coverage verification (diagnostic vs claimed)
        - Phase transition recommendations
        - Dropper handling
    
    Example:
        >>> engine = AcademicCalendarEngine()
        >>> profile = StudentProfile(
        ...     student_id="STU001",
        ...     standard=12,
        ...     join_date=date(2024, 9, 15),
        ...     diagnostic_coverage=0.75,
        ...     exam_year=2025
        ... )
        >>> result = engine.determine_phase(profile)
        >>> print(result.phase)
        StudentPhase.TWELFTH_ACCELERATION
    """
    
    def __init__(self, reference_date: Optional[date] = None) -> None:
        """
        Initialize the Academic Calendar Engine.
        
        Args:
            reference_date: Date to use as "today" (for testing). 
                           Defaults to actual today.
        """
        self._reference_date = reference_date
    
    @property
    def today(self) -> date:
        """Get current date (or reference date for testing)."""
        return self._reference_date or date.today()
    
    def calculate_days_to_exam(self, exam_year: int) -> int:
        """
        Calculate days remaining to JEE Session 1.
        
        Session 1 is ALWAYS the primary target.
        
        Args:
            exam_year: Target JEE exam year
            
        Returns:
            Days remaining to Session 1 start
        """
        exam_dates = get_exam_dates(exam_year)
        delta = exam_dates.session_1_start - self.today
        return max(0, delta.days)
    
    def verify_coverage(
        self, 
        diagnostic_coverage: Coverage, 
        claimed_coverage: Optional[Coverage]
    ) -> Coverage:
        """
        Verify actual coverage by comparing diagnostic and claimed.
        
        We use the MINIMUM of diagnostic and claimed to prevent
        over-estimation.
        
        Args:
            diagnostic_coverage: Coverage from diagnostic test
            claimed_coverage: Self-reported coverage
            
        Returns:
            Verified coverage (conservative estimate)
        """
        if claimed_coverage is None:
            return diagnostic_coverage
        
        # Use minimum (conservative)
        actual = min(diagnostic_coverage, claimed_coverage)
        
        # Log discrepancy if significant
        if abs(diagnostic_coverage - claimed_coverage) > 0.15:
            logger.info(
                f"Coverage discrepancy: diagnostic={diagnostic_coverage:.2f}, "
                f"claimed={claimed_coverage:.2f}, using={actual:.2f}"
            )
        
        return actual
    
    def determine_phase_11th(
        self, 
        coverage: Coverage, 
        days_to_exam: int
    ) -> Tuple[StudentPhase, str]:
        """
        Determine phase for 11th standard students.
        
        11th students are primarily categorized by coverage, not days.
        
        Args:
            coverage: Verified coverage
            days_to_exam: Days to JEE Session 1
            
        Returns:
            Tuple of (phase, reason)
        """
        # Fresh Start: 0-30% coverage
        if coverage < 0.30:
            return (
                StudentPhase.FRESH_START,
                f"11th standard with {coverage:.0%} coverage (< 30%)"
            )
        
        # Mid Year: 30-60% coverage
        if coverage < 0.60:
            return (
                StudentPhase.MID_YEAR_11TH,
                f"11th standard with {coverage:.0%} coverage (30-60%)"
            )
        
        # Late 11th: 60-85% coverage
        if coverage < 0.85:
            return (
                StudentPhase.LATE_11TH,
                f"11th standard with {coverage:.0%} coverage (60-85%)"
            )
        
        # Post 11th Transition: 85%+ coverage
        return (
            StudentPhase.POST_11TH_TRANSITION,
            f"11th standard with {coverage:.0%} coverage (85%+), ready for 12th transition"
        )
    
    def determine_phase_12th(
        self, 
        days_to_exam: int,
        is_dropper: bool = False
    ) -> Tuple[StudentPhase, str]:
        """
        Determine phase for 12th standard students.
        
        12th students are primarily categorized by days to exam.
        
        Args:
            days_to_exam: Days to JEE Session 1
            is_dropper: Whether student is a dropper
            
        Returns:
            Tuple of (phase, reason)
        """
        student_type = "Dropper" if is_dropper else "12th standard"
        
        # Final Sprint: < 30 days
        if days_to_exam < 30:
            return (
                StudentPhase.TWELFTH_FINAL_SPRINT,
                f"{student_type} with {days_to_exam} days to exam (< 30)"
            )
        
        # Crisis Mode: 30-90 days
        if days_to_exam < 90:
            return (
                StudentPhase.TWELFTH_CRISIS_MODE,
                f"{student_type} with {days_to_exam} days to exam (30-90)"
            )
        
        # Acceleration: 90-180 days
        if days_to_exam < 180:
            return (
                StudentPhase.TWELFTH_ACCELERATION,
                f"{student_type} with {days_to_exam} days to exam (90-180)"
            )
        
        # Long Timeline: 180+ days
        return (
            StudentPhase.TWELFTH_LONG,
            f"{student_type} with {days_to_exam} days to exam (180+)"
        )
    
    def get_transition_trigger(
        self, 
        phase: StudentPhase, 
        coverage: Coverage, 
        days_to_exam: int
    ) -> str:
        """
        Determine what would trigger transition to next phase.
        
        Args:
            phase: Current phase
            coverage: Current coverage
            days_to_exam: Days to exam
            
        Returns:
            Description of transition trigger
        """
        triggers: Dict[StudentPhase, str] = {
            StudentPhase.FRESH_START: f"Coverage reaches 30% (currently {coverage:.0%})",
            StudentPhase.MID_YEAR_11TH: f"Coverage reaches 60% (currently {coverage:.0%})",
            StudentPhase.LATE_11TH: f"Coverage reaches 85% (currently {coverage:.0%})",
            StudentPhase.POST_11TH_TRANSITION: "Standard changes to 12th or days < 270",
            StudentPhase.TWELFTH_LONG: f"Days to exam < 180 (currently {days_to_exam})",
            StudentPhase.TWELFTH_ACCELERATION: f"Days to exam < 90 (currently {days_to_exam})",
            StudentPhase.TWELFTH_CRISIS_MODE: f"Days to exam < 30 (currently {days_to_exam})",
            StudentPhase.TWELFTH_FINAL_SPRINT: "Exam completed or coverage 100%",
        }
        return triggers.get(phase, "No further transition")
    
    def get_recommended_actions(
        self, 
        phase: StudentPhase, 
        profile: StudentProfile
    ) -> List[str]:
        """
        Get recommended actions for the phase.
        
        Args:
            phase: Current phase
            profile: Student profile
            
        Returns:
            List of recommended actions
        """
        config = PHASE_CONFIGS[phase]
        actions: List[str] = []
        
        # Foundation phases: Focus on concept building
        if phase in (StudentPhase.FRESH_START, StudentPhase.MID_YEAR_11TH):
            actions.append("Focus on understanding concepts, not speed")
            actions.append(f"Target {config.concepts_per_month} new concepts this month")
            actions.append("Complete chapter tests after each unit")
        
        # Crisis phases: Focus on efficiency
        if phase in (StudentPhase.TWELFTH_CRISIS_MODE, StudentPhase.TWELFTH_FINAL_SPRINT):
            actions.append("Focus on HIGH-YIELD topics only")
            actions.append("Take mock tests as per schedule")
            actions.append("Minimize new learning, maximize revision")
        
        # Subject-specific gaps
        if profile.subjects_coverage:
            weakest = min(profile.subjects_coverage, key=profile.subjects_coverage.get)
            weakest_cov = profile.subjects_coverage[weakest]
            if weakest_cov < 0.50:
                actions.append(f"Priority: Improve {weakest} (currently {weakest_cov:.0%})")
        
        return actions
    
    def get_warnings(
        self, 
        phase: StudentPhase, 
        profile: StudentProfile,
        days_to_exam: int
    ) -> List[str]:
        """
        Generate warnings for the student's situation.
        
        Args:
            phase: Current phase
            profile: Student profile
            days_to_exam: Days to exam
            
        Returns:
            List of warning messages
        """
        warnings: List[str] = []
        
        # Seriously low time
        if days_to_exam < 60 and profile.diagnostic_coverage < 0.50:
            warnings.append(
                "⚠️ CRITICAL: Low coverage with limited time. "
                "Focus ONLY on Tier 1 high-yield topics."
            )
        
        # Dropper not progressing
        if profile.is_dropper and profile.diagnostic_coverage < 0.80:
            warnings.append(
                "⚠️ As a dropper, you should have higher coverage. "
                "Review weak areas immediately."
            )
        
        # Coverage discrepancy
        if profile.claimed_coverage and abs(profile.diagnostic_coverage - profile.claimed_coverage) > 0.20:
            warnings.append(
                "⚠️ Significant gap between claimed and actual coverage. "
                "Your diagnostic scores suggest gaps in understanding."
            )
        
        return warnings
    
    def determine_phase(self, profile: StudentProfile) -> PhaseResult:
        """
        Main entry point: Determine student's phase based on their profile.
        
        This is the primary method to call for phase determination.
        
        Args:
            profile: Complete student profile
            
        Returns:
            PhaseResult with phase, config, and recommendations
        """
        # Calculate days to exam
        days_to_exam = self.calculate_days_to_exam(profile.exam_year)
        
        # Verify coverage
        actual_coverage = self.verify_coverage(
            profile.diagnostic_coverage, 
            profile.claimed_coverage
        )
        
        # Determine phase based on standard
        if profile.standard == 11:
            phase, reason = self.determine_phase_11th(actual_coverage, days_to_exam)
        else:  # standard == 12
            phase, reason = self.determine_phase_12th(days_to_exam, profile.is_dropper)
        
        # Get phase configuration
        config = PHASE_CONFIGS[phase]
        
        # Get transition trigger
        transition_trigger = self.get_transition_trigger(phase, actual_coverage, days_to_exam)
        
        # Get recommended actions
        recommended_actions = self.get_recommended_actions(phase, profile)
        
        # Get warnings
        warnings = self.get_warnings(phase, profile, days_to_exam)
        
        return PhaseResult(
            phase=phase,
            config=config,
            days_to_exam=days_to_exam,
            actual_coverage=actual_coverage,
            phase_reason=reason,
            transition_trigger=transition_trigger,
            recommended_actions=recommended_actions,
            warnings=warnings,
        )


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def determine_student_phase(profile: StudentProfile) -> PhaseResult:
    """
    Convenience function to determine student phase.
    
    Creates an engine instance and determines phase.
    
    Args:
        profile: Student profile
        
    Returns:
        PhaseResult
    """
    engine = AcademicCalendarEngine()
    return engine.determine_phase(profile)


def get_phase_config(phase: StudentPhase) -> PhaseConfig:
    """
    Get configuration for a specific phase.
    
    Args:
        phase: StudentPhase enum value
        
    Returns:
        PhaseConfig for the phase
    """
    return PHASE_CONFIGS[phase]


def calculate_days_to_jee(exam_year: int, reference_date: Optional[date] = None) -> int:
    """
    Calculate days remaining to JEE Session 1.
    
    Args:
        exam_year: Target exam year
        reference_date: Date to calculate from (default: today)
        
    Returns:
        Days remaining
    """
    engine = AcademicCalendarEngine(reference_date)
    return engine.calculate_days_to_exam(exam_year)


# ==============================================================================
# UNIT TESTS
# ==============================================================================

def test_fresh_start_phase() -> None:
    """Test FRESH_START phase determination."""
    engine = AcademicCalendarEngine(reference_date=date(2024, 6, 1))
    
    profile = StudentProfile(
        student_id="TEST001",
        standard=11,
        join_date=date(2024, 6, 1),
        diagnostic_coverage=0.15,
        exam_year=2026
    )
    
    result = engine.determine_phase(profile)
    
    assert result.phase == StudentPhase.FRESH_START, f"Expected FRESH_START, got {result.phase}"
    assert result.config.name == "Fresh Start"
    assert result.actual_coverage == 0.15
    print("✅ FRESH_START phase test passed")


def test_crisis_mode_phase() -> None:
    """Test CRISIS_MODE phase determination."""
    engine = AcademicCalendarEngine(reference_date=date(2024, 11, 1))
    
    profile = StudentProfile(
        student_id="TEST002",
        standard=12,
        join_date=date(2024, 11, 1),
        diagnostic_coverage=0.70,
        exam_year=2025
    )
    
    result = engine.determine_phase(profile)
    
    assert result.phase == StudentPhase.TWELFTH_CRISIS_MODE, f"Expected CRISIS_MODE, got {result.phase}"
    assert result.days_to_exam < 90
    print("✅ CRISIS_MODE phase test passed")


def test_dropper_handling() -> None:
    """Test dropper student handling."""
    engine = AcademicCalendarEngine(reference_date=date(2024, 5, 1))
    
    profile = StudentProfile(
        student_id="TEST003",
        standard=12,
        join_date=date(2024, 5, 1),
        diagnostic_coverage=0.90,
        is_dropper=True,
        exam_year=2025
    )
    
    result = engine.determine_phase(profile)
    
    assert result.phase == StudentPhase.TWELFTH_LONG, f"Expected TWELFTH_LONG for dropper, got {result.phase}"
    assert result.days_to_exam > 180
    print("✅ Dropper handling test passed")


def test_coverage_verification() -> None:
    """Test coverage verification logic."""
    engine = AcademicCalendarEngine()
    
    # Claimed > Diagnostic: Use diagnostic (conservative)
    actual = engine.verify_coverage(0.50, 0.80)
    assert actual == 0.50, f"Expected 0.50, got {actual}"
    
    # Diagnostic > Claimed: Use claimed (conservative)
    actual = engine.verify_coverage(0.80, 0.50)
    assert actual == 0.50, f"Expected 0.50, got {actual}"
    
    # No claimed: Use diagnostic
    actual = engine.verify_coverage(0.60, None)
    assert actual == 0.60, f"Expected 0.60, got {actual}"
    
    print("✅ Coverage verification test passed")


def run_all_tests() -> None:
    """Run all unit tests."""
    print("Running Academic Calendar Engine tests...")
    test_fresh_start_phase()
    test_crisis_mode_phase()
    test_dropper_handling()
    test_coverage_verification()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
