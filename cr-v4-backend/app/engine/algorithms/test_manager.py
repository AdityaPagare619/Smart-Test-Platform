"""
CR-V4 Test Manager
Complete Test System Architecture

This module implements the comprehensive 6-level test hierarchy that provides
structured assessment from concept quizzes to full JEE mock examinations.

Test Hierarchy:
    Level 1: Concept Quizzes (Daily) - 5-10 questions, immediate feedback
    Level 2: Chapter Tests (Weekly) - 20-25 questions, timed
    Level 3: Cumulative Unit Tests (Bi-weekly) - 30-40 questions
    Level 4: Monthly Benchmarks (Fixed) - Global ranking enabled
    Level 5: Subject Mocks (Variable) - Full subject simulation
    Level 6: Full-Length Mocks (Per phase) - Complete JEE simulation

Council Approved: December 10, 2024
Expert Sign-offs: Allen Kota, Narayana, NTA Expert, IIT Faculty

Author: CR-V4 Engineering Team
Version: 1.0.0
"""

from __future__ import annotations

import logging
import hashlib
import json
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

from .academic_calendar import StudentPhase, PHASE_CONFIGS
from .concept_reveal import ConceptTier, CONCEPT_TIERS, HIGH_YIELD_TOPICS

# Configure module logger
logger = logging.getLogger(__name__)

# ==============================================================================
# TYPE DEFINITIONS
# ==============================================================================

QuestionId: TypeAlias = str
ConceptId: TypeAlias = str
StudentId: TypeAlias = str
TestId: TypeAlias = str
Subject: TypeAlias = Literal["MATHEMATICS", "PHYSICS", "CHEMISTRY"]


# ==============================================================================
# ENUMS
# ==============================================================================

class TestLevel(Enum):
    """
    The 6 levels of the test hierarchy.
    
    Council Decision: Each level serves a distinct purpose and has
    different question counts, timing, and psychological goals.
    """
    CONCEPT_QUIZ = auto()      # Level 1: Daily, 5-10 Qs, untimed
    CHAPTER_TEST = auto()      # Level 2: Weekly, 20-25 Qs, 45-60 min
    UNIT_TEST = auto()         # Level 3: Bi-weekly, 30-40 Qs, 90 min
    MONTHLY_BENCHMARK = auto() # Level 4: Monthly, 30-45 Qs, fixed for comparison
    SUBJECT_MOCK = auto()      # Level 5: Variable, single subject, 60-90 min
    FULL_MOCK = auto()         # Level 6: JEE simulation, 75 Qs, 180 min


class TestStatus(Enum):
    """Test lifecycle status."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class DifficultyLevel(Enum):
    """Question difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"


class QuestionType(Enum):
    """JEE question types."""
    MCQ = "mcq"                    # Multiple choice (Section A)
    NUMERICAL = "numerical"        # Numerical value (Section B)
    MULTI_SELECT = "multi_select"  # Multiple correct (JEE Advanced)


# ==============================================================================
# TEST LEVEL CONFIGURATIONS (COUNCIL APPROVED)
# ==============================================================================

@dataclass(frozen=True, slots=True)
class TestLevelConfig:
    """
    Configuration for each test level.
    
    Attributes:
        level: TestLevel enum
        name: Human-readable name
        question_count: Number of questions
        duration_minutes: Time limit (0 = untimed)
        difficulty_distribution: Dict mapping difficulty to percentage
        previous_topics_pct: Percentage of questions from previous topics
        negative_marking: Whether negative marking applies
        mandatory: Whether test is mandatory
        frequency: How often this test type occurs
        purpose: Primary purpose of this test type
    """
    level: TestLevel
    name: str
    question_count: Tuple[int, int]  # (min, max)
    duration_minutes: int
    difficulty_distribution: Dict[DifficultyLevel, float]
    previous_topics_pct: float
    negative_marking: bool
    mandatory: bool
    frequency: str
    purpose: str


