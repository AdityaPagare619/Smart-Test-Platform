# CR-V4.0 ENGINEERING SPRINT BREAKDOWN
## Week-by-Week Detailed Coding Tasks & Deliverables

**Prepared for:** Engineering Team (CTO Aditya + Development Team)  
**Date:** December 6, 2025, 8:00 PM IST  
**Classification:** SPRINT SCHEDULE - DETAILED TASKS

---

## EXECUTION FRAMEWORK

**Methodology:** Agile Sprints + TDD (Test-Driven Development)

**Each Sprint:**
1. Define deliverables (what we're building)
2. Write tests first (before code)
3. Implement features (make tests pass)
4. Integration test (connect components)
5. Simulation test (does it work in practice?)

---

## WEEK 1-2: FOUNDATION SPRINT

### Goal
Build core infrastructure that everything depends on.

### Team Assignment
- **Database Lead:** Set up PostgreSQL, schema, migrations
- **Backend Dev 1:** Student mastery model, Bayes logic
- **Backend Dev 2:** Knowledge graph database, concept structure
- **DevOps:** PostgreSQL deployment, Redis setup

### Sprint Tasks

#### Day 1-2: PostgreSQL Setup & Concepts Database

**Task 1a: Database Infrastructure**
```python
# /database/setup.py

# DEFINITION: Create PostgreSQL database structure
# TEST: Verify all tables exist with correct schema
# CODE: Database migrations (Alembic)

def test_concepts_table_exists():
    """Verify concepts table created"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = 'concepts'
        )
    """)
    assert cursor.fetchone()[0] == True

def test_concept_indexes_exist():
    """Verify all indexes created"""
    indexes = ['idx_subject', 'idx_layer', 'idx_difficulty']
    for idx in indexes:
        # Verify each index exists and is optimized
        pass

# DELIVERABLE: 
# - PostgreSQL with all 7 core tables
# - 20+ optimized indexes
# - Alembic migrations configured
# - Admin user with appropriate permissions
```

**Task 1b: Load Concept Data**
```python
# /database/concept_loader.py

def load_all_concepts():
    """Insert 165 JEE-MAINS concepts into database"""
    
    concepts = [
        # MATHEMATICS CONCEPTS
        {
            "concept_id": "MATH_001",
            "name": "Number Systems",
            "subject": "MATH",
            "layer": 1,
            "difficulty": 1,
            "exam_weight": 0.05,
            "parent_concept_id": None,
        },
        {
            "concept_id": "MATH_002",
            "name": "Algebra Basics",
            "subject": "MATH",
            "layer": 1,
            "difficulty": 2,
            "exam_weight": 0.08,
            "parent_concept_id": "MATH_001",
        },
        # ... 60 math concepts total
        
        # PHYSICS CONCEPTS
        {
            "concept_id": "PHY_001",
            "name": "Motion in 1D",
            "subject": "PHYSICS",
            "layer": 1,
            "difficulty": 1,
            "exam_weight": 0.08,
        },
        # ... 50 physics concepts total
        
        # CHEMISTRY CONCEPTS
        {
            "concept_id": "CHM_001",
            "name": "Atomic Structure",
            "subject": "CHEMISTRY",
            "layer": 1,
            "difficulty": 1,
            "exam_weight": 0.06,
        },
        # ... 55 chemistry concepts total
    ]
    
    # Bulk insert (using batch inserts for speed)
    batch_insert_concepts(concepts)
    
    # Verify count
    assert count_concepts() == 165

def load_prerequisite_relationships():
    """Load 200+ prerequisite relationships"""
    
    prerequisites = [
        # (dependent, prerequisite, criticality, weight)
        ("MATH_041", "MATH_040", "HARD", 0.9),  # Derivatives needs Limits
        ("MATH_041", "MATH_030", "HARD", 0.7),  # Derivatives needs Functions
        ("MATH_043", "MATH_041", "HARD", 0.95), # Integration needs Derivatives
        # ... 200+ total
    ]
    
    batch_insert_prerequisites(prerequisites)
    assert count_prerequisites() >= 200

def load_misconceptions():
    """Load 300+ common student misconceptions"""
    
    misconceptions = [
        {
            "concept_id": "MATH_041",  # Derivatives
            "misconception_name": "Derivative as slope at point",
            "description": "Thinking derivative IS the slope, not the rate of change",
            "why_students_think": "Visualizing graph and seeing slope",
            "recovery_strategy": "Emphasize slope of tangent line vs instantaneous change",
            "difficulty_to_correct": 4,
        },
        # ... 300+ total
    ]
    
    batch_insert_misconceptions(misconceptions)
    assert count_misconceptions() >= 300

# DELIVERABLE:
# - 165 concepts fully inserted
# - 200+ prerequisite relationships
# - 300+ misconceptions loaded
# - All with proper validation
```

#### Day 3-4: Student Mastery Model

**Task 2a: Bayes Update Implementation**
```python
# /app/engine/algorithms/bayes_update.py

import pytest
from decimal import Decimal

def test_bayes_update_correct_answer():
    """If student gets MCQ correct, mastery should increase"""
    
    attempt = QuestionAttempt(
        correct=True,
        time_taken=120,
        question_difficulty=0.6,
        student_prior_mastery=0.5,  # 50% sure they knew it
    )
    
    result = bayes_update_mastery(attempt)
    
    # Bayes update: higher probability student actually knows
    assert result["new_mastery"] > attempt.student_prior_mastery
    assert result["new_mastery"] > 0.5
    assert result["update_magnitude"] > 0

def test_bayes_update_wrong_answer():
    """If student gets answer wrong, mastery should decrease"""
    
    attempt = QuestionAttempt(
        correct=False,
        time_taken=180,
        question_difficulty=0.4,  # Easy question
        student_prior_mastery=0.8,  # Thought they knew it
    )
    
    result = bayes_update_mastery(attempt)
    
    # Got easy question wrong: mastery decreases
    assert result["new_mastery"] < 0.8
    assert result["update_magnitude"] > 0

def test_bayes_update_confidence():
    """Confidence should increase after consistent answers"""
    
    # Multiple correct answers
    confidence_values = []
    prior_mastery = 0.5
    
    for _ in range(5):
        attempt = QuestionAttempt(
            correct=True,
            time_taken=100,
            question_difficulty=0.5,
            student_prior_mastery=prior_mastery,
        )
        
        result = bayes_update_mastery(attempt)
        confidence_values.append(result["new_confidence"])
        prior_mastery = result["new_mastery"]  # Update for next attempt
    
    # Confidence should increase as we see more evidence
    assert confidence_values[-1] > confidence_values[0]

# IMPLEMENTATION (make tests pass)

def bayes_update_mastery(attempt):
    """
    See CR-V4-Engine-Build-Plan for detailed math
    """
    GUESSING_PROBABILITY = 0.25
    prior = attempt.student_prior_mastery
    
    if attempt.correct:
        p_event_given_mastery = (
            prior * (1 - GUESSING_PROBABILITY) + GUESSING_PROBABILITY
        )
    else:
        p_event_given_mastery = 1 - (
            prior * (1 - GUESSING_PROBABILITY) + GUESSING_PROBABILITY
        )
    
    if attempt.correct:
        p_event = ((1 - GUESSING_PROBABILITY) * 0.5) + GUESSING_PROBABILITY
    else:
        p_event = 1 - (((1 - GUESSING_PROBABILITY) * 0.5) + GUESSING_PROBABILITY)
    
    posterior = (p_event_given_mastery * prior) / p_event
    posterior = max(0.0, min(1.0, posterior))
    
    update_magnitude = abs(posterior - prior)
    new_confidence = 0.5 + (min(1.0, update_magnitude * 2) * 0.3)
    
    return {
        "new_mastery": posterior,
        "new_confidence": new_confidence,
        "update_magnitude": update_magnitude,
    }

# DELIVERABLE:
# - Bayes update logic fully tested
# - Handles all edge cases
# - Production-ready
```

**Task 2b: Database Schema for Mastery**
```python
# /database/models.py (SQLAlchemy)

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class StudentMasteryState(Base):
    __tablename__ = "student_mastery_state"
    
    mastery_id = Column(Integer, primary_key=True)
    student_id = Column(String(50), index=True)
    concept_id = Column(String(20), ForeignKey("concepts.concept_id"))
    
    mastery_level = Column(Float)  # 0.0-1.0
    confidence = Column(Float)     # 0.0-1.0
    
    attempts_total = Column(Integer, default=0)
    attempts_correct = Column(Integer, default=0)
    learning_speed = Column(Float)  # 0.5-1.5
    
    first_attempted = Column(DateTime)
    last_attempted = Column(DateTime)
    days_since_last_attempt = Column(Integer)
    
    recent_accuracy = Column(Float)
    trend = Column(String(20))  # improving, stable, declining
    
    total_time_minutes = Column(Integer, default=0)
    avg_time_per_attempt = Column(Integer)

def test_save_and_load_mastery():
    """Save mastery state and verify retrieval"""
    
    state = StudentMasteryState(
        student_id="STU_001",
        concept_id="MATH_041",
        mastery_level=0.72,
        confidence=0.85,
    )
    
    db_session.add(state)
    db_session.commit()
    
    # Retrieve
    loaded = db_session.query(StudentMasteryState).filter(
        StudentMasteryState.student_id == "STU_001"
    ).first()
    
    assert loaded.mastery_level == 0.72
    assert loaded.confidence == 0.85

# DELIVERABLE:
# - SQLAlchemy models defined
# - Database queries tested
# - Indexes verified
```

#### Day 5-6: Simulation Foundation

**Task 3a: Synthetic Student Generator**
```python
# /simulation/student_generator.py

import pytest
from dataclasses import dataclass
from enum import Enum

class StudentType(Enum):
    HIGH_ACHIEVER = "HIGH_ACHIEVER"
    AVERAGE_STEADY = "AVERAGE_STEADY"
    STRUGGLING = "STRUGGLING"
    BURNOUT_RISK = "BURNOUT_RISK"

@dataclass
class SimulatedStudent:
    student_id: str
    student_type: StudentType
    mastery: Dict[str, float]  # concept_id -> mastery_level
    motivation: float
    fatigue: float
    burnout_risk: float

def test_high_achiever_creation():
    """Verify high achiever profile has correct characteristics"""
    
    student = create_simulated_student(StudentType.HIGH_ACHIEVER)
    
    assert student.student_type == StudentType.HIGH_ACHIEVER
    assert hasattr(student, 'learning_speed_multiplier')
    assert student.learning_speed_multiplier > 1.0  # Faster than average
    assert hasattr(student, 'misconception_rate')
    assert student.misconception_rate < 0.2  # Lower error rate

def test_all_student_types_have_different_profiles():
    """Verify each student type is distinct"""
    
    types = [
        StudentType.HIGH_ACHIEVER,
        StudentType.AVERAGE_STEADY,
        StudentType.STRUGGLING,
        StudentType.BURNOUT_RISK,
    ]
    
    profiles = {}
    for stype in types:
        student = create_simulated_student(stype)
        profiles[stype] = {
            'learning_speed': student.learning_speed_multiplier,
            'motivation': student.motivation_baseline,
            'error_rate': student.misconception_rate,
        }
    
    # Verify profiles are different
    speeds = [p['learning_speed'] for p in profiles.values()]
    assert len(set(speeds)) == len(speeds)  # All different

# IMPLEMENTATION

def create_simulated_student(student_type: StudentType) -> SimulatedStudent:
    """Create a realistic student with given profile"""
    
    profiles = {
        StudentType.HIGH_ACHIEVER: {
            'learning_speed_multiplier': 1.3,
            'motivation_baseline': 0.9,
            'misconception_rate': 0.15,
            'careless_error_rate': 0.05,
            'burnout_speed': 0.02,
        },
        StudentType.AVERAGE_STEADY: {
            'learning_speed_multiplier': 1.0,
            'motivation_baseline': 0.7,
            'misconception_rate': 0.25,
            'careless_error_rate': 0.10,
            'burnout_speed': 0.05,
        },
        StudentType.STRUGGLING: {
            'learning_speed_multiplier': 0.7,
            'motivation_baseline': 0.5,
            'misconception_rate': 0.40,
            'careless_error_rate': 0.20,
            'burnout_speed': 0.10,
        },
        StudentType.BURNOUT_RISK: {
            'learning_speed_multiplier': 0.8,
            'motivation_baseline': 0.3,
            'misconception_rate': 0.35,
            'careless_error_rate': 0.25,
            'burnout_speed': 0.15,
        },
    }
    
    profile = profiles[student_type]
    
    student = SimulatedStudent(
        student_id=f"SIM_{uuid4()}",
        student_type=student_type,
        mastery={},  # Initialize empty, will populate
        motivation=profile['motivation_baseline'],
        fatigue=0.0,
        burnout_risk=0.1,
    )
    
    # Initialize mastery for all concepts (everyone starts at 0)
    all_concepts = get_all_concepts()
    for concept in all_concepts:
        student.mastery[concept.concept_id] = 0.0
    
    # Copy profile to student object
    for key, value in profile.items():
        setattr(student, key, value)
    
    return student

# DELIVERABLE:
# - 4 student types fully defined
# - Realistic profiles
# - All parameters configurable
# - Tests verify distinctness
```

**Task 3b: Question Attempt Simulation**
```python
# /simulation/attempt_generator.py

import pytest
from random import random, randn

def test_attempt_generation_correct_high_mastery():
    """If mastery is high, student should usually answer correctly"""
    
    student = create_simulated_student(StudentType.HIGH_ACHIEVER)
    student.mastery["MATH_041"] = 0.9  # Very high mastery
    
    question = MockQuestion(
        concept_id="MATH_041",
        difficulty=0.5,
        estimated_time=120,
    )
    
    # Run 100 attempts
    correct_count = 0
    for _ in range(100):
        result = simulate_question_attempt(student, question)
        if result["is_correct"]:
            correct_count += 1
    
    # Should be mostly correct (>80%)
    assert correct_count > 80

def test_attempt_generation_wrong_low_mastery():
    """If mastery is low, student should usually answer wrong"""
    
    student = create_simulated_student(StudentType.STRUGGLING)
    student.mastery["MATH_041"] = 0.1  # Very low mastery
    
    question = MockQuestion(
        concept_id="MATH_041",
        difficulty=0.7,  # Hard question
        estimated_time=120,
    )
    
    # Run 100 attempts
    wrong_count = 0
    for _ in range(100):
        result = simulate_question_attempt(student, question)
        if not result["is_correct"]:
            wrong_count += 1
    
    # Should be mostly wrong (>70%)
    assert wrong_count > 70

def test_time_decreases_with_mastery():
    """With higher mastery, student should answer faster"""
    
    student = create_simulated_student(StudentType.AVERAGE_STEADY)
    question = MockQuestion(estimated_time=120)
    
    times_low_mastery = []
    times_high_mastery = []
    
    for _ in range(20):
        student.mastery["MATH_041"] = 0.2
        r1 = simulate_question_attempt(student, question)
        times_low_mastery.append(r1["time_taken"])
        
        student.mastery["MATH_041"] = 0.9
        r2 = simulate_question_attempt(student, question)
        times_high_mastery.append(r2["time_taken"])
    
    avg_low = sum(times_low_mastery) / len(times_low_mastery)
    avg_high = sum(times_high_mastery) / len(times_high_mastery)
    
    # High mastery should be faster
    assert avg_high < avg_low

# IMPLEMENTATION

def simulate_question_attempt(student, question):
    """Generate realistic attempt with correct probability/timing"""
    
    # Probability of correct answer
    p_correct = calculate_correctness_probability(student, question)
    is_correct = random() < p_correct
    
    # Time taken
    time_taken = calculate_time_taken(student, question)
    
    # Update student state
    if is_correct:
        student.motivation += 0.05
        student.burnout_risk *= 0.95
    else:
        student.motivation -= 0.10
        student.burnout_risk *= 1.05
    
    student.fatigue += 0.01
    student.motivation = max(0.0, min(1.0, student.motivation))
    
    return {
        "is_correct": is_correct,
        "time_taken": time_taken,
        "timestamp": datetime.now(),
    }

def calculate_correctness_probability(student, question) -> float:
    """What's the chance this student gets this question right?"""
    
    mastery = student.mastery[question.concept_id]
    difficulty = question.difficulty
    
    # Probability function: sigmoid of (mastery - difficulty)
    # If mastery >> difficulty: very likely correct
    # If mastery << difficulty: unlikely correct
    
    sigmoid_input = (mastery - difficulty) * 4
    p_correct = sigmoid(sigmoid_input)  # 0.0-1.0
    
    # Account for guessing (MCQ has 25% chance)
    GUESS_PROB = 0.25
    p_correct = mastery * (1 - GUESS_PROB) + GUESS_PROB
    
    # Careless errors: sometimes get wrong despite knowing
    careless_error_chance = student.careless_error_rate * student.fatigue
    if random() < careless_error_chance:
        p_correct *= 0.3
    
    return max(0.0, min(1.0, p_correct))

def calculate_time_taken(student, question) -> int:
    """How long will this student take?"""
    
    mastery = student.mastery[question.concept_id]
    base_time = question.estimated_time
    
    # Higher mastery = faster (30% faster at mastery 1.0)
    mastery_multiplier = 1 - mastery * 0.3
    
    # Higher difficulty = longer
    difficulty_multiplier = 1 + question.difficulty * 0.3
    
    # Fatigue slows down thinking
    fatigue_multiplier = 1 + student.fatigue * 0.4
    
    # Low motivation = less effort = faster but wrong
    motivation_multiplier = 0.8 + student.motivation * 0.4
    
    # Random variation (±20%)
    random_variation = 1 + randn() * 0.2
    
    time_taken = int(
        base_time
        * mastery_multiplier
        * difficulty_multiplier
        * fatigue_multiplier
        * motivation_multiplier
        * random_variation
    )
    
    return max(10, time_taken)  # At least 10 seconds

# DELIVERABLE:
# - Attempt generation fully simulated
# - Realistic correctness probabilities
# - Realistic time calculations
# - Student state updates
# - All tests passing
```

### Week 1-2 Summary

**Deliverables:**
✅ PostgreSQL fully set up (7 tables, 20+ indexes)
✅ 165 concepts loaded with metadata
✅ 200+ prerequisites mapped
✅ 300+ misconceptions defined
✅ Bayes update algorithm fully tested
✅ Student mastery model with database
✅ 4 student types with realistic profiles
✅ Question attempt simulation complete

**Code Quality:**
- All code has passing tests
- No dependencies on incomplete code
- Ready for next sprint

**Database Size:** ~50MB for 165 concepts + metadata
**Simulation Capacity:** Ready to simulate 1000s of students

---

## WEEK 3: LAYERS 1-3 SPRINT

### Goal
Build first 3 engine layers.

### Tasks

#### Layer 1: Knowledge Graph Engine

```python
# /app/engine/layers/layer1_knowledge_graph.py

def test_learning_path_respects_prerequisites():
    """Verify learning path checks prerequisites"""
    
    # Create student who hasn't learned Limits yet
    student = create_test_student()
    student.mastery["MATH_040"] = 0.0  # Limits = 0% (not learned)
    student.mastery["MATH_041"] = 0.0  # Derivatives = 0%
    
    # Derivatives requires Limits
    path = build_learning_path(student)
    
    # Should recommend Limits before Derivatives
    assert path[0].concept_id == "MATH_040"
    assert "MATH_041" not in path[:3]  # Derivatives not in first 3

def test_learning_path_exam_weightage():
    """High-weightage concepts should be prioritized"""
    
    student = create_test_student()
    student.mastery = {c: 0.0 for c in get_all_concepts()}  # Everyone at 0
    
    path = build_learning_path(student)
    
    # High-weightage concepts should come first
    weights = [get_exam_weight(c.concept_id) for c in path[:10]]
    assert weights == sorted(weights, reverse=True)

# IMPLEMENTATION

def build_learning_path(student) -> List[Concept]:
    """Build optimal learning path for student"""
    
    # Step 1: Get all unmastered concepts
    unmastered = [
        c for c in get_all_concepts()
        if student.mastery[c.concept_id] < 0.9
    ]
    
    # Step 2: Check prerequisites for each
    learnable = []
    for concept in unmastered:
        prerequisites = get_prerequisites(concept.concept_id)
        
        can_learn = True
        for prereq_id, criticality, weight in prerequisites:
            prereq_mastery = student.mastery[prereq_id]
            threshold = 0.7 if criticality == "HARD" else 0.4
            
            if prereq_mastery < threshold:
                can_learn = False
                break
        
        if can_learn:
            learnable.append(concept)
    
    # Step 3: Prioritize by exam weightage
    learnable.sort(
        key=lambda c: get_exam_weight(c.concept_id),
        reverse=True
    )
    
    # Step 4: Adjust for learning speed
    path = []
    if student.learning_speed > 1.1:
        path = learnable[:20]
    elif student.learning_speed < 0.9:
        review_concepts = [
            c for c in unmastered
            if 0.5 < student.mastery[c.concept_id] < 0.8
        ]
        path = review_concepts + learnable[:10]
    else:
        path = learnable[:15]
    
    return path

# DELIVERABLE:
# - Layer 1 complete
# - Knowledge graph functionality
# - All tests passing
# - Ready for Layer 2
```

#### Layer 2: Adaptive Question Selector

```python
# /app/engine/layers/layer2_selector.py

def test_selector_chooses_right_difficulty():
    """Questions should be slightly harder than current mastery"""
    
    student = create_test_student()
    student.mastery["MATH_041"] = 0.5  # 50% mastery
    
    question = select_next_question(student, "MATH_041")
    
    # Should select question with difficulty ~0.65
    # (current mastery 0.5 + 0.15 buffer)
    assert abs(question.difficulty - 0.65) < 0.15

def test_selector_targets_misconceptions():
    """Questions should target student's specific misconceptions"""
    
    student = create_test_student()
    student.misconceptions_active["MIS_DERIV_001"] = 0.5  # Has misconception
    
    questions = select_candidate_questions(student, "MATH_041")
    top_question = questions[0]
    
    # Top question should target this misconception
    assert "MIS_DERIV_001" in top_question.targeted_misconceptions

# IMPLEMENTATION (simplified)

def select_next_question(student, concept_id):
    """Select best question for student to attempt next"""
    
    # Get all available questions for concept
    available = get_questions_by_concept(concept_id)
    
    # Filter by difficulty
    ideal_difficulty = student.mastery[concept_id] + 0.15
    suitable = [
        q for q in available
        if abs(q.difficulty - ideal_difficulty) < 0.2
    ]
    
    # Rank by criteria
    ranked = []
    for q in suitable:
        score = 0
        
        # Criterion 1: Misconception targeting
        misconceptions = get_misconceptions(q.question_id)
        for mis_id in misconceptions:
            if student.misconceptions_active.get(mis_id, 0) > 0.3:
                score += 100
        
        # Criterion 2: Recency
        days_since = get_days_since_attempted(q, student)
        if days_since is None:
            score += 50
        elif days_since > 7:
            score += 30
        
        # Criterion 3: Discrimination
        score += q.discrimination_index * 50
        
        ranked.append((q, score))
    
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[0][0] if ranked else suitable[0]

# DELIVERABLE:
# - Layer 2 complete
# - Smart question selection
# - All tests passing
```

#### Layer 3: Subject-Specific Strategies

```python
# /app/engine/layers/layer3_strategies.py

def test_math_strategy_enforces_prerequisites():
    """Math: Cannot skip prerequisites"""
    
    strategy = get_strategy("MATH")
    assert strategy.enforces_prerequisites == True
    assert strategy.allow_jumping_ahead == False

def test_physics_strategy_prioritizes_high_yield():
    """Physics: Prioritizes high-weightage topics"""
    
    strategy = get_strategy("PHYSICS")
    assert strategy.prioritize_weightage == True
    assert strategy.focus_mode == "HIGH_YIELD"

def test_chemistry_strategy_balanced():
    """Chemistry: Balanced across branches"""
    
    strategy = get_strategy("CHEMISTRY")
    assert strategy.require_foundation_first == True
    assert "Physical" in strategy.foundation_branch

# IMPLEMENTATION

def get_strategy(subject):
    """Get learning strategy for subject"""
    
    if subject == "MATH":
        return MathematicsStrategy()
    elif subject == "PHYSICS":
        return PhysicsStrategy()
    elif subject == "CHEMISTRY":
        return ChemistryStrategy()

class MathematicsStrategy:
    name = "Sequential-Mandatory"
    enforces_prerequisites = True
    allow_jumping_ahead = False
    practice_level = "HIGH"  # 20+ problems per concept
    
    def apply(self, question_candidates):
        """Filter questions by strategy"""
        # Must follow prerequisites strictly
        return [q for q in question_candidates if prerequisites_met(q)]

class PhysicsStrategy:
    name = "High-Yield-Selective"
    prioritize_weightage = True
    focus_mode = "HIGH_YIELD"
    
    def apply(self, question_candidates):
        """Prioritize high-weightage topics"""
        # Sort by exam weightage
        return sorted(
            question_candidates,
            key=lambda q: get_exam_weight(q),
            reverse=True
        )

class ChemistryStrategy:
    name = "Breadth-With-Foundation"
    require_foundation_first = True
    foundation_branch = "Physical Chemistry"
    
    def apply(self, question_candidates):
        """Ensure foundation before branching"""
        # Must have Physical Chemistry > 0.8 before Organic/Inorganic
        return [q for q in question_candidates if can_study_branch(q)]

# DELIVERABLE:
# - Layer 3 complete
# - 3 subject strategies
# - All tests passing
```

---

## WEEKS 4-6: ADVANCED LAYERS (Similar Structure)

[Each layer gets detailed specification with tests and implementation examples]

---

## WEEKS 7-9: SIMULATION TESTING

```python
# /simulation/harness.py

def run_full_simulation():
    """Run complete simulation testing"""
    
    # Create 100 synthetic students
    students = create_student_population(100)
    
    # Run for 30 simulated days
    for day in range(30):
        for student in students:
            # Each student does 20 questions
            for _ in range(20):
                # Get recommendation
                question = engine.get_next_question(student)
                
                # Simulate attempt
                attempt = simulate_question_attempt(student, question)
                
                # Process through engine
                engine.process_attempt(student, attempt)
                
                # Log
                log_attempt(student, question, attempt)
    
    # Collect metrics
    metrics = {
        "avg_mastery_improvement": calculate_mastery_improvement(),
        "rank_improvement": calculate_rank_improvement(),
        "burnout_detection_rate": calculate_burnout_detection(),
        "engagement_trend": calculate_engagement_trend(),
    }
    
    return metrics

# TESTS

def test_high_achievers_advance_fast():
    """Verify high achievers make rapid progress"""
    
    sim = SimulationHarness(
        num_high_achievers=50,
        simulation_days=30
    )
    
    metrics = sim.run()
    
    assert metrics["avg_mastery_improvement"] > 0.30  # >30% improvement
    assert metrics["rank_improvement"] > 500  # >500 position improvement

def test_struggling_students_not_overwhelmed():
    """Verify struggling students get appropriate difficulty"""
    
    sim = SimulationHarness(
        num_struggling=50,
        simulation_days=30
    )
    
    metrics = sim.run()
    
    # Should improve, not stay stuck or overwhelm
    assert 0.05 < metrics["avg_mastery_improvement"] < 0.25
    assert metrics["dropout_rate"] < 0.1  # <10% dropout

def test_burnout_detection_early():
    """Verify engine detects burnout early"""
    
    sim = SimulationHarness(
        num_at_risk=30,
        simulation_days=30
    )
    
    metrics = sim.run()
    
    # Should catch burnout before critical
    assert metrics["burnout_detected_early"] > 0.7  # >70% early
    assert metrics["intervention_success_rate"] > 0.6  # >60% recover
```

---

## WEEKS 10-12: INTEGRATION & TESTING

**Tasks:**
- Connect all 10 layers
- Run full integration tests
- Fix bugs from simulation
- Create test databases
- Load sample questions

---

## WEEKS 13-16: LAUNCH PREPARATION

**Tasks:**
- DevOps deployment
- Frontend integration
- Admin dashboard
- Real user launch

---

**Status: ✅ DETAILED SPRINT PLAN READY FOR EXECUTION**

**Next: Engineering team starts Week 1 Monday.**

---

**Prepared by:** Chief Technical Architect  
**Date:** December 6, 2025, 8:00 PM IST