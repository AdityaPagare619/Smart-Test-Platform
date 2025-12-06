# CR-V4 Database

## Overview
This directory contains the database schema and migrations for the CR-V4 Cognitive Resonance platform.

## Files

### schema.sql
Production-ready PostgreSQL schema with:
- 7 core tables
- 38 optimized indexes
- Complete data validation constraints
- ACID-compliant design
- 3NF normalized structure

## Tables

1. **concepts** - 165 JEE-MAINS concepts with metadata
2. **concept_prerequisites** - 200+ prerequisite relationships
3. **misconceptions** - 300+ common student misconceptions
4. **student_mastery_state** - Bayesian mastery estimation per student
5. **student_misconceptions** - Misconception tracking per student
6. **student_attempts** - Immutable log of all attempts
7. **engine_recommendations** - Recommendation engine decision log

## Usage

```bash
# Create database
psql -U postgres -c "CREATE DATABASE cr_v4;"

# Apply schema
psql -U postgres -d cr_v4 -f schema.sql
```

## Performance Targets

- Query latency: <50ms (99th percentile)
- Write throughput: 1000+ inserts/second
- Index efficiency: 38 optimized indexes
- Scalability: Tested for 1M+ records
