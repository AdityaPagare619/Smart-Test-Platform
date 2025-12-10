"""
CR-V4 Psychology Engine
Layer 10: Psychological Intelligence Engine

This module implements comprehensive psychological monitoring and intervention
to prevent burnout, detect distress signals, and maintain optimal mental health
throughout the intense JEE preparation journey.

Architecture:
    - 5-signal burnout detection
    - 80% threshold interventions
    - Forced break system
    - Motivation recovery protocols
    - Parent/guardian alerts

Council Approved: December 10, 2024
Expert Sign-offs: Psychology Expert, Student Union, All Coaching Experts

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
    Set,
    Tuple,
    TypeAlias,
)

from .academic_calendar import StudentPhase

# Configure module logger
logger = logging.getLogger(__name__)

# ==============================================================================
# TYPE DEFINITIONS
# ==============================================================================

StudentId: TypeAlias = str
Score: TypeAlias = float  # 0.0 to 1.0


# ==============================================================================
# CONSTANTS (COUNCIL APPROVED)
# ==============================================================================

# Burnout thresholds
BURNOUT_WARNING_THRESHOLD: Final[float] = 0.60    # 60% risk = warning
BURNOUT_CRITICAL_THRESHOLD: Final[float] = 0.80   # 80% risk = intervention

# Activity thresholds
MAX_SAFE_HOURS_PER_DAY: Final[float] = 8.0        # Above = overexertion
MAX_SAFE_HOURS_PER_WEEK: Final[float] = 50.0      # Above = unsustainable
IDEAL_BREAK_FREQUENCY: Final[int] = 90            # 90 minutes, then break

# Performance thresholds
ACCURACY_DROP_ALERT: Final[float] = 0.15          # 15% drop = concerning
ACCURACY_DROP_CRITICAL: Final[float] = 0.25       # 25% drop = intervention

# Streak risk
STREAK_PRESSURE_DAYS: Final[int] = 30             # High streak = added pressure


# ==============================================================================
# ENUMS
# ==============================================================================

class BurnoutLevel(Enum):
    """Burnout severity classification."""
    HEALTHY = auto()           # No burnout risk
    LOW_RISK = auto()          # Minor stress, preventive care
    MODERATE = auto()          # Elevated stress, attention needed
    HIGH = auto()              # Serious risk, intervention required
    CRITICAL = auto()          # Immediate intervention


class DistressSignal(Enum):
    """Types of distress signals detected."""
    OVEREXERTION = "overexertion"           # Too many hours
    ACCURACY_DROP = "accuracy_drop"          # Performance decline
    TIME_INCREASE = "time_increase"          # Taking longer per question
    SKIP_PATTERN = "skip_pattern"            # Skipping questions more
    ERRATIC_SCHEDULE = "erratic_schedule"    # Inconsistent timing
    STREAK_ANXIETY = "streak_anxiety"        # Unhealthy streak behavior
    SUBJECT_AVOIDANCE = "subject_avoidance"  # Avoiding weak areas


class InterventionType(Enum):
    """Types of interventions."""
    SOFT_REMINDER = "soft_reminder"          # Gentle nudge
    FORCED_BREAK = "forced_break"            # Must take break
    DIFFICULTY_REDUCTION = "difficulty_reduce"
    ENCOURAGEMENT = "encouragement"
    PARENT_ALERT = "parent_alert"
    COUNSELOR_REFERRAL = "counselor_referral"


class RecoveryAction(Enum):
    """Recovery actions."""
    TAKE_BREAK = "take_break"
    EASIER_CONTENT = "easier_content"
    REVIEW_STRENGTHS = "review_strengths"
    TALK_TO_SOMEONE = "talk_to_someone"
    OUTDOOR_ACTIVITY = "outdoor_activity"
    SLEEP = "sleep"


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass(slots=True)
class StudySession:
    """
    A single study session record.
    
    Attributes:
        session_id: Unique session identifier
        start_time: When session started
        end_time: When session ended (None if ongoing)
        duration_minutes: Duration in minutes
        questions_attempted: Questions attempted
        questions_correct: Questions correct
        avg_time_per_question: Average seconds per question
        subject: Subject studied
        breaks_taken: Number of breaks during session
    """
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: float = 0.0
    questions_attempted: int = 0
    questions_correct: int = 0
    avg_time_per_question: float = 0.0
    subject: Optional[str] = None
    breaks_taken: int = 0


@dataclass(slots=True)
class BurnoutSignals:
    """
    Detected burnout signals for a student.
    
    Attributes:
        overexertion_score: Score for overexertion (0-1)
        accuracy_drop_score: Score for accuracy decline (0-1)
        time_increase_score: Score for time increase (0-1)
        skip_pattern_score: Score for skip patterns (0-1)
        erratic_schedule_score: Score for erratic timing (0-1)
        signals_detected: List of detected signals
    """
    overexertion_score: float = 0.0
    accuracy_drop_score: float = 0.0
    time_increase_score: float = 0.0
    skip_pattern_score: float = 0.0
    erratic_schedule_score: float = 0.0
    signals_detected: List[DistressSignal] = field(default_factory=list)
    
    @property
    def overall_risk(self) -> float:
        """Calculate overall burnout risk (0-1)."""
        scores = [
            self.overexertion_score * 0.25,  # Weight: 25%
            self.accuracy_drop_score * 0.25,  # Weight: 25%
            self.time_increase_score * 0.20,  # Weight: 20%
            self.skip_pattern_score * 0.15,   # Weight: 15%
            self.erratic_schedule_score * 0.15,  # Weight: 15%
        ]
        return min(1.0, sum(scores))


@dataclass(slots=True)
class StudentPsychState:
    """
    Complete psychological state for a student.
    
    Attributes:
        student_id: Student identifier
        burnout_level: Current burnout level
        signals: Detected distress signals
        last_break: When student last took a break
        consecutive_heavy_days: Days of heavy study in a row
        weekly_hours: Total study hours this week
        baseline_accuracy: Student's normal accuracy
        recent_accuracy: Recent 7-day accuracy
        interventions_today: Interventions shown today
        is_forced_break_active: Whether forced break is active
    """
    student_id: StudentId
    burnout_level: BurnoutLevel = BurnoutLevel.HEALTHY
    signals: BurnoutSignals = field(default_factory=BurnoutSignals)
    last_break: datetime = field(default_factory=datetime.now)
    consecutive_heavy_days: int = 0
    weekly_hours: float = 0.0
    baseline_accuracy: float = 0.70
    recent_accuracy: float = 0.70
    interventions_today: int = 0
    is_forced_break_active: bool = False
    forced_break_until: Optional[datetime] = None


@dataclass(frozen=True, slots=True)
class Intervention:
    """
    A psychological intervention.
    
    Attributes:
        intervention_type: Type of intervention
        priority: Priority (1 = highest)
        message: Message to show student
        action_required: Required action
        duration_minutes: How long to enforce (for breaks)
        notify_parents: Whether to alert parents
    """
    intervention_type: InterventionType
    priority: int
    message: str
    action_required: RecoveryAction
    duration_minutes: int = 0
    notify_parents: bool = False


@dataclass(frozen=True, slots=True)
class WellnessReport:
    """
    Complete wellness report for a student.
    
    Attributes:
        student_id: Student identifier
        timestamp: When report was generated
        burnout_level: Current burnout level
        risk_percentage: Overall risk percentage
        signals: Detected signals
        interventions: Recommended interventions
        positive_notes: Positive observations
        recommendations: General recommendations
    """
    student_id: StudentId
    timestamp: datetime
    burnout_level: BurnoutLevel
    risk_percentage: float
    signals: List[DistressSignal]
    interventions: List[Intervention]
    positive_notes: List[str]
    recommendations: List[str]


# ==============================================================================
# CORE ENGINE
# ==============================================================================

class PsychologyEngine:
    """
    Psychological Intelligence Engine.
    
    This engine monitors student psychological health and intervenes
    when burnout risk is detected.
    
    Key Features:
        1. 5-signal burnout detection
        2. 80% threshold automatic interventions
        3. Forced break system
        4. Parent/guardian alerts
        5. Recovery protocol guidance
    
    Example:
        >>> engine = PsychologyEngine()
        >>> state = engine.get_or_create_state("STU001")
        >>> engine.record_session(state, session)
        >>> report = engine.generate_wellness_report(state)
    """
    
    def __init__(self, reference_time: Optional[datetime] = None) -> None:
        """
        Initialize the Psychology Engine.
        
        Args:
            reference_time: Current time (for testing)
        """
        self._reference_time = reference_time
        self._states: Dict[StudentId, StudentPsychState] = {}
        self._sessions: Dict[StudentId, List[StudySession]] = {}
    
    @property
    def now(self) -> datetime:
        """Get current datetime."""
        return self._reference_time or datetime.now()
    
    def get_or_create_state(self, student_id: StudentId) -> StudentPsychState:
        """Get or create psychological state for a student."""
        if student_id not in self._states:
            self._states[student_id] = StudentPsychState(student_id=student_id)
            self._sessions[student_id] = []
        return self._states[student_id]
    
    def record_session(
        self,
        state: StudentPsychState,
        session: StudySession
    ) -> List[Intervention]:
        """
        Record a study session and check for interventions.
        
        Args:
            state: Student's psychological state
            session: The study session to record
            
        Returns:
            List of interventions triggered
        """
        # Store session
        if state.student_id not in self._sessions:
            self._sessions[state.student_id] = []
        self._sessions[state.student_id].append(session)
        
        # Update weekly hours
        state.weekly_hours += session.duration_minutes / 60.0
        
        # Check for heavy day
        if session.duration_minutes > MAX_SAFE_HOURS_PER_DAY * 60:
            state.consecutive_heavy_days += 1
        else:
            state.consecutive_heavy_days = 0
        
        # Analyze signals
        self._analyze_signals(state, session)
        
        # Check for interventions
        return self._check_interventions(state)
    
    def _analyze_signals(
        self,
        state: StudentPsychState,
        session: StudySession
    ) -> None:
        """
        Analyze session for distress signals.
        
        This implements the 5-signal detection system.
        """
        signals = state.signals
        signals.signals_detected.clear()
        
        # Signal 1: Overexertion
        if session.duration_minutes > MAX_SAFE_HOURS_PER_DAY * 60:
            signals.overexertion_score = min(1.0, session.duration_minutes / (12 * 60))
            signals.signals_detected.append(DistressSignal.OVEREXERTION)
        elif state.weekly_hours > MAX_SAFE_HOURS_PER_WEEK:
            signals.overexertion_score = min(1.0, state.weekly_hours / 70)
            signals.signals_detected.append(DistressSignal.OVEREXERTION)
        else:
            signals.overexertion_score = max(0, signals.overexertion_score - 0.1)
        
        # Signal 2: Accuracy Drop
        if session.questions_attempted > 0:
            session_accuracy = session.questions_correct / session.questions_attempted
            accuracy_drop = state.baseline_accuracy - session_accuracy
            
            if accuracy_drop > ACCURACY_DROP_CRITICAL:
                signals.accuracy_drop_score = min(1.0, accuracy_drop / 0.30)
                signals.signals_detected.append(DistressSignal.ACCURACY_DROP)
            elif accuracy_drop > ACCURACY_DROP_ALERT:
                signals.accuracy_drop_score = accuracy_drop / 0.30
            else:
                signals.accuracy_drop_score = max(0, signals.accuracy_drop_score - 0.1)
            
            # Update recent accuracy
            state.recent_accuracy = session_accuracy
        
        # Signal 3: Time Increase
        # If student is taking significantly longer per question
        if session.avg_time_per_question > 180:  # > 3 minutes per question
            signals.time_increase_score = min(1.0, session.avg_time_per_question / 300)
            signals.signals_detected.append(DistressSignal.TIME_INCREASE)
        else:
            signals.time_increase_score = max(0, signals.time_increase_score - 0.1)
        
        # Signal 4: Skip Pattern (detected from attempted vs total available)
        # This would need test-level data; using placeholder logic
        skip_rate = 0.0  # Placeholder
        if skip_rate > 0.20:
            signals.skip_pattern_score = min(1.0, skip_rate / 0.40)
            signals.signals_detected.append(DistressSignal.SKIP_PATTERN)
        
        # Signal 5: Erratic Schedule
        if state.consecutive_heavy_days >= 5:
            signals.erratic_schedule_score = min(1.0, state.consecutive_heavy_days / 7)
            signals.signals_detected.append(DistressSignal.ERRATIC_SCHEDULE)
        else:
            signals.erratic_schedule_score = max(0, signals.erratic_schedule_score - 0.1)
        
        # Update burnout level
        risk = signals.overall_risk
        if risk < 0.30:
            state.burnout_level = BurnoutLevel.HEALTHY
        elif risk < 0.50:
            state.burnout_level = BurnoutLevel.LOW_RISK
        elif risk < 0.70:
            state.burnout_level = BurnoutLevel.MODERATE
        elif risk < 0.85:
            state.burnout_level = BurnoutLevel.HIGH
        else:
            state.burnout_level = BurnoutLevel.CRITICAL
    
    def _check_interventions(
        self,
        state: StudentPsychState
    ) -> List[Intervention]:
        """
        Check if interventions are needed based on state.
        
        80% threshold triggers automatic interventions.
        """
        interventions: List[Intervention] = []
        risk = state.signals.overall_risk
        
        # No interventions needed
        if risk < BURNOUT_WARNING_THRESHOLD:
            return interventions
        
        # Warning level (60-80%)
        if risk < BURNOUT_CRITICAL_THRESHOLD:
            interventions.append(Intervention(
                intervention_type=InterventionType.SOFT_REMINDER,
                priority=3,
                message="You've been working hard! Consider a short break. 🧘",
                action_required=RecoveryAction.TAKE_BREAK,
                duration_minutes=15,
            ))
            
            if DistressSignal.ACCURACY_DROP in state.signals.signals_detected:
                interventions.append(Intervention(
                    intervention_type=InterventionType.ENCOURAGEMENT,
                    priority=4,
                    message="Your accuracy dipped - that's normal! Try reviewing what you know well. 💪",
                    action_required=RecoveryAction.REVIEW_STRENGTHS,
                ))
            
            return interventions
        
        # Critical level (80%+)
        # FORCED BREAK
        interventions.append(Intervention(
            intervention_type=InterventionType.FORCED_BREAK,
            priority=1,
            message="⚠️ You need a break now. Your performance shows fatigue. Taking 30 mins off.",
            action_required=RecoveryAction.TAKE_BREAK,
            duration_minutes=30,
        ))
        state.is_forced_break_active = True
        state.forced_break_until = self.now + timedelta(minutes=30)
        
        # Reduce difficulty
        interventions.append(Intervention(
            intervention_type=InterventionType.DIFFICULTY_REDUCTION,
            priority=2,
            message="When you return, we'll start with easier questions to rebuild momentum.",
            action_required=RecoveryAction.EASIER_CONTENT,
        ))
        
        # Alert parents for very high risk
        if risk > 0.90 or state.consecutive_heavy_days > 7:
            interventions.append(Intervention(
                intervention_type=InterventionType.PARENT_ALERT,
                priority=1,
                message="We've noticed signs of study burnout. Please check in with your child.",
                action_required=RecoveryAction.TALK_TO_SOMEONE,
                notify_parents=True,
            ))
        
        return interventions
    
    def is_break_active(self, state: StudentPsychState) -> bool:
        """Check if forced break is currently active."""
        if not state.is_forced_break_active:
            return False
        
        if state.forced_break_until and self.now >= state.forced_break_until:
            state.is_forced_break_active = False
            state.forced_break_until = None
            return False
        
        return True
    
    def get_break_remaining_minutes(self, state: StudentPsychState) -> int:
        """Get remaining minutes in forced break."""
        if not state.is_forced_break_active or not state.forced_break_until:
            return 0
        
        remaining = (state.forced_break_until - self.now).total_seconds() / 60
        return max(0, int(remaining))
    
    def generate_wellness_report(
        self,
        state: StudentPsychState
    ) -> WellnessReport:
        """
        Generate comprehensive wellness report.
        
        Args:
            state: Student's psychological state
            
        Returns:
            Complete wellness report
        """
        interventions = self._check_interventions(state)
        
        # Generate positive notes
        positive_notes: List[str] = []
        if state.burnout_level in (BurnoutLevel.HEALTHY, BurnoutLevel.LOW_RISK):
            positive_notes.append("✨ Your study patterns are healthy!")
        if state.recent_accuracy >= state.baseline_accuracy:
            positive_notes.append("📈 Your accuracy is on track!")
        if state.consecutive_heavy_days == 0:
            positive_notes.append("👏 Great job maintaining balance!")
        
        # Generate recommendations
        recommendations: List[str] = []
        if state.weekly_hours > MAX_SAFE_HOURS_PER_WEEK * 0.8:
            recommendations.append("Consider lighter study sessions this week")
        if len(state.signals.signals_detected) > 0:
            recommendations.append("Take regular 10-minute breaks every 90 minutes")
        if state.burnout_level.value >= BurnoutLevel.MODERATE.value:
            recommendations.append("Talk to someone about how you're feeling")
            recommendations.append("Get at least 8 hours of sleep tonight")
        
        return WellnessReport(
            student_id=state.student_id,
            timestamp=self.now,
            burnout_level=state.burnout_level,
            risk_percentage=state.signals.overall_risk * 100,
            signals=state.signals.signals_detected,
            interventions=interventions,
            positive_notes=positive_notes,
            recommendations=recommendations
        )
    
    def get_encouragement_message(
        self,
        state: StudentPsychState
    ) -> str:
        """Get contextual encouragement message."""
        if state.burnout_level == BurnoutLevel.HEALTHY:
            return "🌟 You're doing great! Keep up the excellent work."
        elif state.burnout_level == BurnoutLevel.LOW_RISK:
            return "💪 Good progress! Remember to take breaks."
        elif state.burnout_level == BurnoutLevel.MODERATE:
            return "🧘 You've been working hard. It's okay to slow down."
        else:
            return "❤️ Your health matters most. Take care of yourself."


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def create_psychology_engine() -> PsychologyEngine:
    """Create a new Psychology Engine."""
    return PsychologyEngine()


def check_burnout_risk(
    weekly_hours: float,
    accuracy_drop: float,
    consecutive_heavy_days: int
) -> BurnoutLevel:
    """Quick burnout risk check."""
    risk = 0.0
    
    if weekly_hours > MAX_SAFE_HOURS_PER_WEEK:
        risk += 0.3
    if accuracy_drop > ACCURACY_DROP_ALERT:
        risk += 0.3
    if consecutive_heavy_days > 5:
        risk += 0.3
    
    if risk < 0.30:
        return BurnoutLevel.HEALTHY
    elif risk < 0.50:
        return BurnoutLevel.LOW_RISK
    elif risk < 0.70:
        return BurnoutLevel.MODERATE
    else:
        return BurnoutLevel.HIGH


# ==============================================================================
# UNIT TESTS
# ==============================================================================

def test_signal_detection() -> None:
    """Test burnout signal detection."""
    engine = PsychologyEngine()
    state = engine.get_or_create_state("STU001")
    
    # Record a heavy session (> 8 hours)
    session = StudySession(
        session_id="S001",
        start_time=datetime.now(),
        duration_minutes=600,  # 10 hours!
        questions_attempted=100,
        questions_correct=50,  # 50% accuracy (below baseline)
    )
    
    engine.record_session(state, session)
    
    # Should detect overexertion
    assert DistressSignal.OVEREXERTION in state.signals.signals_detected
    # Should detect accuracy drop
    assert state.signals.accuracy_drop_score > 0
    
    print("✅ Signal detection test passed")


def test_intervention_triggers() -> None:
    """Test intervention triggers."""
    engine = PsychologyEngine()
    state = engine.get_or_create_state("STU001")
    
    # Create high-risk state - scores must be high enough to exceed 80% threshold
    # Overall risk = 0.25*overexertion + 0.25*accuracy + 0.20*time + 0.15*skip + 0.15*erratic
    # Need sum > 0.80
    state.signals.overexertion_score = 1.0      # 0.25 contribution
    state.signals.accuracy_drop_score = 1.0     # 0.25 contribution  
    state.signals.time_increase_score = 1.0     # 0.20 contribution
    state.signals.skip_pattern_score = 1.0      # 0.15 contribution
    state.signals.erratic_schedule_score = 1.0  # 0.15 contribution
    # Total = 1.0 (100% risk)
    
    interventions = engine._check_interventions(state)
    
    # Should trigger interventions (>80% risk = forced break)
    assert len(interventions) > 0
    assert any(i.intervention_type == InterventionType.FORCED_BREAK for i in interventions)
    
    print("✅ Intervention triggers test passed")


def test_forced_break() -> None:
    """Test forced break functionality."""
    day_1 = datetime(2024, 12, 10, 10, 0)
    engine = PsychologyEngine(reference_time=day_1)
    state = engine.get_or_create_state("STU001")
    
    # Activate forced break
    state.is_forced_break_active = True
    state.forced_break_until = day_1 + timedelta(minutes=30)
    
    # Should be active
    assert engine.is_break_active(state) == True
    assert engine.get_break_remaining_minutes(state) == 30
    
    # After 30 mins, should be inactive
    engine._reference_time = day_1 + timedelta(minutes=31)
    assert engine.is_break_active(state) == False
    
    print("✅ Forced break test passed")


def test_wellness_report() -> None:
    """Test wellness report generation."""
    engine = PsychologyEngine()
    state = engine.get_or_create_state("STU001")
    
    report = engine.generate_wellness_report(state)
    
    assert report.student_id == "STU001"
    assert report.burnout_level == BurnoutLevel.HEALTHY
    assert len(report.positive_notes) > 0  # Should have positive notes for healthy state
    
    print("✅ Wellness report test passed")


def test_encouragement_messages() -> None:
    """Test contextual encouragement messages."""
    engine = PsychologyEngine()
    state = engine.get_or_create_state("STU001")
    
    # Healthy state
    msg = engine.get_encouragement_message(state)
    assert "great" in msg.lower() or "excellent" in msg.lower()
    
    # Moderate burnout
    state.burnout_level = BurnoutLevel.MODERATE
    msg = engine.get_encouragement_message(state)
    assert "slow down" in msg.lower() or "working hard" in msg.lower()
    
    print("✅ Encouragement messages test passed")


def run_all_tests() -> None:
    """Run all unit tests."""
    print("Running Psychology Engine tests...")
    test_signal_detection()
    test_intervention_triggers()
    test_forced_break()
    test_wellness_report()
    test_encouragement_messages()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
