# CR-V4.0 QUICK REFERENCE CARD
## Print This & Keep On Your Desk

**Date:** December 6, 2025  
**Status:** READY TO EXECUTE

---

## THE 16-WEEK PLAN IN ONE PAGE

```
WEEK 1-2: FOUNDATION
├─ Database: PostgreSQL, 7 tables, 20+ indexes
├─ Data: 165 concepts, 200+ prerequisites, 300+ misconceptions
├─ Algorithms: Bayes update, Learning speed, Burnout scoring
├─ Simulation: 4 student types, attempt generation
└─ DELIVER BY: Friday EOD, Week 2

WEEK 3-6: ENGINE LAYERS 1-10
├─ Layer 1: Knowledge Graph
├─ Layer 2: Adaptive Selector
├─ Layer 3: Subject Strategies
├─ Layer 4: Concept Reveal
├─ Layer 5: Weekly Tests
├─ Layer 6: Caching
├─ Layer 7: Learning Optimization
├─ Layer 8: Burnout Detection
├─ Layer 9: Rank Projection
├─ Layer 10: Engagement
└─ DELIVER BY: Friday EOD, Week 6

WEEK 7-9: SIMULATION TESTING
├─ 100 synthetic students
├─ 30-60 day simulations
├─ Metrics collection
├─ Bug fixing
└─ DELIVER BY: Friday EOD, Week 9

WEEK 10-12: LAUNCH PREP
├─ DevOps/Infrastructure
├─ Admin dashboard
├─ Documentation
├─ Team training
└─ DELIVER BY: Friday EOD, Week 12

WEEK 13-16: PRODUCTION READY
├─ Real data pipeline
├─ Expert templates
├─ Security audit
└─ GO LIVE
```

---

## TECHNOLOGY STACK

```
Language:     Python 3.11
Framework:    FastAPI
Database:     PostgreSQL (primary) + Redis (cache) + TimescaleDB (analytics)
Frontend API: REST JSON
Testing:      pytest + TDD
Deployment:   Docker + Kubernetes
Monitoring:   Prometheus + Grafana
```

---

## DATABASE TABLES (7 CORE)

1. **concepts** - 165 JEE concepts with metadata
2. **concept_prerequisites** - 200+ prerequisite relationships
3. **knowledge_transfer** - How concepts help each other
4. **misconceptions** - 300+ student misconceptions
5. **student_mastery_state** - Student progress (Bayesian model)
6. **student_misconceptions** - Which misconceptions each student has
7. **student_attempts** - Log of all question attempts

---

## CRITICAL ALGORITHMS

```
1. BAYES UPDATE
   New Mastery = (P(Correct|Mastery) × Prior) / P(Event)
   
2. LEARNING SPEED
   Speed = (Time Trend + Accuracy Trend) / 2
   Range: 0.5x (slow) to 1.5x (fast)
   
3. BURNOUT RISK
   Risk = Σ(Motivation × 0.3 + Fatigue × 0.25 + ...)
   Range: 0.0 (no risk) to 1.0 (critical)
```

---

## API ENDPOINTS (MINIMUM)

```
POST /get_next_question
├─ Input: student_id
└─ Output: question with all metadata

POST /submit_answer
├─ Input: student_id, question_id, answer, time_taken
└─ Output: correct/wrong, explanation, next action

GET /student_progress
├─ Input: student_id
└─ Output: mastery, rank, timeline
```

---

## TEAM STRUCTURE (7-15 PEOPLE)

```
CTO (1)
├─ Database Lead (1) → DB Ops Eng (1)
├─ Backend Engineer 1 (1) → Algorithms Eng (1)
├─ Backend Engineer 2 (1) → Burnout Specialist (1)
├─ API Developer (1)
├─ DevOps Engineer (1)
├─ QA/Testing (1-2)
├─ Content Manager (1)
└─ Project Manager (1)
```

---

## SUCCESS METRICS (WEEK 12)

```
Code Quality:
✅ 85%+ test coverage
✅ <200ms API response
✅ <50ms database query
✅ 1000 req/sec throughput

Simulation:
✅ High achievers: >30% improvement
✅ Average students: 15-25% improvement
✅ Struggling students: 5-15% improvement
✅ Burnout detected in >70% of at-risk
✅ Intervention success >60%

Operations:
✅ 0 critical bugs
✅ 100% on-time delivery
✅ Production ready
```

---

## RED FLAGS (STOP & FIX)

