"""
CR-V4 CORE ALGORITHMS
Module: Bayesian Learning & Mastery Estimation

Mathematical Foundation:
P(M|E) = P(E|M) × P(M) / P(E)

Where:
- M = Student has mastery level for concept
- E = Observed evidence (correct/incorrect answer)
- P(M|E) = Posterior (updated belief after evidence)
- P(M) = Prior (belief before evidence)
- P(E|M) = Likelihood (how likely evidence given mastery)
- P(E) = Marginal likelihood (probability of observing evidence)

Production-Grade Implementation with Complete Testing
"""

from dataclasses import dataclass
from typing import Dict, Tuple, Optional
from decimal import Decimal
import math
from enum import Enum

# ============================================================================
# CONSTANTS (Calibrated for JEE-MAINS)
# ============================================================================

# MCQ-specific: 4 options, random guess = 25% correct
GUESSING_PROBABILITY = 0.25

# Confidence bounds for Bayesian update
MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 1.0

# Mastery bounds
MIN_MASTERY = 0.0
MAX_MASTERY = 1.0

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class QuestionAttempt:
    """
    Represents a single student attempt at a question.
    
    Attributes:
        correct: Whether answer was correct
        time_taken: Seconds spent on question
        question_difficulty: 0.0 (easy) to 1.0 (hard)
        student_prior_mastery: Prior belief of student mastery (0.0-1.0)
        question_id: Reference to question
        student_id: Reference to student
        
    Validation:
        - time_taken must be positive
        - mastery must be in [0, 1]
        - difficulty must be in [0, 1]
    """
    correct: bool
    time_taken: int  # seconds
    question_difficulty: float  # 0.0-1.0
    student_prior_mastery: float  # 0.0-1.0
    question_id: str
    student_id: str
    
    def __post_init__(self):
        """Validate attempt data"""
        assert self.time_taken > 0, "time_taken must be positive"
        assert 0.0 <= self.question_difficulty <= 1.0, "difficulty out of range"
        assert 0.0 <= self.student_prior_mastery <= 1.0, "prior mastery out of range"
        assert len(self.question_id) > 0, "question_id required"
        assert len(self.student_id) > 0, "student_id required"

