# CR-V4 Phase 1 Database Seeds (V2)

**Version:** 2.0 - Council Approved Production Ready  
**Status:** ✅ NEP 2020 Compliant

## Files

| File | Contents | Records |
|------|----------|---------|
| `seed_concepts_v2.sql` | 165 JEE concepts (NEP 2020 compliant) | 165 (160 ACTIVE + 5 NEP_REMOVED) |
| `seed_prerequisites_misconceptions_v2.sql` | Prerequisites + Misconceptions | 73 prereqs + 30 misconceptions |

### Legacy Files (V1 - Superseded)
| File | Status |
|------|--------|
| `seed_concepts.sql` | ⚠️ Replaced by V2 |
| `seed_prerequisites_misconceptions.sql` | ⚠️ Replaced by V2 |
| `seed_learning_outcomes.sql` | ℹ️ Reference only |

## Execution Order (V2)

```bash
# 1. Create V2 schema (drops and recreates tables)
psql -f ../migrations/002_phase1_v2_schema.sql

# 2. Load concepts (160 ACTIVE + 5 NEP_REMOVED)
psql -f seed_concepts_v2.sql

# 3. Load prerequisites and misconceptions
psql -f seed_prerequisites_misconceptions_v2.sql

# 4. Verify
psql -c "SELECT syllabus_status, COUNT(*) FROM concepts GROUP BY syllabus_status;"
# Expected: ACTIVE=160, NEP_REMOVED=5
```

## V2 Changes from V1

| Feature | V1 | V2 |
|---------|----|----|
| Schema | concept_id, layer, exam_weight | id, exam_weightage, mastery_time_hours |
| NEP 2020 | ❌ Not supported | ✅ syllabus_status, competency_type |
| IRT | ❌ Not prepared | ✅ irt_a, irt_b, irt_c columns ready |
| Deleted Topics | ❌ None flagged | ✅ 5 NEP_REMOVED |

## NEP_REMOVED Topics (5)

| ID | Topic | Reason |
|----|-------|--------|
| MATH_009 | Mathematical Induction | Removed from NTA 2025 |
| MATH_012 | Mathematical Reasoning | Removed from NTA 2025 |
| PHYS_023 | States of Matter | Reduced in scope |
| CHEM_032 | Surface Chemistry | Reduced in scope |
| CHEM_034 | Polymers & Everyday Chemistry | Removed for rote reduction |

## Competency Distribution (160 ACTIVE)

| Type | Count | Description |
|------|-------|-------------|
| ROTE_MEMORY | ~40 | Direct recall, formula application |
| APPLICATION | ~60 | Standard problem-solving |
| CRITICAL_THINKING | ~60 | Assertion-Reason, multi-step |
