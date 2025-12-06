# CR-V4.0 ENGINE BUILD PLAN
## Complete Phase-Wise Implementation: Backend + AI Engine + Simulation System

**Prepared for:** Aditya Pagare (CTO) & Chief Engineering Department  
**Date:** December 6, 2025, 7:00 PM IST  
**Classification:** DETAILED ENGINEERING BLUEPRINT - CORE ENGINE FOCUS  
**Priority:** Engine First → Simulation System → Testing → Database → DevOps/Frontend Last

---

## EXECUTIVE BRIEFING

### Strategy: Build Smart, Test Rigorously

**Our Approach:**
```
Phase 1: FOUNDATION (Week 1-2)
└─ Core infrastructure, knowledge graph, concept database

Phase 2: CORE ENGINE LAYER (Week 3-6)
└─ All 10 adaptive layers with deep logic implementation
└─ Mathematical models for personalization
└─ Burnout detection algorithms
└─ Strategic recommendation engines (Math/Physics/Chemistry specific)

Phase 3: SIMULATION SYSTEM (Week 7-9)
└─ Honest simulation engine that replicates real student behavior
└─ Test engine with synthetic user profiles
└─ Performance metrics collection
└─ Bug identification and logging

Phase 4: INTEGRATION & REFINEMENT (Week 10-12)
└─ Connect all layers
└─ Test with simulation (find bugs/gaps)
└─ Fix and optimize
└─ Build test databases

Phase 5: LAUNCH PREP (Week 13-16)
└─ Database migration
└─ DevOps deployment
└─ Frontend integration (simple)
└─ Real user launch
```

**Why This Approach?**
- ✅ Build strong core first (no weak foundation)
- ✅ Simulate before real users (catch 90% of bugs)
- ✅ Test with synthetic data (fast iterations)
- ✅ Ensure all layers work together
- ✅ DevOps comes last (infrastructure for proven system)

---

## PART A: FOUNDATION PHASE (WEEK 1-2)

### OBJECTIVE
Set up core infrastructure that all other layers will depend on.

### Week 1: Database Schema & Knowledge Graph

#### Task 1.1: Concept Knowledge Graph Database (Day 1-2)

**What to Build:**
A PostgreSQL database structure that represents all JEE-MAINS knowledge as a directed graph.

**Database Schema:**

```sql
-- CONCEPTS TABLE: Core knowledge nodes
CREATE TABLE concepts (
    concept_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(20),  -- MATH, PHYSICS, CHEMISTRY
    layer INT,  -- Which CR layer (1-10)
    difficulty INT,  -- 1-5 scale
    exam_weight DECIMAL(4,3),  -- 0.001 to 1.0 (importance in JEE)
    description TEXT,
    parent_concept_id VARCHAR(20),  -- Hierarchical structure
    
    INDEX idx_subject (subject),
    INDEX idx_layer (layer),
    FOREIGN KEY (parent_concept_id) REFERENCES concepts(concept_id)
);

-- PREREQUISITE RELATIONSHIPS: What must be learned first
CREATE TABLE concept_prerequisites (
    prerequisite_id BIGSERIAL PRIMARY KEY,
    concept_id VARCHAR(20) NOT NULL,
    prerequisite_concept_id VARCHAR(20) NOT NULL,
    criticality VARCHAR(20),  -- HARD (must know) or SOFT (helpful)
    weight DECIMAL(3,2),  -- 0.5-1.0 (strength of dependency)
    transfer_coefficient DECIMAL(3,2),  -- 0.0-1.0 (how much learning prereq helps current)
    
    UNIQUE (concept_id, prerequisite_concept_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id),
    FOREIGN KEY (prerequisite_concept_id) REFERENCES concepts(concept_id),
    INDEX idx_concept (concept_id)
);

-- KNOWLEDGE TRANSFER MATRIX: Learning relationships
CREATE TABLE knowledge_transfer (
    transfer_id BIGSERIAL PRIMARY KEY,
    source_concept VARCHAR(20) NOT NULL,
    target_concept VARCHAR(20) NOT NULL,
    transfer_type VARCHAR(50),  -- FOUNDATIONAL, REINFORCING, EXTENDING, COMPETING
    transfer_strength DECIMAL(3,2),  -- 0.0-1.0
    learning_time_multiplier DECIMAL(3,2),  -- How much faster to learn target after source
    
    FOREIGN KEY (source_concept) REFERENCES concepts(concept_id),
    FOREIGN KEY (target_concept) REFERENCES concepts(concept_id),
    INDEX idx_source (source_concept)
);

-- MISCONCEPTIONS TABLE: Common student errors
CREATE TABLE misconceptions (
    misconception_id BIGSERIAL PRIMARY KEY,
    concept_id VARCHAR(20) NOT NULL,
    misconception_description TEXT,
    trigger_questions VARCHAR(500),  -- Question IDs that trigger this
    recovery_strategy TEXT,  -- How to help student unlearn
    difficulty_to_correct INT,  -- 1-5 scale
    
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id),
    INDEX idx_concept (concept_id)
);
```

**Subject-Specific Concept Structure:**

**MATHEMATICS (MATH_):**
```
Layer 1: Foundations
├─ MATH_001: Number Systems (integers, rationals, reals, complex)
├─ MATH_002: Algebra Basics (equations, inequalities)
├─ MATH_003: Exponents & Logarithms
└─ MATH_004: Trigonometric Ratios

Layer 2: Intermediate
├─ MATH_010: Sequences & Series
├─ MATH_020: Trigonometric Functions
├─ MATH_030: Functions & Relations
└─ MATH_040: Limits

Layer 3: Advanced
├─ MATH_041: Derivatives (Applications)
├─ MATH_042: Antiderivatives
├─ MATH_043: Definite Integrals
└─ MATH_050: Differential Equations

[... continues for all concepts ...]

Total: ~60 core concepts
Transfer relationships: ~200 edges
Prerequisites: ~150 edges
```