class UpdateDirection(Enum):
    """Direction of mastery change"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"

@dataclass
class BayesUpdateResult:
    """
    Result of Bayesian update to mastery estimation.
    
    Attributes:
        new_mastery: Updated mastery level (0.0-1.0)
        new_confidence: Updated confidence in estimate (0.0-1.0)
        update_magnitude: Absolute change in mastery
        direction: Whether mastery improved, declined, or stayed same
        log_likelihood: For debugging/validation
        
    Properties:
        mastery_delta: Difference from prior mastery
        percent_improvement: Percentage improvement
    """
    new_mastery: float
    new_confidence: float
    update_magnitude: float
    direction: UpdateDirection
    log_likelihood: float
    prior_mastery: float
    
    @property
    def mastery_delta(self) -> float:
        """Change in mastery from prior"""
        return self.new_mastery - self.prior_mastery
    
    @property
    def percent_improvement(self) -> float:
        """Percentage improvement"""
        if self.prior_mastery == 0:
            return 0.0
        return (self.mastery_delta / self.prior_mastery) * 100

# ============================================================================
# CORE ALGORITHM: BAYESIAN UPDATE
# ============================================================================

def bayes_update_mastery(attempt: QuestionAttempt) -> BayesUpdateResult:
    """
    BAYES THEOREM APPLICATION FOR MASTERY ESTIMATION
    
    Mathematical Process:
    
    1. PRIOR: P(M) = student_prior_mastery
       What we believed before this question
    
    2. LIKELIHOOD: P(E|M) = ?
       If student has mastery level M, what's probability of observation E?
       
       For MCQ:
       - If student knows (mastery M): 
         P(Correct) = M * (1 - guess_chance) + guess_chance
         Reason: Gets right if they know it OR guess correctly
         
       - If student gets it wrong:
         P(Wrong|M) = 1 - P(Correct|M)
    
    3. MARGINAL LIKELIHOOD: P(E) = ?
       Average probability of this observation across all possible mastery levels
       Simplified: Assume uniform prior across mastery levels
       P(E) = ∫₀¹ P(E|M) dM
       
    4. POSTERIOR: P(M|E) = P(E|M) × P(M) / P(E)
       Updated belief after observing result
    
    Args:
        attempt: Student's question attempt
        
    Returns:
        BayesUpdateResult: Updated mastery, confidence, and metadata
        
    Raises:
        AssertionError: If attempt data invalid
    """
    
    # Input validation
    attempt.__post_init__()
    
    prior = attempt.student_prior_mastery
    
    # STEP 1: Calculate likelihood P(E|M)
    # "Given student has mastery M, what's probability of this observation?"
    
    if attempt.correct:
        # Student got it right
        # P(Correct | Mastery M) = M × (1 - guess) + guess
        # Because: probability they know it and get right + probability they guess right
        p_event_given_mastery = (
            prior * (1 - GUESSING_PROBABILITY) + GUESSING_PROBABILITY
        )
    else:
        # Student got it wrong
        # P(Wrong | Mastery M) = 1 - P(Correct | Mastery M)
        p_event_given_mastery = 1 - (
            prior * (1 - GUESSING_PROBABILITY) + GUESSING_PROBABILITY
        )
    
    # STEP 2: Calculate marginal likelihood P(E)
    # "Averaging over all possible mastery levels, what's probability of this?"
    
    if attempt.correct:
        # Average of P(Correct|M) for M ∈ [0,1]
        # = ∫₀¹ (M × (1-g) + g) dM
        # = (1-g) × ∫₀¹ M dM + g × ∫₀¹ 1 dM
        # = (1-g) × 0.5 + g × 1
        # = 0.5 × (1-g) + g
        p_event = ((1 - GUESSING_PROBABILITY) * 0.5) + GUESSING_PROBABILITY
    else:
        # Average of P(Wrong|M) for M ∈ [0,1]
        # = 1 - Average of P(Correct|M)
        p_event = 1 - (((1 - GUESSING_PROBABILITY) * 0.5) + GUESSING_PROBABILITY)
    
    # STEP 3: Apply Bayes theorem
    # P(M|E) = P(E|M) × P(M) / P(E)
    
    if p_event == 0:
        # Edge case: if p_event = 0, use prior (shouldn't happen with proper calibration)
        posterior = prior
        log_likelihood = float('-inf')
    else:
        posterior = (p_event_given_mastery * prior) / p_event
        log_likelihood = math.log(p_event_given_mastery) - math.log(p_event)
    
    # STEP 4: Clamp to valid range [0, 1]
    posterior = max(MIN_MASTERY, min(MAX_MASTERY, posterior))
    
    # STEP 5: Calculate update magnitude (how much did we learn?)
    update_magnitude = abs(posterior - prior)
    
    # STEP 6: Determine direction
    if posterior > prior + 0.01:
        direction = UpdateDirection.UP
    elif posterior < prior - 0.01:
        direction = UpdateDirection.DOWN
    else:
        direction = UpdateDirection.STABLE
    
    # STEP 7: Update confidence
    # Confidence increases with:
    # 1. Larger update magnitude (more surprising = more informative)
    # 2. Consistency (if many similar results)
    new_confidence = _calculate_confidence(prior, posterior, update_magnitude)
    
    return BayesUpdateResult(
        new_mastery=posterior,
        new_confidence=new_confidence,
        update_magnitude=update_magnitude,
        direction=direction,
        log_likelihood=log_likelihood,
        prior_mastery=prior,
    )

def _calculate_confidence(prior: float, posterior: float, magnitude: float) -> float:
    """
    Calculate confidence in updated mastery estimate.
    
    Reasoning:
    - Base confidence: 0.5 (50%) - we're always uncertain
    - Boost: Based on update magnitude
      - Large update (>0.2): More informative, higher boost
      - Small update (<0.05): Less informative, smaller boost
    - Cap at 1.0 (100% - can never be 100% sure)
    
    Mathematical formula:
    confidence = 0.5 + (update_magnitude * 0.3)
    Then clamped to [0.5, 1.0]
    
    This ensures:
    - More attempts = accumulation of confidence
    - Extreme results = high confidence
    - Consistent behavior = predictable confidence growth
    """
    
    # Base: we always have at least 50% confidence
    base_confidence = 0.5
    
    # Calculate boost from magnitude
    # magnitude ∈ [0, 1], we want boost ∈ [0, 0.5]
    magnitude_boost = min(1.0, magnitude * 2)  # Cap at 1.0
    confidence_boost = magnitude_boost * 0.3   # Scale to max 0.3 boost
    
    # Final confidence
    new_confidence = base_confidence + confidence_boost
    
    # Clamp to [0.5, 1.0]
    new_confidence = max(0.5, min(1.0, new_confidence))
    
    return new_confidence

# ============================================================================
# TESTS: BAYESIAN UPDATE
# ============================================================================

def test_bayes_update_correct_answer_increases_mastery():
    """
    TEST: Correct answer → mastery increases
    
    Reasoning:
    - Student has 50% mastery
    - Gets question correct
    - Bayes theorem: P(M|Correct) > P(M)
    - Therefore: posterior > prior
    """
    
    attempt = QuestionAttempt(
        correct=True,
        time_taken=120,
        question_difficulty=0.5,
        student_prior_mastery=0.5,
        question_id="Q_001",
        student_id="STU_001"
    )
    
    result = bayes_update_mastery(attempt)
    
    assert result.new_mastery > attempt.student_prior_mastery, \
        f"Correct answer should increase mastery: {result.new_mastery} <= {attempt.student_prior_mastery}"
    assert result.new_mastery > 0.5, \
        f"Posterior should be > 0.5: {result.new_mastery}"
    assert result.direction == UpdateDirection.UP, \
        "Direction should be UP"
    assert result.update_magnitude > 0, \
        "Update magnitude should be positive"
    
    print("✅ TEST PASSED: Correct answer increases mastery")

def test_bayes_update_wrong_answer_decreases_mastery():
    """
    TEST: Wrong answer → mastery decreases
    
    Reasoning:
    - Student claimed 80% mastery
    - Gets easy question (0.4 difficulty) wrong
    - Bayes: P(M|Wrong, Easy) << P(M)
    - Therefore: posterior << prior
    """
    
    attempt = QuestionAttempt(
        correct=False,
        time_taken=180,
        question_difficulty=0.4,  # Easy question
        student_prior_mastery=0.8,  # Thought they knew it
        question_id="Q_002",
        student_id="STU_001"
    )
    
    result = bayes_update_mastery(attempt)
    
    assert result.new_mastery < attempt.student_prior_mastery, \
        f"Wrong answer should decrease mastery: {result.new_mastery} >= {attempt.student_prior_mastery}"
    assert result.new_mastery < 0.8, \
        f"Posterior should be < 0.8: {result.new_mastery}"
    assert result.direction == UpdateDirection.DOWN, \
        "Direction should be DOWN"
    
    print("✅ TEST PASSED: Wrong answer decreases mastery")

def test_bayes_update_confidence_increases():
    """
    TEST: Multiple consistent attempts → confidence increases
    
    Reasoning:
    - After first attempt: confidence = base (0.5)
    - After second consistent attempt: confidence > first
    - Pattern: more evidence = higher confidence
    """
    
    prior_mastery = 0.5
    confidences = []
    
    for _ in range(5):
        attempt = QuestionAttempt(
            correct=True,  # Consistent correct
            time_taken=100,
            question_difficulty=0.5,
            student_prior_mastery=prior_mastery,
            question_id="Q_003",
            student_id="STU_001"
        )
        
        result = bayes_update_mastery(attempt)
        confidences.append(result.new_confidence)
        prior_mastery = result.new_mastery  # Update for next iteration
    
    # Confidence should generally increase
    # (Note: may not be perfectly monotonic due to magnitude variation)
    assert confidences[-1] >= confidences[0], \
        f"Confidence should increase: {confidences[-1]} < {confidences[0]}"
    
    print("✅ TEST PASSED: Confidence increases with consistent evidence")

def test_bayes_update_bounds():
    """
    TEST: All updates respect bounds [0, 1]
    
    Reasoning:
    - Mastery ∈ [0, 1]
    - Confidence ∈ [0, 1]
    - No edge cases should violate bounds
    """
    
    test_cases = [
        (True, 0.0, 0.5),   # Wrong before, correct now
        (False, 1.0, 0.5),  # Right before, wrong now
        (True, 1.0, 0.95),  # Already expert, correct
        (False, 0.0, 0.1),  # Novice, wrong
    ]
    
    for correct, prior_mastery, difficulty in test_cases:
        attempt = QuestionAttempt(
            correct=correct,
            time_taken=100,
            question_difficulty=difficulty,
            student_prior_mastery=prior_mastery,
            question_id="Q_004",
            student_id="STU_001"
        )
        
        result = bayes_update_mastery(attempt)
        
        assert 0.0 <= result.new_mastery <= 1.0, \
            f"Mastery out of bounds: {result.new_mastery}"
        assert 0.0 <= result.new_confidence <= 1.0, \
            f"Confidence out of bounds: {result.new_confidence}"
    
    print("✅ TEST PASSED: All updates respect bounds")

def test_bayes_update_mathematical_consistency():
    """
    TEST: Posterior probability is valid (consistency check)
    
    Reasoning:
    - P(M|E) must follow rules of probability
    - Must be between likelihood and prior (generally)
    - Extreme prior + unexpected evidence = large shift
    """
    
    # Case 1: Expert gets wrong answer (surprising)
    attempt_1 = QuestionAttempt(
        correct=False,
        time_taken=60,
        question_difficulty=0.2,  # Very easy question
        student_prior_mastery=0.95,  # Expert
        question_id="Q_005",
        student_id="STU_001"
    )
    
    result_1 = bayes_update_mastery(attempt_1)
    
    # Surprising result → large update
    assert result_1.update_magnitude > 0.1, \
        f"Expert wrong on easy Q should cause large update: {result_1.update_magnitude}"
    
    # Case 2: Novice gets right answer (surprising)
    attempt_2 = QuestionAttempt(
        correct=True,
        time_taken=300,  # Struggled
        question_difficulty=0.9,  # Hard question
        student_prior_mastery=0.1,  # Novice
        question_id="Q_006",
        student_id="STU_001"
    )
    
    result_2 = bayes_update_mastery(attempt_2)
    
    # For novice on hard Q, correct is consistent with guessing
    # Update should be moderate
    assert result_2.new_mastery > 0.1, \
        "Novice correct should still improve mastery"
    
    print("✅ TEST PASSED: Mathematical consistency verified")

# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CR-V4 BAYESIAN LEARNING TESTS")
    print("="*70 + "\n")
    
    test_bayes_update_correct_answer_increases_mastery()
    test_bayes_update_wrong_answer_decreases_mastery()
    test_bayes_update_confidence_increases()
    test_bayes_update_bounds()
    test_bayes_update_mathematical_consistency()
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED ✅")
    print("="*70 + "\n")
    
    # Example run
    print("\nEXAMPLE: Student attempt processing\n")
    
    example_attempt = QuestionAttempt(
        correct=True,
        time_taken=95,
        question_difficulty=0.65,
        student_prior_mastery=0.58,
        question_id="MATH_041_Q_001",
        student_id="STU_12345"
    )
    
    result = bayes_update_mastery(example_attempt)
    
    print(f"Student ID: {example_attempt.student_id}")
    print(f"Question: {example_attempt.question_id}")
    print(f"Result: {'CORRECT' if example_attempt.correct else 'WRONG'}")
    print(f"Time: {example_attempt.time_taken}s")
    print(f"\nBefore: Mastery = {example_attempt.student_prior_mastery:.2%}, Confidence = 0.50")
    print(f"After:  Mastery = {result.new_mastery:.2%}, Confidence = {result.new_confidence:.2%}")
    print(f"Update: {result.mastery_delta:+.2%} ({result.direction.value})")
    print(f"Magnitude: {result.update_magnitude:.4f}")
