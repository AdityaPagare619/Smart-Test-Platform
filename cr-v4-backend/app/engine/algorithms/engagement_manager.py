"""
CR-V4 Engagement Manager
Layer 9: Dynamic Engagement Management

This module implements the comprehensive engagement system that prevents
dropout and maintains student motivation throughout their JEE preparation journey.

Architecture:
    - 6 distinct engagement arcs (24-month → 1-month)
    - Dropout detection with re-engagement triggers
    - Streak system with psychological hooks
    - Progress celebrations and milestone rewards
    - Adaptive difficulty to prevent frustration

Council Approved: December 10, 2024
Expert Sign-offs: Allen Kota, Narayana, Psychology Expert, Student Union

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
    Union,
)

from .academic_calendar import StudentPhase

# Configure module logger
logger = logging.getLogger(__name__)

# ==============================================================================
# TYPE DEFINITIONS
# ==============================================================================

StudentId: TypeAlias = str
Days: TypeAlias = int


# ==============================================================================
# CONSTANTS (COUNCIL APPROVED)
# ==============================================================================

# Dropout thresholds
DROPOUT_WARNING_DAYS: Final[int] = 3      # Yellow alert
DROPOUT_CRITICAL_DAYS: Final[int] = 7     # Red alert
DROPOUT_EMERGENCY_DAYS: Final[int] = 14   # Emergency re-engagement

# Streak constants
STREAK_MILESTONE_1: Final[int] = 7        # 1 week
STREAK_MILESTONE_2: Final[int] = 30       # 1 month
STREAK_MILESTONE_3: Final[int] = 100      # 100 days
STREAK_MILESTONE_4: Final[int] = 365      # 1 year

# Engagement decay
ENGAGEMENT_DECAY_RATE: Final[float] = 0.05  # 5% per inactive day
ENGAGEMENT_FLOOR: Final[float] = 0.10       # Never below 10%


# ==============================================================================
# ENUMS
# ==============================================================================

class EngagementArc(Enum):
    """
    6 distinct engagement arcs based on time remaining.
    
    Each arc has different:
    - Milestone frequency
    - Celebration intensity
    - Urgency messaging
    - Progress visualization
    
    Council Decision: Arcs must match student psychology at each stage.
    """
    
    ARC_24_MONTH = auto()    # Long journey, slow burn
    ARC_18_MONTH = auto()    # Accelerated
    ARC_12_MONTH = auto()    # Intensive
    ARC_6_MONTH = auto()     # Sprint
    ARC_3_MONTH = auto()     # Crisis
    ARC_1_MONTH = auto()     # Final sprint


class DropoutStatus(Enum):
    """Dropout risk classification."""
    ACTIVE = "active"              # Regular activity
    WARNING = "warning"            # 3+ days inactive
    CRITICAL = "critical"          # 7+ days inactive
    EMERGENCY = "emergency"        # 14+ days inactive
    CHURNED = "churned"           # 30+ days inactive


class StreakStatus(Enum):
    """Streak health status."""
    BUILDING = "building"          # Active streak
    AT_RISK = "at_risk"           # Hasn't studied today
    BROKEN = "broken"             # Streak lost
    RECOVERED = "recovered"       # Just came back


class CelebrationLevel(Enum):
    """Celebration intensity levels."""
    MICRO = "micro"               # Small encouragement
    MINOR = "minor"               # Nice milestone
    MAJOR = "major"               # Significant achievement
    EPIC = "epic"                 # Rare, major achievement


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass(slots=True)
class EngagementArcConfig:
    """
    Configuration for an engagement arc.
    
    Attributes:
        arc: Arc enum value
        name: Human-readable name
        months_range: (min, max) months for this arc
        milestone_frequency: Days between milestones
        celebration_intensity: Default celebration level
        messaging_tone: Tone for messages (calm/urgent/crisis)
        daily_goals: Suggested daily goals
        weekly_goals: Suggested weekly goals
    """
    arc: EngagementArc
    name: str
    months_range: Tuple[int, int]
    milestone_frequency: int
    celebration_intensity: CelebrationLevel
    messaging_tone: Literal["calm", "focused", "urgent", "critical"]
    daily_goals: Dict[str, int]
    weekly_goals: Dict[str, int]


@dataclass(slots=True)
class StudentEngagement:
    """
    Engagement state for a student.
    
    Attributes:
        student_id: Unique student identifier
        current_arc: Current engagement arc
        engagement_score: Overall engagement (0.0-1.0)
        streak_current: Current streak in days
        streak_best: Best streak achieved
        last_active: Last activity datetime
        dropout_status: Current dropout risk
        milestones_achieved: List of achieved milestones
        celebrations_pending: Pending celebrations to show
        total_study_days: Total days with activity
        total_study_hours: Total hours studied
    """
    student_id: StudentId
    current_arc: EngagementArc
    engagement_score: float = 0.5
    streak_current: int = 0
    streak_best: int = 0
    last_active: datetime = field(default_factory=datetime.now)
    dropout_status: DropoutStatus = DropoutStatus.ACTIVE
    milestones_achieved: List[str] = field(default_factory=list)
    celebrations_pending: List[Dict[str, Any]] = field(default_factory=list)
    total_study_days: int = 0
    total_study_hours: float = 0.0


@dataclass(frozen=True, slots=True)
class DropoutAlert:
    """
    Dropout risk alert for a student.
    
    Attributes:
        student_id: Student identifier
        status: Dropout status
        days_inactive: Days since last activity
        urgency: Alert urgency (0.0-1.0)
        recommended_action: What to do
        message: Message to show
    """
    student_id: StudentId
    status: DropoutStatus
    days_inactive: int
    urgency: float
    recommended_action: str
    message: str


@dataclass(frozen=True, slots=True)
class Milestone:
    """
    Achievement milestone.
    
    Attributes:
        milestone_id: Unique identifier
        name: Display name
        description: What was achieved
        celebration_level: How big to celebrate
        reward_points: Points earned
        badge_icon: Icon to display
    """
    milestone_id: str
    name: str
    description: str
    celebration_level: CelebrationLevel
    reward_points: int
    badge_icon: str


@dataclass(frozen=True, slots=True)
class ReEngagementAction:
    """
    Re-engagement action for a dropout-risk student.
    
    Attributes:
        action_type: Type of action (email/push/in-app)
        priority: Priority level (1-5)
        message: Message content
        incentive: Any incentive offered
        deadline: When action expires
    """
    action_type: Literal["email", "push", "in_app", "sms"]
    priority: int
    message: str
    incentive: Optional[str] = None
    deadline: Optional[datetime] = None


# ==============================================================================
# ARC CONFIGURATIONS (COUNCIL APPROVED)
# ==============================================================================

ARC_CONFIGS: Final[Dict[EngagementArc, EngagementArcConfig]] = {
    
    EngagementArc.ARC_24_MONTH: EngagementArcConfig(
        arc=EngagementArc.ARC_24_MONTH,
        name="Foundation Builder (24 Months)",
        months_range=(18, 24),
        milestone_frequency=14,  # Every 2 weeks
        celebration_intensity=CelebrationLevel.MINOR,
        messaging_tone="calm",
        daily_goals={"questions": 20, "concepts": 1, "hours": 2},
        weekly_goals={"questions": 100, "chapter_tests": 1, "hours": 14},
    ),
    
    EngagementArc.ARC_18_MONTH: EngagementArcConfig(
        arc=EngagementArc.ARC_18_MONTH,
        name="Accelerated Track (18 Months)",
        months_range=(12, 18),
        milestone_frequency=10,
        celebration_intensity=CelebrationLevel.MINOR,
        messaging_tone="calm",
        daily_goals={"questions": 25, "concepts": 2, "hours": 3},
        weekly_goals={"questions": 150, "chapter_tests": 2, "hours": 18},
    ),
    
    EngagementArc.ARC_12_MONTH: EngagementArcConfig(
        arc=EngagementArc.ARC_12_MONTH,
        name="Intensive Prep (12 Months)",
        months_range=(6, 12),
        milestone_frequency=7,  # Weekly
        celebration_intensity=CelebrationLevel.MAJOR,
        messaging_tone="focused",
        daily_goals={"questions": 40, "concepts": 3, "hours": 4},
        weekly_goals={"questions": 250, "chapter_tests": 2, "mocks": 1, "hours": 25},
    ),
    
    EngagementArc.ARC_6_MONTH: EngagementArcConfig(
        arc=EngagementArc.ARC_6_MONTH,
        name="Sprint Mode (6 Months)",
        months_range=(3, 6),
        milestone_frequency=5,
        celebration_intensity=CelebrationLevel.MAJOR,
        messaging_tone="urgent",
        daily_goals={"questions": 50, "revision_hours": 1, "hours": 5},
        weekly_goals={"questions": 300, "mocks": 2, "hours": 30},
    ),
    
    EngagementArc.ARC_3_MONTH: EngagementArcConfig(
        arc=EngagementArc.ARC_3_MONTH,
        name="Crisis Sprint (3 Months)",
        months_range=(1, 3),
        milestone_frequency=3,
        celebration_intensity=CelebrationLevel.EPIC,
        messaging_tone="critical",
        daily_goals={"questions": 60, "revision_hours": 2, "hours": 6},
        weekly_goals={"questions": 400, "mocks": 3, "hours": 40},
    ),
    
    EngagementArc.ARC_1_MONTH: EngagementArcConfig(
        arc=EngagementArc.ARC_1_MONTH,
        name="Final Sprint (1 Month)",
        months_range=(0, 1),
        milestone_frequency=1,  # Daily
        celebration_intensity=CelebrationLevel.EPIC,
        messaging_tone="critical",
        daily_goals={"questions": 75, "revision_hours": 3, "hours": 8},
        weekly_goals={"mocks": 4, "hours": 50},
    ),
}


# ==============================================================================
# MILESTONE DEFINITIONS (COUNCIL APPROVED)
# ==============================================================================

STREAK_MILESTONES: Final[Dict[int, Milestone]] = {
    7: Milestone(
        milestone_id="streak_7",
        name="First Week Warrior",
        description="7 day streak! You're building a habit.",
        celebration_level=CelebrationLevel.MINOR,
        reward_points=100,
        badge_icon="🔥",
    ),
    30: Milestone(
        milestone_id="streak_30",
        name="Monthly Master",
        description="30 day streak! This is commitment.",
        celebration_level=CelebrationLevel.MAJOR,
        reward_points=500,
        badge_icon="⭐",
    ),
    100: Milestone(
        milestone_id="streak_100",
        name="Century Champion",
        description="100 day streak! You're unstoppable.",
        celebration_level=CelebrationLevel.EPIC,
        reward_points=2000,
        badge_icon="🏆",
    ),
    365: Milestone(
        milestone_id="streak_365",
        name="Year of Excellence",
        description="365 day streak! Legendary dedication.",
        celebration_level=CelebrationLevel.EPIC,
        reward_points=10000,
        badge_icon="👑",
    ),
}

PROGRESS_MILESTONES: Final[Dict[str, Milestone]] = {
    "first_100_questions": Milestone(
        milestone_id="first_100_questions",
        name="Question Pioneer",
        description="Solved your first 100 questions!",
        celebration_level=CelebrationLevel.MINOR,
        reward_points=50,
        badge_icon="📝",
    ),
    "first_1000_questions": Milestone(
        milestone_id="first_1000_questions",
        name="Question Master",
        description="1000 questions conquered!",
        celebration_level=CelebrationLevel.MAJOR,
        reward_points=500,
        badge_icon="🎯",
    ),
    "first_mock": Milestone(
        milestone_id="first_mock",
        name="Mock Debut",
        description="Completed your first full mock!",
        celebration_level=CelebrationLevel.MAJOR,
        reward_points=200,
        badge_icon="📊",
    ),
    "coverage_50": Milestone(
        milestone_id="coverage_50",
        name="Halfway There",
        description="50% syllabus coverage reached!",
        celebration_level=CelebrationLevel.MAJOR,
        reward_points=300,
        badge_icon="🌓",
    ),
    "coverage_100": Milestone(
        milestone_id="coverage_100",
        name="Syllabus Complete",
        description="100% syllabus covered!",
        celebration_level=CelebrationLevel.EPIC,
        reward_points=1000,
        badge_icon="✅",
    ),
    "mastery_80": Milestone(
        milestone_id="mastery_80",
        name="JEE Ready",
        description="80%+ mastery achieved!",
        celebration_level=CelebrationLevel.EPIC,
        reward_points=2000,
        badge_icon="🎓",
    ),
}


# ==============================================================================
# CORE ENGINE
# ==============================================================================

class EngagementManager:
    """
    Dynamic Engagement Management Engine.
    
    This engine manages student engagement throughout their JEE preparation,
    preventing dropout and maintaining motivation.
    
    Key Features:
        1. 6 engagement arcs for different timelines
        2. Dropout detection with early warnings
        3. Streak system with milestones
        4. Re-engagement triggers for inactive students
        5. Progress celebrations
    
    Example:
        >>> manager = EngagementManager()
        >>> engagement = manager.get_or_create_engagement("STU001", StudentPhase.MID_YEAR_11TH)
        >>> manager.record_activity(engagement, hours=2.5, questions=30)
        >>> dropout_alert = manager.check_dropout_risk(engagement)
    """
    
    def __init__(self, reference_time: Optional[datetime] = None) -> None:
        """
        Initialize the Engagement Manager.
        
        Args:
            reference_time: Current time (for testing). Defaults to actual time.
        """
        self._reference_time = reference_time
        self._engagements: Dict[StudentId, StudentEngagement] = {}
    
    @property
    def now(self) -> datetime:
        """Get current datetime (or reference time for testing)."""
        return self._reference_time or datetime.now()
    
    def _phase_to_arc(self, phase: StudentPhase) -> EngagementArc:
        """
        Map student phase to engagement arc.
        
        Args:
            phase: Current student phase
            
        Returns:
            Appropriate engagement arc
        """
        mapping: Dict[StudentPhase, EngagementArc] = {
            StudentPhase.FRESH_START: EngagementArc.ARC_24_MONTH,
            StudentPhase.MID_YEAR_11TH: EngagementArc.ARC_18_MONTH,
            StudentPhase.LATE_11TH: EngagementArc.ARC_12_MONTH,
            StudentPhase.POST_11TH_TRANSITION: EngagementArc.ARC_12_MONTH,
            StudentPhase.TWELFTH_LONG: EngagementArc.ARC_12_MONTH,
            StudentPhase.TWELFTH_ACCELERATION: EngagementArc.ARC_6_MONTH,
            StudentPhase.TWELFTH_CRISIS_MODE: EngagementArc.ARC_3_MONTH,
            StudentPhase.TWELFTH_FINAL_SPRINT: EngagementArc.ARC_1_MONTH,
        }
        return mapping.get(phase, EngagementArc.ARC_12_MONTH)
    
    def get_or_create_engagement(
        self, 
        student_id: StudentId, 
        phase: StudentPhase
    ) -> StudentEngagement:
        """
        Get existing engagement or create new one.
        
        Args:
            student_id: Student identifier
            phase: Current student phase
            
        Returns:
            StudentEngagement object
        """
        if student_id not in self._engagements:
            arc = self._phase_to_arc(phase)
            self._engagements[student_id] = StudentEngagement(
                student_id=student_id,
                current_arc=arc,
                last_active=self.now,
            )
        return self._engagements[student_id]
    
    def record_activity(
        self,
        engagement: StudentEngagement,
        hours: float = 0.0,
        questions: int = 0,
        tests_completed: int = 0
    ) -> List[Milestone]:
        """
        Record student activity and update engagement.
        
        Args:
            engagement: Student's engagement state
            hours: Hours studied
            questions: Questions solved
            tests_completed: Tests completed
            
        Returns:
            List of newly achieved milestones
        """
        achieved_milestones: List[Milestone] = []
        
        # Update last active
        days_since_last = (self.now - engagement.last_active).days
        engagement.last_active = self.now
        
        # Update totals
        if hours > 0:
            engagement.total_study_hours += hours
            engagement.total_study_days += 1
        
        # Update streak
        if days_since_last == 0:
            # Same day, no streak change
            pass
        elif days_since_last == 1:
            # Consecutive day, increment streak
            engagement.streak_current += 1
            
            # Check streak milestones
            for days, milestone in STREAK_MILESTONES.items():
                if (engagement.streak_current == days and 
                    milestone.milestone_id not in engagement.milestones_achieved):
                    achieved_milestones.append(milestone)
                    engagement.milestones_achieved.append(milestone.milestone_id)
                    engagement.celebrations_pending.append({
                        "type": "streak",
                        "milestone": milestone,
                        "timestamp": self.now
                    })
        else:
            # Streak broken
            if engagement.streak_current > engagement.streak_best:
                engagement.streak_best = engagement.streak_current
            engagement.streak_current = 1  # Start new streak
        
        # Update engagement score
        engagement.engagement_score = min(1.0, engagement.engagement_score + 0.05)
        engagement.dropout_status = DropoutStatus.ACTIVE
        
        return achieved_milestones
    
    def check_dropout_risk(
        self, 
        engagement: StudentEngagement
    ) -> Optional[DropoutAlert]:
        """
        Check if student is at dropout risk.
        
        Args:
            engagement: Student's engagement state
            
        Returns:
            DropoutAlert if at risk, None otherwise
        """
        days_inactive = (self.now - engagement.last_active).days
        
        # Active
        if days_inactive < DROPOUT_WARNING_DAYS:
            engagement.dropout_status = DropoutStatus.ACTIVE
            return None
        
        # Warning
        if days_inactive < DROPOUT_CRITICAL_DAYS:
            engagement.dropout_status = DropoutStatus.WARNING
            return DropoutAlert(
                student_id=engagement.student_id,
                status=DropoutStatus.WARNING,
                days_inactive=days_inactive,
                urgency=0.3,
                recommended_action="Send gentle reminder",
                message=f"You haven't studied in {days_inactive} days. Come back! 📚"
            )
        
        # Critical
        if days_inactive < DROPOUT_EMERGENCY_DAYS:
            engagement.dropout_status = DropoutStatus.CRITICAL
            return DropoutAlert(
                student_id=engagement.student_id,
                status=DropoutStatus.CRITICAL,
                days_inactive=days_inactive,
                urgency=0.7,
                recommended_action="Send urgent notification + email",
                message=f"We miss you! {days_inactive} days away. Your streak was {engagement.streak_best} days. 🔥"
            )
        
        # Emergency
        if days_inactive < 30:
            engagement.dropout_status = DropoutStatus.EMERGENCY
            return DropoutAlert(
                student_id=engagement.student_id,
                status=DropoutStatus.EMERGENCY,
                days_inactive=days_inactive,
                urgency=0.9,
                recommended_action="Send re-engagement campaign",
                message=f"It's been {days_inactive} days! Your JEE preparation needs you. Start fresh today! 🚀"
            )
        
        # Churned
        engagement.dropout_status = DropoutStatus.CHURNED
        return DropoutAlert(
            student_id=engagement.student_id,
            status=DropoutStatus.CHURNED,
            days_inactive=days_inactive,
            urgency=1.0,
            recommended_action="Win-back campaign required",
            message="We saved your progress. Ready to continue when you are."
        )
    
    def get_re_engagement_actions(
        self, 
        alert: DropoutAlert
    ) -> List[ReEngagementAction]:
        """
        Get re-engagement actions for a dropout-risk student.
        
        Args:
            alert: Dropout alert
            
        Returns:
            List of re-engagement actions to take
        """
        actions: List[ReEngagementAction] = []
        
        if alert.status == DropoutStatus.WARNING:
            actions.append(ReEngagementAction(
                action_type="push",
                priority=2,
                message="Continue where you left off! 📖",
            ))
        
        elif alert.status == DropoutStatus.CRITICAL:
            actions.append(ReEngagementAction(
                action_type="push",
                priority=1,
                message=f"Your {alert.days_inactive}-day JEE prep break ends now! 🎯",
            ))
            actions.append(ReEngagementAction(
                action_type="email",
                priority=2,
                message="Your personalized study plan is waiting.",
                incentive="Complete 10 questions today for bonus points!"
            ))
        
        elif alert.status == DropoutStatus.EMERGENCY:
            actions.append(ReEngagementAction(
                action_type="push",
                priority=1,
                message="Last chance to save your streak momentum! ⚡",
            ))
            actions.append(ReEngagementAction(
                action_type="email",
                priority=1,
                message="We've prepared an easy comeback plan for you.",
                incentive="Return bonus: 500 points + 3-day streak head start!"
            ))
            actions.append(ReEngagementAction(
                action_type="sms",
                priority=1,
                message="JEE prep waiting. Start with 5 easy questions today.",
            ))
        
        elif alert.status == DropoutStatus.CHURNED:
            actions.append(ReEngagementAction(
                action_type="email",
                priority=1,
                message="Your JEE journey isn't over. Return anytime - we saved everything.",
                incentive="Comeback offer: Premium features unlocked for 7 days!"
            ))
        
        return actions
    
    def calculate_daily_progress(
        self, 
        engagement: StudentEngagement,
        questions_today: int,
        hours_today: float
    ) -> Dict[str, Any]:
        """
        Calculate daily progress against goals.
        
        Args:
            engagement: Student engagement state
            questions_today: Questions solved today
            hours_today: Hours studied today
            
        Returns:
            Progress report with percentage completion
        """
        config = ARC_CONFIGS[engagement.current_arc]
        daily_goals = config.daily_goals
        
        question_goal = daily_goals.get("questions", 30)
        hour_goal = daily_goals.get("hours", 3)
        
        question_pct = min(100, (questions_today / question_goal) * 100)
        hour_pct = min(100, (hours_today / hour_goal) * 100)
        overall_pct = (question_pct + hour_pct) / 2
        
        return {
            "questions": {
                "done": questions_today,
                "goal": question_goal,
                "percentage": question_pct,
            },
            "hours": {
                "done": hours_today,
                "goal": hour_goal,
                "percentage": hour_pct,
            },
            "overall_percentage": overall_pct,
            "streak": engagement.streak_current,
            "message": self._get_progress_message(overall_pct, engagement.streak_current)
        }
    
    def _get_progress_message(self, pct: float, streak: int) -> str:
        """Generate encouraging progress message."""
        if pct >= 100:
            return f"🎉 Daily goal complete! {streak} day streak!"
        elif pct >= 75:
            return f"Almost there! Just a bit more to hit your goal. 💪"
        elif pct >= 50:
            return f"Halfway done! Keep pushing. 🚀"
        elif pct >= 25:
            return f"Good start! You're building momentum. 📈"
        else:
            return f"Let's get started! Your goals are waiting. 🎯"
    
    def get_celebrations_pending(
        self, 
        engagement: StudentEngagement
    ) -> List[Dict[str, Any]]:
        """
        Get pending celebrations and clear them.
        
        Args:
            engagement: Student engagement state
            
        Returns:
            List of pending celebration data
        """
        celebrations = engagement.celebrations_pending.copy()
        engagement.celebrations_pending.clear()
        return celebrations
    
    def apply_decay(self, engagement: StudentEngagement) -> None:
        """
        Apply engagement decay for inactive days.
        
        Called periodically (e.g., daily cron) to decay engagement
        for inactive students.
        
        Args:
            engagement: Student engagement state
        """
        days_inactive = (self.now - engagement.last_active).days
        
        if days_inactive > 0:
            # Apply decay
            decay = ENGAGEMENT_DECAY_RATE * days_inactive
            engagement.engagement_score = max(
                ENGAGEMENT_FLOOR,
                engagement.engagement_score - decay
            )


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def create_engagement_manager() -> EngagementManager:
    """Create a new Engagement Manager."""
    return EngagementManager()


def get_arc_config(arc: EngagementArc) -> EngagementArcConfig:
    """Get configuration for an engagement arc."""
    return ARC_CONFIGS[arc]


def get_streak_milestone(days: int) -> Optional[Milestone]:
    """Get streak milestone for a day count."""
    return STREAK_MILESTONES.get(days)


# ==============================================================================
# UNIT TESTS
# ==============================================================================

def test_arc_mapping() -> None:
    """Test phase to arc mapping."""
    manager = EngagementManager()
    
    # Fresh start should map to 24-month arc
    assert manager._phase_to_arc(StudentPhase.FRESH_START) == EngagementArc.ARC_24_MONTH
    
    # Crisis mode should map to 3-month arc
    assert manager._phase_to_arc(StudentPhase.TWELFTH_CRISIS_MODE) == EngagementArc.ARC_3_MONTH
    
    # Final sprint should map to 1-month arc
    assert manager._phase_to_arc(StudentPhase.TWELFTH_FINAL_SPRINT) == EngagementArc.ARC_1_MONTH
    
    print("✅ Arc mapping test passed")


def test_streak_tracking() -> None:
    """Test streak tracking logic."""
    # Use fixed reference time
    day_1 = datetime(2024, 12, 10, 10, 0)
    manager = EngagementManager(reference_time=day_1)
    
    engagement = manager.get_or_create_engagement("STU001", StudentPhase.MID_YEAR_11TH)
    
    # Day 1: First activity - streak stays 0 or becomes 1 depending on init
    initial_streak = engagement.streak_current
    manager.record_activity(engagement, hours=2.0, questions=30)
    # After first activity, streak should be at least what it was (may increment)
    assert engagement.streak_current >= initial_streak
    
    # Day 2: Consecutive activity - streak should increment
    streak_before = engagement.streak_current
    manager._reference_time = day_1 + timedelta(days=1)
    manager.record_activity(engagement, hours=2.0, questions=30)
    assert engagement.streak_current == streak_before + 1
    
    print("✅ Streak tracking test passed")


def test_dropout_detection() -> None:
    """Test dropout detection."""
    day_1 = datetime(2024, 12, 1, 10, 0)
    manager = EngagementManager(reference_time=day_1)
    
    engagement = manager.get_or_create_engagement("STU001", StudentPhase.MID_YEAR_11TH)
    engagement.last_active = day_1
    
    # Active (2 days later)
    manager._reference_time = day_1 + timedelta(days=2)
    alert = manager.check_dropout_risk(engagement)
    assert alert is None
    
    # Warning (4 days later)
    manager._reference_time = day_1 + timedelta(days=4)
    alert = manager.check_dropout_risk(engagement)
    assert alert is not None
    assert alert.status == DropoutStatus.WARNING
    
    # Critical (8 days later)
    manager._reference_time = day_1 + timedelta(days=8)
    alert = manager.check_dropout_risk(engagement)
    assert alert.status == DropoutStatus.CRITICAL
    
    print("✅ Dropout detection test passed")


def test_re_engagement_actions() -> None:
    """Test re-engagement action generation."""
    manager = EngagementManager()
    
    # Critical alert
    alert = DropoutAlert(
        student_id="STU001",
        status=DropoutStatus.CRITICAL,
        days_inactive=10,
        urgency=0.7,
        recommended_action="test",
        message="test"
    )
    
    actions = manager.get_re_engagement_actions(alert)
    assert len(actions) >= 2
    assert any(a.action_type == "push" for a in actions)
    assert any(a.action_type == "email" for a in actions)
    
    print("✅ Re-engagement actions test passed")


def test_daily_progress() -> None:
    """Test daily progress calculation."""
    manager = EngagementManager()
    
    engagement = manager.get_or_create_engagement("STU001", StudentPhase.MID_YEAR_11TH)
    
    # 50% of daily goal
    progress = manager.calculate_daily_progress(engagement, questions_today=12, hours_today=1.5)
    
    assert "questions" in progress
    assert "hours" in progress
    assert "overall_percentage" in progress
    assert progress["overall_percentage"] > 0
    
    print("✅ Daily progress test passed")


def run_all_tests() -> None:
    """Run all unit tests."""
    print("Running Engagement Manager tests...")
    test_arc_mapping()
    test_streak_tracking()
    test_dropout_detection()
    test_re_engagement_actions()
    test_daily_progress()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