**PHYSICS (PHY_):**
```
Layer 1: Kinematics & Forces
├─ PHY_001: Motion in 1D
├─ PHY_002: Motion in 2D
├─ PHY_003: Newton's Laws
└─ PHY_004: Friction & Normal Force

Layer 2: Energy & Momentum
├─ PHY_010: Work & Energy
├─ PHY_011: Momentum & Collisions
├─ PHY_012: Rotational Motion
└─ PHY_013: Gravitation

[... continues ...]

Total: ~50 core concepts
```

**CHEMISTRY (CHM_):**
```
Layer 1: Basics
├─ CHM_001: Atomic Structure
├─ CHM_002: Periodic Table
├─ CHM_003: Chemical Bonding
└─ CHM_004: States of Matter

Layer 2: Inorganic
├─ CHM_010: Thermodynamics
├─ CHM_011: Equilibrium
├─ CHM_012: Redox Reactions
└─ CHM_020: Coordination Chemistry

Layer 3: Organic
├─ CHM_030: Nomenclature
├─ CHM_031: Isomerism
├─ CHM_032: Reaction Mechanisms
└─ CHM_040: Synthesis

[... continues ...]

Total: ~55 core concepts
```

**Implementation Steps:**

1. **Day 1 Morning:** Define all concept nodes
   - Mathematics: 60 concepts
   - Physics: 50 concepts
   - Chemistry: 55 concepts
   - Insert into concepts table with hierarchies

2. **Day 1 Afternoon:** Define prerequisite relationships
   - For each concept, identify what MUST be known first (criticality: HARD)
   - Identify helpful background (criticality: SOFT)
   - Set weights (0.5 = weak dependency, 1.0 = absolute requirement)

3. **Day 2 Morning:** Define knowledge transfer relationships
   - FOUNDATIONAL: Learning X makes Y much easier (high transfer)
   - REINFORCING: Y reinforces X (bidirectional benefit)
   - EXTENDING: X is applied in Y (extension relationship)
   - COMPETING: X and Y are often confused (negative transfer)

4. **Day 2 Afternoon:** Load misconceptions
   - 3-5 common misconceptions per concept
   - Recovery strategies
   - Test question sets that trigger each

**Deliverable:**
- PostgreSQL database with 165 concepts
- 200+ prerequisite relationships mapped
- 150+ knowledge transfer relationships defined
- 300+ misconceptions documented
- All indexed and optimized for fast queries

---

#### Task 1.2: Question Bank Database Schema (Day 3-4)

**What to Build:**
PostgreSQL schema for storing question metadata (separate from content DB).

```sql
-- QUESTIONS TABLE (Metadata Only)
CREATE TABLE questions_metadata (
    question_id VARCHAR(50) PRIMARY KEY,
    subject VARCHAR(20),  -- MATH, PHYSICS, CHEMISTRY
    concept_id VARCHAR(20) NOT NULL,
    difficulty_level INT,  -- 1-4 scale
    question_type VARCHAR(20),  -- MCQ, NUMERICAL, INTEGER
    marks INT,
    jee_weightage DECIMAL(4,3),  -- How common in actual JEE
    
    -- Learning classification
    bloom_level VARCHAR(20),  -- Remember, Understand, Apply, Analyze, Evaluate, Create
    learning_time_seconds INT,
    
    -- Performance tracking
    student_attempts INT DEFAULT 0,
    student_correct INT DEFAULT 0,
    difficulty_discrimination DECIMAL(3,2),  -- How well differentiates strong/weak
    
    -- Quality
    expert_accuracy_rating INT,  -- 1-5 stars
    is_approved BOOLEAN,
    
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id),
    INDEX idx_subject (subject),
    INDEX idx_concept (concept_id),
    INDEX idx_difficulty (difficulty_level)
);

-- QUESTION OPTIONS
CREATE TABLE question_options (
    option_id BIGSERIAL PRIMARY KEY,
    question_id VARCHAR(50) NOT NULL,
    option_letter VARCHAR(1),
    is_correct BOOLEAN,
    misconception_id BIGINT,  -- Which misconception this distracter targets
    
    FOREIGN KEY (question_id) REFERENCES questions_metadata(question_id),
    FOREIGN KEY (misconception_id) REFERENCES misconceptions(misconception_id)
);

-- QUESTION PREREQUISITE REQUIREMENTS
CREATE TABLE question_prerequisite_mapping (
    mapping_id BIGSERIAL PRIMARY KEY,
    question_id VARCHAR(50) NOT NULL,
    required_concept_id VARCHAR(20) NOT NULL,
    criticality VARCHAR(20),  -- ESSENTIAL, HELPFUL, BACKGROUND
    weight DECIMAL(3,2),
    
    FOREIGN KEY (question_id) REFERENCES questions_metadata(question_id),
    FOREIGN KEY (required_concept_id) REFERENCES concepts(concept_id)
);
```

**Design Principles:**

1. **Separation:** Question metadata separate from actual question text (which comes from expert DB)
2. **Tagging:** Every question tagged with concepts it tests
3. **Classification:** Bloom level + question type + marks for adaptive routing
4. **Performance Tracking:** Ready to store student attempt data
5. **Quality Metrics:** Expert rating + student performance data