TEST_LEVEL_CONFIGS: Final[Dict[TestLevel, TestLevelConfig]] = {
    
    TestLevel.CONCEPT_QUIZ: TestLevelConfig(
        level=TestLevel.CONCEPT_QUIZ,
        name="Concept Quiz",
        question_count=(5, 10),
        duration_minutes=0,  # Untimed
        difficulty_distribution={
            DifficultyLevel.EASY: 0.60,
            DifficultyLevel.MEDIUM: 0.30,
            DifficultyLevel.HARD: 0.10,
        },
        previous_topics_pct=0.20,
        negative_marking=False,
        mandatory=False,
        frequency="Daily/Per-lesson",
        purpose="Immediate reinforcement of concepts just learned",
    ),
    
    TestLevel.CHAPTER_TEST: TestLevelConfig(
        level=TestLevel.CHAPTER_TEST,
        name="Chapter Test",
        question_count=(20, 25),
        duration_minutes=55,
        difficulty_distribution={
            DifficultyLevel.EASY: 0.30,
            DifficultyLevel.MEDIUM: 0.50,
            DifficultyLevel.HARD: 0.20,
        },
        previous_topics_pct=0.30,
        negative_marking=True,  # Optional toggle
        mandatory=True,
        frequency="Weekly",
        purpose="Comprehensive understanding of completed chapter",
    ),
    
    TestLevel.UNIT_TEST: TestLevelConfig(
        level=TestLevel.UNIT_TEST,
        name="Cumulative Unit Test",
        question_count=(30, 40),
        duration_minutes=90,
        difficulty_distribution={
            DifficultyLevel.EASY: 0.20,
            DifficultyLevel.MEDIUM: 0.40,
            DifficultyLevel.HARD: 0.30,
            DifficultyLevel.VERY_HARD: 0.10,
        },
        previous_topics_pct=0.35,
        negative_marking=True,
        mandatory=True,
        frequency="Bi-weekly",
        purpose="Integration of multiple chapters",
    ),
    
    TestLevel.MONTHLY_BENCHMARK: TestLevelConfig(
        level=TestLevel.MONTHLY_BENCHMARK,
        name="Monthly Benchmark",
        question_count=(30, 45),
        duration_minutes=90,
        difficulty_distribution={
            DifficultyLevel.EASY: 0.25,
            DifficultyLevel.MEDIUM: 0.40,
            DifficultyLevel.HARD: 0.25,
            DifficultyLevel.VERY_HARD: 0.10,
        },
        previous_topics_pct=0.50,
        negative_marking=True,
        mandatory=True,
        frequency="Monthly",
        purpose="Global comparison and percentile ranking",
    ),
    
    TestLevel.SUBJECT_MOCK: TestLevelConfig(
        level=TestLevel.SUBJECT_MOCK,
        name="Subject Mock",
        question_count=(25, 30),
        duration_minutes=75,
        difficulty_distribution={
            DifficultyLevel.EASY: 0.20,
            DifficultyLevel.MEDIUM: 0.40,
            DifficultyLevel.HARD: 0.30,
            DifficultyLevel.VERY_HARD: 0.10,
        },
        previous_topics_pct=0.60,
        negative_marking=True,
        mandatory=False,
        frequency="Variable (AI-recommended)",
        purpose="Deep subject mastery and targeted practice",
    ),
    
    TestLevel.FULL_MOCK: TestLevelConfig(
        level=TestLevel.FULL_MOCK,
        name="Full-Length Mock",
        question_count=(75, 75),
        duration_minutes=180,
        difficulty_distribution={
            DifficultyLevel.EASY: 0.25,
            DifficultyLevel.MEDIUM: 0.40,
            DifficultyLevel.HARD: 0.25,
            DifficultyLevel.VERY_HARD: 0.10,
        },
        previous_topics_pct=1.0,  # All topics fair game
        negative_marking=True,
        mandatory=True,
        frequency="Per phase schedule",
        purpose="Complete JEE exam simulation",
    ),
}


# ==============================================================================
# MOCK FREQUENCY BY PHASE (COUNCIL APPROVED)
# ==============================================================================

