# CR-V4 Cognitive Resonance Backend

## JEE-MAINS AI Coaching Platform - Phase 1 Foundation

**Status:** ✅ Phase 1 Complete  
**Version:** 4.0  
**Date:** December 6, 2025

---

## Overview

CR-V4 is a rules-based adaptive coaching engine for JEE-MAINS that:
- Knows 250 concepts (hand-verified knowledge graph)
- Uses 3 subject-specific strategies (Math, Physics, Chemistry)
- Adapts to 8 different student timelines
- Detects & prevents burnout in real-time
- Generates unique tests per student per week
- Scales to 1M+ users with minimal infrastructure

**NOT ML-based. NOT LLM-based. IS rules-based, JEE-specific, psychologically intelligent.**

---

## Project Structure

```
cr-v4-backend/
├── database/           # PostgreSQL schema and migrations
├── app/
│   ├── engine/        # Core CR-V4 engine
│   │   ├── algorithms/  # Bayesian learning, burnout detection
│   │   └── layers/      # 10 adaptive layers
│   ├── database/      # SQLAlchemy models and queries
│   └── api/           # FastAPI endpoints
├── simulation/        # Synthetic student simulation
├── tests/             # Pytest test suite
├── requirements.txt   # Python dependencies
└── PHASE_1_AUDIT.md   # Implementation audit
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis (for caching)

### Installation

```bash
# Clone repository
cd cr-v4-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
psql -U postgres -c "CREATE DATABASE cr_v4;"
psql -U postgres -d cr_v4 -f database/schema.sql
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific tests
pytest tests/test_algorithms/test_bayesian_learning.py -v

# Run with coverage
pytest tests/ -v --cov=app
```

---

## Phase 1 Deliverables

### ✅ Completed

1. **Database Schema** (`database/schema.sql`)
   - 7 core tables
   - 38 optimized indexes
   - Complete constraints and validation

2. **Bayesian Learning Algorithm** (`app/engine/algorithms/bayesian_learning.py`)
   - Mastery estimation via Bayes theorem
   - Confidence calculation
   - 100% test coverage

3. **Test Suite** (`tests/test_algorithms/test_bayesian_learning.py`)
   - 20+ test cases
   - Performance validation
   - Edge case handling

---

## Next Phases

- **Phase 2 (Weeks 3-6):** Core Engine Layers 1-10
- **Phase 3 (Weeks 7-9):** Simulation Testing
- **Phase 4 (Weeks 10-12):** Integration & Refinement
- **Phase 5 (Weeks 13-16):** Launch Preparation

---

## Team

- **Chief Architect:** CR-V4 Technical Council
- **Target Launch:** May 2026 (MVP)
- **Target Users:** 10,000+ students

---

## License

Proprietary - Confidential