**Implementation:**

1. **Day 3 Morning:** Create schema
2. **Day 3 Afternoon:** Create indexes (20+ critical indexes)
3. **Day 4 Morning:** Sample data load (1000 questions for testing)
4. **Day 4 Afternoon:** Query optimization and verification

**Deliverable:**
- Complete PostgreSQL schema for 100K+ questions capacity
- Efficient indexing strategy
- Ready to accept both test and real data

---

### Week 2: Core Data Models & Simulation Foundation

#### Task 2.1: Student Model & Mastery Calculation (Day 1-2)

**What to Build:**
The data structure that represents a student's knowledge state.

```python
# PostgreSQL Schema for Student State

class StudentMasteryModel:
    """
    Represents what a student knows at any point in time.
    This is the brain's working memory.
    """
    
    student_id: str
    cohort_id: str  # Which exam batch (e.g., "JEE_DEC_2025")
    
    # Knowledge State: For each concept, how well does student know it?
    concept_mastery: Dict[str, MasteryState]
    
    # Example MasteryState for concept MATH_041 (Derivatives):
    {
        "concept_id": "MATH_041",
        "mastery_level": 0.72,  # 0.0 (no knowledge) to 1.0 (expert)
        "confidence": 0.85,  # How confident are we in this assessment?
        "last_attempted": "2025-12-06 15:30:00",
        "attempts_total": 5,
        "attempts_correct": 3,
        "time_to_answer_avg": 145,  # seconds
        "learning_speed": 0.8,  # How fast they learn (0.5-1.5x)
        "recent_trend": "improving",  # improving, stable, declining
        "prerequisite_gaps": ["MATH_040"],  # Which prerequisites weak
    }

# PostgreSQL Schema
CREATE TABLE student_mastery (
    mastery_id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    concept_id VARCHAR(20) NOT NULL,
    mastery_level DECIMAL(3,2),  -- 0.0-1.0
    confidence DECIMAL(3,2),
    last_attempted TIMESTAMP,
    attempts_total INT DEFAULT 0,
    attempts_correct INT DEFAULT 0,
    time_to_answer_avg INT,  -- seconds
    learning_speed DECIMAL(3,2),
    recent_trend VARCHAR(20),
    prerequisite_gaps TEXT,  -- JSON array
    
    UNIQUE (student_id, concept_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id),
    INDEX idx_student (student_id),
    INDEX idx_mastery_level (mastery_level)
);

# Mastery Calculation Logic (Bayes Update)

def update_mastery(current_mastery, question_result):
    """
    Bayesian update: Based on question attempt, update belief about knowledge.
    
    Args:
        current_mastery: Previous belief (0.0-1.0)
        question_result: {
            "correct": True/False,
            "time_taken": int (seconds),
            "question_difficulty": 0.0-1.0,
            "guessing_probability": 0.0-1.0 (was answer lucky guess?)
        }
    
    Returns:
        Updated mastery level using Bayes theorem
    """
    
    # Prior: What we believed before
    prior = current_mastery
    
    # Likelihood: P(observation | mastery_level)
    if question_result["correct"]:
        # Student got it right. How likely given different mastery levels?
        # If mastery = 0.9, very likely to get it right
        # If mastery = 0.3, less likely (but possible)
        
        p_correct_given_mastery = (
            prior * (1 - GUESSING_PROBABILITY)  # Actual knowledge
            + GUESSING_PROBABILITY  # Random guess luck
        )
        likelihood = p_correct_given_mastery
    else:
        # Student got it wrong
        p_wrong_given_mastery = 1 - prior * (1 - GUESSING_PROBABILITY)
        likelihood = p_wrong_given_mastery
    
    # Posterior: Updated belief (Bayes theorem)
    posterior = (likelihood * prior) / (
        likelihood * prior + (1 - likelihood) * (1 - prior)
    )
    
    # Confidence: How sure are we? (Based on consistency)
    # More attempts = higher confidence
    confidence = calculate_confidence(
        attempts=question_result["total_attempts"],
        variance=question_result["attempt_variance"]
    )
    
    return {
        "mastery_level": posterior,
        "confidence": confidence,
        "update_reason": "Bayes update from question attempt"
    }

# Time-to-Answer Analysis
def calculate_learning_speed(question_history):
    """
    How fast does student learn? (Multiplicative factor on learning rate)
    
    If learning_speed = 0.7: Student learns 30% slower than average
    If learning_speed = 1.3: Student learns 30% faster than average
    
    This affects how much to advance to next concept.
    """
    
    # Look at time trend: Is time per question decreasing?
    times = [q["time_taken"] for q in question_history[-5:]]  # Last 5 attempts
    
    if len(times) < 2:
        return 1.0  # Default (average speed)
    
    # Linear regression on times
    time_trend = linear_regression(times)
    
    if time_trend < -5:  # Time decreasing by >5 sec per attempt
        return 1.3  # Fast learner
    elif time_trend < 0:
        return 1.1
    elif time_trend < 5:
        return 0.9  # Slow learner
    else:
        return 0.7
    
    # Example:
    # If system calculates "advance by 0.1 mastery"
    # Slow learner (0.7x): advances by 0.07
    # Fast learner (1.3x): advances by 0.13

# Recent Trend Detection
def detect_trend(question_history):
    """
    Is student improving, stable, or declining?
    Affects: confidence in recommendations, need for review, motivation tracking
    """
    
    recent = question_history[-5:]
    accuracy = [1 if q["correct"] else 0 for q in recent]
    
    # Linear fit to accuracy trend
    slope, intercept = linear_regression(accuracy)
    
    if slope > 0.05:
        return "improving"
    elif slope < -0.05:
        return "declining"
    else:
        return "stable"
```

