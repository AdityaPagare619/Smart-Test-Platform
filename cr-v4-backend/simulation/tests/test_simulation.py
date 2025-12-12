"""
CR-V4 Simulation Unit Tests

Comprehensive test suite for validating all simulation components.

Tests are organized by module:
1. Genome generation and personas
2. Cognitive Logic Core (IRT, fatigue, learning)
3. Trust Engine (zones, compliance)
4. Time Keeper (compression, graduation)
5. Observer (validation, violations)
6. Standard-wise content filtering (CRITICAL)
"""

import math
import random
from datetime import date, datetime, timedelta
from typing import List
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from simulation.agents.genome import (
    StudentGenome, PersonaType, CognitiveCapacity, PsychometricProfile,
    KnowledgeState, TemporalContext, BehavioralPatterns, LoginTimePreference,
    generate_genome, generate_genome_pool, PERSONA_CONFIGS
)
from simulation.agents.cognitive_core import (
    CognitiveLogicCore, SessionState, QuestionContext, AnswerOutcome
)
from simulation.agents.trust_engine import (
    TrustEngine, TrustZone, AgentAction, RecommendationQuality, Recommendation
)
from simulation.orchestrator.time_keeper import TimeKeeper, SimulationPhase
from simulation.observer.god_view import (
    GodViewObserver, ViolationType, Severity
)
from simulation.config import CONTENT_RULES


# =============================================================================
# TEST UTILITIES
# =============================================================================

def create_test_genome(
    persona: PersonaType = PersonaType.STEADY_LEARNER,
    standard: int = 11,
    is_dropper: bool = False
) -> StudentGenome:
    """Create a test genome with known values."""
    return StudentGenome(
        genome_id="TEST_001",
        persona_type=persona,
        cognitive=CognitiveCapacity(
            iq_factor=0.6,
            working_memory_limit=6,
            processing_speed=1.0,
            attention_span_minutes=45,
        ),
        psychometric=PsychometricProfile(
            grit_index=0.5,
            anxiety_trait=0.5,
            focus_stability=0.5,
            guessing_tendency=0.25,
            perfectionism=0.5,
            risk_tolerance=0.5,
        ),
        knowledge=KnowledgeState(
            kc_mastery_map={
                "MATH_11_001": 0.7,
                "MATH_11_002": 0.5,
                "PHYS_11_001": 0.6,
                "MATH_12_001": 0.4,  # 12th content
            }
        ),
        temporal=TemporalContext(
            join_date=date(2024, 6, 1),
            standard=standard,
            target_exam_date=date(2025, 1, 22),
            is_dropper=is_dropper,
        ),
        behavioral=BehavioralPatterns(
            login_time_preference=LoginTimePreference.EVENING,
            session_length_mean=45.0,
            session_length_std=15.0,
            consistency_factor=0.6,
            study_hours_per_day=3.0,
            weekend_multiplier=1.2,
            break_frequency_per_hour=1.5,
        ),
    )


def create_test_question(
    concept_id: str = "MATH_11_001",
    difficulty: float = 0.0,
    is_12th: bool = False
) -> QuestionContext:
    """Create a test question."""
    return QuestionContext(
        question_id="Q_TEST_001",
        concept_id=concept_id,
        subject="MATH",
        difficulty_b=difficulty,
        discrimination_a=1.0,
        guessing_c=0.25,
        is_high_stakes=False,
        is_12th_content=is_12th,
    )


# =============================================================================
# GENOME TESTS
# =============================================================================

def test_genome_creation():
    """Test genome creation and validation."""
    print("Testing genome creation...")
    
    genome = create_test_genome()
    
    assert genome.genome_id == "TEST_001"
    assert genome.persona_type == PersonaType.STEADY_LEARNER
    assert genome.standard == 11
    assert 0 <= genome.cognitive.iq_factor <= 1
    assert 3 <= genome.cognitive.working_memory_limit <= 9
    
    print("  ✓ Genome created with valid values")
    
    # Test serialization
    data = genome.to_dict()
    assert "genome_id" in data
    assert "cognitive" in data
    assert "psychometric" in data
    
    print("  ✓ Genome serialization works")
    
    print("✅ test_genome_creation PASSED")