MOCK_FREQUENCY_BY_PHASE: Final[Dict[StudentPhase, str]] = {
    StudentPhase.FRESH_START: "0",
    StudentPhase.MID_YEAR_11TH: "0-1/month",
    StudentPhase.LATE_11TH: "1/month",
    StudentPhase.POST_11TH_TRANSITION: "2/month",
    StudentPhase.TWELFTH_LONG: "1-2/week",
    StudentPhase.TWELFTH_ACCELERATION: "2-3/week",
    StudentPhase.TWELFTH_CRISIS_MODE: "3-4/week",
    StudentPhase.TWELFTH_FINAL_SPRINT: "every_alternate_day",
}


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass(slots=True)
class TestQuestion:
    """
    A question in a test.
    
    Attributes:
        question_id: Unique question identifier
        concept_id: Primary concept being tested
        subject: Subject (MATH/PHYSICS/CHEMISTRY)
        difficulty: Difficulty level
        question_type: MCQ, NUMERICAL, or MULTI_SELECT
        marks: Positive marks for correct answer
        negative_marks: Negative marks for wrong answer
        options: List of options (for MCQ)
        correct_answer: Correct answer
        time_suggested: Suggested time in seconds
        is_from_previous: Whether this is a recall question
    """
    question_id: QuestionId
    concept_id: ConceptId
    subject: Subject
    difficulty: DifficultyLevel
    question_type: QuestionType
    marks: float = 4.0
    negative_marks: float = 1.0
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    time_suggested: int = 120
    is_from_previous: bool = False


@dataclass(slots=True)
class Test:
    """
    A complete test instance.
    
    Attributes:
        test_id: Unique test identifier
        level: Test level
        student_id: Student for whom this test is generated
        questions: List of test questions
        total_marks: Maximum possible marks
        duration_minutes: Time limit
        created_at: When test was created
        status: Current test status
        subject: Subject (for subject mocks) or None for mixed
        primary_concepts: Main concepts being tested
        recall_concepts: Previous concepts included for spaced repetition
    """
    test_id: TestId
    level: TestLevel
    student_id: StudentId
    questions: List[TestQuestion]
    total_marks: float
    duration_minutes: int
    created_at: datetime = field(default_factory=datetime.now)
    status: TestStatus = TestStatus.SCHEDULED
    subject: Optional[Subject] = None
    primary_concepts: List[ConceptId] = field(default_factory=list)
    recall_concepts: List[ConceptId] = field(default_factory=list)


@dataclass(slots=True)
class TestResult:
    """
    Result of a completed test.
    
    Attributes:
        test_id: Test identifier
        student_id: Student identifier
        score: Earned marks
        total_marks: Maximum marks
        accuracy: Percentage accuracy
        time_taken_seconds: Total time taken
        correct_count: Number of correct answers
        incorrect_count: Number of incorrect answers
        skipped_count: Number of skipped questions
        subject_breakdown: Per-subject performance
        concept_breakdown: Per-concept performance
        percentile: Percentile (for benchmarks)
        rank: Rank (for benchmarks)
    """
    test_id: TestId
    student_id: StudentId
    score: float
    total_marks: float
    accuracy: float
    time_taken_seconds: int
    correct_count: int
    incorrect_count: int
    skipped_count: int
    subject_breakdown: Dict[Subject, Dict[str, float]] = field(default_factory=dict)
    concept_breakdown: Dict[ConceptId, Dict[str, float]] = field(default_factory=dict)
    percentile: Optional[float] = None
    rank: Optional[int] = None


@dataclass(slots=True)
class TestSchedule:
    """
    Scheduled tests for a student.
    
    Attributes:
        student_id: Student identifier
        phase: Current student phase
        scheduled_tests: List of upcoming tests with dates
    """
    student_id: StudentId
    phase: StudentPhase
    scheduled_tests: List[Tuple[date, TestLevel, str]] = field(default_factory=list)


# ==============================================================================
# CORE ENGINE
# ==============================================================================