**Implementation Steps:**

1. **Day 1 Morning:** Design student_mastery table
2. **Day 1 Afternoon:** Implement Bayes update logic
3. **Day 2 Morning:** Implement learning speed calculation
4. **Day 2 Afternoon:** Implement trend detection

**Deliverable:**
- Complete student mastery model
- Bayes update logic tested mathematically
- Learning speed and trend detection algorithms
- PostgreSQL table ready for 1M+ students

---

#### Task 2.2: Simulation System Foundation (Day 3-5)

**What to Build:**
A synthetic student generator that creates realistic student behavior for testing.

```python
# Simulation System: Create Fake Students

class SimulatedStudent:
    """
    A synthetic student that behaves realistically.
    Used for testing the engine without real users.
    """
    
    def __init__(self, profile):
        self.student_id = f"SIM_{uuid4()}"
        self.profile = profile  # See below
        
        # Knowledge state
        self.mastery = {}  # concept_id -> mastery_level
        self.misconceptions_active = {}  # misconception_id -> active or not
        
        # Psychological state
        self.motivation = 0.8  # 0.0-1.0
        self.fatigue = 0.0  # 0.0-1.0
        self.stress = 0.5  # 0.0-1.0
        self.burnout_risk = 0.1  # 0.0-1.0
        
        # Session state
        self.session_question_count = 0
        self.session_start_time = None

class StudentProfile:
    """
    Different types of students with different learning patterns.
    """
    
    def __init__(self, student_type):
        self.student_type = student_type
        
        if student_type == "HIGH_ACHIEVER":
            self.base_learning_speed = 1.3
            self.motivation_baseline = 0.9
            self.misconception_rate = 0.15
            self.careless_error_rate = 0.05
            self.burnout_speed = 0.02  # Slow
            
        elif student_type == "AVERAGE_STEADY":
            self.base_learning_speed = 1.0
            self.motivation_baseline = 0.7
            self.misconception_rate = 0.25
            self.careless_error_rate = 0.10
            self.burnout_speed = 0.05
            
        elif student_type == "STRUGGLING":
            self.base_learning_speed = 0.7
            self.motivation_baseline = 0.5
            self.misconception_rate = 0.40
            self.careless_error_rate = 0.20
            self.burnout_speed = 0.10
            
        elif student_type == "BURNOUT_RISK":
            self.base_learning_speed = 0.8
            self.motivation_baseline = 0.3
            self.misconception_rate = 0.35
            self.careless_error_rate = 0.25
            self.burnout_speed = 0.15  # Very fast burnout

# Synthetic Question Attempt Generator

def simulate_question_attempt(student, question):
    """
    Given a student and question, generate realistic answer + metadata.
    
    This is where the magic happens - creates synthetic data that's
    statistically similar to real student behavior.
    """
    
    # Step 1: Determine if student will get it right
    # Based on: mastery level, question difficulty, misconceptions
    
    # Check if student has relevant misconception
    for misconception_id in question.misconceptions:
        if student.misconceptions_active[misconception_id]:
            # Student will likely get wrong (if this misconception triggers)
            p_correct = 0.2  # Only 20% chance of getting right despite misconception
            break
    else:
        # No active misconception for this question
        # Probability of correct = function of mastery and difficulty
        question_difficulty = question.difficulty_level  # 0.0-1.0
        student_mastery = student.mastery[question.concept_id]  # 0.0-1.0
        
        # If mastery >> difficulty: very likely correct
        # If mastery << difficulty: unlikely correct
        p_correct = sigmoid(
            (student_mastery - question_difficulty) * 4
        )  # Sigmoid for smooth probability
        
        # Add careless errors: sometimes get it wrong despite knowing
        careless_error_chance = student.profile.careless_error_rate * student.fatigue
        if random() < careless_error_chance:
            p_correct *= 0.3  # Reduce by 70% (careless error)
    
    # Step 2: Generate time taken
    # Based on: mastery, question difficulty, fatigue, motivation
    
    base_time = question.estimated_time  # From question metadata (e.g., 120 sec)
    
    # Mastery effect: Higher mastery = faster answer
    mastery_multiplier = 1 + (1 - student_mastery) * 0.5
    
    # Difficulty effect: Higher difficulty = longer time
    difficulty_multiplier = 1 + question_difficulty * 0.3
    
    # Fatigue effect: More fatigue = slower thinking
    fatigue_multiplier = 1 + student.fatigue * 0.4
    
    # Motivation effect: Low motivation = less effort = faster (but wrong)
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
    
    # Step 3: Generate answer result
    
    is_correct = random() < p_correct
    
    # Step 4: Update student state based on attempt
    
    # Update fatigue (increases with every question)
    student.fatigue += 0.01 * (1 - student.motivation)
    
    # If answered wrong: increase misconception risk
    if not is_correct and student.mastery[question.concept_id] < 0.6:
        # Student might pick up misconception
        if random() < question.misconception_trigger_probability:
            misconception_id = select_random_misconception(question)
            student.misconceptions_active[misconception_id] += 0.2
    
    # Update motivation (decreases with failures, increases with success)
    if is_correct:
        student.motivation += 0.05
        student.burnout_risk *= 0.95  # Small recovery
    else:
        student.motivation -= 0.10
        student.burnout_risk *= 1.05  # Small increase
    
    # Clamp values
    student.motivation = max(0.0, min(1.0, student.motivation))
    student.burnout_risk = max(0.0, min(1.0, student.burnout_risk))
    
    # Step 5: Return simulation result
    
    return {
        "question_id": question.question_id,
        "is_correct": is_correct,
        "time_taken": time_taken,
        "timestamp": datetime.now(),
        "student_state_after": {
            "mastery": student.mastery[question.concept_id],
            "motivation": student.motivation,
            "fatigue": student.fatigue,
            "burnout_risk": student.burnout_risk,
        }
    }

# Simulation Harness: Run simulations

class SimulationHarness:
    """
    Run synthetic students through the platform.
    Collect data to verify engine works.
    """
    
    def __init__(self, num_students=100):
        self.students = []
        self.results = []
        
        # Create diverse student population
        profiles = [
            ("HIGH_ACHIEVER", 0.2),  # 20% high achievers
            ("AVERAGE_STEADY", 0.5),  # 50% average
            ("STRUGGLING", 0.2),  # 20% struggling
            ("BURNOUT_RISK", 0.1),  # 10% at risk
        ]
        
        for profile_type, fraction in profiles:
            count = int(num_students * fraction)
            for _ in range(count):
                profile = StudentProfile(profile_type)
                student = SimulatedStudent(profile)
                self.students.append(student)
    
    def run_simulation_day(self, day_num):
        """
        Run 1 simulated day of all students using platform.
        """
        
        for student in self.students:
            # Each student gets 20 questions per day
            for _ in range(20):
                # Engine recommends next question
                question = self.engine.get_next_question(student)
                
                # Student attempts question
                result = simulate_question_attempt(student, question)
                
                # Engine processes result
                self.engine.process_attempt(student, result)
                
                # Log result
                self.results.append({
                    "day": day_num,
                    "student_id": student.student_id,
                    "result": result
                })
    
    def collect_metrics(self):
        """
        After simulation, analyze results.
        """
        
        return {
            "avg_mastery_improvement": ...,
            "rank_improvement": ...,
            "burnout_cases_detected": ...,
            "personalization_effectiveness": ...,
            "engine_recommendations_accuracy": ...,
        }
```