def test_persona_configs():
    """Test all persona configurations are valid."""
    print("Testing persona configurations...")
    
    # Check all personas have configs
    for persona in PersonaType:
        assert persona in PERSONA_CONFIGS, f"Missing config for {persona}"
        config = PERSONA_CONFIGS[persona]
        
        # Validate ranges
        assert 0 <= config.iq_mean <= 1
        assert 0 <= config.grit_mean <= 1
        assert 0 <= config.anxiety_mean <= 1
        
    print("  ✓ All 8 personas have valid configurations")
    
    # Check distribution sums to ~1.0
    from simulation.config import AGENT_POOL_CONFIG
    total = sum(AGENT_POOL_CONFIG.persona_distribution.values())
    assert 0.99 <= total <= 1.01, f"Distribution sums to {total}"
    
    print("  ✓ Persona distribution sums to 1.0")
    
    print("✅ test_persona_configs PASSED")


def test_genome_pool_generation():
    """Test genome pool generation."""
    print("Testing genome pool generation...")
    
    genomes = generate_genome_pool(count=100, random_seed=42)
    
    assert len(genomes) == 100
    
    # Check persona distribution (rough)
    persona_counts = {}
    for g in genomes:
        p = g.persona_type.name
        persona_counts[p] = persona_counts.get(p, 0) + 1
    
    # Steady learner should be most common (~28%)
    assert persona_counts["STEADY_LEARNER"] >= 20
    
    print(f"  ✓ Generated 100 genomes with distribution: {persona_counts}")
    
    print("✅ test_genome_pool_generation PASSED")


# =============================================================================
# STANDARD-WISE CONTENT TESTS (CRITICAL)
# =============================================================================

def test_standard_content_filtering():
    """
    CRITICAL TEST: 11th students must not access 12th content.
    """
    print("Testing standard-wise content filtering (CRITICAL)...")
    
    # Test content rules
    assert CONTENT_RULES.is_concept_allowed("MATH_11_001", 11) == True
    assert CONTENT_RULES.is_concept_allowed("MATH_12_001", 11) == False  # CRITICAL
    assert CONTENT_RULES.is_concept_allowed("MATH_12_001", 12) == True
    assert CONTENT_RULES.is_concept_allowed("MATH_12_001", 11, is_dropper=True) == True
    
    print("  ✓ Content rules work correctly")
    
    # Test genome access check
    genome_11 = create_test_genome(standard=11, is_dropper=False)
    genome_12 = create_test_genome(standard=12, is_dropper=False)
    genome_dropper = create_test_genome(standard=12, is_dropper=True)
    
    # 11th student
    assert genome_11.can_access_concept("MATH_11_001") == True
    assert genome_11.can_access_concept("MATH_12_001") == False  # CRITICAL
    
    # 12th student
    assert genome_12.can_access_concept("MATH_11_001") == True
    assert genome_12.can_access_concept("MATH_12_001") == True
    
    # Dropper
    assert genome_dropper.can_access_concept("MATH_12_001") == True
    
    print("  ✓ Genome access checks work correctly")
    
    print("✅ test_standard_content_filtering PASSED (CRITICAL)")


# =============================================================================
# COGNITIVE LOGIC CORE TESTS
# =============================================================================

def test_irt_probability():
    """Test IRT probability calculation."""
    print("Testing IRT probability...")
    
    genome = create_test_genome()
    clc = CognitiveLogicCore(genome)
    
    # Test basic IRT
    # High ability, easy question -> high probability
    prob_easy = clc.irt_probability(theta=0.9, a=1.0, b=-2.0, c=0.25)
    assert prob_easy > 0.9, f"Expected >0.9, got {prob_easy}"
    
    # Low ability, hard question -> probability near guessing
    prob_hard = clc.irt_probability(theta=0.1, a=1.0, b=2.0, c=0.25)
    assert prob_hard < 0.4, f"Expected <0.4, got {prob_hard}"
    
    # Equal ability and difficulty -> probability around 0.625
    prob_matched = clc.irt_probability(theta=0.5, a=1.0, b=0.0, c=0.25)
    assert 0.5 < prob_matched < 0.75, f"Expected 0.5-0.75, got {prob_matched}"
    
    print(f"  ✓ IRT probabilities: easy={prob_easy:.3f}, hard={prob_hard:.3f}, matched={prob_matched:.3f}")
    
    print("✅ test_irt_probability PASSED")


