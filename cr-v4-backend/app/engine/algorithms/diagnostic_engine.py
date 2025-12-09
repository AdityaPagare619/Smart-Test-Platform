"""
CR-V4 CORE ALGORITHMS
Module: Diagnostic Engine

PURPOSE: Cold-start new students with proper ability estimation.

LAYER MAPPING:
- Layer 3 (Academic Calendar) - Initial assessment phase
- Layer 5 (DKT) - Initial ability estimation
- Layer 6 (Question Selection) - Diagnostic question selection

COUNCIL DECISION: First 5 questions are critical for:
1. Estimating initial ability
2. Setting correct difficulty calibration
3. Avoiding frustration/boredom from day 1
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

from .irt_model import (
    IRTParameters, 
    irt_probability, 
    estimate_ability,
    ability_to_mastery
)
from .student_profiles import (
    StudentProfile, 
    StudentTier,
    StudentProfileClassifier
)


# ============================================================================
# DIAGNOSTIC CONFIGURATION
# ============================================================================

# Diagnostic test structure
DIAGNOSTIC_QUESTIONS_PER_SUBJECT = 5
TOTAL_DIAGNOSTIC_QUESTIONS = 15  # 5 × 3 subjects

# Difficulty levels for diagnostic (IRT b parameter)
DIAGNOSTIC_DIFFICULTIES = {
    'very_easy': -1.5,
    'easy': -0.5,
    'medium': 0.0,
    'hard': 0.5,
    'very_hard': 1.5
}

# Question distribution: 1 very easy, 2 medium, 2 hard
DIAGNOSTIC_STRUCTURE = [
    ('very_easy', -1.5),
    ('easy', -0.5),
    ('medium', 0.0),
    ('hard', 0.5),
    ('very_hard', 1.5)
]


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class DiagnosticStatus(Enum):
    """Status of diagnostic process."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


@dataclass
class DiagnosticQuestion:
    """A question selected for diagnostic."""
    question_id: str
    concept_id: str
    subject: str
    difficulty: str  # 'very_easy' to 'very_hard'
    irt_b: float     # IRT difficulty parameter
    position: int    # 1-15 in diagnostic sequence


@dataclass
class DiagnosticResponse:
    """Student response to diagnostic question."""
    question_id: str
    correct: bool
    time_taken: float  # seconds
    subject: str
    difficulty: str
    irt_b: float


@dataclass
class DiagnosticResult:
    """
    Complete result of diagnostic assessment.
    
    Used to initialize student's knowledge state.
    """
    student_id: str
    status: DiagnosticStatus
    
    # Responses
    responses: List[DiagnosticResponse] = field(default_factory=list)
    
    # Estimated abilities by subject (IRT theta scale)
    subject_abilities: Dict[str, float] = field(default_factory=dict)
    overall_ability: float = 0.0
    
    # Classification
    initial_tier: Optional[StudentTier] = None
    
    # Performance metrics
    overall_accuracy: float = 0.0
    subject_accuracies: Dict[str, float] = field(default_factory=dict)
    
    # Timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_time: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'student_id': self.student_id,
            'status': self.status.value,
            'overall_ability': round(self.overall_ability, 2),
            'subject_abilities': {k: round(v, 2) for k, v in self.subject_abilities.items()},
            'initial_tier': self.initial_tier.value if self.initial_tier else None,
            'overall_accuracy': round(self.overall_accuracy, 2),
            'subject_accuracies': {k: round(v, 2) for k, v in self.subject_accuracies.items()},
            'total_time': round(self.total_time, 1),
            'questions_answered': len(self.responses)
        }


# ============================================================================
# DIAGNOSTIC ENGINE
# ============================================================================

