"""
CR-V4 God-View Observer Module

This module implements the ground truth validation system,
comparing agent genomes against platform's inferred states.

COUNCIL DECISIONS IMPLEMENTED:
1. Detects cold-start hallucinations
2. Detects fatigue blindness
3. Detects gaming not caught
4. Validates standard-wise content filtering (CRITICAL)
5. Calculates truth fidelity metrics (RMSE, MAE)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math
import logging

from ..agents.genome import StudentGenome
from ..data.storage import DataWriter

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS
# =============================================================================

class ViolationType(Enum):
    """Types of validation violations."""
    COLD_START_HALLUCINATION = "cold_start_hallucination"
    FATIGUE_BLINDNESS = "fatigue_blindness"
    GAMING_NOT_DETECTED = "gaming_not_detected"
    FORGETTING_LAG = "forgetting_lag"
    BURNOUT_FALSE_POSITIVE = "burnout_false_positive"
    BURNOUT_FALSE_NEGATIVE = "burnout_false_negative"
    ROOT_CAUSE_WRONG = "root_cause_wrong"
    OVER_CONFIDENCE = "over_confidence"
    STANDARD_VIOLATION = "standard_violation"  # CRITICAL


class Severity(Enum):
    """Violation severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Violation:
    """A detected validation violation."""
    violation_id: str
    violation_type: ViolationType
    severity: Severity
    agent_id: str
    timestamp: datetime
    message: str
    genome_value: float = 0.0
    inferred_value: float = 0.0
    discrepancy: float = 0.0
    concept_id: Optional[str] = None
    additional_data: dict = field(default_factory=dict)
    
    @property
    def is_critical(self) -> bool:
        return self.severity == Severity.CRITICAL
    
    def to_dict(self) -> dict:
        return {
            "violation_id": self.violation_id,
            "violation_type": self.violation_type.value,
            "severity": self.severity.value,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "genome_value": self.genome_value,
            "inferred_value": self.inferred_value,
            "discrepancy": self.discrepancy,
            "concept_id": self.concept_id,
        }


@dataclass
class ComparisonRecord:
    """Record of a genome vs inferred comparison."""
    agent_id: str
    concept_id: str
    genome_mastery: float
    inferred_mastery: float
    discrepancy: float
    timestamp: datetime
    interaction_count: int


@dataclass
class TruthFidelityMetrics:
    """Aggregate metrics for truth fidelity."""
    total_agents: int = 0
    total_comparisons: int = 0
    rmse: float = 0.0                    # Root Mean Square Error
    mae: float = 0.0                     # Mean Absolute Error
    max_discrepancy: float = 0.0
    min_discrepancy: float = 0.0
    violations_count: int = 0
    critical_violations: int = 0
    trust_retention_rate: float = 0.0    # % with trust > 0.5
    standard_violations: int = 0          # CRITICAL METRIC
    diagnostic_precision: float = 0.0    # Correct gap identification
    
    def is_passing(self) -> bool:
        """Check if metrics meet council thresholds."""
        from ..config import VALIDATION_THRESHOLDS
        
        return (
            self.rmse <= VALIDATION_THRESHOLDS.rmse_threshold and
            self.mae <= VALIDATION_THRESHOLDS.mae_threshold and
            self.trust_retention_rate >= VALIDATION_THRESHOLDS.trust_retention_threshold and
            self.standard_violations == 0  # Zero tolerance
        )


# =============================================================================
# GOD-VIEW OBSERVER
# =============================================================================

