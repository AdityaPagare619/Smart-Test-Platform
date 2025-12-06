# CR-V4.0 SYSTEM ARCHITECTURE DIAGRAM
## Visual Reference for Building

**Date:** December 6, 2025  
**Purpose:** Quick visual understanding of how everything connects

---

## COMPLETE SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CR-V4 PLATFORM                                 │
│                     (Cognitive Resonance Engine)                        │
└─────────────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  Mobile App / Web Browser                                               │
│  ├─ /get_next_question  → Get personalized question                    │
│  ├─ /submit_answer      → Submit student response                      │
│  ├─ /get_progress       → View student progress                        │
│  └─ /get_recommendation → Next action recommendation                   │
└─────────────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                        API LAYER (FastAPI)                              │
├─────────────────────────────────────────────────────────────────────────┤
│  Endpoints & Request/Response Handling                                  │
│  ├─ Input Validation                                                    │
│  ├─ Auth & Authorization                                                │
│  ├─ Response Formatting                                                 │
│  └─ Error Handling                                                      │
└─────────────────────────────────────────────────────────────────────────┘

                              ▼

┌────────────────────────────────────────────────────────────────────────────┐
│                      CR-V4 ENGINE (CORE LOGIC)                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 1: Knowledge Graph Engine                                     │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Load prerequisite graph                                           │ │
│  │ • Build learning path                                              │ │
│  │ • Check prerequisites satisfied                                    │ │
│  │ • Recommend next concept                                           │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 2: Adaptive Question Selector                                │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Calculate ideal difficulty (mastery + 0.15)                      │ │
│  │ • Find questions targeting student misconceptions                  │ │
│  │ • Rank by discrimination index                                     │ │
│  │ • Weight by recency                                                │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 3: Subject Strategies                                         │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ Math: Sequential-mandatory (must follow prerequisites)              │ │
│  │ Physics: High-yield selective (prioritize exam weightage)           │ │
│  │ Chemistry: Breadth with foundation (foundation first)               │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 4: Concept Reveal                                             │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Progressive difficulty increase                                   │ │
│  │ • Unlock concept components gradually                               │ │
│  │ • Show related concepts                                             │ │
│  │ • Suggest prerequisites                                             │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 5: Weekly Tests                                               │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Comprehensive weekly assessment                                   │ │
│  │ • Mixed difficulty (review + challenge)                             │ │
│  │ • Mock exam format                                                  │ │
│  │ • Generate performance report                                       │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 6: Caching Layer                                              │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Hot data in Redis (frequently accessed concepts)                  │ │
│  │ • Student session state                                             │ │
│  │ • Question metadata cache                                           │ │
│  │ • LRU eviction policy                                               │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 7: Learning Optimization                                      │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Spaced repetition scheduling                                      │ │
│  │ • Active recall practice                                            │ │
│  │ • Interleaving similar concepts                                     │ │
│  │ • Vary question types                                               │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 8: Burnout Detection                                          │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Monitor motivation trend                                          │ │
│  │ • Track fatigue accumulation                                        │ │
│  │ • Detect performance decline                                        │ │
│  │ • Trigger interventions (breaks, encouragement, easier questions)   │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 9: Rank Projection                                            │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Estimate current JEE rank                                         │ │
│  │ • Project final rank based on trajectory                            │ │
│  │ • Identify weak areas needing work                                  │ │
│  │ • Goal-based recommendations                                        │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 10: Engagement & Motivation                                   │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ • Gamification (streaks, achievements, badges)                      │ │
│  │ • Peer comparisons (anonymized)                                     │ │
│  │ • Motivational notifications                                        │ │
│  │ • Celebrate milestones                                              │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

                              ▼

┌────────────────────────────────────────────────────────────────────────────┐
│                    ALGORITHMS & COMPUTATION                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────┐  ┌──────────────────────────┐              │
│  │  BAYES UPDATE            │  │  LEARNING SPEED          │              │
│  ├──────────────────────────┤  ├──────────────────────────┤              │
│  │ P(M|E) = P(E|M)×P(M)     │  │ Speed = (TimeTrend +     │              │
│  │          ─────────────   │  │          AccuracyTrend) │              │
│  │           P(E)           │  │         / 2              │              │
│  │                          │  │                          │              │
│  │ Updates mastery after    │  │ Identifies fast/slow     │              │
│  │ each attempt             │  │ learners (0.5x to 1.5x)  │              │
│  └──────────────────────────┘  └──────────────────────────┘              │
│                                                                            │
│  ┌──────────────────────────┐  ┌──────────────────────────┐              │
│  │  BURNOUT RISK SCORING    │  │  MISCONCEPTION           │              │
│  ├──────────────────────────┤  ├──────────────────────────┤              │
│  │ Risk = Σ(Motivation×0.3  │  │ Detection when student   │              │
│  │        + Fatigue×0.25    │  │ answers incorrectly in   │              │
│  │        + ...)            │  │ specific pattern         │              │
│  │                          │  │                          │              │
│  │ Predicts burnout days    │  │ Triggers targeted        │              │
│  │ in advance               │  │ correction questions     │              │
│  └──────────────────────────┘  └──────────────────────────┘              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

                              ▼