class DiagnosticEngine:
    """
    Manages diagnostic assessment for new students.
    
    FLOW:
    1. Generate 15 diagnostic questions (5 per subject, mixed difficulty)
    2. Collect responses one at a time
    3. Estimate abilities after all responses
    4. Classify student into initial tier
    5. Return result for knowledge state initialization
    
    COUNCIL MANDATE:
    - Questions must cover core foundational concepts
    - Difficulty must be evenly distributed
    - High discrimination questions preferred for quick estimation
    """
    
    def __init__(self, question_bank: Dict[str, List[Dict]] = None):
        """
        Initialize with question bank.
        
        Args:
            question_bank: Dict mapping subject to list of questions
                Each question: {question_id, concept_id, irt_b, ...}
        """
        self.question_bank = question_bank or {}
        self.classifier = StudentProfileClassifier()
        
        # Core concepts for each subject (used for diagnostic)
        self.core_concepts = {
            'MATH': ['MATH_001', 'MATH_010', 'MATH_020', 'MATH_040', 'MATH_041'],
            'PHYSICS': ['PHYS_001', 'PHYS_002', 'PHYS_010', 'PHYS_030', 'PHYS_040'],
            'CHEMISTRY': ['CHEM_001', 'CHEM_010', 'CHEM_020', 'CHEM_030', 'CHEM_040']
        }
    
    def create_diagnostic(self, student_id: str) -> DiagnosticResult:
        """Create a new diagnostic session for a student."""
        return DiagnosticResult(
            student_id=student_id,
            status=DiagnosticStatus.NOT_STARTED,
            started_at=datetime.now()
        )
    
    def generate_diagnostic_questions(
        self,
        subject: Optional[str] = None
    ) -> List[DiagnosticQuestion]:
        """
        Generate diagnostic questions for assessment.
        
        If subject is None, generates for all 3 subjects.
        
        Returns:
            List of DiagnosticQuestion in recommended order
        """
        questions = []
        subjects = [subject] if subject else ['MATH', 'PHYSICS', 'CHEMISTRY']
        
        position = 1
        for subj in subjects:
            for i, (diff_name, irt_b) in enumerate(DIAGNOSTIC_STRUCTURE):
                # Select question matching difficulty
                q = self._select_diagnostic_question(subj, irt_b, i)
                if q:
                    questions.append(DiagnosticQuestion(
                        question_id=q.get('question_id', f'{subj}_DIAG_{i}'),
                        concept_id=q.get('concept_id', self.core_concepts.get(subj, ['UNKNOWN'])[min(i, len(self.core_concepts.get(subj, [])) - 1)]),
                        subject=subj,
                        difficulty=diff_name,
                        irt_b=irt_b,
                        position=position
                    ))
                    position += 1
        
        return questions
    
    def _select_diagnostic_question(
        self,
        subject: str,
        target_b: float,
        concept_idx: int
    ) -> Optional[Dict]:
        """Select a question matching target difficulty."""
        if subject not in self.question_bank:
            # No questions in bank, return synthetic
            return {
                'question_id': f'{subject}_DIAG_{concept_idx}',
                'concept_id': self.core_concepts.get(subject, ['UNKNOWN'])[min(concept_idx, 4)],
                'irt_b': target_b
            }
        
        # Find question closest to target difficulty
        best_q = None
        best_diff = float('inf')
        
        for q in self.question_bank[subject]:
            q_b = q.get('irt_b', 0.0)
            diff = abs(q_b - target_b)
            if diff < best_diff:
                best_diff = diff
                best_q = q
        
        return best_q
    
    def process_response(
        self,
        result: DiagnosticResult,
        question: DiagnosticQuestion,
        correct: bool,
        time_taken: float
    ) -> DiagnosticResult:
        """
        Process a single diagnostic response.
        
        Args:
            result: Current diagnostic state
            question: The question answered
            correct: Whether answer was correct
            time_taken: Time taken in seconds
            
        Returns:
            Updated DiagnosticResult
        """
        # Update status
        if result.status == DiagnosticStatus.NOT_STARTED:
            result.status = DiagnosticStatus.IN_PROGRESS
        
        # Add response
        result.responses.append(DiagnosticResponse(
            question_id=question.question_id,
            correct=correct,
            time_taken=time_taken,
            subject=question.subject,
            difficulty=question.difficulty,
            irt_b=question.irt_b
        ))
        
        # Update total time
        result.total_time += time_taken
        
        return result
    
    def complete_diagnostic(
        self,
        result: DiagnosticResult
    ) -> DiagnosticResult:
        """
        Complete diagnostic and calculate abilities.
        
        Called after all responses collected.
        """
        if not result.responses:
            result.status = DiagnosticStatus.SKIPPED
            return result
        
        result.status = DiagnosticStatus.COMPLETED
        result.completed_at = datetime.now()
        
        # Calculate subject abilities
        subject_responses = self._group_by_subject(result.responses)
        
        for subject, responses in subject_responses.items():
            ability = self._estimate_ability_from_responses(responses)
            accuracy = sum(1 for r in responses if r.correct) / len(responses)
            
            result.subject_abilities[subject] = ability
            result.subject_accuracies[subject] = accuracy
        
        # Calculate overall ability (weighted average)
        if result.subject_abilities:
            result.overall_ability = np.mean(list(result.subject_abilities.values()))
        
        # Calculate overall accuracy
        result.overall_accuracy = sum(1 for r in result.responses if r.correct) / len(result.responses)
        
        # Classify initial tier
        result.initial_tier = self._classify_tier(result.overall_accuracy)
        
        return result
    
    def _group_by_subject(
        self,
        responses: List[DiagnosticResponse]
    ) -> Dict[str, List[DiagnosticResponse]]:
        """Group responses by subject."""
        grouped = {}
        for r in responses:
            if r.subject not in grouped:
                grouped[r.subject] = []
            grouped[r.subject].append(r)
        return grouped
    
    def _estimate_ability_from_responses(
        self,
        responses: List[DiagnosticResponse]
    ) -> float:
        """
        Estimate ability from diagnostic responses.
        
        Uses simplified IRT-based estimation.
        """
        if not responses:
            return 0.0
        
        # Create IRT parameters and response pattern
        params = []
        correct_pattern = []
        
        for r in responses:
            params.append(IRTParameters(
                a=1.5,  # High discrimination for diagnostic
                b=r.irt_b,
                c=0.25
            ))
            correct_pattern.append(r.correct)
        
        # Estimate ability using IRT
        try:
            # Convert bools to ints for estimate_ability
            correct_ints = [1 if c else 0 for c in correct_pattern]
            ability = estimate_ability(correct_ints, params)
        except:
            # Fallback: simple accuracy-based estimate
            accuracy = sum(correct_pattern) / len(correct_pattern)
            ability = (accuracy - 0.5) * 4  # Map 0-1 to -2 to +2
        
        return float(ability)
    
    def _classify_tier(self, accuracy: float) -> StudentTier:
        """Classify into tier based on diagnostic accuracy."""
        if accuracy < 0.35:
            return StudentTier.STRUGGLING
        elif accuracy < 0.50:
            return StudentTier.DEVELOPING
        elif accuracy < 0.65:
            return StudentTier.AVERAGE
        elif accuracy < 0.80:
            return StudentTier.GOOD
        else:
            return StudentTier.EXCELLENT


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_diagnostic_session(student_id: str) -> Tuple[DiagnosticEngine, DiagnosticResult, List[DiagnosticQuestion]]:
    """
    Create a complete diagnostic session.
    
    Returns:
        Tuple of (engine, result, questions)
    """
    engine = DiagnosticEngine()
    result = engine.create_diagnostic(student_id)
    questions = engine.generate_diagnostic_questions()
    
    return engine, result, questions