**Implementation:**

1. **Day 3 Morning:** Design SimulatedStudent class
2. **Day 3 Afternoon:** Implement StudentProfile types (4 types)
3. **Day 4 Morning:** Implement question attempt simulation
4. **Day 4 Afternoon:** Build simulation harness
5. **Day 5 Morning/Afternoon:** Test simulation (run 100 students × 20 days)

**Deliverable:**
- Fully functional simulation system
- 4 different student types with realistic behavior
- Simulation harness that can run 1000s of synthetic days
- Data collection infrastructure ready

---

### Week 2 Completion Check

**By End of Week 2:**
- ✅ Knowledge graph database (165 concepts, 200+ relationships)
- ✅ Question metadata database (100K capacity)
- ✅ Student mastery model with Bayes updates
- ✅ Learning speed and trend detection
- ✅ Simulation system with 4 student types
- ✅ Simulation harness ready to run
- ✅ All databases indexed and optimized

**Status:** Foundation complete. Ready for core engine build.

---

## PART B: CORE ENGINE BUILD (WEEK 3-6)

### OBJECTIVE
Build all 10 adaptive layers with deep mathematical logic and AI algorithms.

### Layer 1-3: Foundational Layers (Week 3)

#### Layer 1: Knowledge Graph & Concept Sequencing

**Mathematical Logic:**

```python
# Layer 1: Build optimal learning path

class KnowledgeGraphEngine:
    """
    Determine: What should student learn next?
    Based on: Current mastery, prerequisites, learning speed, exam objectives
    """
    
    def build_learning_path(self, student):
        """
        Topological sort of concepts with mastery constraints.
        Returns ordered list of concepts to learn.
        """
        
        # Step 1: Identify all concepts with mastery < 0.9 (not yet mastered)
        unlearned = [
            c for c in all_concepts 
            if student.mastery[c] < 0.9
        ]
        
        # Step 2: For each unlearned concept, check prerequisites
        # Can only learn if: prerequisite_mastery > threshold OR soft_prerequisite
        
        learnable = []
        for concept in unlearned:
            prerequisites = get_prerequisites(concept)
            
            can_learn = True
            for prereq, criticality, weight in prerequisites:
                prereq_mastery = student.mastery[prereq]
                
                if criticality == "HARD":
                    if prereq_mastery < 0.7:  # Must know 70%
                        can_learn = False
                        break
                elif criticality == "SOFT":
                    if prereq_mastery < 0.4:  # Nice to have 40%
                        pass  # Can still learn but suboptimally
            
            if can_learn:
                learnable.append(concept)
        
        # Step 3: Prioritize by exam importance
        # High weightage concepts = higher priority
        
        learnable.sort(
            key=lambda c: get_exam_weight(c),
            reverse=True
        )
        
        # Step 4: Apply learning speed adjustment
        # Fast learner: fewer review concepts
        # Slow learner: more review concepts
        
        if student.learning_speed > 1.1:  # Fast
            # Jump ahead more aggressively
            path = learnable[:20]
        elif student.learning_speed < 0.9:  # Slow
            # Include more review concepts
            review_concepts = [
                c for c in unlearned 
                if student.mastery[c] > 0.5 and student.mastery[c] < 0.8
            ]
            path = review_concepts + learnable[:10]
        else:
            path = learnable[:15]
        
        return path

# Concept Sequencing Constraints

def check_prerequisite_satisfaction(student, concept):
    """
    Can student learn this concept?
    Returns: (can_learn, missing_prerequisites)
    """
    
    prerequisites = get_prerequisites(concept)
    missing = []
    
    for prereq, criticality, weight in prerequisites:
        prereq_mastery = student.mastery[prereq]
        threshold = 0.7 if criticality == "HARD" else 0.4
        
        if prereq_mastery < threshold:
            missing.append({
                "concept": prereq,
                "current_mastery": prereq_mastery,
                "required_mastery": threshold,
                "criticality": criticality,
            })
    
    can_learn = len(missing) == 0
    return can_learn, missing
```