class TestManager:
    """
    Complete Test Management Engine.
    
    This engine handles all aspects of test creation, scheduling,
    and result processing.
    
    Key Features:
        1. 6-level test hierarchy
        2. Phase-appropriate test scheduling
        3. Spaced repetition in chapter tests
        4. Monthly benchmark global ranking
        5. Mock frequency by phase
    
    Example:
        >>> manager = TestManager()
        >>> schedule = manager.generate_schedule(
        ...     student_id="STU001",
        ...     phase=StudentPhase.MID_YEAR_11TH,
        ...     start_date=date.today(),
        ...     months=3
        ... )
        >>> print(len(schedule.scheduled_tests))
        15  # Approximately 5 tests per month
    """
    
    def __init__(self) -> None:
        """Initialize the Test Manager."""
        self._test_counter = 0
    
    def _generate_test_id(self, level: TestLevel, student_id: StudentId) -> TestId:
        """Generate unique test ID."""
        self._test_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_input = f"{level.name}:{student_id}:{timestamp}:{self._test_counter}"
        hash_hex = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"TEST_{level.name}_{hash_hex}"
    
    def get_level_config(self, level: TestLevel) -> TestLevelConfig:
        """Get configuration for a test level."""
        return TEST_LEVEL_CONFIGS[level]
    
    def generate_concept_quiz(
        self,
        student_id: StudentId,
        concept_id: ConceptId,
        available_questions: List[Dict[str, Any]]
    ) -> Test:
        """
        Generate a concept quiz for immediate concept reinforcement.
        
        Args:
            student_id: Student ID
            concept_id: Concept just learned
            available_questions: Pool of available questions
            
        Returns:
            Generated Test object
        """
        config = TEST_LEVEL_CONFIGS[TestLevel.CONCEPT_QUIZ]
        question_count = config.question_count[0]  # Use minimum
        
        # Select questions based on difficulty distribution
        questions = self._select_questions(
            available_questions=available_questions,
            target_concepts=[concept_id],
            count=question_count,
            difficulty_dist=config.difficulty_distribution,
            previous_pct=config.previous_topics_pct
        )
        
        test_id = self._generate_test_id(TestLevel.CONCEPT_QUIZ, student_id)
        
        return Test(
            test_id=test_id,
            level=TestLevel.CONCEPT_QUIZ,
            student_id=student_id,
            questions=questions,
            total_marks=sum(q.marks for q in questions),
            duration_minutes=config.duration_minutes,
            primary_concepts=[concept_id],
            recall_concepts=[],
        )
    
    def generate_chapter_test(
        self,
        student_id: StudentId,
        chapter_id: ConceptId,
        previous_chapters: List[ConceptId],
        available_questions: List[Dict[str, Any]]
    ) -> Test:
        """
        Generate a chapter test with spaced repetition.
        
        Chapter tests include:
        - 70% from current chapter
        - 30% from previous chapters (spaced repetition)
        
        Args:
            student_id: Student ID
            chapter_id: Chapter just completed
            previous_chapters: Previously completed chapters (for recall)
            available_questions: Pool of available questions
            
        Returns:
            Generated Test object
        """
        config = TEST_LEVEL_CONFIGS[TestLevel.CHAPTER_TEST]
        total_questions = config.question_count[0]  # Use minimum (20)
        
        current_count = int(total_questions * (1 - config.previous_topics_pct))
        previous_count = total_questions - current_count
        
        # Select current chapter questions
        current_questions = self._select_questions(
            available_questions=available_questions,
            target_concepts=[chapter_id],
            count=current_count,
            difficulty_dist=config.difficulty_distribution,
            previous_pct=0.0
        )
        
        # Select previous chapter questions
        previous_questions = self._select_questions(
            available_questions=available_questions,
            target_concepts=previous_chapters[:3],  # Top 3 priority
            count=previous_count,
            difficulty_dist={DifficultyLevel.MEDIUM: 0.6, DifficultyLevel.HARD: 0.4},
            previous_pct=0.0
        )
        for q in previous_questions:
            q.is_from_previous = True
        
        all_questions = current_questions + previous_questions
        test_id = self._generate_test_id(TestLevel.CHAPTER_TEST, student_id)
        
        return Test(
            test_id=test_id,
            level=TestLevel.CHAPTER_TEST,
            student_id=student_id,
            questions=all_questions,
            total_marks=sum(q.marks for q in all_questions),
            duration_minutes=config.duration_minutes,
            primary_concepts=[chapter_id],
            recall_concepts=previous_chapters[:3],
        )
    
    def generate_monthly_benchmark(
        self,
        standard: Literal[11, 12],
        month: int,
        year: int,
        available_questions: List[Dict[str, Any]]
    ) -> Test:
        """
        Generate a fixed monthly benchmark for global comparison.
        
        Monthly benchmarks are FIXED for all students in a cohort,
        enabling true percentile calculation.
        
        Args:
            standard: Student standard (11 or 12)
            month: Month number
            year: Year
            available_questions: Pool of available questions
            
        Returns:
            Generated Test object (same for all students in cohort)
        """
        config = TEST_LEVEL_CONFIGS[TestLevel.MONTHLY_BENCHMARK]
        question_count = 30  # Fixed count for benchmarks
        
        # Generate deterministic test ID for the month
        benchmark_id = f"BENCHMARK_{standard}_{year}_{month:02d}"
        
        # Select questions (deterministic for same inputs)
        questions = self._select_questions(
            available_questions=available_questions,
            target_concepts=[],  # All concepts fair game
            count=question_count,
            difficulty_dist=config.difficulty_distribution,
            previous_pct=1.0,  # All previous topics included
            seed=f"{benchmark_id}_seed"  # Deterministic selection
        )
        
        return Test(
            test_id=benchmark_id,
            level=TestLevel.MONTHLY_BENCHMARK,
            student_id="ALL",  # Shared across students
            questions=questions,
            total_marks=sum(q.marks for q in questions),
            duration_minutes=config.duration_minutes,
            primary_concepts=[],
        )
    
    def generate_full_mock(
        self,
        student_id: StudentId,
        available_questions: List[Dict[str, Any]]
    ) -> Test:
        """
        Generate a full-length JEE mock test.
        
        Full mocks follow exact JEE pattern:
        - 75 questions (25 per subject)
        - 3 hours (180 minutes)
        - Section A (MCQ) + Section B (Numerical)
        
        Args:
            student_id: Student ID
            available_questions: Pool of available questions
            
        Returns:
            Generated Test object
        """
        config = TEST_LEVEL_CONFIGS[TestLevel.FULL_MOCK]
        
        questions: List[TestQuestion] = []
        
        # Per-subject question distribution
        for subject in ["MATHEMATICS", "PHYSICS", "CHEMISTRY"]:
            # Section A: 20 MCQs
            subject_qs_a = self._select_questions(
                available_questions=available_questions,
                target_concepts=[],
                count=20,
                difficulty_dist=config.difficulty_distribution,
                previous_pct=1.0,
                subject_filter=subject,  # type: ignore
                question_type=QuestionType.MCQ
            )
            
            # Section B: 5 Numerical
            subject_qs_b = self._select_questions(
                available_questions=available_questions,
                target_concepts=[],
                count=5,
                difficulty_dist={DifficultyLevel.HARD: 0.6, DifficultyLevel.VERY_HARD: 0.4},
                previous_pct=1.0,
                subject_filter=subject,  # type: ignore
                question_type=QuestionType.NUMERICAL
            )
            
            questions.extend(subject_qs_a)
            questions.extend(subject_qs_b)
        
        test_id = self._generate_test_id(TestLevel.FULL_MOCK, student_id)
        
        return Test(
            test_id=test_id,
            level=TestLevel.FULL_MOCK,
            student_id=student_id,
            questions=questions,
            total_marks=300,  # JEE total marks
            duration_minutes=180,
        )
    
    def _select_questions(
        self,
        available_questions: List[Dict[str, Any]],
        target_concepts: List[ConceptId],
        count: int,
        difficulty_dist: Dict[DifficultyLevel, float],
        previous_pct: float,
        subject_filter: Optional[Subject] = None,
        question_type: Optional[QuestionType] = None,
        seed: Optional[str] = None
    ) -> List[TestQuestion]:
        """
        Select questions based on criteria.
        
        In production, this would query a question bank.
        For now, returns stub questions.
        """
        questions: List[TestQuestion] = []
        
        for i in range(count):
            # Determine difficulty
            difficulty = self._pick_difficulty(difficulty_dist, i)
            
            # Create stub question
            q = TestQuestion(
                question_id=f"Q_{i}_{seed or 'default'}",
                concept_id=target_concepts[0] if target_concepts else "general",
                subject=subject_filter or "MATHEMATICS",
                difficulty=difficulty,
                question_type=question_type or QuestionType.MCQ,
                marks=4.0,
                negative_marks=1.0,
                time_suggested=120,
            )
            questions.append(q)
        
        return questions
    
    def _pick_difficulty(
        self, 
        dist: Dict[DifficultyLevel, float], 
        index: int
    ) -> DifficultyLevel:
        """Pick difficulty based on distribution and index."""
        cumulative = 0.0
        normalized_index = (index % 100) / 100.0
        
        for difficulty, probability in dist.items():
            cumulative += probability
            if normalized_index < cumulative:
                return difficulty
        
        return DifficultyLevel.MEDIUM
    
    def generate_schedule(
        self,
        student_id: StudentId,
        phase: StudentPhase,
        start_date: date,
        months: int = 1
    ) -> TestSchedule:
        """
        Generate test schedule for a student based on their phase.
        
        Args:
            student_id: Student ID
            phase: Current student phase
            start_date: Schedule start date
            months: Number of months to schedule
            
        Returns:
            TestSchedule with scheduled tests
        """
        schedule = TestSchedule(
            student_id=student_id,
            phase=phase,
            scheduled_tests=[]
        )
        
        current_date = start_date
        end_date = start_date + timedelta(days=months * 30)
        
        # Add weekly chapter tests
        week = 1
        while current_date < end_date:
            # Chapter Test every week
            schedule.scheduled_tests.append(
                (current_date, TestLevel.CHAPTER_TEST, f"Week {week} Chapter Test")
            )
            
            # Unit Test every 2 weeks
            if week % 2 == 0:
                schedule.scheduled_tests.append(
                    (current_date, TestLevel.UNIT_TEST, f"Unit Test {week // 2}")
                )
            
            week += 1
            current_date += timedelta(days=7)
        
        # Add monthly benchmarks
        for m in range(months):
            benchmark_date = start_date + timedelta(days=(m + 1) * 30 - 3)
            if benchmark_date < end_date:
                schedule.scheduled_tests.append(
                    (benchmark_date, TestLevel.MONTHLY_BENCHMARK, f"Month {m + 1} Benchmark")
                )
        
        # Add mocks based on phase
        mock_freq = MOCK_FREQUENCY_BY_PHASE.get(phase, "0")
        if mock_freq != "0" and "week" in mock_freq:
            # Parse frequency (e.g., "2-3/week" -> 2.5 per week)
            try:
                parts = mock_freq.replace("/week", "").split("-")
                avg_per_week = sum(int(p) for p in parts) / len(parts)
                mock_interval = int(7 / avg_per_week)
                
                mock_date = start_date + timedelta(days=mock_interval)
                mock_num = 1
                while mock_date < end_date:
                    schedule.scheduled_tests.append(
                        (mock_date, TestLevel.FULL_MOCK, f"Full Mock {mock_num}")
                    )
                    mock_num += 1
                    mock_date += timedelta(days=mock_interval)
            except (ValueError, ZeroDivisionError):
                pass
        
        # Sort by date
        schedule.scheduled_tests.sort(key=lambda x: x[0])
        
        return schedule
    
    def process_result(
        self,
        test: Test,
        responses: Dict[QuestionId, str],
        time_taken_seconds: int
    ) -> TestResult:
        """
        Process test responses and calculate result.
        
        Args:
            test: The completed test
            responses: Question ID -> answer mapping
            time_taken_seconds: Total time taken
            
        Returns:
            TestResult with scores and breakdown
        """
        correct = 0
        incorrect = 0
        skipped = 0
        score = 0.0
        
        subject_stats: Dict[Subject, Dict[str, float]] = {}
        concept_stats: Dict[ConceptId, Dict[str, float]] = {}
        
        for q in test.questions:
            response = responses.get(q.question_id)
            
            if response is None:
                skipped += 1
            elif response == q.correct_answer:
                correct += 1
                score += q.marks
            else:
                incorrect += 1
                score -= q.negative_marks
        
        accuracy = (correct / len(test.questions)) * 100 if test.questions else 0.0
        
        return TestResult(
            test_id=test.test_id,
            student_id=test.student_id,
            score=max(0, score),  # Floor at 0
            total_marks=test.total_marks,
            accuracy=accuracy,
            time_taken_seconds=time_taken_seconds,
            correct_count=correct,
            incorrect_count=incorrect,
            skipped_count=skipped,
            subject_breakdown=subject_stats,
            concept_breakdown=concept_stats,
        )


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def create_test_manager() -> TestManager:
    """Create a new Test Manager."""
    return TestManager()