┌────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌────────────────────────────┐  ┌────────────────────────────┐          │
│  │ POSTGRESQL (Main DB)       │  │ REDIS (Cache Layer)        │          │
│  ├────────────────────────────┤  ├────────────────────────────┤          │
│  │ • concepts (165)           │  │ • Hot concepts             │          │
│  │ • prerequisites (200+)     │  │ • Student sessions         │          │
│  │ • misconceptions (300+)    │  │ • Question metadata        │          │
│  │ • mastery_state            │  │ • Ranking cache            │          │
│  │ • misconceptions_active    │  │ • LRU eviction             │          │
│  │ • attempts (immutable log) │  │ • <10ms access time        │          │
│  │ • recommendations          │  │                            │          │
│  │                            │  │                            │          │
│  │ Queries: <50ms (avg)       │  │ Hit rate: >85%             │          │
│  │ Indexes: 20+               │  │ Memory: <1GB per 1000 users│          │
│  └────────────────────────────┘  └────────────────────────────┘          │
│                                                                            │
│  ┌────────────────────────────┐                                          │
│  │ TIMESCALEDB (Analytics)    │                                          │
│  ├────────────────────────────┤                                          │
│  │ • Performance trends       │                                          │
│  │ • Burnout patterns         │                                          │
│  │ • Engagement metrics       │                                          │
│  │ • Auto-compress after 365 days                                       │
│  │ • Analytical queries only  │                                          │
│  └────────────────────────────┘                                          │
│                                                                            │
│  ┌────────────────────────────┐                                          │
│  │ CDN (Image Delivery)       │                                          │
│  ├────────────────────────────┤                                          │
│  │ • Question diagrams        │                                          │
│  │ • WebP optimized           │                                          │
│  │ • LQI preview              │                                          │
│  │ • Global distribution      │                                          │
│  └────────────────────────────┘                                          │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## DATA FLOW (Question Delivery)

```
Student Opens App
     ▼
GET /get_next_question (student_id)
     ▼
┌──────────────────────────────────────┐
│ CR-V4 ENGINE PROCESSING              │
├──────────────────────────────────────┤
│ 1. Load student from DB              │
│    (mastery for all concepts)        │
│                                      │
│ 2. Layer 1: Build learning path      │
│    (respects prerequisites)          │
│                                      │
│ 3. Layer 2: Select question          │
│    (right difficulty + misconception)│
│                                      │
│ 4. Layer 3: Apply subject strategy   │
│    (Math strict, Physics high-yield) │
│                                      │
│ 5. Layer 6: Check cache              │
│    (use Redis if available)          │
│                                      │
│ 6. Fetch from DB if needed           │
│    (question metadata + options)     │
│                                      │
│ 7. Log recommendation (Layer 9 info) │
│                                      │
│ 8. Format response                   │
└──────────────────────────────────────┘
     ▼
Return JSON:
{
  "question_id": "Q_12345",
  "concept_id": "MATH_041",
  "text": "Find derivative of...",
  "options": ["A", "B", "C", "D"],
  "time_limit": 120,
  "difficulty": 0.65,
  "ranked_estimate": 450,
  "motivation_level": 0.8,
  "burnout_risk": 0.2
}
     ▼
Student Attempts Question
     ▼
POST /submit_answer
├─ question_id
├─ submitted_answer: "C"
├─ time_taken: 95 seconds
└─ timestamp
     ▼
┌──────────────────────────────────────┐
│ CR-V4 PROCESSING ANSWER              │
├──────────────────────────────────────┤
│ 1. Check if correct (compare DB)     │
│                                      │
│ 2. Log attempt to database           │
│    (immutable record)                │
│                                      │
│ 3. Bayes update mastery              │
│    (new_mastery = P(M|E))            │
│                                      │
│ 4. Check misconceptions              │
│    (did they make typical error?)    │
│                                      │
│ 5. Update learning speed             │
│    (faster or slower than average?)  │
│                                      │
│ 6. Calculate burnout risk            │
│    (any warning signs?)              │
│                                      │
│ 7. Generate next recommendation      │
│    (which question next?)            │
│                                      │
│ 8. Save updated state to DB + cache  │
└──────────────────────────────────────┘
     ▼
Return JSON:
{
  "correct": true,
  "explanation": "The derivative is...",
  "mastery_before": 0.58,
  "mastery_after": 0.63,
  "mastery_change": "+5%",
  "next_concept": "MATH_042",
  "next_difficulty": 0.68,
  "burnout_alert": false,
  "engagement_bonus": "+10 points"
}
```

