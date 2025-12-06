# CR-V4.0 TECHNICAL STACK & CODE ARCHITECTURE
## Complete Backend Architecture with Technology Choices

**Prepared for:** Engineering Team & CTO  
**Date:** December 6, 2025, 7:45 PM IST  
**Classification:** TECHNICAL SPECIFICATION - IMPLEMENTATION READY

---

## PART A: TECHNOLOGY STACK

### Backend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CR-V4 PLATFORM                       │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  API Layer (FastAPI Python)                             │
│  ├─ /get_next_question                                  │
│  ├─ /submit_answer                                      │
│  ├─ /get_student_progress                               │
│  └─ /admin/* (internal)                                 │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │         CR-V4 ENGINE (Core Logic)                  │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ Layer 1: Knowledge Graph Engine (Python)           │ │
│  │ Layer 2: Adaptive Selector (Python)                │ │
│  │ Layer 3: Subject Strategies (Python)               │ │
│  │ Layer 4: Concept Reveal (Python)                   │ │
│  │ Layer 5: Weekly Tests (Python)                     │ │
│  │ Layer 6: Caching (Redis)                           │ │
│  │ Layer 7: Learning Optimization (Python)           │ │
│  │ Layer 8: Burnout Detection (Python)               │ │
│  │ Layer 9: Rank Projection (Python)                 │ │
│  │ Layer 10: Engagement (Python)                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │         DATA LAYER                                  │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ PostgreSQL (Concepts, Questions, Mastery)         │ │
│  │ Redis (Hot data, session cache)                   │ │
│  │ TimescaleDB (Analytics, burnout trends)           │ │
│  │ CDN (Question diagrams, images)                   │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │         SIMULATION SYSTEM (Testing)                │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ Synthetic Student Generator (Python)              │ │
│  │ Behavior Simulator (Python)                       │ │
│  │ Metrics Collector (Python)                        │ │
│  │ Results Database (PostgreSQL)                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Language & Framework Choices

| Component | Language | Framework | Reason |
|-----------|----------|-----------|--------|
| Engine Core | Python 3.11 | FastAPI | Fast, typed, perfect for ML/AI |
| Database | SQL | PostgreSQL | ACID, reliable, scales |
| Cache Layer | - | Redis | Sub-millisecond queries |
| Analytics | SQL | TimescaleDB | Time-series optimized |
| API | Python | FastAPI | Modern, async, efficient |
| Simulation | Python | Custom | Integrates with engine |
| Testing | Python | pytest | Industry standard |
| DevOps | - | Docker + K8s | Container + orchestration |
| Monitoring | - | Prometheus + Grafana | Production monitoring |

---

## PART B: DATABASE DESIGN (DETAILED SQL)

### 1. Concepts & Knowledge Graph

```sql
-- Core Concepts (Knowledge Nodes)
CREATE TABLE concepts (
    concept_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(20),  -- MATH, PHYSICS, CHEMISTRY
    layer INT,  -- 1-10 (which CR layer)
    difficulty INT,  -- 1-5
    exam_weight DECIMAL(4,3),  -- 0.001-1.0
    
    -- Hierarchical structure
    parent_concept_id VARCHAR(20),
    breadth INT,  -- How broad the concept (1=narrow, 10=broad)
    
    -- Learning metrics
    avg_learning_time_minutes INT,
    avg_study_time_hours INT,
    prerequisite_depth INT,  -- How many prerequisites
    
    -- Metadata
    description TEXT,
    thumbnail_url VARCHAR(500),
    common_mistakes TEXT,
    learning_tips TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_subject (subject),
    INDEX idx_layer (layer),
    FOREIGN KEY (parent_concept_id) REFERENCES concepts(concept_id)
);

-- Prerequisite Relationships
CREATE TABLE concept_prerequisites (
    prerequisite_id BIGSERIAL PRIMARY KEY,
    dependent_concept VARCHAR(20),  -- What needs to be learned
    prerequisite_concept VARCHAR(20),  -- What must come first
    
    -- Relationship properties
    criticality VARCHAR(20),  -- HARD (must know) or SOFT (helpful)
    weight DECIMAL(3,2),  -- 0.5-1.0 (strength)
    transfer_coefficient DECIMAL(3,2),  -- How much learning transfers
    is_gating BOOLEAN,  -- TRUE if absolutely must know first
    
    -- Temporal properties
    min_mastery_required DECIMAL(3,2),  -- 0.7 for HARD, 0.4 for SOFT
    time_before_advance INT,  -- Days to wait before advancing
    
    created_at TIMESTAMP,
    INDEX idx_dependent (dependent_concept),
    UNIQUE (dependent_concept, prerequisite_concept),
    FOREIGN KEY (dependent_concept) REFERENCES concepts(concept_id),
    FOREIGN KEY (prerequisite_concept) REFERENCES concepts(concept_id)
);

-- Knowledge Transfer Matrix
CREATE TABLE knowledge_transfer (
    transfer_id BIGSERIAL PRIMARY KEY,
    source_concept VARCHAR(20),
    target_concept VARCHAR(20),
    
    transfer_type VARCHAR(50),  -- FOUNDATIONAL, REINFORCING, EXTENDING, COMPETING
    transfer_strength DECIMAL(3,2),  -- 0.0-1.0 (how much helps)
    learning_time_reduction DECIMAL(3,2),  -- 0.0-1.0 (20% faster = 0.2)
    
    bidirectional BOOLEAN,  -- Does transfer go both ways?
    
    INDEX idx_source (source_concept),
    INDEX idx_target (target_concept),
    FOREIGN KEY (source_concept) REFERENCES concepts(concept_id),
    FOREIGN KEY (target_concept) REFERENCES concepts(concept_id)
);

-- Misconceptions
CREATE TABLE misconceptions (
    misconception_id BIGSERIAL PRIMARY KEY,
    concept_id VARCHAR(20),
    
    misconception_name VARCHAR(255),
    description TEXT,
    why_students_think TEXT,  -- Psychological basis
    consequence TEXT,  -- What happens if believe this
    
    recovery_strategy TEXT,  -- How to fix
    recovery_difficulty INT,  -- 1-5 (hard to fix)
    
    trigger_questions TEXT,  -- JSON list of Q_IDs
    trigger_probability DECIMAL(3,2),  -- 0.0-1.0
    
    frequency_percent DECIMAL(5,2),  -- How many students have this (%)
    
    INDEX idx_concept (concept_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id)
);
```

### 2. Questions Metadata

```sql
-- Question Metadata (Separate from content DB)
CREATE TABLE questions_metadata (
    question_id VARCHAR(50) PRIMARY KEY,
    subject VARCHAR(20),
    concept_id VARCHAR(20),
    
    -- Question classification
    question_type VARCHAR(20),  -- MCQ, NUMERICAL, INTEGER
    marks INT,  -- 4 or 2
    difficulty_level DECIMAL(3,2),  -- 0.0-1.0
    bloom_level VARCHAR(20),  -- Remember, Understand, Apply, Analyze, Evaluate, Create
    
    -- JEE specifics
    jee_exam_id VARCHAR(20),  -- Which exam it appeared in
    jee_weightage DECIMAL(4,3),  -- How common in JEE
    jee_percentile INT,  -- What percentile of students answer correctly
    
    -- Learning properties
    estimated_time_seconds INT,
    prerequisite_concepts TEXT,  -- JSON list
    related_questions TEXT,  -- JSON list
    
    -- Performance data (after students attempt)
    student_attempts INT DEFAULT 0,
    student_correct INT DEFAULT 0,
    accuracy_rate DECIMAL(5,2),
    discrimination_index DECIMAL(3,2),  -- How well differentiates strong/weak
    difficulty_index DECIMAL(3,2),  -- Actual difficulty from performance
    
    -- Quality
    expert_created_by VARCHAR(50),
    expert_accuracy_rating INT,  -- 1-5
    is_approved BOOLEAN,
    
    -- Misconceptions this question targets
    targeted_misconceptions TEXT,  -- JSON list
    distracter_strategy TEXT,  -- How wrong answers target misconceptions
    
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    INDEX idx_subject (subject),
    INDEX idx_concept (concept_id),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_type (question_type),
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id)
);

-- Question Options (MCQ)
CREATE TABLE question_options (
    option_id BIGSERIAL PRIMARY KEY,
    question_id VARCHAR(50),
    option_letter VARCHAR(1),  -- A, B, C, D
    option_order INT,  -- 1-4
    
    is_correct BOOLEAN,
    misconception_targeted BIGINT,  -- Which misconception this distracter hits
    distracter_reason TEXT,  -- Why this is appealing but wrong
    appeal_percent DECIMAL(5,2),  -- % of students who pick this
    
    FOREIGN KEY (question_id) REFERENCES questions_metadata(question_id),
    FOREIGN KEY (misconception_targeted) REFERENCES misconceptions(misconception_id),
    INDEX idx_question (question_id),
    UNIQUE (question_id, option_letter)
);
```

### 3. Student Mastery State

```sql
-- Student Mastery (Core)
CREATE TABLE student_mastery_state (
    mastery_id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(50),
    concept_id VARCHAR(20),
    
    -- Knowledge estimation
    mastery_level DECIMAL(3,2),  -- 0.0-1.0 (how well student knows concept)
    confidence DECIMAL(3,2),  -- 0.0-1.0 (how sure we are about estimate)
    
    -- Learning metrics
    attempts_total INT DEFAULT 0,
    attempts_correct INT DEFAULT 0,
    learning_speed DECIMAL(3,2),  -- 0.5-1.5x (relative to average)
    
    -- Temporal
    first_attempted TIMESTAMP,
    last_attempted TIMESTAMP,
    days_since_last_attempt INT,
    
    -- Trend
    recent_accuracy DECIMAL(3,2),  -- Last 5 attempts accuracy
    trend VARCHAR(20),  -- improving, stable, declining
    
    -- Prerequisite status
    prerequisites_satisfied BOOLEAN,
    missing_prerequisites TEXT,  -- JSON list of concept_ids
    prerequisite_mastery_min DECIMAL(3,2),  -- Lowest prerequisite mastery
    
    -- Time spent
    total_time_minutes INT DEFAULT 0,
    avg_time_per_attempt INT,  -- seconds
    
    UNIQUE (student_id, concept_id),
    INDEX idx_student (student_id),
    INDEX idx_concept (concept_id),
    INDEX idx_mastery (mastery_level)
);

-- Misconception Status (Per Student)
CREATE TABLE student_misconceptions (
    student_misconception_id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(50),
    misconception_id BIGINT,
    
    -- Misconception state
    misconception_prevalence DECIMAL(3,2),  -- 0.0-1.0 (how strongly held)
    trigger_count INT DEFAULT 0,  -- Times triggered
    recovery_progress DECIMAL(3,2),  -- 0.0-1.0 (towards fixing)
    
    -- Temporal
    first_detected TIMESTAMP,
    last_triggered TIMESTAMP,
    
    is_corrected BOOLEAN DEFAULT FALSE,
    correction_time INT,  -- Seconds spent on recovery
    
    INDEX idx_student (student_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (misconception_id) REFERENCES misconceptions(misconception_id)
);
```

### 4. Student Attempt History

```sql
-- Attempt History (Immutable Log)
CREATE TABLE student_attempts (
    attempt_id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(50),
    question_id VARCHAR(50),
    
    -- Answer info
    submitted_answer VARCHAR(10),  -- A, B, C, D or number
    is_correct BOOLEAN,
    time_taken INT,  -- seconds
    
    -- Session info
    session_id VARCHAR(50),
    day_num INT,  -- Which day of use
    question_num_in_session INT,  -- 1st, 2nd, ... question
    
    -- Student state at time of attempt
    mastery_before DECIMAL(3,2),
    motivation_before DECIMAL(3,2),
    fatigue_before DECIMAL(3,2),
    
    -- Student state after
    mastery_after DECIMAL(3,2),
    misconception_triggered BIGINT,
    
    -- Metadata
    recommended_by_layer VARCHAR(50),  -- Which layer recommended this
    ip_address VARCHAR(50),
    device_type VARCHAR(20),
    
    attempted_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    
    INDEX idx_student (student_id),
    INDEX idx_question (question_id),
    INDEX idx_correct (is_correct),
    INDEX idx_time (attempted_at)
);
```

### 5. Engine State & Decisions

```sql
-- Engine Recommendations Log
CREATE TABLE engine_recommendations (
    recommendation_id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(50),
    
    -- Recommendation
    recommended_concept VARCHAR(20),
    recommended_question_id VARCHAR(50),
    priority_score DECIMAL(5,2),
    
    -- Reasoning
    reason TEXT,  -- Why this was chosen
    layer_responsible VARCHAR(20),  -- Which layer made this decision
    
    -- Candidate alternatives
    alternatives TEXT,  -- JSON list of other options considered
    
    -- Did student accept?
    accepted BOOLEAN,
    if_rejected_chose VARCHAR(50),  -- What they chose instead
    
    created_at TIMESTAMP,
    INDEX idx_student (student_id)
);

-- Burnout Signals
CREATE TABLE burnout_signals (
    signal_id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(50),
    
    -- Signal properties
    signal_type VARCHAR(50),  -- MOTIVATION_DROP, FATIGUE_HIGH, PERFORMANCE_DECLINE, etc.
    severity DECIMAL(3,2),  -- 0.0-1.0
    confidence DECIMAL(3,2),  -- How sure we are
    
    -- Context
    preceding_events TEXT,  -- What led to this signal
    recommendation TEXT,  -- What engine recommended
    
    -- Outcome
    intervention_triggered BOOLEAN,
    intervention_type VARCHAR(50),
    student_response VARCHAR(20),  -- ACCEPTED, IGNORED, DECLINED
    
    detected_at TIMESTAMP,
    resolved_at TIMESTAMP,
    
    INDEX idx_student (student_id),
    INDEX idx_severity (severity)
);
```

---

## PART C: BACKEND CODE STRUCTURE

### Directory Layout

```
/cr-v4-backend/
├── /app/
│   ├── main.py (FastAPI app)
│   ├── config.py (Settings)
│   │
│   ├── /api/
│   │   ├── endpoints.py (API routes)
│   │   └── models.py (Pydantic schemas)
│   │
│   ├── /engine/
│   │   ├── __init__.py
│   │   ├── core.py (Main CR_V4_Engine class)
│   │   │
│   │   ├── /layers/
│   │   │   ├── layer1_knowledge_graph.py
│   │   │   ├── layer2_selector.py
│   │   │   ├── layer3_strategies.py
│   │   │   ├── layer4_concept_reveal.py
│   │   │   ├── layer5_weekly_tests.py
│   │   │   ├── layer6_caching.py
│   │   │   ├── layer7_learning_opt.py
│   │   │   ├── layer8_burnout.py
│   │   │   ├── layer9_rank_projection.py
│   │   │   └── layer10_engagement.py
│   │   │
│   │   └── /algorithms/
│   │       ├── bayes_update.py
│   │       ├── learning_speed.py
│   │       ├── misconception_detection.py
│   │       └── burnout_metrics.py
│   │
│   ├── /database/
│   │   ├── models.py (SQLAlchemy models)
│   │   ├── connection.py (DB connections)
│   │   ├── queries.py (Database functions)
│   │   └── migrations/ (Alembic)
│   │
│   ├── /cache/
│   │   ├── redis_client.py
│   │   └── cache_strategies.py
│   │
│   └── /utils/
│       ├── logging.py
│       ├── errors.py
│       └── validators.py
│
├── /simulation/
│   ├── __init__.py
│   ├── student_generator.py
│   ├── behavior_simulator.py
│   ├── attempt_generator.py
│   ├── harness.py
│   └── metrics_collector.py
│
├── /tests/
│   ├── conftest.py
│   ├── test_layers/
│   ├── test_algorithms/
│   ├── test_simulation/
│   └── test_integration/
│
├── requirements.txt
├── docker/
│   └── Dockerfile
└── README.md
```

---

## PART D: CRITICAL ALGORITHMS (Math & Logic)

### 1. Bayes Update (Mastery Calculation)

```python
# /app/engine/algorithms/bayes_update.py

from dataclasses import dataclass
from typing import Dict
import math

@dataclass
class QuestionAttempt:
    """Student's attempt at a question"""
    correct: bool
    time_taken: int
    question_difficulty: float  # 0.0-1.0
    student_prior_mastery: float  # 0.0-1.0
    question_id: str

def bayes_update_mastery(attempt: QuestionAttempt) -> Dict:
    """
    Bayesian update of student mastery after question attempt.
    
    Mathematical foundation:
    P(M|E) = P(E|M) * P(M) / P(E)
    
    Where:
    - M = student has mastery level
    - E = observed evidence (correct/wrong)
    - P(M|E) = posterior (updated belief)
    
    Returns:
        {
            "new_mastery": float,
            "new_confidence": float,
            "update_magnitude": float,
        }
    """
    
    # Prior: What we believed before
    prior = attempt.student_prior_mastery
    
    # Likelihood: P(Correct | Mastery Level)
    # How likely this outcome given the mastery level?
    
    GUESSING_PROBABILITY = 0.25  # For MCQ with 4 options
    
    if attempt.correct:
        # Student got it right
        # If mastery is high, likely correct (from actual knowledge)
        # If mastery is low, likely correct only by guessing
        
        # P(Correct | Mastery) = Mastery * (1 - guessing) + guessing
        # Because they get right if:
        #   - They know it: mastery * (1 - guess_chance)
        #   - They guess right: guessing_prob
        
        p_event_given_mastery = (
            prior * (1 - GUESSING_PROBABILITY) + GUESSING_PROBABILITY
        )
    else:
        # Student got it wrong
        # P(Wrong | Mastery) = 1 - P(Correct | Mastery)
        p_event_given_mastery = 1 - (
            prior * (1 - GUESSING_PROBABILITY) + GUESSING_PROBABILITY
        )
    
    # Marginal likelihood: P(E) = Integrate over all possible mastery levels
    # Simplified: assume uniform prior distribution of mastery levels
    
    # If attempt is correct:
    #   P(E) = average of P(Correct | M) over all M
    #   = integral_0^1 (M * (1-g) + g) dM
    #   = [(1-g)*0.5 + g]  (average of linear)
    
    if attempt.correct:
        p_event = ((1 - GUESSING_PROBABILITY) * 0.5) + GUESSING_PROBABILITY
    else:
        p_event = 1 - (((1 - GUESSING_PROBABILITY) * 0.5) + GUESSING_PROBABILITY)
    
    # Posterior: Bayes theorem
    posterior = (p_event_given_mastery * prior) / p_event
    
    # Clamp to [0, 1]
    posterior = max(0.0, min(1.0, posterior))
    
    # Update magnitude: How much did we update?
    update_magnitude = abs(posterior - prior)
    
    # Confidence: How sure are we about this estimate?
    # Based on:
    # 1. Consistency (do similar questions have similar results?)
    # 2. Sample size (more attempts = more confident)
    # 3. Discriminative power (does question distinguish well?)
    
    # For now, simple formula:
    # Confidence = 0.5 + (0.5 * confidence_boost)
    # Where confidence_boost depends on consistency
    
    base_confidence = 0.5  # Start with 50%
    confidence_boost = min(1.0, update_magnitude * 2)  # Cap at 1.0
    new_confidence = base_confidence + (confidence_boost * 0.3)
    
    return {
        "new_mastery": posterior,
        "new_confidence": new_confidence,
        "update_magnitude": update_magnitude,
        "direction": "up" if posterior > prior else "down",
    }
```

### 2. Learning Speed Calculation

```python
# /app/engine/algorithms/learning_speed.py

def calculate_learning_speed(question_history: list) -> float:
    """
    How fast does student learn relative to average?
    
    Returns: 0.5 (half speed) to 1.5 (1.5x speed)
    
    Based on:
    1. Time trend: Is time per question decreasing? (learning)
    2. Accuracy trend: Is accuracy improving?  (understanding)
    3. Consistency: Are patterns regular or random?
    """
    
    if len(question_history) < 3:
        return 1.0  # Not enough data
    
    # Look at last 10 attempts
    recent = question_history[-10:]
    
    # 1. Time Analysis
    times = [q["time_taken"] for q in recent]
    accuracy = [1 if q["correct"] else 0 for q in recent]
    
    # Linear regression on times: is it decreasing?
    # time_trend = slope of line fit through times
    time_slope = linear_regression_slope(times)
    
    # time_slope < -5 means each attempt ~5 sec faster
    # This indicates fast learning (getting more comfortable)
    
    if time_slope < -10:
        time_based_speed = 1.4  # Very fast learner
    elif time_slope < -5:
        time_based_speed = 1.2
    elif time_slope < 0:
        time_based_speed = 1.0
    elif time_slope < 5:
        time_based_speed = 0.9
    else:
        time_based_speed = 0.7  # Slow learner
    
    # 2. Accuracy Analysis
    accuracy_slope = linear_regression_slope(accuracy)
    
    if accuracy_slope > 0.05:  # Accuracy improving >5% per attempt
        accuracy_based_speed = 1.3
    elif accuracy_slope > 0:
        accuracy_based_speed = 1.1
    elif accuracy_slope > -0.05:
        accuracy_based_speed = 0.9
    else:
        accuracy_based_speed = 0.7
    
    # 3. Combine
    learning_speed = (time_based_speed + accuracy_based_speed) / 2
    
    # Clamp to [0.5, 1.5]
    learning_speed = max(0.5, min(1.5, learning_speed))
    
    return learning_speed

def linear_regression_slope(values):
    """Simple linear regression to get slope"""
    n = len(values)
    if n < 2:
        return 0
    
    x = list(range(n))
    mean_x = sum(x) / n
    mean_y = sum(values) / n
    
    numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
    
    if denominator == 0:
        return 0
    
    slope = numerator / denominator
    return slope
```

### 3. Burnout Risk Scoring

```python
# /app/engine/algorithms/burnout_metrics.py

def calculate_burnout_risk(student_state) -> float:
    """
    Burnout risk score: 0.0 (no risk) to 1.0 (critical risk)
    
    Based on:
    1. Motivation trend
    2. Fatigue accumulation
    3. Recent failures
    4. Engagement consistency
    5. Time patterns
    """
    
    # Factor 1: Motivation Trend
    motivation_history = student_state["motivation_history"][-7:]  # Last 7 days
    motivation_slope = linear_regression_slope(motivation_history)
    
    if motivation_slope < -0.1:  # Losing motivation fast
        motivation_risk = 0.8
    elif motivation_slope < 0:
        motivation_risk = 0.5
    else:
        motivation_risk = 0.0
    
    # Factor 2: Fatigue Accumulation
    recent_fatigue = student_state["current_fatigue"]  # 0.0-1.0
    
    if recent_fatigue > 0.8:
        fatigue_risk = 0.9
    elif recent_fatigue > 0.6:
        fatigue_risk = 0.6
    else:
        fatigue_risk = 0.2
    
    # Factor 3: Recent Performance
    recent_accuracy = student_state["recent_accuracy"]  # Last 5 questions
    
    if recent_accuracy < 0.3:  # Lots of failures
        performance_risk = 0.7
    elif recent_accuracy < 0.5:
        performance_risk = 0.4
    else:
        performance_risk = 0.1
    
    # Factor 4: Session Consistency
    # Are they showing up consistently?
    sessions_this_week = student_state["sessions_this_week"]
    days_since_last_session = student_state["days_since_last_session"]
    
    if sessions_this_week < 2:  # Only 1-2 sessions
        consistency_risk = 0.7
    elif days_since_last_session > 3:  # Gap in activity
        consistency_risk = 0.5
    else:
        consistency_risk = 0.1
    
    # Factor 5: Time Patterns
    avg_daily_minutes = student_state["avg_daily_minutes"]
    
    if avg_daily_minutes < 15:  # Very light usage
        engagement_risk = 0.6
    elif avg_daily_minutes < 30:
        engagement_risk = 0.3
    else:
        engagement_risk = 0.0
    
    # Combine factors with weights
    burnout_risk = (
        motivation_risk * 0.30 +  # Motivation important
        fatigue_risk * 0.25 +      # Fatigue important
        performance_risk * 0.20 +  # Performance matters
        consistency_risk * 0.15 +  # Consistency matters
        engagement_risk * 0.10     # Engagement matters
    )
    
    # Apply non-linear scaling (burnout accelerates)
    # Once risk > 0.5, it increases faster
    if burnout_risk > 0.5:
        burnout_risk = 0.5 + (burnout_risk - 0.5) ** 1.5
    
    # Clamp to [0, 1]
    burnout_risk = max(0.0, min(1.0, burnout_risk))
    
    return burnout_risk

def predict_burnout_day(student_state) -> int:
    """
    If current trends continue, how many days until burnout?
    
    Returns: days until predicted burnout
    """
    
    motivation_slope = linear_regression_slope(
        student_state["motivation_history"][-7:]
    )
    
    current_motivation = student_state["current_motivation"]
    
    # How many days until motivation hits critical level (0.2)?
    critical_level = 0.2
    
    if motivation_slope >= 0:
        return float('inf')  # Not declining
    
    days_to_critical = (current_motivation - critical_level) / abs(motivation_slope)
    
    return int(max(1, days_to_critical))
```

---

## PART E: INTEGRATION POINTS

### FastAPI Endpoints

```python
# /app/api/endpoints.py

from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI()
engine = CR_V4_Engine()

@app.post("/get_next_question")
async def get_next_question(student_id: str) -> Dict:
    """
    Main endpoint: Get next question for student.
    Calls all layers in sequence.
    """
    
    try:
        # Load student state from database
        student = load_student_state(student_id)
        
        # Call engine
        question = engine.get_next_question(student)
        
        # Return formatted response
        return {
            "question_id": question.id,
            "question_text": question.text,
            "options": question.options,
            "time_limit": question.time_limit,
            "estimated_difficulty": question.difficulty,
        }
    
    except Exception as e:
        logger.error(f"Error getting next question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit_answer")
async def submit_answer(
    student_id: str,
    question_id: str,
    answer: str,
    time_taken: int
) -> Dict:
    """
    Student submitted answer.
    Process it through all layers.
    """
    
    try:
        # Load student
        student = load_student_state(student_id)
        
        # Create attempt object
        attempt = {
            "question_id": question_id,
            "submitted_answer": answer,
            "time_taken": time_taken,
            "timestamp": datetime.now(),
        }
        
        # Verify answer
        question = load_question(question_id)
        is_correct = (answer == question.correct_answer)
        
        # Update student state via engine
        result = engine.process_attempt(student, attempt, is_correct)
        
        # Log attempt
        log_attempt(student_id, question_id, is_correct, time_taken)
        
        # Check for burnout signal
        burnout_signal = engine.check_burnout_signal(student)
        
        return {
            "correct": is_correct,
            "explanation": question.explanation,
            "mastery_update": result["mastery_change"],
            "next_recommended": result["next_question"],
            "burnout_alert": burnout_signal is not None,
        }
    
    except Exception as e:
        logger.error(f"Error processing answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## SUMMARY: TECH STACK

✅ **Backend:** Python 3.11 + FastAPI  
✅ **Database:** PostgreSQL (primary) + Redis (cache) + TimescaleDB (analytics)  
✅ **Algorithms:** Bayesian learning, complex math models  
✅ **Simulation:** Custom Python system for synthetic testing  
✅ **Testing:** pytest for unit + integration tests  
✅ **Deployment:** Docker + Kubernetes  
✅ **Monitoring:** Prometheus + Grafana  

**Next: Team starts coding with this architecture.**

---

**Prepared by:** Chief Technical Architect  
**Date:** December 6, 2025, 7:45 PM IST  
**Status:** ✅ READY FOR IMPLEMENTATION