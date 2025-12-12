"""
CR-V4 Simulation Configuration

This module contains all configuration for the simulation system,
including council-approved constants and runtime settings.

COUNCIL DECISIONS IMPLEMENTED:
1. Standard-wise content: 11th students get NO 12th content
2. Time Period: Simulation runs until target_exam_date, then ends
3. Incomplete Data: Missing concepts handled gracefully
4. Data Format: Parquet for 10x faster than JSON storage
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Final, List, Literal, Optional


# =============================================================================
# PATHS
# =============================================================================

SIMULATION_ROOT = Path(__file__).parent
DATA_DIR = SIMULATION_ROOT / "data"
PARQUET_DIR = DATA_DIR / "parquet"
CHECKPOINTS_DIR = DATA_DIR / "checkpoints"
REPORTS_DIR = DATA_DIR / "reports"


# =============================================================================
# TIME CONFIGURATION (Council Approved)
# =============================================================================

@dataclass(frozen=True)
class TimeConfig:
    """
    Time compression and period configuration.
    
    COUNCIL DECISION: Simulation is EXAM-BOUND, not endless.
    - Each agent has a target_exam_date (JEE Session 1)
    - Simulation for that agent ENDS when exam date passes
    - Agent is marked "graduated" and stops generating data
    - Simulation completes when ALL agents have graduated
    
    Time Compression:
    - 100x default: 24 simulated months = 5.3 real days
    - 1000x turbo: 24 simulated months = 0.53 real days (12.7 hours)
    """
    # Time compression ratio
    compression_ratio: float = 100.0  # 1 real second = 100 sim seconds
    
    # Simulation bounds
    max_real_hours: float = 24.0      # Max real-time hours to run
    
    # Tick configuration
    tick_interval_sim_hours: float = 1.0  # Each tick = 1 simulated hour
    
    @property
    def real_seconds_per_tick(self) -> float:
        """Real seconds between ticks."""
        sim_seconds = self.tick_interval_sim_hours * 3600
        return sim_seconds / self.compression_ratio
    
    @property
    def sim_days_per_real_hour(self) -> float:
        """Simulated days per real hour."""
        return (self.compression_ratio * 3600) / 86400


# Default time configs
TIME_CONFIG_STANDARD = TimeConfig(compression_ratio=100.0)
TIME_CONFIG_TURBO = TimeConfig(compression_ratio=1000.0)
TIME_CONFIG_REALTIME = TimeConfig(compression_ratio=1.0)


# =============================================================================
# STANDARD-WISE CONTENT RULES (Council Critical)
# =============================================================================

@dataclass(frozen=True)
class StandardContentRules:
    """
    CRITICAL COUNCIL DECISION: Standard-wise content filtering.
    
    11th grade students should NEVER receive 12th grade content.
    This is a PRIMARY validation target for the simulation.
    
    Rules:
    1. 11th students ONLY get 11th syllabus concepts
    2. 12th students get 11th (revision) + 12th content
    3. Droppers get full access
    4. Transition happens on April 1st (new academic year)
    """
    # Concept prefix mappings
    eleventh_prefixes: tuple = (
        "MATH_11_", "PHYS_11_", "CHEM_11_",  # Explicit prefixes
    )
    twelfth_prefixes: tuple = (
        "MATH_12_", "PHYS_12_", "CHEM_12_",  # Explicit prefixes
    )
    
    # Concept ID ranges (if using numeric IDs)
    # Concepts 1-75 are 11th, 76-165 are 12th
    eleventh_concept_range: tuple = (1, 75)
    twelfth_concept_range: tuple = (76, 165)
    
    @staticmethod
    def is_concept_allowed(
        concept_id: str,
        student_standard: Literal[11, 12],
        is_dropper: bool = False
    ) -> bool:
        """
        Check if a concept is allowed for a student.
        
        Args:
            concept_id: The concept identifier
            student_standard: 11 or 12
            is_dropper: If student is attempting 2nd+ time
            
        Returns:
            True if concept is allowed, False otherwise
        """
        # Droppers get everything
        if is_dropper:
            return True
        
        # Check for explicit 12th prefix
        is_12th_concept = (
            "_12_" in concept_id or 
            concept_id.startswith("12_") or
            "TWELFTH" in concept_id.upper()
        )
        
        # 11th students cannot access 12th content
        if student_standard == 11 and is_12th_concept:
            return False
        
        return True


CONTENT_RULES = StandardContentRules()


# =============================================================================
# INCOMPLETE DATA HANDLING (Council Decision)
# =============================================================================

@dataclass
class IncompleteDataConfig:
    """
    Configuration for handling incomplete question/concept data.
    
    COUNCIL DECISION: Simulation must handle missing data gracefully.
    
    Scenarios:
    1. Concept exists but no questions -> Skip, log warning
    2. Question has no IRT parameters -> Use defaults
    3. Prerequisite not in system -> Ignore that prereq
    4. New concept added mid-sim -> Hot-reload support
    """
    # Default IRT parameters when missing
    default_irt_a: float = 1.0      # Discrimination
    default_irt_b: float = 0.0      # Difficulty (medium)
    default_irt_c: float = 0.25     # Guessing (MCQ baseline)
    
    # Minimum questions per concept to be "valid"
    min_questions_per_concept: int = 3
    
    # What to do when concept has insufficient questions
    insufficient_questions_action: Literal["skip", "warn", "error"] = "warn"
    
    # Allow partial concept coverage
    allow_partial_coverage: bool = True
    min_coverage_percentage: float = 0.30  # At least 30% of concepts needed


INCOMPLETE_DATA_CONFIG = IncompleteDataConfig()


# =============================================================================
# AGENT POOL CONFIGURATION
# =============================================================================

@dataclass
class AgentPoolConfig:
    """Configuration for the agent pool."""
    total_agents: int = 1000
    
    # Persona distribution (must sum to 1.0)
    persona_distribution: Dict[str, float] = field(default_factory=lambda: {
        "STRUGGLING_PERSISTER": 0.15,
        "ANXIOUS_PERFECTIONIST": 0.12,
        "DISENGAGED_GAMER": 0.10,
        "CONCEPTUALLY_GAPPED": 0.15,
        "STEADY_LEARNER": 0.28,
        "FAST_TRACKER": 0.10,
        "LATE_JOINER": 0.06,
        "DROPPER": 0.04,
    })
    
    # Standard distribution
    standard_distribution: Dict[int, float] = field(default_factory=lambda: {
        11: 0.45,  # 45% are 11th
        12: 0.55,  # 55% are 12th (includes droppers)
    })
    
    # Join date distribution (months before exam)
    join_date_distribution: Dict[str, tuple] = field(default_factory=lambda: {
        "FRESH_START": (20, 24),       # 20-24 months before
        "MID_YEAR": (12, 20),          # 12-20 months
        "LATE_JOINER": (1, 6),         # 1-6 months
        "DROPPER": (10, 14),           # Previous year droppers
    })


AGENT_POOL_CONFIG = AgentPoolConfig()


# =============================================================================
# DATA STORAGE CONFIGURATION
# =============================================================================

@dataclass
class DataStorageConfig:
    """
    Configuration for data storage.
    
    COUNCIL DECISION: Use Parquet for 10x faster than JSON.
    
    Benefits of Parquet:
    - Columnar format: Fast aggregations
    - Compressed: 5-10x smaller than JSON
    - Schema-enforced: Type safety
    - DuckDB compatible: SQL queries on files
    """
    # Primary format
    primary_format: Literal["parquet", "arrow", "json"] = "parquet"
    
    # Compression
    compression: Literal["snappy", "gzip", "lz4", "zstd"] = "snappy"
    
    # Partitioning
    partition_by_date: bool = True
    partition_by_persona: bool = False
    
    # Batch sizes
    write_batch_size: int = 1000     # Rows per batch
    checkpoint_interval: int = 500   # Steps between checkpoints
    
    # Retention
    keep_detailed_logs: bool = True
    detailed_log_days: int = 7       # Keep detailed for 7 days
    
    # File naming
    file_prefix: str = "sim_"
    timestamp_format: str = "%Y%m%d_%H%M%S"


DATA_STORAGE_CONFIG = DataStorageConfig()


# =============================================================================
# IRT PARAMETERS (Council Approved)
# =============================================================================

@dataclass(frozen=True)
class IRTConfig:
    """IRT model configuration."""
    # Parameter bounds
    ability_min: float = -3.0
    ability_max: float = 3.0
    difficulty_min: float = -3.0
    difficulty_max: float = 3.0
    discrimination_min: float = 0.1
    discrimination_max: float = 3.0
    
    # Subject-specific guessing parameters (must be last due to field())
    # Note: frozen dataclasses with mutable defaults need special handling
    @property
    def guessing_by_subject(self) -> dict:
        return {
            "MATH": 0.20,
            "PHYSICS": 0.22,
            "CHEMISTRY": 0.25,
        }


IRT_CONFIG = IRTConfig()



# =============================================================================
# VALIDATION THRESHOLDS (Council Approved)
# =============================================================================

@dataclass(frozen=True)
class ValidationThresholds:
    """Thresholds for simulation validation."""
    # Truth fidelity
    rmse_threshold: float = 0.15              # Max acceptable RMSE
    mae_threshold: float = 0.12               # Max acceptable MAE
    
    # Trust retention
    trust_retention_threshold: float = 0.70   # 70% must have T > 0.5
    
    # Detection rates
    burnout_detection_rate: float = 0.85      # 85% detection required
    gaming_detection_rate: float = 0.70       # 70% gaming detected
    
    # Error rates
    false_positive_max: float = 0.10          # Max 10% false positives
    cold_start_hallucination_max: int = 0     # Zero tolerance
    
    # Content filtering
    standard_violation_max: int = 0           # Zero 12th content to 11th


VALIDATION_THRESHOLDS = ValidationThresholds()


# =============================================================================
# EXAM DATES
# =============================================================================

JEE_EXAM_DATES = {
    2025: date(2025, 1, 22),  # Session 1 start
    2026: date(2026, 1, 20),
    2027: date(2027, 1, 18),
}


# =============================================================================
# SIMULATION CONFIG AGGREGATOR
# =============================================================================

@dataclass
class SimulationConfig:
    """Complete simulation configuration."""
    # Sub-configs
    time: TimeConfig = field(default_factory=lambda: TIME_CONFIG_STANDARD)
    agents: AgentPoolConfig = field(default_factory=AgentPoolConfig)
    storage: DataStorageConfig = field(default_factory=DataStorageConfig)
    irt: IRTConfig = field(default_factory=IRTConfig)
    validation: ValidationThresholds = field(default_factory=ValidationThresholds)
    content_rules: StandardContentRules = field(default_factory=StandardContentRules)
    incomplete_data: IncompleteDataConfig = field(default_factory=IncompleteDataConfig)
    
    # Runtime settings
    random_seed: Optional[int] = 42
    verbose: bool = True
    
    @classmethod
    def standard(cls) -> "SimulationConfig":
        """Get standard configuration."""
        return cls()
    
    @classmethod
    def turbo(cls) -> "SimulationConfig":
        """Get turbo (fast) configuration."""
        return cls(time=TIME_CONFIG_TURBO)