---

## LAYER DEPENDENCY GRAPH

```
                    Layer 1 (Knowledge Graph)
                            ▲
                    ┌───────┴───────┐
                    │               │
            Layer 2 (Selector)   Layer 3 (Strategies)
                    │               │
                    └───────┬───────┘
                            ▼
        Layer 4 (Concept Reveal) + Layer 5 (Tests)
                    │               │
                    └───────┬───────┘
                            ▼
        Layer 6 (Caching) ← Optimization required
                            ▼
        Layer 7 (Learning Opt) + Layer 8 (Burnout)
                    │               │
                    └───────┬───────┘
                            ▼
        Layer 9 (Rank) + Layer 10 (Engagement)
```

**Note:** Layers can be built in parallel, but dependency respect required for integration.

---

## SIMULATION FLOW

```
SIMULATION HARNESS
     ▼
Create 100 Synthetic Students
├─ 25 High Achievers
├─ 50 Average Students
├─ 20 Struggling Students
└─ 5 Burnout Risk
     ▼
FOR EACH DAY (30-60 days):
     ▼
FOR EACH STUDENT:
     ▼
  FOR 20 QUESTIONS:
     ▼
    1. Get next question from engine
    2. Simulate attempt (Bayes model)
    3. Process answer through engine
    4. Record metrics
    ▼
     Collect Daily Metrics:
     ├─ Average mastery improvement
     ├─ Accuracy by student type
     ├─ Burnout detection rate
     ├─ Engagement trends
     └─ No errors/data loss
     ▼
END SIMULATION
     ▼
Validate Results:
├─ High achievers: >30% improvement ✅
├─ Average: 15-25% improvement ✅
├─ Struggling: 5-15% improvement ✅
├─ Burnout detected: >70% ✅
└─ Database integrity: 100% ✅
```

---

## DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ FastAPI Pods (3) │  │ Worker Pods (2)  │           │
│  │ ├─ Replica 1     │  │ ├─ Worker 1      │           │
│  │ ├─ Replica 2     │  │ └─ Worker 2      │           │
│  │ └─ Replica 3     │  │ (Batch jobs)     │           │
│  └──────────────────┘  └──────────────────┘           │
│                                                         │
│  Load Balancer (Nginx)                                │
│  ├─ /get_next_question → FastAPI Pods               │
│  ├─ /submit_answer → FastAPI Pods                   │
│  └─ Health checks → All pods                        │
│                                                         │
└─────────────────────────────────────────────────────────┘

Attached Services:
├─ PostgreSQL (RDS)
├─ Redis (Elasticache)
├─ TimescaleDB (Cloud SQL)
└─ CDN (CloudFront/Cloudflare)

Monitoring:
├─ Prometheus (metrics)
├─ Grafana (dashboards)
├─ ELK Stack (logs)
└─ PagerDuty (alerts)
```

---

## STUDENT MASTERY STATE EXAMPLE

```
Student: Aditya (top achiever)

MATH Concepts:
├─ Number Systems (001)        → 0.95 ✅ (mastered)
├─ Algebra Basics (002)        → 0.88 ✓ (strong)
├─ Functions (010)             → 0.75 ○ (learning)
├─ Derivatives (041)           → 0.62 ○ (in progress)
├─ Integration (043)           → 0.10 ✗ (not started)
└─ Matrices (015)              → 0.00 ✗ (not yet)

Misconceptions Active:
├─ Derivative as slope (MIS_DERIV_001)  → 0.3 (partially held)
└─ Integration by substitution (MIS_INT_002) → 0.0 (none detected)

Learning Metrics:
├─ Learning speed: 1.2x (20% faster than average)
├─ Recent accuracy: 0.85 (last 5 questions)
├─ Motivation: 0.9 (high)
├─ Fatigue: 0.1 (low)
├─ Burnout risk: 0.05 (very low)
└─ Projected rank: 350 (goal: 200)

Next Recommendation:
├─ Continue Derivatives (current focus)
├─ Move to Integration next week
├─ Revisit Algebra if struggling
└─ Mock test scheduled: Friday
```

---

**This diagram system shows how CR-V4.0 works end-to-end.**

**Refer to this when building to verify connections and data flow.**

---

**Prepared by:** Chief Technical Architect  
**Date:** December 6, 2025  
**Status:** ✅ REFERENCE COMPLETE