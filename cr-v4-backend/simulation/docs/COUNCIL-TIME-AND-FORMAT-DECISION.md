# Council Deliberation: Simulation Time Isolation & Data Format

**Date**: December 12, 2024  
**Status**: URGENT - Critical Issues Identified  

---

## Issue 1: Simulation Time Isolation

### Problem Statement
The simulation currently uses `date.today()` and real-world time references in several places, causing the simulation to fail or behave incorrectly when the exam date is in the "past" relative to real-world time.

### Council Decision ✅
**APPROVED**: Implement complete time isolation:
1. Remove ALL `date.today()` from business logic
2. Pass `sim_date` as parameter to all time-dependent methods
3. Only use real time for logging/performance metrics
4. Simulation should work for ANY date range (past, present, future)

---

## Issue 2: JSON vs Parquet/TOON Data Format

### Problem Statement
JSON files become extremely large (50-100MB for 178K interactions). Parquet = 5-10MB with 10x faster read/write.

### Council Decision ✅
**APPROVED**: Mandate Parquet format:
1. Add `pyarrow` to requirements.txt as REQUIRED dependency
2. Remove JSON fallback for production data
3. Use Snappy compression by default

---

**APPROVED BY USER** ✅ - Proceeding to Implementation