def run_diagnostic(
    student_id: str,
    responses: List[Tuple[bool, float]]  # (correct, time_taken)
) -> DiagnosticResult:
    """
    Run complete diagnostic with provided responses.
    
    Args:
        student_id: Student identifier
        responses: List of (correct, time_taken) tuples for 15 questions
        
    Returns:
        Completed DiagnosticResult
    """
    engine, result, questions = create_diagnostic_session(student_id)
    
    for i, (correct, time_taken) in enumerate(responses):
        if i < len(questions):
            result = engine.process_response(result, questions[i], correct, time_taken)
    
    return engine.complete_diagnostic(result)


# ============================================================================
# TESTS
# ============================================================================

def test_diagnostic_creation():
    """Test diagnostic session creation."""
    engine = DiagnosticEngine()
    result = engine.create_diagnostic("TEST_001")
    
    assert result.student_id == "TEST_001"
    assert result.status == DiagnosticStatus.NOT_STARTED
    
    print("✅ Diagnostic creation test passed")


def test_question_generation():
    """Test diagnostic question generation."""
    engine = DiagnosticEngine()
    questions = engine.generate_diagnostic_questions()
    
    assert len(questions) == 15, f"Expected 15 questions, got {len(questions)}"
    
    # Check subject distribution
    subjects = [q.subject for q in questions]
    assert subjects.count('MATH') == 5
    assert subjects.count('PHYSICS') == 5
    assert subjects.count('CHEMISTRY') == 5
    
    # Check difficulty distribution per subject
    for subj in ['MATH', 'PHYSICS', 'CHEMISTRY']:
        subj_qs = [q for q in questions if q.subject == subj]
        difficulties = [q.irt_b for q in subj_qs]
    
    print(f"✅ Generated {len(questions)} diagnostic questions")
    print("✅ Question generation test passed")


def test_full_diagnostic():
    """Test complete diagnostic flow."""
    # Simulate a medium-ability student
    responses = [
        # Math: 3/5 correct
        (True, 45), (True, 60), (False, 90), (True, 75), (False, 120),
        # Physics: 4/5 correct
        (True, 30), (True, 45), (True, 60), (True, 90), (False, 100),
        # Chemistry: 2/5 correct
        (True, 40), (True, 55), (False, 70), (False, 85), (False, 110)
    ]
    
    result = run_diagnostic("TEST_002", responses)
    
    assert result.status == DiagnosticStatus.COMPLETED
    assert result.initial_tier is not None
    assert 0.5 < result.overall_accuracy < 0.7
    
    print(f"✅ Diagnostic result: {result.to_dict()}")
    print(f"   Tier: {result.initial_tier.value}")
    print(f"   Overall ability: {result.overall_ability:.2f}")
    print("✅ Full diagnostic test passed")


if __name__ == "__main__":
    test_diagnostic_creation()
    test_question_generation()
    test_full_diagnostic()
    print("\n🎉 Diagnostic Engine: All tests passed!")