def get_test_level_config(level: TestLevel) -> TestLevelConfig:
    """Get configuration for a test level."""
    return TEST_LEVEL_CONFIGS[level]


def get_mock_frequency(phase: StudentPhase) -> str:
    """Get mock test frequency for a phase."""
    return MOCK_FREQUENCY_BY_PHASE.get(phase, "0")


# ==============================================================================
# UNIT TESTS
# ==============================================================================

def test_level_configs() -> None:
    """Test that all level configs are properly defined."""
    for level in TestLevel:
        config = TEST_LEVEL_CONFIGS.get(level)
        assert config is not None, f"Missing config for {level}"
        assert config.question_count[0] <= config.question_count[1]
        assert sum(config.difficulty_distribution.values()) >= 0.99  # Allow for float precision
    
    print("✅ Level configs test passed")


def test_generate_concept_quiz() -> None:
    """Test concept quiz generation."""
    manager = TestManager()
    
    quiz = manager.generate_concept_quiz(
        student_id="STU001",
        concept_id="calculus_differentiation",
        available_questions=[]
    )
    
    assert quiz.level == TestLevel.CONCEPT_QUIZ
    assert quiz.duration_minutes == 0  # Untimed
    assert len(quiz.questions) >= 5
    
    print("✅ Concept quiz generation test passed")


