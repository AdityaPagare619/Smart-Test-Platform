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
    
    # Student Profiles (NEW)
    'StudentProfile',
    'StudentTier',
    'LearningStyle',
    'StudentClassification',
    'StudentProfileClassifier',
    'get_selection_weights',
    'get_subject_adjustments',
    
    # Diagnostic Engine (NEW)
    'DiagnosticEngine',
    'DiagnosticResult',
    'DiagnosticStatus',
    'DiagnosticQuestion',
    'create_diagnostic_session',
    'run_diagnostic',
    
    # JEE MAINS Engine (NEW)
    'JEE_MAINS_PATTERN',
    'MARKS_TO_PERCENTILE_2024',
    'HIGH_YIELD_TOPICS',
    'ScorePrediction',
    'TimeStrategy',
    'get_time_allocation',
    'get_topic_priority',
    'predict_score',
    'percentile_to_rank'
]