**Implementation:** 
- Day 1: Build concept sequencing algorithm
- Day 1: Implement prerequisite checking
- Day 2: Test with simulation (does learning path make sense?)

**Code to Write:**
- `build_learning_path()` function (50 lines)
- `check_prerequisite_satisfaction()` function (30 lines)
- `prioritize_by_exam_weight()` function (20 lines)
- Tests with simulation students (verify paths are logical)

---

#### Layer 2: Adaptive Question Selection

**Mathematical Logic:**

```python
# Layer 2: Select which question to show student next

class AdaptiveQuestionSelector:
    """
    Given: Student's current mastery and learning state
    Select: Next question that maximizes learning
    
    Not random. Carefully chosen for each student.
    """
    
    def select_next_question(self, student, concept_to_learn):
        """
        Question selection strategy:
        1. If mastery 0.0-0.2: Show BASIC questions (difficulty 1)
        2. If mastery 0.2-0.5: Show MEDIUM questions (difficulty 2-3)
        3. If mastery 0.5-0.8: Show CHALLENGING questions (difficulty 3-4)
        4. If mastery 0.8+: Show EXPERT questions (difficulty 4) or new concept
        
        Question difficulty should be: student_mastery ± 0.1
        (Sweet spot for learning - not too easy, not too hard)
        """
        
        # Get current mastery
        current_mastery = student.mastery[concept_to_learn]
        
        # Calculate ideal difficulty
        # Questions slightly above current level are best for learning
        ideal_difficulty = min(1.0, current_mastery + 0.15)
        
        # Get available questions for this concept
        available_questions = get_questions_by_concept(
            concept_to_learn,
            available_only=True
        )
        
        # Filter by difficulty
        # Select questions where difficulty is close to ideal
        difficulty_tolerance = 0.1
        suitable_questions = [
            q for q in available_questions
            if abs(q.difficulty - ideal_difficulty) < difficulty_tolerance
        ]
        
        # If not enough similar difficulty, widen tolerance
        if len(suitable_questions) < 5:
            difficulty_tolerance = 0.2
            suitable_questions = [
                q for q in available_questions
                if abs(q.difficulty - ideal_difficulty) < difficulty_tolerance
            ]
        
        # Rank by additional criteria
        # Prioritize questions that:
        # 1. Target known misconceptions (personalized)
        # 2. Haven't been attempted recently
        # 3. Have good discrimination index (good at measuring knowledge)
        
        ranked = []
        for question in suitable_questions:
            score = 0
            
            # Criterion 1: Misconception targeting
            misconceptions_in_q = get_misconceptions(question)
            active_misconceptions = [
                m for m in misconceptions_in_q
                if student.misconceptions_active[m] > 0.3
            ]
            score += len(active_misconceptions) * 100  # High priority
            
            # Criterion 2: Recency (haven't seen recently)
            days_since_attempted = get_days_since_attempted(question, student)
            if days_since_attempted is None:
                score += 50  # Never attempted: bonus
            elif days_since_attempted > 7:
                score += 30  # Old question: good for review
            else:
                score -= 20  # Recent question: skip for variety
            
            # Criterion 3: Discrimination
            discrimination = question.discrimination_index  # 0-1
            score += discrimination * 50  # Good discriminators: bonus
            
            ranked.append((question, score))
        
        # Sort by score and return top question
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        if len(ranked) == 0:
            # Fallback: any question for this concept
            return available_questions[0] if available_questions else None
        
        selected = ranked[0][0]
        return selected

def calculate_adaptive_difficulty_adjustment():
    """
    Micro-adjust question difficulty based on recent performance.
    
    If student: getting last 5 questions right → increase difficulty
    If student: getting last 5 questions wrong → decrease difficulty
    """
    
    recent_questions = student.recent_attempts[-5:]
    accuracy = sum(1 for q in recent_questions if q["correct"]) / 5
    
    if accuracy > 0.8:  # 4+ correct out of 5
        return +0.2  # Next question 20% harder
    elif accuracy < 0.4:  # 2 or fewer correct
        return -0.2  # Next question 20% easier
    else:
        return 0  # Keep same difficulty
```

**Implementation:**
- Day 2-3: Build question selector
- Day 3: Implement difficulty adjustment
- Day 3-4: Test with simulation (verify good questions chosen)

**Code to Write:**
- `select_next_question()` function (80 lines)
- `calculate_adaptive_difficulty_adjustment()` function (20 lines)
- `rank_questions_by_criteria()` function (50 lines)
- Misconception detection in questions (30 lines)
- Tests verifying smart selection (not random)

---

#### Layer 3: Subject-Specific Learning Strategies

**Mathematical Logic:**

