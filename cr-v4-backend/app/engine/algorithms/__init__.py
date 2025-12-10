"""
CR-V4 Core Algorithms Package

Contains the mathematical foundation of the AI engine:
- bayesian_learning: Mastery estimation using Bayes theorem
- irt_model: Item Response Theory 3PL model
- knowledge_state: 3 time-scale knowledge tracking (SAINT-equivalent)
- question_selector: Multi-criteria question selection
- misconception_detector: Severity-based misconception detection
- student_profiles: Student classification and dynamic weights
- diagnostic_engine: Cold-start assessment
- jee_mains_engine: JEE-MAINS structure and strategies
- academic_calendar: Dynamic academic calendar with 8 phases (NEW)
"""

from .bayesian_learning import (
    QuestionAttempt,
    BayesUpdateResult,
    UpdateDirection,
    bayes_update_mastery
)

from .irt_model import (
    IRTParameters,
    QuestionDifficulty,
    irt_probability,
    fisher_information,
    estimate_ability,
    ability_to_mastery,
    mastery_to_ability,
    calculate_selection_score,
    calibrate_question,
    get_subject_c,
    SUBJECT_C_VALUES
)

from .knowledge_state import (
    StudentKnowledgeState,
    ConceptState,
    InteractionRecord,
    KnowledgeStateTracker,
    create_student_state,
    process_interaction,
    SUBJECT_TIME_WEIGHTS,
    RETENTION_FLOOR
)

from .question_selector import (
    Question,
    SelectionResult,
    ConceptNode,
    QuestionSelector,
    MathSelector,
    PhysicsSelector,
    ChemistrySelector,
    SyllabusStatus,
    CompetencyType,
    SUBJECT_STRATEGIES
)

from .misconception_detector import (
    Misconception,
    MisconceptionSeverity,
    MisconceptionCategory,
    DetectionResult,
    RecoveryPlan,
    MisconceptionDetector,
    RecoveryEngine,
    analyze_and_intervene
)

from .student_profiles import (
    StudentProfile,
    StudentTier,
    LearningStyle,
    StudentClassification,
    StudentProfileClassifier,
    get_selection_weights,
    get_subject_adjustments
)

from .diagnostic_engine import (
    DiagnosticEngine,
    DiagnosticResult,
    DiagnosticStatus,
    DiagnosticQuestion,
    create_diagnostic_session,
    run_diagnostic
)

from .jee_mains_engine import (
    JEE_MAINS_PATTERN,
    MARKS_TO_PERCENTILE_2024,
    HIGH_YIELD_TOPICS,
    ScorePrediction,
    TimeStrategy,
    get_time_allocation,
    get_topic_priority,
    predict_score,
    percentile_to_rank
)

from .academic_calendar import (
    StudentPhase,
    PhaseConfig,
    StudentProfile as CalendarStudentProfile,
    PhaseResult,
    AcademicCalendarEngine,
    PHASE_CONFIGS,
    determine_student_phase,
    get_phase_config,
    calculate_days_to_jee,
)

from .concept_reveal import (
    ConceptTier,
    RevealStatus,
    ConceptVisibility,
    RevealSchedule,
    ProgressMessage,
    ConceptRevealEngine,
    HIGH_YIELD_TOPICS,
    CONCEPT_TIERS,
    create_reveal_engine,
    get_visible_for_phase,
    get_high_yield_topics,
    get_concept_tier,
)

from .test_manager import (
    TestLevel,
    TestStatus,
    DifficultyLevel,
    QuestionType,
    TestLevelConfig,
    Test,
    TestResult,
    TestManager,
    TEST_LEVEL_CONFIGS,
    create_test_manager,
)

from .engagement_manager import (
    EngagementArc,
    DropoutStatus,
    StreakStatus,
    CelebrationLevel,
    StudentEngagement,
    DropoutAlert,
    Milestone,
    EngagementManager,
    ARC_CONFIGS,
    STREAK_MILESTONES,
    create_engagement_manager,
)

from .root_cause_analyzer import (
    GapSeverity,
    RootCauseType,
    RemediationType,
    RootCause,
    FailureAnalysis,
    RootCauseAnalyzer,
    create_root_cause_analyzer,
    analyze_concept_failure,
)