```
WEEK 1-2:
🚩 DB schema incomplete → STOP
🚩 Tests not written → REVERT
🚩 >10% test coverage gap → STOP
🚩 Algorithms not validated → HALT

WEEK 3-6:
🚩 API >500ms → OPTIMIZE
🚩 Queries >100ms → ADD INDEXES
🚩 Layers not integrating → SYNC
🚩 Layer tests failing → DEBUG

WEEK 7-9:
🚩 Wrong simulation results → DEBUG ENGINE
🚩 High achievers not improving → ALGORITHM BUG
🚩 Burnout not detected → REVIEW LAYER 8
🚩 Data loss → CHECK DATABASE

WEEK 10-12:
🚩 Deployment issues → DEVOPS SUPPORT
🚩 Security audit fails → FIX IMMEDIATELY
🚩 Performance degrades → PROFILE & OPTIMIZE
```

---

## DELIVERABLES CHECKLIST

```
WEEK 1-2:
✅ PostgreSQL instance running
✅ 165 concepts loaded
✅ 200+ prerequisites mapped
✅ 300+ misconceptions loaded
✅ Bayes algorithm: 100% tests pass
✅ Learning speed: 100% tests pass
✅ Burnout scoring: 100% tests pass
✅ 4 student types created
✅ Attempt simulator working
✅ Simulation harness ready
✅ 85%+ test coverage

WEEK 3-6:
✅ Layer 1: All tests pass
✅ Layer 2: All tests pass
✅ ...
✅ Layer 10: All tests pass
✅ All layers integrate
✅ API endpoints working

WEEK 7-9:
✅ 100 synthetic students ready
✅ 30-day simulation complete
✅ Metrics collected
✅ Bugs found & fixed
✅ Engine validated

WEEK 10-12:
✅ Production infrastructure ready
✅ All monitoring running
✅ Documentation complete
✅ Team trained
✅ Security audit passed
✅ GO LIVE READY
```

---

## BUDGET QUICK MATH

```
Engineering Salaries (12 weeks):       ₹21L
Infrastructure & Tools:                ₹2.5L
Contingency (15%):                     ₹3.5L
─────────────────────────────────────
Total: ₹27L (₹25-30L range)

Monthly Ongoing (after launch):        ₹6.5L/month
```

---

## COMMUNICATION CADENCE

```
Daily:       Standup (15 min, 10:30 AM)
Weekly:      Tech sync (1 hour, Monday 4 PM)
Bi-weekly:   Sprint review (1 hour, Friday 5 PM)
Monthly:     Architecture review (2 hours)
```

---

## PRIORITY ORDER (NEVER CHANGE)

```
1️⃣ Database foundation
   └─ Everything depends on this

2️⃣ Core algorithms (Bayes, Learning Speed, Burnout)
   └─ Engine depends on this

3️⃣ Layers 1-3 (Knowledge, Selection, Strategies)
   └─ Other layers depend on this

4️⃣ Layers 4-6 (Assessment, Caching)
   └─ Needed for simulation

5️⃣ Layers 7-10 (Optimization, Engagement)
   └─ Advanced features

6️⃣ Simulation testing
   └─ Validates everything

7️⃣ DevOps & Deployment
   └─ Only after testing complete
```

---

## COMMON MISTAKES (AVOID THESE)

❌ Skipping tests (write tests first!)  
❌ Rushing database setup (do it perfectly)  
❌ Not validating algorithms early (test math)  
❌ Building layers in wrong order  
❌ Missing edge cases in simulation  
❌ Not running load tests  
❌ Deploying before simulation validation  
❌ Ignoring performance warnings  

---

## QUESTIONS? REFER TO:

**What to build?**  
→ CR-V4-Engine-Build-Plan.md

**How to build it?**  
→ CR-V4-Technical-Stack-Architecture.md

**Week-by-week code?**  
→ CR-V4-Engineering-Sprint-Breakdown.md

**Team/process?**  
→ CR-V4-Production-Charter.md

**Executive summary?**  
→ CR-V4-Build-Plan-Summary.md

**Quick reference?**  
→ This file!

---

## THE ONE SENTENCE SUMMARY

**Build a 10-layer adaptive learning engine that uses Bayesian mastery estimation, misconception detection, and burnout prevention to personalize JEE preparation for 100K+ students.**

---

## START DATE

📅 **Monday, December 9, 2025**  
🚀 **Ready to execute**  
✅ **All specifications complete**  
🎯 **16 weeks to production**

---

**Print this card. Put it on your desk. Reference it daily.**

**Questions? Check the full documents.**

**Ready? Let's build.**

---

**Issued:** December 6, 2025, 8:45 PM IST  
**Status:** ✅ READY FOR IMMEDIATE EXECUTION