```python
# Layer 3: Different strategies for Math, Physics, Chemistry

class MathematicsStrategy:
    """
    Mathematics: Sequential mandatory learning
    Must learn: A → B → C (can't skip)
    
    Example: Can't do Calculus before Algebra
    """
    
    def get_learning_strategy(self, student):
        """
        For mathematics:
        1. Ensure foundation knowledge (basics)
        2. Build sequentially (no jumping)
        3. Emphasize practice (many problems)
        4. Test frequently (verify understanding)
        """
        
        strategy = {
            "name": "Sequential-Mandatory",
            "description": "Build step-by-step foundation",
            
            "practice_level": "HIGH",  # 20+ problems per concept
            "test_frequency": "HIGH",  # Test every 3 concepts
            "review_intensity": "MEDIUM",  # Review if mastery drops
            
            "question_type_distribution": {
                "MCQ": 0.3,  # 30% multiple choice
                "NUMERICAL": 0.4,  # 40% numerical (requires calculation)
                "INTEGER": 0.3,  # 30% integer type
            },
            
            "difficulty_progression": [
                0.2,  # Start very easy
                0.3,
                0.4,
                0.5,
                0.6,  # Build up
                0.65,
                0.7,
                0.75,
                0.8,  # Test harder problems
            ],
        }
        
        return strategy

class PhysicsStrategy:
    """
    Physics: High-yield selective learning
    Focus on high-weightage topics
    
    Example: Mechanics appears in 20% of questions → prioritize
    Optics appears in 5% → learn if time
    """
    
    def get_learning_strategy(self, student):
        """
        For physics:
        1. Prioritize high-weightage topics
        2. Understand concepts deeply (not just practice)
        3. Mixed topics after mastery
        4. Visualizations important (diagrams)
        """
        
        strategy = {
            "name": "High-Yield-Selective",
            "description": "Focus on high-impact topics",
            
            "practice_level": "MEDIUM",  # 10-15 problems per concept
            "test_frequency": "MEDIUM",
            "review_intensity": "LOW",  # Only if critical
            
            "question_type_distribution": {
                "MCQ": 0.4,
                "NUMERICAL": 0.6,  # Physics needs calculations
            },
            
            "emphasis": "CONCEPTUAL_UNDERSTANDING",  # Why, not just how
            
            # Weightage-based prioritization
            "topic_priority": {
                "Mechanics": 0.25,  # 25% of exam
                "Optics": 0.15,
                "Electromagnetism": 0.20,
                "Modern Physics": 0.10,
                # ... etc
            },
        }
        
        return strategy

class ChemistryStrategy:
    """
    Chemistry: Breadth-first with reinforcement
    Three branches: Inorganic, Organic, Physical
    
    Need foundation in physical chemistry
    Then branch into inorganic + organic
    """
    
    def get_learning_strategy(self, student):
        """
        For chemistry:
        1. Physical chemistry first (foundation)
        2. Branch into inorganic + organic
        3. Connect concepts (same principles apply)
        4. Memorization + problem-solving mix
        """
        
        strategy = {
            "name": "Breadth-With-Foundation",
            "description": "Learn across all branches with physical base",
            
            "practice_level": "MEDIUM",
            "test_frequency": "MEDIUM",
            "review_intensity": "HIGH",  # Memorization requires review
            
            "branch_structure": {
                "Physical Chemistry": {
                    "priority": "FIRST",
                    "mastery_required": 0.8,
                },
                "Inorganic Chemistry": {
                    "priority": "SECOND",
                    "depends_on": "Physical Chemistry",
                },
                "Organic Chemistry": {
                    "priority": "SECOND",
                    "depends_on": "Physical Chemistry",
                },
            },
            
            # Balance theory vs practice
            "learning_mix": {
                "concept_learning": 0.4,  # Understand theory
                "practice_problems": 0.4,  # Apply knowledge
                "memorization": 0.2,  # Remember facts
            },
        }
        
        return strategy

# Application

def select_questions_by_subject_strategy(student, subject):
    """
    Based on subject, apply different selection strategies.
    """
    
    if subject == "MATH":
        strategy = MathematicsStrategy().get_learning_strategy(student)
    elif subject == "PHYSICS":
        strategy = PhysicsStrategy().get_learning_strategy(student)
    elif subject == "CHEMISTRY":
        strategy = ChemistryStrategy().get_learning_strategy(student)
    
    # Use strategy to adjust question selection
    # E.g., for math: never skip prerequisites
    # E.g., for physics: prioritize high-weightage topics
    # E.g., for chemistry: ensure foundation in physical chemistry
    
    return select_questions_with_strategy(student, strategy)
```

**Implementation:**
- Day 4: Design 3 subject-specific strategies
- Day 4-5: Implement Mathematics strategy
- Day 5: Implement Physics and Chemistry strategies
- Day 5-6: Test with simulation (verify strategies produce different paths)

**Code to Write:**
- `MathematicsStrategy` class (60 lines)
- `PhysicsStrategy` class (60 lines)
- `ChemistryStrategy` class (70 lines)
- `select_questions_by_subject_strategy()` function (40 lines)
- Simulation tests for each strategy (verify different learning paths)

---

**Week 3 Deliverables:**
- ✅ Layer 1: Knowledge graph engine
- ✅ Layer 2: Adaptive question selector
- ✅ Layer 3: Subject-specific strategies
- ✅ All tested with simulation students

---

### Layer 4-6: Advanced Personalization (Week 4)

[Detailed implementation continues with same depth...]

---

### Layer 7-8: Learning Optimization & Burnout Detection (Week 5)

[Detailed implementation continues...]

---

### Layer 9-10: Rank Projection & Engagement (Week 6)

[Detailed implementation continues...]

---

## PART C: SIMULATION TESTING PHASE (WEEK 7-9)

