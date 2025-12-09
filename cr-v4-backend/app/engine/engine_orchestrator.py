"""
CR-V4 AI ENGINE ORCHESTRATOR
Central coordination of all AI components

The Engine Orchestrator is the brain that connects:
1. Knowledge State Tracker (student ability)
2. Question Selector (optimal next question)
3. Misconception Detector (intervention decisions)
4. IRT Model (difficulty calibration)

Single entry point for the frontend API.
Handles the complete learning loop.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

# Import all algorithm components
from .algorithms import (
    # Knowledge State
    StudentKnowledgeState,
    ConceptState,
    InteractionRecord,
    KnowledgeStateTracker,
    create_student_state,
    process_interaction,
    
    # Question Selection
    Question,
    SelectionResult,
    ConceptNode,
    QuestionSelector,
    MathSelector,
    PhysicsSelector,
    ChemistrySelector,
    SyllabusStatus,
    CompetencyType,
    
    # Misconception
    MisconceptionDetector,
    RecoveryEngine,
    analyze_and_intervene,
    MisconceptionSeverity,
    
    # IRT
    IRTParameters,
    irt_probability,
    fisher_information,
    ability_to_mastery
)


# ============================================================================
# CONSTANTS
# ============================================================================

# Engine configuration
DEFAULT_BATCH_SIZE = 25
MAX_RECENT_QUESTIONS = 50
SESSION_TIMEOUT_MINUTES = 30

# Response targets (for balanced learning)
TARGET_SUCCESS_RATE = 0.75  # Aim for 75% correct (optimal learning zone)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class SessionState:
    """
    Current study session state for a student.
    
    Tracks within-session progress and recent questions.
    """
    student_id: str
    session_start: datetime = field(default_factory=datetime.now)
    
    questions_attempted: int = 0
    questions_correct: int = 0
    
    recent_question_ids: List[str] = field(default_factory=list)
    recent_concept_ids: List[str] = field(default_factory=list)
    
    # Active recovery plans
    active_misconception_recovery: Optional[str] = None
    
    # Subject focus (if student selected)
    current_subject: Optional[str] = None
    
    def get_session_accuracy(self) -> float:
        if self.questions_attempted == 0:
            return 0.5
        return self.questions_correct / self.questions_attempted
    
    def add_question(self, question_id: str, concept_id: str):
        """Track attempted question"""
        self.recent_question_ids.append(question_id)
        if len(self.recent_question_ids) > MAX_RECENT_QUESTIONS:
            self.recent_question_ids.pop(0)
        
        if concept_id not in self.recent_concept_ids:
            self.recent_concept_ids.append(concept_id)
            if len(self.recent_concept_ids) > 20:
                self.recent_concept_ids.pop(0)


@dataclass
class EngineResponse:
    """
    Response from the engine to frontend.
    
    Contains everything needed to display:
    - Next question
    - Student state summary
    - Any interventions
    """
    success: bool
    
    # Next question (if available)
    next_question: Optional[Dict] = None
    selection_reasons: List[str] = field(default_factory=list)
    
    # Student state summary
    student_summary: Optional[Dict] = None
    
    # Intervention (if misconception detected)
    intervention: Optional[Dict] = None
    
    # Feedback on previous question
    previous_feedback: Optional[Dict] = None
    
    # Performance metrics
    session_stats: Optional[Dict] = None
    
    # Error handling
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'success': self.success,
            'next_question': self.next_question,
            'selection_reasons': self.selection_reasons,
            'student_summary': self.student_summary,
            'intervention': self.intervention,
            'previous_feedback': self.previous_feedback,
            'session_stats': self.session_stats,
            'error': self.error
        }


# ============================================================================
# ENGINE ORCHESTRATOR
# ============================================================================

class CognitiveResonanceEngine:
    """
    Main AI Engine Orchestrator.
    
    Coordinates all components to provide:
    1. Optimal question selection
    2. Real-time knowledge state updates
    3. Misconception detection and intervention
    4. Personalized learning paths
    
    Usage:
        engine = CognitiveResonanceEngine()
        
        # Initialize student
        engine.initialize_student("STU_001")
        
        # Get next question
        response = engine.get_next_question("STU_001")
        
        # Process answer
        response = engine.process_answer("STU_001", "Q_001", True, 45.0)
    """
    
    def __init__(
        self,
        questions: Optional[List[Question]] = None,
        concepts: Optional[Dict[str, ConceptNode]] = None
    ):
        """
        Initialize the engine with question bank and concept graph.
        
        In production, these would be loaded from database.
        """
        self.questions = questions or []
        self.concepts = concepts or {}
        
        # Initialize components
        self.knowledge_tracker = KnowledgeStateTracker()
        
        # Subject-specific selectors
        self.selectors: Dict[str, QuestionSelector] = {}
        if self.questions:
            self.selectors['MATH'] = MathSelector(
                [q for q in self.questions if q.subject == 'MATH'],
                self.concepts
            )
            self.selectors['PHYSICS'] = PhysicsSelector(
                [q for q in self.questions if q.subject == 'PHYSICS'],
                self.concepts
            )
            self.selectors['CHEMISTRY'] = ChemistrySelector(
                [q for q in self.questions if q.subject == 'CHEMISTRY'],
                self.concepts
            )
            self.selectors['ALL'] = QuestionSelector(self.questions, self.concepts)
        
        self.misconception_detector = MisconceptionDetector()
        self.recovery_engine = RecoveryEngine(self.misconception_detector)
        
        # State storage (in production, this would be Redis/database)
        self.student_states: Dict[str, StudentKnowledgeState] = {}
        self.session_states: Dict[str, SessionState] = {}
    
    def initialize_student(
        self,
        student_id: str,
        initial_state: Optional[StudentKnowledgeState] = None
    ) -> StudentKnowledgeState:
        """
        Initialize or load a student's knowledge state.
        
        In production, would load from database.
        """
        if initial_state:
            self.student_states[student_id] = initial_state
        elif student_id not in self.student_states:
            self.student_states[student_id] = create_student_state(student_id)
        
        # Initialize session
        self.session_states[student_id] = SessionState(student_id=student_id)
        
        return self.student_states[student_id]
    
    def get_next_question(
        self,
        student_id: str,
        subject: Optional[str] = None,
        target_difficulty: Optional[str] = None
    ) -> EngineResponse:
        """
        Get the optimal next question for a student.
        
        This is the main API endpoint for the frontend.
        
        Args:
            student_id: Student identifier
            subject: Optional subject filter
            target_difficulty: Optional difficulty target
            
        Returns:
            EngineResponse with next question and context
        """
        # Get student state
        if student_id not in self.student_states:
            self.initialize_student(student_id)
        
        student_state = self.student_states[student_id]
        session_state = self.session_states[student_id]
        
        # Check for active misconception recovery
        priority_recovery = self.recovery_engine.get_priority_misconception(student_id)
        
        if priority_recovery and priority_recovery.misconception.severity == MisconceptionSeverity.HIGH:
            # Force recovery flow
            return self._get_recovery_question(student_id, priority_recovery)
        
        # Determine selector
        selector_key = subject if subject in self.selectors else 'ALL'
        selector = self.selectors.get(selector_key)
        
        if not selector:
            return EngineResponse(
                success=False,
                error="No questions available"
            )
        
        # Get excluded questions (recently attempted)
        excluded = set(session_state.recent_question_ids)
        
        # Select question
        result = selector.select_next_question(
            student_state,
            subject=subject,
            excluded_questions=excluded,
            target_difficulty=target_difficulty
        )
        
        if not result.question:
            return EngineResponse(
                success=False,
                error="No suitable question found"
            )
        
        # Prepare response
        return EngineResponse(
            success=True,
            next_question=result.question.to_dict(),
            selection_reasons=result.reasons,
            student_summary=self._get_student_summary(student_state),
            session_stats=self._get_session_stats(session_state)
        )
    
    def process_answer(
        self,
        student_id: str,
        question_id: str,
        correct: bool,
        time_taken: float,
        student_answer: Optional[str] = None
    ) -> EngineResponse:
        """
        Process a student's answer and update all states.
        
        This is called after each question attempt.
        
        Args:
            student_id: Student identifier
            question_id: Question that was answered
            correct: Whether answer was correct
            time_taken: Seconds spent on question
            student_answer: Actual answer text (for misconception analysis)
            
        Returns:
            EngineResponse with feedback and next question
        """
        # Get states
        student_state = self.student_states.get(student_id)
        session_state = self.session_states.get(student_id)
        
        if not student_state or not session_state:
            self.initialize_student(student_id)
            student_state = self.student_states[student_id]
            session_state = self.session_states[student_id]
        
        # Find question details
        question = next(
            (q for q in self.questions if q.question_id == question_id),
            None
        )
        
        if not question:
            # Unknown question - still process for state update
            question = Question(
                question_id=question_id,
                concept_id="UNKNOWN",
                subject="UNKNOWN"
            )
        
        # Step 1: Update knowledge state
        student_state = process_interaction(
            student_state,
            concept_id=question.concept_id,
            question_id=question_id,
            correct=correct,
            time_taken=time_taken,
            difficulty=question.irt_params.b / 3 + 0.5,  # Normalize to 0-1
            timestamp=datetime.now()
        )
        self.student_states[student_id] = student_state
        
        # Step 2: Update session state
        session_state.questions_attempted += 1
        if correct:
            session_state.questions_correct += 1
        session_state.add_question(question_id, question.concept_id)
        
        # Step 3: Analyze for misconceptions
        misconception_analysis = analyze_and_intervene(
            student_id=student_id,
            concept_id=question.concept_id,
            correct=correct,
            student_answer=student_answer,
            time_taken=time_taken,
            question_difficulty=question.irt_params.b / 3 + 0.5,
            detector=self.misconception_detector,
            recovery_engine=self.recovery_engine
        )
        
        # Step 4: Prepare feedback
        feedback = self._generate_feedback(
            correct=correct,
            question=question,
            time_taken=time_taken,
            student_state=student_state
        )
        
        # Step 5: Determine next steps
        response = EngineResponse(
            success=True,
            previous_feedback=feedback,
            student_summary=self._get_student_summary(student_state),
            session_stats=self._get_session_stats(session_state)
        )
        
        # Check if intervention needed
        if misconception_analysis.get('intervention', {}).get('required', False):
            response.intervention = misconception_analysis['intervention']
            
            if misconception_analysis['intervention'].get('severity') == 'HIGH':
                # Get recovery question instead of normal flow
                priority_recovery = self.recovery_engine.get_priority_misconception(student_id)
                if priority_recovery:
                    response.next_question = None  # Will be handled by recovery flow
                    response.intervention['next_action'] = 'RECOVERY_QUESTION'
            else:
                # Continue normal flow with intervention message
                next_q = self.get_next_question(student_id, session_state.current_subject)
                response.next_question = next_q.next_question
                response.selection_reasons = next_q.selection_reasons
        else:
            # Normal flow - get next question
            next_q = self.get_next_question(student_id, session_state.current_subject)
            response.next_question = next_q.next_question
            response.selection_reasons = next_q.selection_reasons
        
        return response
    
    def _get_recovery_question(
        self,
        student_id: str,
        recovery_plan
    ) -> EngineResponse:
        """Get a question from the recovery plan"""
        # In production, fetch actual diagnostic questions
        return EngineResponse(
            success=True,
            intervention={
                'type': 'RECOVERY',
                'misconception': recovery_plan.misconception.name,
                'message': f"Let's work on: {recovery_plan.misconception.name}",
                'recovery_strategy': recovery_plan.misconception.recovery_strategy
            },
            next_question={
                'type': 'DIAGNOSTIC',
                'concept_id': recovery_plan.misconception.concept_id,
                'message': 'Answer this diagnostic question to help identify the issue'
            }
        )
    
    def _generate_feedback(
        self,
        correct: bool,
        question: Question,
        time_taken: float,
        student_state: StudentKnowledgeState
    ) -> Dict:
        """Generate feedback for the answered question"""
        concept_mastery = student_state.get_concept_mastery(question.concept_id)
        
        if correct:
            if time_taken < 30:
                message = "Excellent! Quick and correct! 🎯"
            elif time_taken < 60:
                message = "Great job! You got it right! ✓"
            else:
                message = "Correct! Keep practicing to improve speed. ✓"
        else:
            if concept_mastery < 0.4:
                message = "Let's review this concept. You'll get it with practice! 📚"
            elif concept_mastery < 0.7:
                message = "Close! Review the concept and try similar problems. 🔄"
            else:
                message = "Oops! Careless mistake? Review and move on. ↩️"
        
        return {
            'correct': correct,
            'message': message,
            'time_taken': time_taken,
            'concept_mastery': f"{concept_mastery:.0%}",
            'concept_id': question.concept_id
        }
    
    def _get_student_summary(self, student_state: StudentKnowledgeState) -> Dict:
        """Get summary of student's current state"""
        return {
            'student_id': student_state.student_id,
            'ability': round(student_state.ability, 2),
            'ability_percent': f"{ability_to_mastery(student_state.ability):.0%}",
            'overall_mastery': f"{student_state.get_overall_mastery():.0%}",
            'accuracy': f"{student_state.get_accuracy():.0%}",
            'total_interactions': student_state.total_interactions,
            'concepts_attempted': len(student_state.concept_states),
            'study_streak': student_state.study_streak_days
        }
    
    def _get_session_stats(self, session_state: SessionState) -> Dict:
        """Get current session statistics"""
        return {
            'session_questions': session_state.questions_attempted,
            'session_correct': session_state.questions_correct,
            'session_accuracy': f"{session_state.get_session_accuracy():.0%}",
            'concepts_covered': len(session_state.recent_concept_ids)
        }
    
    def generate_test(
        self,
        student_id: str,
        num_questions: int = 25,
        subject: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate a personalized test for a student.
        
        Ensures:
        - Balanced difficulty distribution
        - Concept diversity
        - Competency coverage (NEP 2020)
        """
        student_state = self.student_states.get(student_id)
        if not student_state:
            self.initialize_student(student_id)
            student_state = self.student_states[student_id]
        
        selector_key = subject if subject in self.selectors else 'ALL'
        selector = self.selectors.get(selector_key)
        
        if not selector:
            return []
        
        batch = selector.select_batch(student_state, num_questions, subject)
        
        return [result.to_dict() for result in batch]
    
    def get_study_plan(self, student_id: str) -> Dict:
        """
        Generate a personalized study plan.
        
        Based on:
        - Current mastery levels
        - Upcoming review schedule
        - Weak areas needing focus
        - Time until exam
        """
        student_state = self.student_states.get(student_id)
        if not student_state:
            return {'error': 'Student not initialized'}
        
        # Get concepts due for review
        due_for_review = student_state.get_concepts_due_for_review(datetime.now())
        
        # Get weak concepts (mastery < 60%)
        weak_concepts = [
            (cid, cs.get_combined_mastery())
            for cid, cs in student_state.concept_states.items()
            if cs.get_combined_mastery() < 0.6
        ]
        weak_concepts.sort(key=lambda x: x[1])
        
        return {
            'student_id': student_id,
            'overall_mastery': f"{student_state.get_overall_mastery():.0%}",
            'priority_review': due_for_review[:5],
            'weak_areas': [
                {'concept': cid, 'mastery': f"{m:.0%}"}
                for cid, m in weak_concepts[:5]
            ],
            'recommendations': [
                "Focus on weak areas first",
                "Complete spaced reviews for better retention",
                f"{len(weak_concepts)} concepts need improvement"
            ]
        }


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_engine(
    questions: Optional[List[Question]] = None,
    concepts: Optional[Dict[str, ConceptNode]] = None
) -> CognitiveResonanceEngine:
    """
    Factory function to create the engine.
    
    In production, would load questions and concepts from database.
    """
    return CognitiveResonanceEngine(questions, concepts)


# ============================================================================
# TESTS
# ============================================================================

def test_engine_initialization():
    """Test engine initialization"""
    engine = create_engine()
    
    assert engine is not None, "Engine should be created"
    assert engine.knowledge_tracker is not None, "Should have knowledge tracker"
    
    print("✅ TEST PASSED: Engine initialization")


def test_student_initialization():
    """Test student state initialization"""
    engine = create_engine()
    
    state = engine.initialize_student("TEST_001")
    
    assert state is not None, "Should create state"
    assert state.student_id == "TEST_001", "Should have correct ID"
    
    print("✅ TEST PASSED: Student initialization")


def test_get_next_question():
    """Test question selection"""
    # Create test questions
    questions = [
        Question("Q1", "MATH_001", "MATH", IRTParameters(b=0.0)),
        Question("Q2", "MATH_002", "MATH", IRTParameters(b=0.5)),
    ]
    
    engine = create_engine(questions=questions)
    engine.initialize_student("TEST_002")
    
    response = engine.get_next_question("TEST_002")
    
    assert response.success, "Should succeed"
    assert response.next_question is not None, "Should have next question"
    
    print("✅ TEST PASSED: Get next question")


def test_process_answer():
    """Test answer processing"""
    questions = [
        Question("Q1", "MATH_001", "MATH", IRTParameters(b=0.0)),
        Question("Q2", "MATH_002", "MATH", IRTParameters(b=0.5)),
    ]
    
    engine = create_engine(questions=questions)
    engine.initialize_student("TEST_003")
    
    response = engine.process_answer(
        student_id="TEST_003",
        question_id="Q1",
        correct=True,
        time_taken=45.0
    )
    
    assert response.success, "Should succeed"
    assert response.previous_feedback is not None, "Should have feedback"
    assert response.previous_feedback['correct'] == True, "Should reflect correct answer"
    
    print("✅ TEST PASSED: Process answer")


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CR-V4 ENGINE ORCHESTRATOR TESTS")
    print("="*70 + "\n")
    
    test_engine_initialization()
    test_student_initialization()
    test_get_next_question()
    test_process_answer()
    
    print("\n" + "="*70)
    print("ALL ENGINE TESTS PASSED ✅")
    print("="*70 + "\n")
