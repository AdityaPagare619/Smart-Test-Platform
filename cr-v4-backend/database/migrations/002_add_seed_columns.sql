-- CR-V4 SCHEMA MIGRATION: Phase 1 Seed Data Support
-- Migration: 002_add_seed_columns.sql
-- Created: December 8, 2025
-- Purpose: Add columns required by Phase 1 seed data files

-- ============================================================================
-- CONCEPTS TABLE: Add additional columns from seed files
-- ============================================================================

-- Add layer_level (mapped from layer in original schema)
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS layer_level INT;

-- Add exam_weightage (more specific than exam_weight)
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS exam_weightage DECIMAL(5,4);

-- Add typical_mastery_time_hours
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS typical_mastery_time_hours DECIMAL(4,1);

-- Add nta_frequency_papers (number of papers where concept appeared)
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS nta_frequency_papers INT;

-- Add irt_difficulty (Item Response Theory difficulty parameter)
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS irt_difficulty DECIMAL(3,2);

-- Add learning_outcomes (text description)
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS learning_outcomes TEXT;

-- ============================================================================
-- CONCEPT_PREREQUISITES TABLE: Update column names for seed compatibility
-- ============================================================================

-- Add prerequisite_concept_id (alternative name)
ALTER TABLE concept_prerequisites ADD COLUMN IF NOT EXISTS prerequisite_concept_id VARCHAR(20);
ALTER TABLE concept_prerequisites ADD COLUMN IF NOT EXISTS dependent_concept_id VARCHAR(20);
ALTER TABLE concept_prerequisites ADD COLUMN IF NOT EXISTS dependency_strength DECIMAL(3,2);
ALTER TABLE concept_prerequisites ADD COLUMN IF NOT EXISTS transfer_learning_weight DECIMAL(3,2);
ALTER TABLE concept_prerequisites ADD COLUMN IF NOT EXISTS is_hard_dependency BOOLEAN DEFAULT FALSE;

-- ============================================================================
-- MISCONCEPTIONS TABLE: Update columns for seed compatibility
-- ============================================================================

ALTER TABLE misconceptions ADD COLUMN IF NOT EXISTS correct_concept TEXT;
ALTER TABLE misconceptions ADD COLUMN IF NOT EXISTS diagnostic_question TEXT;
ALTER TABLE misconceptions ADD COLUMN IF NOT EXISTS severity_level VARCHAR(20);

-- ============================================================================
-- CREATE INDEXES FOR NEW COLUMNS
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_concepts_layer_level ON concepts(layer_level);
CREATE INDEX IF NOT EXISTS idx_concepts_irt_difficulty ON concepts(irt_difficulty);
CREATE INDEX IF NOT EXISTS idx_concepts_nta_frequency ON concepts(nta_frequency_papers DESC);

CREATE INDEX IF NOT EXISTS idx_prereq_strength ON concept_prerequisites(dependency_strength DESC);
CREATE INDEX IF NOT EXISTS idx_prereq_hard ON concept_prerequisites(is_hard_dependency);

CREATE INDEX IF NOT EXISTS idx_misconceptions_severity ON misconceptions(severity_level);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- This migration adds support for:
-- ✅ 165 JEE Concepts with full metadata
-- ✅ 200+ Prerequisites with transfer learning weights
-- ✅ 320+ Misconceptions with diagnostic questions

COMMIT;
