-- CR-V4 SCHEMA MIGRATION: Phase 1 V2 Production Schema
-- Migration: 002_phase1_v2_schema.sql
-- Created: December 8, 2025 (Updated for V2)
-- Purpose: Production-ready schema for V2 concepts with NEP 2020 compliance

-- ============================================================================
-- STEP 1: DROP OLD MIGRATION IF EXISTS (Clean slate)
-- ============================================================================

-- Note: This replaces the previous 002_add_seed_columns.sql

-- ============================================================================
-- STEP 2: CONCEPTS TABLE - V2 PRODUCTION SCHEMA
-- ============================================================================

-- Drop and recreate concepts table with V2 schema
DROP TABLE IF EXISTS concepts CASCADE;

CREATE TABLE concepts (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(20) NOT NULL CHECK (subject IN ('MATHEMATICS', 'PHYSICS', 'CHEMISTRY')),
    difficulty DECIMAL(3,2) NOT NULL CHECK (difficulty BETWEEN 0.0 AND 1.0),
    mastery_time_hours DECIMAL(4,1) NOT NULL CHECK (mastery_time_hours > 0),
    exam_weightage DECIMAL(4,1) NOT NULL CHECK (exam_weightage >= 0.0),
    nta_frequency_score INT NOT NULL CHECK (nta_frequency_score BETWEEN 0 AND 10),
    syllabus_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (syllabus_status IN ('ACTIVE', 'LEGACY', 'NEP_REMOVED')),
    competency_type VARCHAR(20) CHECK (competency_type IS NULL OR competency_type IN ('ROTE_MEMORY', 'APPLICATION', 'CRITICAL_THINKING')),
    nep_verified BOOLEAN DEFAULT TRUE,
    
    -- IRT Parameters (Phase 2 Calibration)
    irt_a FLOAT DEFAULT NULL,  -- Discrimination
    irt_b FLOAT DEFAULT NULL,  -- Difficulty
    irt_c FLOAT DEFAULT NULL,  -- Guessing
    irt_calibrated_date TIMESTAMP DEFAULT NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for V2
CREATE INDEX idx_concepts_subject ON concepts(subject);
CREATE INDEX idx_concepts_difficulty ON concepts(difficulty);
CREATE INDEX idx_concepts_syllabus_status ON concepts(syllabus_status);
CREATE INDEX idx_concepts_competency_type ON concepts(competency_type);
CREATE INDEX idx_concepts_nta_frequency ON concepts(nta_frequency_score DESC);
CREATE INDEX idx_concepts_nep_verified ON concepts(nep_verified);
CREATE INDEX idx_concepts_exam_weightage ON concepts(exam_weightage DESC);

-- ============================================================================
-- STEP 3: PREREQUISITES TABLE - V2 PRODUCTION SCHEMA
-- ============================================================================

DROP TABLE IF EXISTS prerequisites CASCADE;

CREATE TABLE prerequisites (
    id BIGSERIAL PRIMARY KEY,
    dependent_concept_id VARCHAR(20) NOT NULL,
    prerequisite_concept_id VARCHAR(20) NOT NULL,
    strength DECIMAL(3,2) NOT NULL CHECK (strength BETWEEN 0.0 AND 1.0),
    transfer_learning_weight DECIMAL(3,2) NOT NULL CHECK (transfer_learning_weight BETWEEN 0.0 AND 1.0),
    is_hard_dependency BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_dependent FOREIGN KEY (dependent_concept_id) REFERENCES concepts(id),
    CONSTRAINT fk_prerequisite FOREIGN KEY (prerequisite_concept_id) REFERENCES concepts(id),
    CONSTRAINT unique_prereq_pair UNIQUE (dependent_concept_id, prerequisite_concept_id),
    CONSTRAINT no_self_prereq CHECK (dependent_concept_id != prerequisite_concept_id)
);

-- Indexes
CREATE INDEX idx_prereq_dependent ON prerequisites(dependent_concept_id);
CREATE INDEX idx_prereq_prerequisite ON prerequisites(prerequisite_concept_id);
CREATE INDEX idx_prereq_strength ON prerequisites(strength DESC);
CREATE INDEX idx_prereq_hard ON prerequisites(is_hard_dependency);

-- ============================================================================
-- STEP 4: MISCONCEPTIONS TABLE - V2 PRODUCTION SCHEMA
-- ============================================================================

DROP TABLE IF EXISTS misconceptions CASCADE;

CREATE TABLE misconceptions (
    id BIGSERIAL PRIMARY KEY,
    concept_id VARCHAR(20) NOT NULL,
    misconception_text TEXT NOT NULL,
    correction TEXT NOT NULL,
    recovery_strategy TEXT NOT NULL,
    diagnostic_question TEXT NOT NULL,
    severity_level VARCHAR(10) NOT NULL CHECK (severity_level IN ('LOW', 'MEDIUM', 'HIGH')),
    common_exam_trap BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT fk_misconception_concept FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

-- Indexes
CREATE INDEX idx_misconceptions_concept ON misconceptions(concept_id);
CREATE INDEX idx_misconceptions_severity ON misconceptions(severity_level);
CREATE INDEX idx_misconceptions_exam_trap ON misconceptions(common_exam_trap);

-- ============================================================================
-- STEP 5: QUESTIONS TABLE PREPARATION (Phase 2)
-- ============================================================================

-- Add columns to existing questions table for IRT and NEP compliance
-- Note: Execute only if questions table exists

-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS syllabus_status VARCHAR(20) DEFAULT 'ACTIVE';
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS competency_type VARCHAR(20) DEFAULT 'APPLICATION';
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS irt_a FLOAT DEFAULT NULL;
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS irt_b FLOAT DEFAULT NULL;
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS irt_c FLOAT DEFAULT NULL;
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS irt_calibrated_date TIMESTAMP DEFAULT NULL;
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS exam_year INT DEFAULT 2025;
-- ALTER TABLE questions ADD COLUMN IF NOT EXISTS nep_verified BOOLEAN DEFAULT FALSE;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- After running seeds, verify:
-- SELECT COUNT(*) as total_concepts FROM concepts; -- Should be 165
-- SELECT syllabus_status, COUNT(*) FROM concepts GROUP BY syllabus_status; -- 160 ACTIVE, 5 NEP_REMOVED
-- SELECT competency_type, COUNT(*) FROM concepts WHERE syllabus_status = 'ACTIVE' GROUP BY competency_type;
-- SELECT COUNT(*) as total_prerequisites FROM prerequisites; -- Should be 65+
-- SELECT COUNT(*) as total_misconceptions FROM misconceptions; -- Should be 30+

-- ============================================================================
-- SCHEMA VERSION
-- ============================================================================

-- Version: 2.0 (V2 Production Schema)
-- Created: December 8, 2025
-- Status: PRODUCTION READY
-- Verified: Council Approved

COMMIT;
