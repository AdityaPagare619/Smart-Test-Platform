"""
CR-V4 Concept Reveal Engine
Layer 4: Progressive Concept Visibility

This module implements the Progressive Concept Reveal Engine that prevents
student overwhelm by controlling which concepts are visible at any time.

Key Features:
    - Phase-based reveal schedules (15-30 concepts/month)
    - High-yield subset for crisis mode students
    - Dynamic reveal based on mastery progress
    - Psychology-optimized progress messaging

Architecture Philosophy:
    "If a student sees 280 concepts on Day 1, they think 'impossible' and quit.
    Instead, show 140 concepts and say 'You've learned 50%!'"
    - CR-V4 Council Psychology Expert

Council Approved: December 10, 2024
Expert Sign-offs: Psychology Expert, Coaching Director, UX Lead

Author: CR-V4 Engineering Team
Version: 1.0.0
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum, auto
from typing import (
    Dict,
    Final,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    TypeAlias,
)

from .academic_calendar import (
    StudentPhase,
    PhaseConfig,
    PHASE_CONFIGS,
    AcademicCalendarEngine,
)

# Configure module logger
logger = logging.getLogger(__name__)

# ==============================================================================
# TYPE DEFINITIONS
# ==============================================================================

ConceptId: TypeAlias = str
Subject: TypeAlias = Literal["MATHEMATICS", "PHYSICS", "CHEMISTRY"]


# ==============================================================================
# ENUMS
# ==============================================================================

class ConceptTier(Enum):
    """
    Concept priority tiers based on JEE weightage.
    
    Council Decision: 30% of topics (Tier 1) contribute 50% of marks.
    These must be prioritized for time-constrained students.
    """
    TIER_1_HIGH_YIELD = auto()   # 30% topics, 50% marks - MUST master
    TIER_2_MEDIUM = auto()       # 40% topics, 35% marks - Should cover
    TIER_3_LOW_YIELD = auto()    # 30% topics, 15% marks - Optional


class RevealStatus(Enum):
    """
    Visibility status of a concept.
    """
    HIDDEN = "hidden"            # Not yet revealed
    REVEALED = "revealed"        # Visible and available
    LOCKED = "locked"            # Visible but requires prerequisite
    MASTERED = "mastered"        # Completed with high mastery


# ==============================================================================
# TOPIC TIER CLASSIFICATION (COUNCIL APPROVED)
# ==============================================================================

# High-yield topics by subject (contribute 50% of JEE marks)
# These are revealed FIRST for all students, especially crisis mode

HIGH_YIELD_TOPICS: Final[Dict[Subject, List[str]]] = {
    "MATHEMATICS": [
        "calculus_differentiation",
        "calculus_integration",
        "coordinate_geometry_straight_lines",
        "coordinate_geometry_circles",
        "coordinate_geometry_conics",
        "algebra_quadratic",
        "algebra_complex_numbers",
        "probability",
        "vectors_3d",
        "trigonometry_equations",
    ],
    "PHYSICS": [
        "mechanics_kinematics",
        "mechanics_newton_laws",
        "mechanics_work_energy",
        "mechanics_rotation",
        "electrostatics",
        "current_electricity",
        "magnetism",
        "electromagnetic_induction",
        "optics_wave",
        "modern_physics_atomic",
    ],
    "CHEMISTRY": [
        "chemical_bonding",
        "coordination_compounds",
        "electrochemistry",
        "chemical_kinetics",
        "thermodynamics",
        "organic_reactions_mechanisms",
        "organic_hydrocarbons",
        "organic_functional_groups",
        "p_block_elements",
        "solutions_colligative",
    ],
}

# Tier classification for all concepts
CONCEPT_TIERS: Final[Dict[str, ConceptTier]] = {
    # Mathematics - Tier 1
    "calculus_differentiation": ConceptTier.TIER_1_HIGH_YIELD,
    "calculus_integration": ConceptTier.TIER_1_HIGH_YIELD,
    "calculus_differential_equations": ConceptTier.TIER_1_HIGH_YIELD,
    "coordinate_geometry_straight_lines": ConceptTier.TIER_1_HIGH_YIELD,
    "coordinate_geometry_circles": ConceptTier.TIER_1_HIGH_YIELD,
    "coordinate_geometry_conics": ConceptTier.TIER_1_HIGH_YIELD,
    "algebra_quadratic": ConceptTier.TIER_1_HIGH_YIELD,
    "algebra_complex_numbers": ConceptTier.TIER_1_HIGH_YIELD,
    "probability": ConceptTier.TIER_1_HIGH_YIELD,
    "vectors_3d": ConceptTier.TIER_1_HIGH_YIELD,
    
    # Mathematics - Tier 2
    "trigonometry_equations": ConceptTier.TIER_2_MEDIUM,
    "trigonometry_identities": ConceptTier.TIER_2_MEDIUM,
    "algebra_sequences_series": ConceptTier.TIER_2_MEDIUM,
    "algebra_matrices_determinants": ConceptTier.TIER_2_MEDIUM,
    "algebra_permutation_combination": ConceptTier.TIER_2_MEDIUM,
    "calculus_limits_continuity": ConceptTier.TIER_2_MEDIUM,
    "sets_relations_functions": ConceptTier.TIER_2_MEDIUM,
    
    # Mathematics - Tier 3
    "statistics": ConceptTier.TIER_3_LOW_YIELD,
    "mathematical_reasoning": ConceptTier.TIER_3_LOW_YIELD,
    "binomial_theorem": ConceptTier.TIER_3_LOW_YIELD,
    
    # Physics - Tier 1
    "mechanics_kinematics": ConceptTier.TIER_1_HIGH_YIELD,
    "mechanics_newton_laws": ConceptTier.TIER_1_HIGH_YIELD,
    "mechanics_work_energy": ConceptTier.TIER_1_HIGH_YIELD,
    "mechanics_rotation": ConceptTier.TIER_1_HIGH_YIELD,
    "electrostatics": ConceptTier.TIER_1_HIGH_YIELD,
    "current_electricity": ConceptTier.TIER_1_HIGH_YIELD,
    "magnetism": ConceptTier.TIER_1_HIGH_YIELD,
    "electromagnetic_induction": ConceptTier.TIER_1_HIGH_YIELD,
    "optics_wave": ConceptTier.TIER_1_HIGH_YIELD,
    "modern_physics_atomic": ConceptTier.TIER_1_HIGH_YIELD,
    
    # Physics - Tier 2
    "mechanics_momentum_collision": ConceptTier.TIER_2_MEDIUM,
    "mechanics_gravitation": ConceptTier.TIER_2_MEDIUM,
    "oscillations_shm": ConceptTier.TIER_2_MEDIUM,
    "waves_sound": ConceptTier.TIER_2_MEDIUM,
    "thermodynamics_laws": ConceptTier.TIER_2_MEDIUM,
    "optics_ray": ConceptTier.TIER_2_MEDIUM,
    "modern_physics_nuclear": ConceptTier.TIER_2_MEDIUM,
    
    # Physics - Tier 3
    "semiconductors": ConceptTier.TIER_3_LOW_YIELD,
    "communication_systems": ConceptTier.TIER_3_LOW_YIELD,
    "units_measurements": ConceptTier.TIER_3_LOW_YIELD,
    
    # Chemistry - Tier 1
    "chemical_bonding": ConceptTier.TIER_1_HIGH_YIELD,
    "coordination_compounds": ConceptTier.TIER_1_HIGH_YIELD,
    "electrochemistry": ConceptTier.TIER_1_HIGH_YIELD,
    "chemical_kinetics": ConceptTier.TIER_1_HIGH_YIELD,
    "thermodynamics": ConceptTier.TIER_1_HIGH_YIELD,
    "organic_reactions_mechanisms": ConceptTier.TIER_1_HIGH_YIELD,
    "organic_hydrocarbons": ConceptTier.TIER_1_HIGH_YIELD,
    "organic_functional_groups": ConceptTier.TIER_1_HIGH_YIELD,
    "p_block_elements": ConceptTier.TIER_1_HIGH_YIELD,
    "solutions_colligative": ConceptTier.TIER_1_HIGH_YIELD,
    
    # Chemistry - Tier 2
    "atomic_structure": ConceptTier.TIER_2_MEDIUM,
    "periodic_table": ConceptTier.TIER_2_MEDIUM,
    "chemical_equilibrium": ConceptTier.TIER_2_MEDIUM,
    "ionic_equilibrium": ConceptTier.TIER_2_MEDIUM,
    "organic_biomolecules": ConceptTier.TIER_2_MEDIUM,
    "d_block_elements": ConceptTier.TIER_2_MEDIUM,
    "s_block_elements": ConceptTier.TIER_2_MEDIUM,
    
    # Chemistry - Tier 3
    "surface_chemistry": ConceptTier.TIER_3_LOW_YIELD,
    "polymers": ConceptTier.TIER_3_LOW_YIELD,
    "chemistry_everyday_life": ConceptTier.TIER_3_LOW_YIELD,
    "metallurgy": ConceptTier.TIER_3_LOW_YIELD,
}


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass(frozen=True, slots=True)
class ConceptVisibility:
    """
    Visibility state for a single concept.
    
    Attributes:
        concept_id: Unique concept identifier
        subject: Subject (MATHEMATICS/PHYSICS/CHEMISTRY)
        tier: Priority tier
        status: Current visibility status
        revealed_date: When concept was revealed (None if hidden)
        mastery: Current mastery level (0.0-1.0)
        prerequisites_met: Whether all prerequisites are satisfied
    """
    concept_id: ConceptId
    subject: Subject
    tier: ConceptTier
    status: RevealStatus
    revealed_date: Optional[date] = None
    mastery: float = 0.0
    prerequisites_met: bool = True


@dataclass(slots=True)
class RevealSchedule:
    """
    Month-by-month reveal schedule for a student.
    
    Attributes:
        month: Month number (1-indexed from join date)
        total_visible: Total concepts visible by end of month
        revealed_this_month: New concepts revealed this month
        concepts_to_reveal: List of concept IDs to reveal
        progress_message: Psychology-optimized message
    """
    month: int
    total_visible: int
    revealed_this_month: int
    concepts_to_reveal: List[ConceptId]
    progress_message: str


@dataclass(slots=True)
class StudentConceptState:
    """
    Complete concept visibility state for a student.
    
    Attributes:
        student_id: Unique student identifier
        phase: Current student phase
        total_concepts: Total concepts in syllabus
        visible_concepts: Currently visible concepts
        hidden_concepts: Not yet revealed
        mastered_concepts: Completed with high mastery
        current_month: Current month of journey
        reveal_schedule: Full reveal schedule
    """
    student_id: str
    phase: StudentPhase
    total_concepts: int
    visible_concepts: Set[ConceptId]
    hidden_concepts: Set[ConceptId]
    mastered_concepts: Set[ConceptId]
    current_month: int
    reveal_schedule: List[RevealSchedule] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ProgressMessage:
    """
    Psychology-optimized progress message.
    
    Attributes:
        headline: Main message
        percentage_complete: Completion percentage
        concepts_learned: Number of concepts learned
        concepts_remaining: Number remaining
        encouragement: Motivational text
        next_milestone: Next milestone description
    """
    headline: str
    percentage_complete: float
    concepts_learned: int
    concepts_remaining: int
    encouragement: str
    next_milestone: str


# ==============================================================================
# REVEAL RATE CONFIGURATION (COUNCIL APPROVED)
# ==============================================================================

# Base concepts to reveal initially (ALWAYS visible from Day 1)
BASE_INITIAL_CONCEPTS: Final[int] = 60  # Foundation concepts

# Monthly reveal rates by phase
MONTHLY_REVEAL_RATES: Final[Dict[StudentPhase, int]] = {
    StudentPhase.FRESH_START: 15,
    StudentPhase.MID_YEAR_11TH: 17,
    StudentPhase.LATE_11TH: 20,
    StudentPhase.POST_11TH_TRANSITION: 25,
    StudentPhase.TWELFTH_LONG: 20,
    StudentPhase.TWELFTH_ACCELERATION: 30,
    StudentPhase.TWELFTH_CRISIS_MODE: -1,  # All visible immediately
    StudentPhase.TWELFTH_FINAL_SPRINT: -1,  # All visible immediately
}

# Total concepts in syllabus (Math + Physics + Chemistry)
TOTAL_SYLLABUS_CONCEPTS: Final[int] = 165


# ==============================================================================
# CORE ENGINE
# ==============================================================================

class ConceptRevealEngine:
    """
    Progressive Concept Reveal Engine.
    
    This engine controls which concepts are visible to a student at any
    given time, preventing overwhelm while ensuring complete coverage.
    
    Key Principles:
        1. Start small (60 concepts), grow gradually
        2. Tier 1 first, Tier 3 last
        3. Crisis mode = all high-yield visible immediately
        4. Progress messages are psychology-optimized
    
    Example:
        >>> engine = ConceptRevealEngine()
        >>> schedule = engine.generate_reveal_schedule(
        ...     phase=StudentPhase.FRESH_START,
        ...     total_months=20
        ... )
        >>> print(schedule[0].total_visible)
        60  # Month 1: 60 foundation concepts
    """
    
    def __init__(self, all_concepts: Optional[Set[ConceptId]] = None) -> None:
        """
        Initialize the Concept Reveal Engine.
        
        Args:
            all_concepts: Set of all concept IDs (defaults to standard syllabus)
        """
        self._all_concepts = all_concepts or self._get_default_concepts()
        self._total = len(self._all_concepts)
    
    def _get_default_concepts(self) -> Set[ConceptId]:
        """Get default syllabus concepts."""
        return set(CONCEPT_TIERS.keys())
    
    def _get_concepts_by_tier(self, tier: ConceptTier) -> List[ConceptId]:
        """
        Get all concepts of a specific tier.
        
        Args:
            tier: The tier to filter by
            
        Returns:
            List of concept IDs in that tier
        """
        return [
            cid for cid, t in CONCEPT_TIERS.items() 
            if t == tier and cid in self._all_concepts
        ]
    
    def _get_high_yield_for_crisis(self) -> Set[ConceptId]:
        """
        Get high-yield concepts for crisis mode students.
        
        Crisis mode students with limited time should focus ONLY on
        Tier 1 topics that contribute 50% of JEE marks.
        
        Returns:
            Set of high-yield concept IDs
        """
        high_yield: Set[ConceptId] = set()
        
        for subject_topics in HIGH_YIELD_TOPICS.values():
            high_yield.update(t for t in subject_topics if t in self._all_concepts)
        
        return high_yield
    
    def generate_reveal_schedule(
        self,
        phase: StudentPhase,
        total_months: int,
        start_date: Optional[date] = None
    ) -> List[RevealSchedule]:
        """
        Generate complete reveal schedule for a student phase.
        
        Args:
            phase: Current student phase
            total_months: Total months in journey
            start_date: Journey start date (defaults to today)
            
        Returns:
            Month-by-month reveal schedule
        """
        start_date = start_date or date.today()
        schedule: List[RevealSchedule] = []
        
        # Get monthly reveal rate for this phase
        reveal_rate = MONTHLY_REVEAL_RATES.get(phase, 15)
        
        # Crisis mode: All visible immediately
        if reveal_rate == -1:
            return self._generate_crisis_schedule(phase)
        
        # Get concepts by tier (reveal order: Tier 1 → Tier 2 → Tier 3)
        tier_1 = self._get_concepts_by_tier(ConceptTier.TIER_1_HIGH_YIELD)
        tier_2 = self._get_concepts_by_tier(ConceptTier.TIER_2_MEDIUM)
        tier_3 = self._get_concepts_by_tier(ConceptTier.TIER_3_LOW_YIELD)
        
        reveal_order = tier_1 + tier_2 + tier_3
        
        # Track revealed concepts
        revealed: List[ConceptId] = []
        
        # Month 1: Initial foundation (base concepts)
        initial_count = min(BASE_INITIAL_CONCEPTS, len(reveal_order))
        initial_concepts = reveal_order[:initial_count]
        revealed.extend(initial_concepts)
        
        schedule.append(RevealSchedule(
            month=1,
            total_visible=len(revealed),
            revealed_this_month=len(initial_concepts),
            concepts_to_reveal=initial_concepts,
            progress_message=self._generate_progress_message(
                revealed=len(revealed),
                total=len(reveal_order),
                month=1
            )
        ))
        
        # Subsequent months: Progressive reveal
        for month in range(2, total_months + 1):
            remaining = [c for c in reveal_order if c not in revealed]
            
            if not remaining:
                # All revealed
                schedule.append(RevealSchedule(
                    month=month,
                    total_visible=len(revealed),
                    revealed_this_month=0,
                    concepts_to_reveal=[],
                    progress_message="🎯 All concepts revealed! Focus on mastery."
                ))
                continue
            
            # Reveal up to monthly rate
            to_reveal = remaining[:reveal_rate]
            revealed.extend(to_reveal)
            
            schedule.append(RevealSchedule(
                month=month,
                total_visible=len(revealed),
                revealed_this_month=len(to_reveal),
                concepts_to_reveal=to_reveal,
                progress_message=self._generate_progress_message(
                    revealed=len(revealed),
                    total=len(reveal_order),
                    month=month
                )
            ))
        
        return schedule
    
    def _generate_crisis_schedule(self, phase: StudentPhase) -> List[RevealSchedule]:
        """
        Generate schedule for crisis mode (all visible immediately).
        
        Crisis mode students don't have time for progressive reveal.
        Show all high-yield topics immediately, mark rest as "Optional".
        """
        high_yield = list(self._get_high_yield_for_crisis())
        all_other = [c for c in self._all_concepts if c not in high_yield]
        
        return [RevealSchedule(
            month=1,
            total_visible=len(self._all_concepts),
            revealed_this_month=len(self._all_concepts),
            concepts_to_reveal=high_yield + all_other,
            progress_message=(
                f"⚡ Crisis Mode: Focus on {len(high_yield)} high-yield topics. "
                f"{len(all_other)} others are optional based on time."
            )
        )]
    
    def _generate_progress_message(
        self,
        revealed: int,
        total: int,
        month: int
    ) -> str:
        """
        Generate psychology-optimized progress message.
        
        Messages are designed to encourage, not overwhelm.
        """
        percentage = (revealed / total) * 100
        
        if percentage < 30:
            return f"🌱 Great start! {revealed} concepts unlocked ({percentage:.0f}%)"
        elif percentage < 50:
            return f"📈 Building momentum! {revealed}/{total} concepts ({percentage:.0f}%)"
        elif percentage < 70:
            return f"🔥 Halfway there! {revealed} concepts mastered ({percentage:.0f}%)"
        elif percentage < 90:
            return f"🚀 Almost complete! {revealed}/{total} concepts ({percentage:.0f}%)"
        else:
            return f"🎯 Final stretch! All {revealed} concepts available!"
    
    def get_visible_concepts(
        self,
        phase: StudentPhase,
        current_month: int
    ) -> Tuple[Set[ConceptId], ProgressMessage]:
        """
        Get currently visible concepts for a student.
        
        Args:
            phase: Student's current phase
            current_month: Current month of journey
            
        Returns:
            Tuple of (visible_concepts, progress_message)
        """
        schedule = self.generate_reveal_schedule(
            phase=phase,
            total_months=max(current_month, 12)
        )
        
        # Get all revealed up to current month
        visible: Set[ConceptId] = set()
        for entry in schedule[:current_month]:
            visible.update(entry.concepts_to_reveal)
        
        # Generate progress message
        remaining = len(self._all_concepts) - len(visible)
        percentage = (len(visible) / len(self._all_concepts)) * 100
        
        message = ProgressMessage(
            headline=f"You've unlocked {len(visible)} concepts!",
            percentage_complete=percentage,
            concepts_learned=len(visible),
            concepts_remaining=remaining,
            encouragement=self._get_encouragement(percentage),
            next_milestone=self._get_next_milestone(percentage)
        )
        
        return visible, message
    
    def _get_encouragement(self, percentage: float) -> str:
        """Get phase-appropriate encouragement."""
        if percentage < 25:
            return "Every journey starts with a single step. You're doing great!"
        elif percentage < 50:
            return "Consistent progress leads to success. Keep going!"
        elif percentage < 75:
            return "You've come so far! The finish line is in sight."
        else:
            return "You're almost there! Final push to mastery!"
    
    def _get_next_milestone(self, percentage: float) -> str:
        """Get next milestone description."""
        if percentage < 25:
            return "Reach 25% - Foundation Complete"
        elif percentage < 50:
            return "Reach 50% - Halfway Champion"
        elif percentage < 75:
            return "Reach 75% - Advanced Learner"
        elif percentage < 100:
            return "Reach 100% - Full Syllabus Master"
        else:
            return "All milestones achieved! Focus on mastery."
    
    def get_achievable_subset(
        self,
        days_remaining: int,
        hours_per_day: float = 6.0
    ) -> Tuple[Set[ConceptId], str]:
        """
        Get achievable concept subset for time-constrained students.
        
        Council Decision: Be HONEST about what's achievable.
        Don't promise 100% coverage in 60 days.
        
        Args:
            days_remaining: Days to JEE exam
            hours_per_day: Estimated productive hours per day
            
        Returns:
            Tuple of (achievable_concepts, honest_message)
        """
        # Average hours per concept (including practice)
        HOURS_PER_CONCEPT: float = 4.0
        
        total_hours = days_remaining * hours_per_day
        max_concepts = int(total_hours / HOURS_PER_CONCEPT)
        
        # Prioritize by tier
        tier_1 = self._get_concepts_by_tier(ConceptTier.TIER_1_HIGH_YIELD)
        tier_2 = self._get_concepts_by_tier(ConceptTier.TIER_2_MEDIUM)
        tier_3 = self._get_concepts_by_tier(ConceptTier.TIER_3_LOW_YIELD)
        
        priority_order = tier_1 + tier_2 + tier_3
        achievable = set(priority_order[:max_concepts])
        
        # Generate honest message
        coverage_pct = (len(achievable) / len(self._all_concepts)) * 100
        
        if coverage_pct >= 90:
            message = (
                f"✅ With {days_remaining} days, you can cover {len(achievable)} concepts "
                f"({coverage_pct:.0f}%). Full preparation is achievable!"
            )
        elif coverage_pct >= 60:
            message = (
                f"⚠️ With {days_remaining} days, you can realistically cover "
                f"{len(achievable)} concepts ({coverage_pct:.0f}%). "
                f"Focus on high-yield topics first."
            )
        else:
            message = (
                f"🚨 With {days_remaining} days, maximum {len(achievable)} concepts "
                f"({coverage_pct:.0f}%) is realistic. Focus ONLY on Tier 1 "
                f"(high-yield) topics for best results."
            )
        
        return achievable, message


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def create_reveal_engine() -> ConceptRevealEngine:
    """Create a new Concept Reveal Engine with default concepts."""
    return ConceptRevealEngine()


def get_visible_for_phase(
    phase: StudentPhase,
    month: int
) -> Tuple[Set[ConceptId], ProgressMessage]:
    """
    Convenience function to get visible concepts for a phase.
    
    Args:
        phase: Student phase
        month: Current month
        
    Returns:
        Tuple of (visible_concepts, progress_message)
    """
    engine = ConceptRevealEngine()
    return engine.get_visible_concepts(phase, month)


def get_high_yield_topics() -> Dict[Subject, List[str]]:
    """Get high-yield topics by subject."""
    return HIGH_YIELD_TOPICS.copy()


def get_concept_tier(concept_id: ConceptId) -> ConceptTier:
    """Get tier for a concept."""
    return CONCEPT_TIERS.get(concept_id, ConceptTier.TIER_2_MEDIUM)


# ==============================================================================
# UNIT TESTS
# ==============================================================================

def test_fresh_start_reveal() -> None:
    """Test FRESH_START reveal schedule."""
    engine = ConceptRevealEngine()
    schedule = engine.generate_reveal_schedule(
        phase=StudentPhase.FRESH_START,
        total_months=12
    )
    
    assert len(schedule) == 12, f"Expected 12 months, got {len(schedule)}"
    
    # Initial reveal should be min(BASE, total_concepts)
    expected_initial = min(BASE_INITIAL_CONCEPTS, len(engine._all_concepts))
    assert schedule[0].total_visible == expected_initial, f"Expected {expected_initial}, got {schedule[0].total_visible}"
    assert schedule[0].revealed_this_month == expected_initial
    
    # Month 2 should reveal remaining concepts (if any) up to monthly rate
    remaining_after_initial = len(engine._all_concepts) - expected_initial
    expected_month2 = min(15, remaining_after_initial)  # 15 is FRESH_START rate
    assert schedule[1].revealed_this_month == expected_month2, f"Expected {expected_month2}, got {schedule[1].revealed_this_month}"
    
    print("✅ FRESH_START reveal test passed")


def test_crisis_mode_reveal() -> None:
    """Test CRISIS_MODE immediate reveal."""
    engine = ConceptRevealEngine()
    schedule = engine.generate_reveal_schedule(
        phase=StudentPhase.TWELFTH_CRISIS_MODE,
        total_months=3
    )
    
    assert len(schedule) == 1, "Crisis mode should have single reveal"
    assert schedule[0].total_visible == len(engine._all_concepts)
    assert "Crisis Mode" in schedule[0].progress_message
    
    print("✅ CRISIS_MODE reveal test passed")


def test_achievable_subset() -> None:
    """Test achievable subset calculation."""
    engine = ConceptRevealEngine()
    
    # 10 days: Very limited - should be less than total
    achievable_10, msg_10 = engine.get_achievable_subset(days_remaining=10)
    
    # 60 days: Should cover more (or all)
    achievable_60, msg_60 = engine.get_achievable_subset(days_remaining=60)
    
    # 10 days should cover fewer concepts than 60 days (or both cover all)
    assert len(achievable_10) <= len(achievable_60), "10 days should not exceed 60 days coverage"
    
    # Message should contain the days and be informative
    assert "days" in msg_10.lower() or "day" in msg_10.lower(), f"Message should mention days: {msg_10}"
    
    print("✅ Achievable subset test passed")


def test_progress_messages() -> None:
    """Test progress message generation."""
    engine = ConceptRevealEngine()
    visible, message = engine.get_visible_concepts(
        phase=StudentPhase.MID_YEAR_11TH,
        current_month=3
    )
    
    assert message.percentage_complete > 0
    assert message.concepts_learned > 0
    assert len(message.headline) > 0
    assert len(message.encouragement) > 0
    
    print("✅ Progress messages test passed")


def run_all_tests() -> None:
    """Run all unit tests."""
    print("Running Concept Reveal Engine tests...")
    test_fresh_start_reveal()
    test_crisis_mode_reveal()
    test_achievable_subset()
    test_progress_messages()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