### Simulation Scenarios

```
Scenario 1: 100 HIGH_ACHIEVER students
└─ Verify: Rapid advancement without overwhelming
└─ Metric: Average rank improvement > 500 positions

Scenario 2: 100 AVERAGE students
└─ Verify: Steady progress with engagement
└─ Metric: Retention > 85%, rank improvement 50-200

Scenario 3: 100 STRUGGLING students
└─ Verify: Personalization helps, not overwhelming
└─ Metric: Burnout detection triggers appropriately

Scenario 4: 100 BURNOUT_RISK students
└─ Verify: Engine detects risk early and intervenes
└─ Metric: Recovery rate > 60%
```

---

## PART D: INTEGRATION & REFINEMENT (WEEK 10-12)

### Connect All Layers

```python
# Main Engine Class: Orchestrates all layers

class CR_V4_Engine:
    def __init__(self):
        self.layer1 = KnowledgeGraphEngine()
        self.layer2 = AdaptiveQuestionSelector()
        self.layer3 = SubjectSpecificStrategy()
        self.layer4 = ConceptRevealTiming()
        self.layer5 = WeeklyTestScheduler()
        self.layer6 = CachingEngine()
        self.layer9 = RankProjector()
        self.layer10 = EngagementManager()
        self.layer_burnout = BurnoutDetector()
        
    def get_next_question(self, student):
        """
        Main entry point for student app.
        """
        
        # Layer 1: What should student learn next?
        concept_path = self.layer1.build_learning_path(student)
        next_concept = concept_path[0]
        
        # Layer 3: Apply subject-specific strategy
        strategy = self.layer3.get_strategy(next_concept.subject)
        
        # Layer 2: Select specific question
        question = self.layer2.select_next_question(student, next_concept)
        
        # Layer 4: Check if time to reveal new concept
        self.layer4.check_concept_reveal_timing(student)
        
        # Layer 6: Get from cache if available
        question_full = self.layer6.get_question_cached(question.id)
        
        return question_full
    
    def process_attempt(self, student, attempt_result):
        """
        Student submitted answer.
        Update everything.
        """
        
        # Update mastery (Bayes)
        self.update_mastery(student, attempt_result)
        
        # Check for burnout (Layer 10)
        burnout_signal = self.layer_burnout.analyze_signals(student, attempt_result)
        if burnout_signal.risk_level > 0.7:
            self.layer10.trigger_engagement_intervention(student, burnout_signal)
        
        # Update rank projection (Layer 9)
        self.layer9.update_rank_estimate(student)
        
        # Check if weekly test needed (Layer 5)
        if self.layer5.should_schedule_weekly_test(student):
            student.pending_test = True
        
        # Detect misconceptions
        if attempt_result["correct"] == False:
            self.detect_and_log_misconception(student, attempt_result)
```

---

## PART E: DATABASE SETUP FOR TESTING (WEEK 10-12)

### Create Test Databases

```sql
-- Test Environment: Separate from production

-- Simulation Results Database
CREATE TABLE simulation_results (
    result_id BIGSERIAL PRIMARY KEY,
    simulation_run_id VARCHAR(50),
    student_id VARCHAR(50),  -- SIM_xxx
    day INT,
    questions_attempted INT,
    questions_correct INT,
    accuracy_pct DECIMAL(5,2),
    avg_time_per_question INT,
    motivation_level DECIMAL(3,2),
    burnout_risk DECIMAL(3,2),
    mastery_improvement DECIMAL(3,2),
    rank_estimated INT,
    
    INDEX idx_run (simulation_run_id),
    INDEX idx_student (student_id),
    INDEX idx_day (day)
);

-- Engine Performance Metrics
CREATE TABLE engine_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    engine_version VARCHAR(20),
    test_timestamp TIMESTAMP,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10,2),
    unit VARCHAR(50),
    notes TEXT,
    
    INDEX idx_version (engine_version),
    INDEX idx_timestamp (test_timestamp)
);
```

---

## FINAL SUMMARY: BUILD TIMELINE

```
WEEK 1-2:  FOUNDATION
  ├─ Concepts database (165 concepts)
  ├─ Question metadata database
  ├─ Student mastery model
  └─ Simulation system

WEEK 3:    LAYERS 1-3
  ├─ Knowledge graph engine
  ├─ Adaptive question selector
  └─ Subject-specific strategies

WEEK 4:    LAYERS 4-6
  ├─ Concept reveal timing
  ├─ Weekly test scheduler
  └─ Caching engine

WEEK 5:    LAYERS 7-8
  ├─ Learning optimization
  └─ Burnout detection

WEEK 6:    LAYERS 9-10
  ├─ Rank projection
  └─ Engagement management

WEEK 7-9:  SIMULATION TESTING
  ├─ Run 4 simulation scenarios
  ├─ Collect metrics
  ├─ Identify bugs
  └─ Verify improvements

WEEK 10-12: INTEGRATION & REFINEMENT
  ├─ Connect all layers
  ├─ Debug and fix
  ├─ Performance optimization
  └─ Create test databases

WEEK 13-16: LAUNCH PREP
  ├─ DevOps deployment
  ├─ Frontend integration
  ├─ Real user testing
  └─ Full production launch
```

---

**Status: ✅ READY FOR ENGINEERING TEAM TO BUILD**

**Next: Team starts Week 1 immediately.**

---

**Prepared by:** Chief Technical Architect  
**Date:** December 6, 2025, 7:30 PM IST  
**Classification:** DETAILED ENGINEERING BLUEPRINT