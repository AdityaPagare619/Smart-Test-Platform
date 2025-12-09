"""
CR-V4 AI Engine Core
Central entry point for all AI functionality

Phase 2 Implementation - Council Approved Architecture
"""

from .engine_orchestrator import (
    CognitiveResonanceEngine,
    EngineResponse,
    SessionState,
    create_engine
)

from .algorithms import (
    # Bayesian
    QuestionAttempt,
    BayesUpdateResult,
    bayes_update_mastery,
    
    # IRT
    IRTParameters,
    irt_probability,
    fisher_information,
    estimate_ability,
    ability_to_mastery,
    
    # Knowledge State
    StudentKnowledgeState,
    KnowledgeStateTracker,
    create_student_state,
    process_interaction,
    
    # Question Selection
    Question,
    SelectionResult,
    QuestionSelector,
    
    # Misconception
    MisconceptionDetector,
    RecoveryEngine,
    analyze_and_intervene
)

__all__ = [
    # Main Engine
    'CognitiveResonanceEngine',
    'EngineResponse',
    'SessionState',
    'create_engine',
    
    # Algorithms
    'QuestionAttempt',
    'BayesUpdateResult',
    'bayes_update_mastery',
    'IRTParameters',
    'irt_probability',
    'fisher_information',
    'estimate_ability',
    'ability_to_mastery',
    'StudentKnowledgeState',
    'KnowledgeStateTracker',
    'create_student_state',
    'process_interaction',
    'Question',
    'SelectionResult',
    'QuestionSelector',
    'MisconceptionDetector',
    'RecoveryEngine',
    'analyze_and_intervene'
]