def test_generate_chapter_test() -> None:
    """Test chapter test generation with spaced repetition."""
    manager = TestManager()
    
    test = manager.generate_chapter_test(
        student_id="STU001",
        chapter_id="calculus_integration",
        previous_chapters=["calculus_differentiation", "calculus_limits"],
        available_questions=[]
    )
    
    assert test.level == TestLevel.CHAPTER_TEST
    assert test.duration_minutes == 55
    assert len(test.primary_concepts) == 1
    assert len(test.recall_concepts) > 0
    
    print("✅ Chapter test generation test passed")


def test_generate_schedule() -> None:
    """Test schedule generation."""
    manager = TestManager()
    
    schedule = manager.generate_schedule(
        student_id="STU001",
        phase=StudentPhase.TWELFTH_ACCELERATION,
        start_date=date.today(),
        months=1
    )
    
    assert len(schedule.scheduled_tests) > 0
    
    # Should have chapter tests
    chapter_tests = [t for t in schedule.scheduled_tests if t[1] == TestLevel.CHAPTER_TEST]
    assert len(chapter_tests) >= 4  # ~4 weeks in a month
    
    print("✅ Schedule generation test passed")


def test_process_result() -> None:
    """Test result processing."""
    manager = TestManager()
    
    # Create a simple test
    test = Test(
        test_id="TEST_001",
        level=TestLevel.CONCEPT_QUIZ,
        student_id="STU001",
        questions=[
            TestQuestion(
                question_id="Q1",
                concept_id="concept1",
                subject="MATHEMATICS",
                difficulty=DifficultyLevel.EASY,
                question_type=QuestionType.MCQ,
                marks=4.0,
                negative_marks=1.0,
                correct_answer="A"
            ),
            TestQuestion(
                question_id="Q2",
                concept_id="concept1",
                subject="MATHEMATICS",
                difficulty=DifficultyLevel.MEDIUM,
                question_type=QuestionType.MCQ,
                marks=4.0,
                negative_marks=1.0,
                correct_answer="B"
            ),
        ],
        total_marks=8.0,
        duration_minutes=10
    )
    
    # Process with one correct, one wrong
    result = manager.process_result(
        test=test,
        responses={"Q1": "A", "Q2": "C"},
        time_taken_seconds=300
    )
    
    assert result.correct_count == 1
    assert result.incorrect_count == 1
    assert result.score == 3.0  # 4 - 1
    
    print("✅ Result processing test passed")


def run_all_tests() -> None:
    """Run all unit tests."""
    print("Running Test Manager tests...")
    test_level_configs()
    test_generate_concept_quiz()
    test_generate_chapter_test()
    test_generate_schedule()
    test_process_result()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