class GodViewObserver:
    """
    Validates platform AI against ground truth genomes.
    
    The Observer has access to:
    - All agent genomes (hidden truth)
    - All platform inferred states
    - Compares and flags discrepancies
    
    This is the "Oracle" that knows everything and validates
    whether the platform is correctly estimating student states.
    
    CRITICAL VALIDATION:
    - Standard-wise content filtering (11th gets no 12th content)
    - Cold-start hallucination detection
    - Gaming detection verification
    """
    
    # Council-approved thresholds
    COLD_START_INTERACTION_LIMIT: int = 10
    COLD_START_CONFIDENCE_THRESHOLD: float = 0.3
    FATIGUE_THRESHOLD: float = 0.7
    MASTERY_DROP_THRESHOLD: float = 0.2
    GAMING_RESPONSE_TIME_THRESHOLD: float = 5.0
    
    def __init__(self, data_writer: Optional[DataWriter] = None):
        """
        Initialize God-View Observer.
        
        Args:
            data_writer: For logging violations
        """
        self.data_writer = data_writer
        
        # Genome registry
        self.genomes: Dict[str, StudentGenome] = {}
        
        # Tracking
        self.violations: List[Violation] = []
        self.comparison_log: List[ComparisonRecord] = []
        self.standard_violations_count: int = 0
        
        # Counters per violation type
        self.violation_counts: Dict[ViolationType, int] = {
            vt: 0 for vt in ViolationType
        }
        
        # Counter
        self._violation_counter = 0
    
    def register_genome(self, genome: StudentGenome):
        """
        Register a genome for tracking.
        
        Args:
            genome: Student genome to track
        """
        self.genomes[genome.genome_id] = genome
    
    def register_genomes(self, genomes: List[StudentGenome]):
        """Register multiple genomes."""
        for genome in genomes:
            self.register_genome(genome)
    
    # =========================================================================
    # VALIDATION METHODS
    # =========================================================================
    
    def validate_interaction(
        self,
        agent_id: str,
        concept_id: str,
        inferred_mastery: float,
        interaction_count: int,
        response_time_seconds: float = 60.0,
        is_12th_content: bool = False,
        fatigue_level: float = 0.0,
        burnout_detected: bool = False,
        **context
    ) -> List[Violation]:
        """
        Validate a single interaction against genome.
        
        This is the MAIN validation method called after each interaction.
        
        Args:
            agent_id: Agent identifier
            concept_id: Concept being tested
            inferred_mastery: Platform's mastery estimate
            interaction_count: Total interactions so far
            response_time_seconds: Response time
            is_12th_content: If this is 12th grade content
            fatigue_level: Agent's fatigue (0-1)
            burnout_detected: If platform flagged burnout
            **context: Additional context
            
        Returns:
            List of violations detected
        """
        genome = self.genomes.get(agent_id)
        if not genome:
            return []
        
        violations = []
        
        # Get ground truth
        genome_mastery = genome.knowledge.get_mastery(concept_id)
        discrepancy = abs(inferred_mastery - genome_mastery)
        
        # Log comparison
        self.comparison_log.append(ComparisonRecord(
            agent_id=agent_id,
            concept_id=concept_id,
            genome_mastery=genome_mastery,
            inferred_mastery=inferred_mastery,
            discrepancy=discrepancy,
            timestamp=datetime.now(),
            interaction_count=interaction_count,
        ))
        
        # === CRITICAL: Standard Violation ===
        if is_12th_content and genome.standard == 11:
            if not genome.is_dropper:
                v = self._create_violation(
                    ViolationType.STANDARD_VIOLATION,
                    Severity.CRITICAL,
                    agent_id,
                    genome_mastery,
                    inferred_mastery,
                    f"12th GRADE CONTENT given to 11th student! "
                    f"Agent {agent_id} (standard=11) received concept {concept_id} "
                    f"which is 12th grade content. THIS IS A CRITICAL FAILURE.",
                    concept_id=concept_id,
                )
                violations.append(v)
                self.standard_violations_count += 1
        
        # === Cold Start Hallucination ===
        if interaction_count < self.COLD_START_INTERACTION_LIMIT:
            if discrepancy > self.COLD_START_CONFIDENCE_THRESHOLD:
                v = self._create_violation(
                    ViolationType.COLD_START_HALLUCINATION,
                    Severity.HIGH,
                    agent_id,
                    genome_mastery,
                    inferred_mastery,
                    f"Platform estimates {concept_id} at {inferred_mastery:.2f} "
                    f"but actual is {genome_mastery:.2f} after only "
                    f"{interaction_count} interactions",
                    concept_id=concept_id,
                )
                violations.append(v)
        
        # === Fatigue Blindness ===
        if fatigue_level > self.FATIGUE_THRESHOLD:
            if (genome_mastery - inferred_mastery) > self.MASTERY_DROP_THRESHOLD:
                if not burnout_detected:
                    v = self._create_violation(
                        ViolationType.FATIGUE_BLINDNESS,
                        Severity.HIGH,
                        agent_id,
                        genome_mastery,
                        inferred_mastery,
                        f"Agent fatigued (F={fatigue_level:.2f}), mastery dropped "
                        f"from {genome_mastery:.2f} to {inferred_mastery:.2f}, "
                        f"but burnout not detected by platform",
                        concept_id=concept_id,
                    )
                    violations.append(v)
        
        # === Gaming Not Detected ===
        if response_time_seconds < self.GAMING_RESPONSE_TIME_THRESHOLD:
            if inferred_mastery > genome_mastery + 0.1:
                v = self._create_violation(
                    ViolationType.GAMING_NOT_DETECTED,
                    Severity.CRITICAL,
                    agent_id,
                    genome_mastery,
                    inferred_mastery,
                    f"Agent gaming (response {response_time_seconds:.1f}s) but "
                    f"mastery was increased from {genome_mastery:.2f} to "
                    f"{inferred_mastery:.2f}",
                    concept_id=concept_id,
                )
                violations.append(v)
        
        return violations
    
    def validate_content_access(
        self,
        agent_id: str,
        concept_id: str,
        is_12th_content: bool
    ) -> Optional[Violation]:
        """
        Validate that content access respects standard rules.
        
        CRITICAL: This is the primary test for standard-wise filtering.
        
        Args:
            agent_id: Agent identifier
            concept_id: Concept being accessed
            is_12th_content: If this is 12th grade content
            
        Returns:
            Violation if standard rule broken, None otherwise
        """
        genome = self.genomes.get(agent_id)
        if not genome:
            return None
        
        if is_12th_content and genome.standard == 11 and not genome.is_dropper:
            violation = self._create_violation(
                ViolationType.STANDARD_VIOLATION,
                Severity.CRITICAL,
                agent_id,
                0.0,
                0.0,
                f"STANDARD VIOLATION: 11th grade student {agent_id} "
                f"accessed 12th grade content: {concept_id}",
                concept_id=concept_id,
            )
            self.standard_violations_count += 1
            return violation
        
        return None
    
    def _create_violation(
        self,
        vtype: ViolationType,
        severity: Severity,
        agent_id: str,
        genome_val: float,
        inferred_val: float,
        message: str,
        concept_id: Optional[str] = None,
        **additional
    ) -> Violation:
        """Create and record a violation."""
        self._violation_counter += 1
        violation_id = f"V{self._violation_counter:06d}"
        
        violation = Violation(
            violation_id=violation_id,
            violation_type=vtype,
            severity=severity,
            agent_id=agent_id,
            timestamp=datetime.now(),
            message=message,
            genome_value=genome_val,
            inferred_value=inferred_val,
            discrepancy=abs(genome_val - inferred_val),
            concept_id=concept_id,
            additional_data=additional,
        )
        
        self.violations.append(violation)
        self.violation_counts[vtype] += 1
        
        # Log to data writer
        if self.data_writer:
            self.data_writer.log_validation(violation.to_dict())
        
        # Log to console for critical
        if severity == Severity.CRITICAL:
            logger.error(f"CRITICAL VIOLATION: {message}")
        elif severity == Severity.HIGH:
            logger.warning(f"HIGH VIOLATION: {message}")
        
        return violation
    
    # =========================================================================
    # METRICS CALCULATION
    # =========================================================================
    
    def calculate_metrics(
        self,
        trust_scores: Optional[Dict[str, float]] = None
    ) -> TruthFidelityMetrics:
        """
        Calculate aggregate truth fidelity metrics.
        
        Args:
            trust_scores: Dict of agent_id -> trust_score
            
        Returns:
            Aggregated metrics
        """
        if not self.comparison_log:
            return TruthFidelityMetrics(
                total_agents=len(self.genomes),
                violations_count=len(self.violations),
                critical_violations=sum(
                    1 for v in self.violations if v.is_critical
                ),
                standard_violations=self.standard_violations_count,
            )
        
        # Calculate RMSE and MAE
        discrepancies = [c.discrepancy for c in self.comparison_log]
        
        n = len(discrepancies)
        rmse = math.sqrt(sum(d**2 for d in discrepancies) / n)
        mae = sum(discrepancies) / n
        max_disc = max(discrepancies)
        min_disc = min(discrepancies)
        
        # Critical violations
        critical = sum(1 for v in self.violations if v.is_critical)
        
        # Trust retention
        if trust_scores:
            retained = sum(1 for t in trust_scores.values() if t > 0.5)
            retention_rate = retained / len(trust_scores)
        else:
            retention_rate = 1.0
        
        return TruthFidelityMetrics(
            total_agents=len(self.genomes),
            total_comparisons=len(self.comparison_log),
            rmse=rmse,
            mae=mae,
            max_discrepancy=max_disc,
            min_discrepancy=min_disc,
            violations_count=len(self.violations),
            critical_violations=critical,
            trust_retention_rate=retention_rate,
            standard_violations=self.standard_violations_count,
            diagnostic_precision=0.85,  # Placeholder
        )
    
    # =========================================================================
    # REPORTING
    # =========================================================================
    
    def generate_report(
        self,
        trust_scores: Optional[Dict[str, float]] = None
    ) -> str:
        """Generate human-readable validation report."""
        metrics = self.calculate_metrics(trust_scores)
        
        lines = [
            "=" * 70,
            "                   GOD-VIEW OBSERVER REPORT",
            "=" * 70,
            f"Timestamp: {datetime.now().isoformat()}",
            "",
            "AGENTS:",
            f"  Registered: {metrics.total_agents}",
            f"  Comparisons: {metrics.total_comparisons}",
            "",
            "TRUTH FIDELITY METRICS:",
            f"  RMSE: {metrics.rmse:.4f} (threshold: ≤0.15)",
            f"  MAE: {metrics.mae:.4f} (threshold: ≤0.12)",
            f"  Max Discrepancy: {metrics.max_discrepancy:.4f}",
            "",
            "TRUST METRICS:",
            f"  Retention Rate: {metrics.trust_retention_rate*100:.1f}% (threshold: ≥70%)",
            "",
            "VIOLATIONS:",
            f"  Total: {metrics.violations_count}",
            f"  Critical: {metrics.critical_violations}",
            f"  Standard Violations: {metrics.standard_violations} (MUST BE ZERO)",
            "",
            "VIOLATIONS BY TYPE:",
        ]
        
        for vtype, count in self.violation_counts.items():
            if count > 0:
                lines.append(f"  {vtype.value}: {count}")
        
        lines.extend([
            "",
            "STATUS:",
            f"  {'✅ PASSING' if metrics.is_passing() else '❌ FAILING'}",
        ])
        
        if not metrics.is_passing():
            lines.append("")
            lines.append("FAILURE REASONS:")
            from ..config import VALIDATION_THRESHOLDS
            
            if metrics.rmse > VALIDATION_THRESHOLDS.rmse_threshold:
                lines.append(f"  - RMSE {metrics.rmse:.4f} > {VALIDATION_THRESHOLDS.rmse_threshold}")
            if metrics.mae > VALIDATION_THRESHOLDS.mae_threshold:
                lines.append(f"  - MAE {metrics.mae:.4f} > {VALIDATION_THRESHOLDS.mae_threshold}")
            if metrics.trust_retention_rate < VALIDATION_THRESHOLDS.trust_retention_threshold:
                lines.append(f"  - Trust retention {metrics.trust_retention_rate*100:.1f}% < 70%")
            if metrics.standard_violations > 0:
                lines.append(f"  - CRITICAL: {metrics.standard_violations} standard violations!")
        
        if self.violations:
            lines.extend([
                "",
                "RECENT VIOLATIONS (last 10):",
            ])
            for v in self.violations[-10:]:
                lines.append(f"  [{v.severity.value}] {v.violation_type.value}")
                lines.append(f"    Agent: {v.agent_id}")
                lines.append(f"    {v.message[:80]}...")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def get_summary(self) -> dict:
        """Get summary for monitoring dashboard."""
        metrics = self.calculate_metrics()
        return {
            "total_agents": metrics.total_agents,
            "total_comparisons": metrics.total_comparisons,
            "rmse": round(metrics.rmse, 4),
            "mae": round(metrics.mae, 4),
            "violations_total": metrics.violations_count,
            "violations_critical": metrics.critical_violations,
            "standard_violations": metrics.standard_violations,
            "trust_retention_rate": round(metrics.trust_retention_rate, 3),
            "is_passing": metrics.is_passing(),
            "violation_types": {
                vt.value: count for vt, count in self.violation_counts.items() if count > 0
            },
        }