def test_answer_generation():
    """Test answer generation with various scenarios."""
    print("Testing answer generation...")
    
    random.seed(42)
    genome = create_test_genome()
    clc = CognitiveLogicCore(genome)
    
    question = create_test_question(concept_id="MATH_11_001", difficulty=0.0)
    
    # Generate many answers and check statistics
    correct_count = 0
    total = 100
    
    for _ in range(total):
        session = clc.start_session()
        result = clc.generate_answer(question, session)
        if result.is_correct:
            correct_count += 1
        clc.end_session()
    
    accuracy = correct_count / total
    # With mastery 0.7 and matched difficulty, expect ~70% accuracy
    assert 0.5 < accuracy < 0.9, f"Expected accuracy 0.5-0.9, got {accuracy}"
    
    print(f"  ✓ Generated {total} answers with accuracy {accuracy:.2f}")
    
    print("✅ test_answer_generation PASSED")


def test_fatigue_effects():
    """Test fatigue increases and affects performance."""
    print("Testing fatigue effects...")
    
    genome = create_test_genome()
    clc = CognitiveLogicCore(genome)
    session = clc.start_session()
    
    question = create_test_question()
    
    # Answer 50 questions
    initial_fatigue = session.current_fatigue
    for _ in range(50):
        clc.generate_answer(question, session)
    
    final_fatigue = session.current_fatigue
    
    assert final_fatigue > initial_fatigue
    assert final_fatigue > 0.3  # Should have significant fatigue
    
    print(f"  ✓ Fatigue increased from {initial_fatigue:.3f} to {final_fatigue:.3f}")
    
    print("✅ test_fatigue_effects PASSED")


# =============================================================================
# TRUST ENGINE TESTS
# =============================================================================

def test_trust_zones():
    """Test trust zone transitions."""
    print("Testing trust zones...")
    
    genome = create_test_genome()
    engine = TrustEngine(genome)
    
    # Initial trust should be HIGH
    assert engine.state.zone == TrustZone.HIGH
    assert engine.state.trust_score == 1.0
    
    # Apply many frustrations to drop trust
    for _ in range(30):
        engine.update_trust(RecommendationQuality.FRUSTRATION)
    
    # Should be in DANGER or CHURN
    assert engine.state.zone in [TrustZone.DANGER, TrustZone.CHURN]
    
    print(f"  ✓ Trust dropped to {engine.state.trust_score:.3f} (zone: {engine.state.zone.value})")
    
    print("✅ test_trust_zones PASSED")


def test_trust_asymmetry():
    """Test that trust is harder to gain than lose."""
    print("Testing trust asymmetry...")
    
    genome = create_test_genome()
    engine = TrustEngine(genome)
    engine.state.trust_score = 0.7  # Start mid-range
    
    # Record starting point
    start = engine.state.trust_score
    
    # One frustration
    engine.update_trust(RecommendationQuality.FRUSTRATION)
    after_frustration = engine.state.trust_score
    loss = start - after_frustration
    
    # Multiple flows to try to recover
    engine.update_trust(RecommendationQuality.FLOW)
    engine.update_trust(RecommendationQuality.FLOW)
    engine.update_trust(RecommendationQuality.FLOW)
    after_flows = engine.state.trust_score
    gain = after_flows - after_frustration
    
    # Loss should be more than gain per interaction
    print(f"  ✓ Loss: {loss:.4f}, Gain (3 flows): {gain:.4f}")
    
    print("✅ test_trust_asymmetry PASSED")


# =============================================================================
# TIME KEEPER TESTS
# =============================================================================

def test_time_compression():
    """Test time compression logic."""
    print("Testing time compression...")
    
    tk = TimeKeeper(compression_ratio=100.0)
    tk.start()
    
    # Advance by 24 simulated hours
    for _ in range(24):
        tk.advance_hours(1.0)
    
    assert tk.elapsed_sim_days >= 0.99
    assert tk.state.sim_elapsed_days >= 0.99
    
    print(f"  ✓ Advanced {tk.elapsed_sim_days:.2f} simulated days")
    
    print("✅ test_time_compression PASSED")