from .psychology_engine import (
    BurnoutLevel,
    DistressSignal,
    InterventionType,
    RecoveryAction,
    StudySession,
    BurnoutSignals,
    StudentPsychState,
    Intervention,
    WellnessReport,
    PsychologyEngine,
    create_psychology_engine,
    check_burnout_risk,
)

__all__ = [
    # Bayesian
    'QuestionAttempt',
    'BayesUpdateResult',
    'UpdateDirection',
    'bayes_update_mastery',
    
    # IRT
    'IRTParameters',
    'QuestionDifficulty',
    'irt_probability',
    'fisher_information',
    'estimate_ability',
    'ability_to_mastery',
    'mastery_to_ability',
    'calculate_selection_score',
    'calibrate_question',
    'get_subject_c',
    'SUBJECT_C_VALUES',
    
    # Knowledge State
    'StudentKnowledgeState',
    'ConceptState',
    'InteractionRecord',
    'KnowledgeStateTracker',
    'create_student_state',
    'process_interaction',
    'SUBJECT_TIME_WEIGHTS',
    'RETENTION_FLOOR',
    
    # Question Selection
    'Question',
    'SelectionResult',
    'ConceptNode',
    'QuestionSelector',
    'MathSelector',
    'PhysicsSelector',
    'ChemistrySelector',
    'SyllabusStatus',
    'CompetencyType',
    'SUBJECT_STRATEGIES',
    
    # Misconception
    'Misconception',
    'MisconceptionSeverity',
    'MisconceptionCategory',
    'DetectionResult',
    'RecoveryPlan',
    'MisconceptionDetector',
    'RecoveryEngine',
    'analyze_and_intervene',
    
    # Student Profiles
    'StudentProfile',
    'StudentTier',
    'LearningStyle',
    'StudentClassification',
    'StudentProfileClassifier',
    'get_selection_weights',
    'get_subject_adjustments',
    
    # Diagnostic Engine
    'DiagnosticEngine',
    'DiagnosticResult',
    'DiagnosticStatus',
    'DiagnosticQuestion',
    'create_diagnostic_session',
    'run_diagnostic',
    
    # JEE MAINS Engine
    'JEE_MAINS_PATTERN',
    'MARKS_TO_PERCENTILE_2024',
    'HIGH_YIELD_TOPICS',
    'ScorePrediction',
    'TimeStrategy',
    'get_time_allocation',
    'get_topic_priority',
    'predict_score',
    'percentile_to_rank',
    
    # Academic Calendar (Phase 3)
    'StudentPhase',
    'PhaseConfig',
    'CalendarStudentProfile',
    'PhaseResult',
    'AcademicCalendarEngine',
    'PHASE_CONFIGS',
    'determine_student_phase',
    'get_phase_config',
    'calculate_days_to_jee',
    
    # Concept Reveal (Phase 3)
    'ConceptTier',
    'RevealStatus',
    'ConceptVisibility',
    'RevealSchedule',
    'ProgressMessage',
    'ConceptRevealEngine',
    'CONCEPT_TIERS',
    'create_reveal_engine',
    'get_visible_for_phase',
    'get_concept_tier',
    
    # Test Manager (Phase 3)
    'TestLevel',
    'TestStatus',
    'DifficultyLevel',
    'QuestionType',
    'TestLevelConfig',
    'Test',
    'TestResult',
    'TestManager',
    'TEST_LEVEL_CONFIGS',
    'create_test_manager',
    
    # Engagement Manager (Phase 3)
    'EngagementArc',
    'DropoutStatus',
    'StreakStatus',
    'CelebrationLevel',
    'StudentEngagement',
    'DropoutAlert',
    'Milestone',
    'EngagementManager',
    'ARC_CONFIGS',
    'STREAK_MILESTONES',
    'create_engagement_manager',
    
    # Root Cause Analyzer (Phase 3)
    'GapSeverity',
    'RootCauseType',
    'RemediationType',
    'RootCause',
    'FailureAnalysis',
    'RootCauseAnalyzer',
    'create_root_cause_analyzer',
    'analyze_concept_failure',
    
    # Psychology Engine (Phase 3)
    'BurnoutLevel',
    'DistressSignal',
    'InterventionType',
    'RecoveryAction',
    'StudySession',
    'BurnoutSignals',
    'StudentPsychState',
    'Intervention',
    'WellnessReport',
    'PsychologyEngine',
    'create_psychology_engine',
    'check_burnout_risk',
]
