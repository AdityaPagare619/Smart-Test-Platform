# 🚀 RANKAK AI ENGINE

> **Intelligent Adaptive Learning System for JEE Preparation**

---

## What is RANKAK?

RANKAK is the AI-powered adaptive learning engine that powers the CR-V4 Smart Exams Platform. Named to reflect its mission of helping students improve their **RANK** through intelligent learning pathways.

## Core Features

### 🧠 10-Layer Intelligence Architecture

| Layer | Module | Function |
|-------|--------|----------|
| L1 | Knowledge Graph | 165 JEE concepts with prerequisites |
| L2 | Subject Strategy | MATH/PHYS/CHEM specific rules |
| L3 | Academic Calendar | 8 student lifecycle phases |
| L4 | Concept Reveal | Progressive content visibility |
| L5 | DKT Engine | Deep Knowledge Tracing with 3 time scales |
| L6 | Question Selector | IRT + Fisher Information scoring |
| L7 | Root Cause | BFS prerequisite gap analysis |
| L8 | Percentile Map | Score → Rank prediction |
| L9 | Engagement | Dropout prevention system |
| L10 | Psychology | Burnout & anxiety detection |

### 🎯 Key Capabilities

- **3PL-IRT Model**: Psychometrically accurate question difficulty matching
- **Trust-Based Learning**: Adaptive recommendations that build student confidence
- **Standard-Wise Filtering**: Ensures 11th grade students never see 12th grade content
- **Exam-Bound Logic**: All learning paths aligned to JEE exam dates

## Simulation System

RANKAK includes a High-Fidelity User Simulation System (HF-USS) for testing:

```bash
# Run simulation with 1000 agents
python -m simulation.main --agents 1000 --turbo --exam-date 2026-01-20

# Run adversarial testing
python -m simulation.main --agents 100 --turbo --adversarial

# Generate per-persona analytics
python -m simulation.analyze_personas
```

### 8 Student Personas Simulated

1. **Struggling Persister** - High grit, lower aptitude
2. **Anxious Perfectionist** - High ability, high anxiety
3. **Disengaged Gamer** - Low engagement, high guessing
4. **Conceptually Gapped** - Missing prerequisites
5. **Steady Learner** - Baseline behavior
6. **Fast Tracker** - High aptitude, fast progress
7. **Late Joiner** - Crisis mode (30 days to exam)
8. **Dropper** - 2nd attempt, high stakes

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| 1.0 | Dec 12, 2024 | Core AI Engine + Simulation Complete |

## Technology Stack

- **Backend**: Python 3.8+, FastAPI
- **Database**: PostgreSQL, Redis
- **ML Models**: PyTorch (DKT), SciPy (IRT)
- **Data Storage**: Apache Parquet (10x compression)
- **Testing**: pytest, 1000-agent simulation

---

*Built with ❤️ by the CR-V4 Team*