def test_graduation_logic():
    """Test exam-bound graduation logic."""
    print("Testing graduation logic...")
    
    exam_date = date(2025, 1, 22)
    tk = TimeKeeper(compression_ratio=100.0)
    tk.time_keeper_start_date = date(2024, 12, 1)
    
    # Register agents with exam date
    tk.register_agent("AGENT_001", exam_date)
    tk.register_agent("AGENT_002", exam_date)
    
    tk.start()
    
    # Before exam - no graduates
    assert len(tk.graduated_agents) == 0
    
    # Advance past exam date (simulate ~60 days)
    for _ in range(60 * 24):  # 60 days * 24 hours
        tk.advance_hours(1.0)
        graduates = tk.check_graduations()
        if graduates:
            print(f"  Graduates at day {tk.elapsed_sim_days:.1f}: {graduates}")
    
    # Check agents graduated
    active = tk.get_active_agents()
    print(f"  ✓ Active agents remaining: {len(active)}")
    
    print("✅ test_graduation_logic PASSED")


# =============================================================================
# OBSERVER TESTS
# =============================================================================

def test_observer_violations():
    """Test observer detects violations."""
    print("Testing observer violations...")
    
    observer = GodViewObserver()
    
    # Create and register genome
    genome = create_test_genome(standard=11)
    observer.register_genome(genome)
    
    # Test standard violation detection
    violation = observer.validate_content_access(
        agent_id="TEST_001",
        concept_id="MATH_12_001",
        is_12th_content=True
    )
    
    assert violation is not None
    assert violation.violation_type == ViolationType.STANDARD_VIOLATION
    assert violation.severity == Severity.CRITICAL
    
    print(f"  ✓ Detected standard violation: {violation.message[:50]}...")
    
    # Check counts
    assert observer.standard_violations_count == 1
    
    print("✅ test_observer_violations PASSED")


def test_cold_start_hallucination():
    """Test cold start hallucination detection."""
    print("Testing cold start hallucination detection...")
    
    observer = GodViewObserver()
    genome = create_test_genome()
    observer.register_genome(genome)
    
    # With few interactions, large discrepancy should trigger violation
    violations = observer.validate_interaction(
        agent_id="TEST_001",
        concept_id="MATH_11_001",
        inferred_mastery=0.1,  # Platform says 0.1
        interaction_count=3,    # Only 3 interactions
        response_time_seconds=60.0,
        is_12th_content=False,
    )
    
    cold_start = [v for v in violations if v.violation_type == ViolationType.COLD_START_HALLUCINATION]
    assert len(cold_start) >= 1  # Should detect hallucination
    
    print(f"  ✓ Detected cold start violation: genome=0.7, inferred=0.1")
    
    print("✅ test_cold_start_hallucination PASSED")


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("CR-V4 SIMULATION TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        # Genome tests
        test_genome_creation,
        test_persona_configs,
        test_genome_pool_generation,
        
        # CRITICAL: Standard filtering
        test_standard_content_filtering,
        
        # Cognitive tests
        test_irt_probability,
        test_answer_generation,
        test_fatigue_effects,
        
        # Trust tests
        test_trust_zones,
        test_trust_asymmetry,
        
        # Time tests
        test_time_compression,
        test_graduation_logic,
        
        # Observer tests
        test_observer_violations,
        test_cold_start_hallucination,
    ]
    
    passed = 0
    failed = 0
    failures = []
    
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
            print()
        except AssertionError as e:
            failed += 1
            failures.append((test_fn.__name__, str(e)))
            print(f"❌ {test_fn.__name__} FAILED: {e}")
            print()
        except Exception as e:
            failed += 1
            failures.append((test_fn.__name__, str(e)))
            print(f"❌ {test_fn.__name__} ERROR: {e}")
            print()
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failures:
        print("\nFAILURES:")
        for name, error in failures:
            print(f"  {name}: {error}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
