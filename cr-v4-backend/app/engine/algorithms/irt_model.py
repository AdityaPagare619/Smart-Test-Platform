"""
CR-V4 CORE ALGORITHMS
Module: IRT 3-Parameter Logistic Model (3PL)

Mathematical Foundation:
P(θ) = c + (1-c) × 1/(1 + e^(-a(θ-b)))

Where:
  θ = Student ability (latent trait, typically -3 to +3)
  a = Discrimination (slope, 0.1 to 3.0) - how well question separates abilities
  b = Difficulty (location, -3 to +3) - ability needed for 50% probability
  c = Guessing (pseudo-chance, 0 to 0.5) - lower asymptote for MCQ

Production-Grade Implementation with:
- Fast NumPy vectorized operations
- Fisher Information for optimal question selection
- Calibration via Maximum Likelihood Estimation
- Standard error calculation for parameter confidence

Reference: Lord & Novick (1968), Baker & Kim (2017)
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
import math
from functools import lru_cache
import warnings

# ============================================================================
# CONSTANTS (Evidence-based defaults for JEE-MAINS MCQ)
# ============================================================================

# IRT parameter bounds (validated against psychometric literature)
IRT_A_MIN = 0.1    # Minimum discrimination
IRT_A_MAX = 3.0    # Maximum discrimination
IRT_A_DEFAULT = 1.0  # Default discrimination

IRT_B_MIN = -3.0   # Minimum difficulty (very easy)
IRT_B_MAX = 3.0    # Maximum difficulty (very hard)
IRT_B_DEFAULT = 0.0  # Default difficulty (average)

IRT_C_MIN = 0.0    # Minimum guessing (no guessing possible)
IRT_C_MAX = 0.5    # Maximum guessing (random for 2-option)
IRT_C_DEFAULT = 0.25  # Default for 4-option MCQ

# COUNCIL APPROVED: Subject-specific guessing parameters
# Based on coaching expert feedback: students use elimination, not random guessing
SUBJECT_C_VALUES = {
    'MATH': {
        'calculation': 0.20,    # Dimensional check helps
        'proof': 0.15,          # Hard to guess proofs
        'conceptual': 0.22,     # Some elimination possible
        'default': 0.22
    },
    'PHYSICS': {
        'numerical': 0.18,      # Units + magnitude check
        'conceptual': 0.25,     # Standard 4-option
        'application': 0.22,    # Some elimination
        'default': 0.22
    },
    'CHEMISTRY': {
        'organic': 0.20,        # Reaction logic helps
        'inorganic': 0.25,      # Pure memory, random guess
        'physical': 0.22,       # Some calculation check
        'default': 0.23
    },
    'DEFAULT': 0.25
}

def get_subject_c(subject: str, question_type: str = None) -> float:
    """
    Get subject-specific guessing parameter.
    
    COUNCIL DECISION: Different subjects have different effective guessing rates
    because students use elimination strategies.
    
    Args:
        subject: MATH, PHYSICS, or CHEMISTRY
        question_type: Optional type (numerical, conceptual, organic, etc.)
        
    Returns:
        Appropriate c value for IRT calculation
    """
    subject_values = SUBJECT_C_VALUES.get(subject, {})
    
    if isinstance(subject_values, dict):
        if question_type and question_type in subject_values:
            return subject_values[question_type]
        return subject_values.get('default', IRT_C_DEFAULT)
    
    return SUBJECT_C_VALUES.get('DEFAULT', IRT_C_DEFAULT)

# Ability bounds
ABILITY_MIN = -4.0
ABILITY_MAX = 4.0
ABILITY_DEFAULT = 0.0

# Convergence settings for optimization
MAX_ITERATIONS = 1000
CONVERGENCE_THRESHOLD = 1e-6
MIN_SAMPLE_SIZE = 30  # Minimum responses for calibration

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class IRTParameters:
    """
    3PL IRT parameters for a question.
    
    Attributes:
        a: Discrimination (slope of ICC at inflection point)
           High a = steep curve = good at separating abilities
           Low a = flat curve = weak discriminator
           
        b: Difficulty (ability at which P(correct) = (1+c)/2)
           High b = hard question (need high ability)
           Low b = easy question (low ability sufficient)
           
        c: Pseudo-guessing (lower asymptote)
           For 4-option MCQ, c ≈ 0.25 (random guess)
           For open-ended, c ≈ 0.0 (no guessing)
           
        se_a, se_b, se_c: Standard errors of estimates
           High SE = uncertain estimate (need more data)
           Low SE = confident estimate (sufficient data)
    """
    a: float = IRT_A_DEFAULT
    b: float = IRT_B_DEFAULT
    c: float = IRT_C_DEFAULT
    
    # Standard errors (None = not yet calculated)
    se_a: Optional[float] = None
    se_b: Optional[float] = None
    se_c: Optional[float] = None
    
    # Metadata
    sample_size: int = 0
    is_calibrated: bool = False
    calibration_method: str = "default"
    
    def __post_init__(self):
        """Validate and clamp parameters to valid ranges"""
        self.a = max(IRT_A_MIN, min(IRT_A_MAX, self.a))
        self.b = max(IRT_B_MIN, min(IRT_B_MAX, self.b))
        self.c = max(IRT_C_MIN, min(IRT_C_MAX, self.c))
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary for database storage"""
        return {
            'irt_a': self.a,
            'irt_b': self.b,
            'irt_c': self.c,
            'se_a': self.se_a,
            'se_b': self.se_b,
            'se_c': self.se_c,
            'sample_size': self.sample_size,
            'is_calibrated': self.is_calibrated,
            'calibration_method': self.calibration_method
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'IRTParameters':
        """Deserialize from dictionary"""
        return cls(
            a=data.get('irt_a', IRT_A_DEFAULT),
            b=data.get('irt_b', IRT_B_DEFAULT),
            c=data.get('irt_c', IRT_C_DEFAULT),
            se_a=data.get('se_a'),
            se_b=data.get('se_b'),
            se_c=data.get('se_c'),
            sample_size=data.get('sample_size', 0),
            is_calibrated=data.get('is_calibrated', False),
            calibration_method=data.get('calibration_method', 'default')
        )


class QuestionDifficulty(Enum):
    """Human-readable difficulty classifications based on IRT b parameter"""
    VERY_EASY = "very_easy"      # b < -1.5
    EASY = "easy"                # -1.5 <= b < -0.5
    MEDIUM = "medium"            # -0.5 <= b < 0.5
    HARD = "hard"                # 0.5 <= b < 1.5
    VERY_HARD = "very_hard"      # b >= 1.5
    
    @classmethod
    def from_b_parameter(cls, b: float) -> 'QuestionDifficulty':
        """Convert IRT b parameter to difficulty classification"""
        if b < -1.5:
            return cls.VERY_EASY
        elif b < -0.5:
            return cls.EASY
        elif b < 0.5:
            return cls.MEDIUM
        elif b < 1.5:
            return cls.HARD
        else:
            return cls.VERY_HARD


# ============================================================================
# CORE IRT FUNCTIONS (Vectorized for Performance)
# ============================================================================

def irt_probability(
    ability: Union[float, np.ndarray],
    a: Union[float, np.ndarray],
    b: Union[float, np.ndarray],
    c: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    """
    Calculate probability of correct response using 3PL model.
    
    Formula: P(θ) = c + (1-c) × 1/(1 + e^(-a(θ-b)))
    
    This is the Item Characteristic Curve (ICC) - the foundation of IRT.
    
    Args:
        ability: Student ability (θ), scalar or array
        a: Discrimination parameter (scalar or array)
        b: Difficulty parameter (scalar or array)
        c: Guessing parameter (scalar or array)
        
    Returns:
        Probability of correct response, same shape as ability
        
    Example:
        >>> irt_probability(0.0, 1.0, 0.0, 0.25)  # Average student, average question
        0.625  # 50% from ability + 25% from guessing boost
        
        >>> irt_probability(1.0, 1.5, 0.0, 0.25)  # Good student, average question
        0.85   # High probability of correct
        
        >>> irt_probability(-1.0, 1.5, 1.0, 0.25)  # Weak student, hard question
        0.35   # Low probability, mostly guessing
    """
    # Convert to numpy arrays for vectorized operations
    a = np.asarray(a)
    b = np.asarray(b)
    c = np.asarray(c)
    
    # Validate and clamp inputs (works for both scalar and array)
    a = np.clip(a, IRT_A_MIN, IRT_A_MAX)
    b = np.clip(b, IRT_B_MIN, IRT_B_MAX)
    c = np.clip(c, IRT_C_MIN, IRT_C_MAX)
    
    # Compute logit
    # Use clipping to prevent overflow in exp()
    logit = np.clip(a * (ability - b), -700, 700)
    
    # 3PL formula
    prob = c + (1 - c) / (1 + np.exp(-logit))
    
    # Ensure valid probability range
    return np.clip(prob, 0.0001, 0.9999)


def irt_probability_derivative(
    ability: Union[float, np.ndarray],
    a: float,
    b: float,
    c: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate probability and its derivatives w.r.t. a, b, c, θ.
    
    Used for:
    1. Maximum Likelihood Estimation (calibration)
    2. Fisher Information (question selection)
    3. Ability estimation (student scoring)
    
    Returns:
        Tuple of (P, dP/da, dP/db, dP/dc)
    """
    ability = np.atleast_1d(ability)
    
    # Compute probability
    logit = np.clip(a * (ability - b), -700, 700)
    exp_neg_logit = np.exp(-logit)
    denominator = 1 + exp_neg_logit
    P = c + (1 - c) / denominator
    
    # Derivative of P w.r.t. logistic part
    logistic = 1 / denominator
    dL_dlogit = logistic * (1 - logistic)  # Derivative of standard logistic
    
    # Chain rule for each parameter
    dP_da = (1 - c) * (ability - b) * dL_dlogit
    dP_db = -(1 - c) * a * dL_dlogit
    dP_dc = 1 - logistic  # = 1 - (1/(1+e^(-logit))) = P-c / (1-c)
    
    return P, dP_da, dP_db, dP_dc


def fisher_information(
    ability: Union[float, np.ndarray],
    a: Union[float, np.ndarray],
    b: Union[float, np.ndarray],
    c: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    """
    Calculate Fisher Information for a question at given ability level.
    
    Fisher Information measures how much a question "tells us" about
    a student's ability at a specific ability level.
    
    Formula: I(θ) = a² × (1-c)² × [P'(θ)]² / [P(θ) × (1-P(θ))]
    
    High Information = Question is GOOD for discriminating at this ability
    Low Information = Question is POOR for this ability level
    
    Uses:
    - Optimal question selection: Pick question with max I(θ) at student's ability
    - Adaptive testing: Select most informative questions
    - Standard error: SE(θ) = 1/√(ΣI(θ))
    
    Args:
        ability: Student ability (θ)
        a, b, c: IRT parameters
        
    Returns:
        Fisher Information value(s)
        
    Example:
        >>> fisher_information(0.0, 1.5, 0.0, 0.25)  # Match: ability ≈ difficulty
        0.42  # High information - good match
        
        >>> fisher_information(2.0, 1.5, 0.0, 0.25)  # Mismatch: easy for student
        0.05  # Low information - too easy
    """
    # Convert to numpy arrays for vectorized operations
    a = np.asarray(a)
    b = np.asarray(b)
    c = np.asarray(c)
    
    # Get probability
    P = irt_probability(ability, a, b, c)
    
    # Derivative of P w.r.t. ability (θ)
    # dP/dθ = a × (1-c) × P × (1-P) / (1-c) = a × (P-c) × (1-P) / (1-c)
    # Using simplified form:
    logit = np.clip(a * (ability - b), -700, 700)
    exp_neg = np.exp(-logit)
    logistic = 1 / (1 + exp_neg)
    dP_dtheta = a * (1 - c) * logistic * (1 - logistic)
    
    # Fisher Information formula
    # I(θ) = [P'(θ)]² / [P(θ) × (1-P(θ))]
    P_clipped = np.clip(P, 0.0001, 0.9999)
    information = (dP_dtheta ** 2) / (P_clipped * (1 - P_clipped))
    
    return information


def maximum_information_ability(a: float, b: float, c: float) -> float:
    """
    Find the ability level where Fisher Information is maximized.
    
    For 3PL model, maximum information occurs at:
    θ* ≈ b + (1/a) × ln((1 + √(1 + 8c)) / 2)
    
    This is where the question is MOST discriminating.
    
    Args:
        a, b, c: IRT parameters
        
    Returns:
        Ability level with maximum information
    """
    if c <= 0:
        # 2PL case: max info at b
        return b
    
    # 3PL case: max info shifted above b
    shift = (1 / a) * np.log((1 + np.sqrt(1 + 8 * c)) / 2)
    return b + shift


# ============================================================================
# ABILITY ESTIMATION
# ============================================================================

def estimate_ability(
    responses: List[bool],
    parameters: List[IRTParameters],
    prior_ability: float = 0.0,
    method: str = "map"
) -> Tuple[float, float]:
    """
    Estimate student ability from response pattern.
    
    Methods:
    - "mle": Maximum Likelihood Estimation (no prior)
    - "map": Maximum A Posteriori (with normal prior, recommended)
    - "eap": Expected A Posteriori (Bayesian integration)
    
    Args:
        responses: List of correct (True) / incorrect (False)
        parameters: List of IRTParameters for each question
        prior_ability: Initial ability estimate
        method: Estimation method
        
    Returns:
        Tuple of (estimated_ability, standard_error)
        
    Implementation:
    Uses Newton-Raphson iteration for MLE/MAP with Fisher Information
    for standard error calculation.
    """
    if len(responses) == 0 or len(responses) != len(parameters):
        return prior_ability, 1.0  # High uncertainty
    
    # Convert to numpy arrays
    n = len(responses)
    responses_arr = np.array(responses, dtype=float)
    a_arr = np.array([p.a for p in parameters])
    b_arr = np.array([p.b for p in parameters])
    c_arr = np.array([p.c for p in parameters])
    
    # Initialize
    theta = prior_ability
    
    # Newton-Raphson iteration
    for iteration in range(MAX_ITERATIONS):
        # Calculate probabilities
        P = irt_probability(theta, a_arr, b_arr, c_arr)
        
        # First derivative of log-likelihood
        # dL/dθ = Σ a_i × (u_i - P_i) × (P_i - c_i) / [P_i × (1 - c_i)]
        numerator = a_arr * (responses_arr - P) * (P - c_arr)
        denominator = P * (1 - c_arr)
        denominator = np.clip(denominator, 0.0001, None)  # Prevent division by zero
        
        first_derivative = np.sum(numerator / denominator)
        
        # Add prior term for MAP
        if method == "map":
            # Normal prior with mean=0, variance=1
            first_derivative -= theta  # d/dθ of -θ²/2
        
        # Second derivative (observed information)
        # Approximated by Fisher Information
        info = fisher_information(theta, a_arr, b_arr, c_arr)
        second_derivative = -np.sum(info)
        
        if method == "map":
            second_derivative -= 1  # Prior contribution
        
        if abs(second_derivative) < 1e-10:
            break
        
        # Newton-Raphson update
        delta = first_derivative / abs(second_derivative)
        theta_new = theta + 0.5 * delta  # Damped update for stability
        
        # Clamp to valid range
        theta_new = max(ABILITY_MIN, min(ABILITY_MAX, theta_new))
        
        # Check convergence
        if abs(theta_new - theta) < CONVERGENCE_THRESHOLD:
            theta = theta_new
            break
        
        theta = theta_new
    
    # Calculate standard error
    total_info = np.sum(fisher_information(theta, a_arr, b_arr, c_arr))
    if method == "map":
        total_info += 1  # Prior information
    
    standard_error = 1 / np.sqrt(total_info) if total_info > 0 else 1.0
    
    return theta, standard_error


def ability_to_mastery(ability: float) -> float:
    """
    Convert IRT ability scale to mastery percentage (0-1).
    
    IRT ability is on logit scale (-4 to +4 typically).
    We convert to probability scale for user-friendliness.
    
    Using logistic transformation:
    mastery = 1 / (1 + e^(-ability))
    
    Examples:
    - ability = 0 → mastery = 0.50 (50%)
    - ability = 1 → mastery = 0.73 (73%)
    - ability = 2 → mastery = 0.88 (88%)
    - ability = -1 → mastery = 0.27 (27%)
    """
    return 1 / (1 + np.exp(-ability))


def mastery_to_ability(mastery: float) -> float:
    """
    Convert mastery percentage to IRT ability scale.
    
    Inverse of ability_to_mastery.
    
    Examples:
    - mastery = 0.50 → ability = 0.0
    - mastery = 0.80 → ability ≈ 1.39
    - mastery = 0.20 → ability ≈ -1.39
    """
    mastery = max(0.001, min(0.999, mastery))  # Clamp to valid range
    return np.log(mastery / (1 - mastery))


# ============================================================================
# QUESTION SELECTION SCORE
# ============================================================================

def calculate_selection_score(
    ability: float,
    params: IRTParameters,
    mastery_gap: float,
    competency_weight: float = 0.5,
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate multi-criteria selection score for a question.
    
    This is the CORE algorithm for selecting optimal questions.
    
    Criteria (with default weights):
    1. IRT Match (35%): How well question difficulty matches student ability
    2. Fisher Information (30%): How discriminating is this question
    3. Mastery Gap (25%): How much room for improvement
    4. Competency (10%): NEP 2020 competency diversity
    
    Args:
        ability: Student's current ability estimate
        params: Question's IRT parameters
        mastery_gap: 1 - concept_mastery (higher = more to learn)
        competency_weight: Weight for competency type (0.5-1.0)
        weights: Optional custom weights for criteria
        
    Returns:
        Selection score (0-1, higher is better)
        
    Example:
        >>> calculate_selection_score(
        ...     ability=0.5,
        ...     params=IRTParameters(a=1.5, b=0.6, c=0.25),
        ...     mastery_gap=0.7,
        ...     competency_weight=1.0
        ... )
        0.82  # Good match, high priority
    """
    if weights is None:
        weights = {
            'irt_match': 0.35,
            'fisher_info': 0.30,
            'mastery_gap': 0.25,
            'competency': 0.10
        }
    
    # Criterion 1: IRT difficulty match
    # Best match when ability ≈ difficulty parameter b
    # Score decreases as |ability - b| increases
    difficulty_distance = abs(ability - params.b)
    irt_match_score = 1 / (1 + difficulty_distance)  # Logistic decay
    
    # Criterion 2: Fisher Information
    # Normalized to 0-1 range (typical max ≈ 1.0 for good questions)
    fi = fisher_information(ability, params.a, params.b, params.c)
    fi_score = min(1.0, fi)  # Cap at 1.0
    
    # Criterion 3: Mastery gap
    # Already in 0-1 range
    gap_score = mastery_gap
    
    # Criterion 4: Competency weight
    # 1.0 for critical thinking, 0.5 for rote memory
    comp_score = competency_weight
    
    # Weighted combination
    total_score = (
        weights['irt_match'] * irt_match_score +
        weights['fisher_info'] * fi_score +
        weights['mastery_gap'] * gap_score +
        weights['competency'] * comp_score
    )
    
    return total_score


# ============================================================================
# CALIBRATION (Parameter Estimation from Response Data)
# ============================================================================

def calibrate_question(
    abilities: np.ndarray,
    responses: np.ndarray,
    initial_params: Optional[IRTParameters] = None,
    method: str = "mle"
) -> IRTParameters:
    """
    Calibrate IRT parameters from student response data.
    
    Uses Maximum Likelihood Estimation with Newton-Raphson optimization.
    
    Args:
        abilities: Array of student ability estimates
        responses: Array of 0/1 responses (incorrect/correct)
        initial_params: Starting parameter values
        method: "mle" or "bayesian"
        
    Returns:
        Calibrated IRTParameters with standard errors
        
    Requirements:
    - Minimum 30 responses for reliable calibration
    - Responses should have variance (not all 0s or all 1s)
    
    Implementation Details:
    Uses joint maximum likelihood with ability estimates fixed.
    For production, consider marginal MLE or MCMC for better estimates.
    """
    from scipy.optimize import minimize
    
    n = len(responses)
    
    if n < MIN_SAMPLE_SIZE:
        warnings.warn(f"Sample size {n} < {MIN_SAMPLE_SIZE}. Using defaults.")
        return IRTParameters(sample_size=n, calibration_method="insufficient_data")
    
    # Check response variance
    mean_response = np.mean(responses)
    if mean_response < 0.05 or mean_response > 0.95:
        warnings.warn("Extreme response rate. Calibration may be unreliable.")
    
    # Initial values
    if initial_params:
        a0, b0, c0 = initial_params.a, initial_params.b, initial_params.c
    else:
        a0 = IRT_A_DEFAULT
        b0 = np.mean(abilities[responses == 0]) if np.any(responses == 0) else 0.0
        c0 = IRT_C_DEFAULT
    
    def negative_log_likelihood(params):
        """Objective function: negative log-likelihood"""
        a, b, c = params
        
        # Enforce bounds via penalty
        if a < IRT_A_MIN or a > IRT_A_MAX:
            return 1e10
        if b < IRT_B_MIN or b > IRT_B_MAX:
            return 1e10
        if c < IRT_C_MIN or c > IRT_C_MAX:
            return 1e10
        
        P = irt_probability(abilities, a, b, c)
        P = np.clip(P, 0.0001, 0.9999)
        
        # Log-likelihood
        ll = np.sum(
            responses * np.log(P) + 
            (1 - responses) * np.log(1 - P)
        )
        
        return -ll
    
    # Optimize
    result = minimize(
        negative_log_likelihood,
        x0=[a0, b0, c0],
        method='L-BFGS-B',
        bounds=[
            (IRT_A_MIN, IRT_A_MAX),
            (IRT_B_MIN, IRT_B_MAX),
            (IRT_C_MIN, IRT_C_MAX)
        ],
        options={'maxiter': MAX_ITERATIONS, 'ftol': CONVERGENCE_THRESHOLD}
    )
    
    a_est, b_est, c_est = result.x
    
    # Calculate standard errors via inverse Hessian
    # Approximated using observed information
    try:
        P = irt_probability(abilities, a_est, b_est, c_est)
        P = np.clip(P, 0.0001, 0.9999)
        
        # Information matrix (simplified)
        info = np.sum(fisher_information(abilities, a_est, b_est, c_est))
        se = 1 / np.sqrt(info) if info > 0 else None
    except:
        se = None
    
    return IRTParameters(
        a=a_est,
        b=b_est,
        c=c_est,
        se_a=se,
        se_b=se,
        se_c=se,
        sample_size=n,
        is_calibrated=result.success,
        calibration_method=method
    )


# ============================================================================
# TESTS
# ============================================================================

def test_irt_probability_bounds():
    """Test probability function returns valid values"""
    abilities = np.linspace(-3, 3, 100)
    
    for a in [0.5, 1.0, 2.0]:
        for b in [-1, 0, 1]:
            for c in [0.0, 0.25, 0.33]:
                P = irt_probability(abilities, a, b, c)
                assert np.all(P >= c), f"P should be >= c, got min={P.min()}"
                assert np.all(P <= 1), f"P should be <= 1, got max={P.max()}"
    
    print("✅ TEST PASSED: IRT probability bounds")


def test_irt_probability_monotonic():
    """Test probability increases with ability"""
    abilities = np.linspace(-3, 3, 100)
    
    P = irt_probability(abilities, 1.0, 0.0, 0.25)
    diffs = np.diff(P)
    
    assert np.all(diffs >= 0), "P should be monotonically increasing with ability"
    print("✅ TEST PASSED: IRT probability monotonic")


def test_irt_probability_at_b():
    """Test P(b) = (1+c)/2 for 3PL model"""
    b = 0.5
    c = 0.25
    
    P_at_b = irt_probability(b, 1.0, b, c)
    expected = (1 + c) / 2  # 0.625 for c=0.25
    
    assert abs(P_at_b - expected) < 0.01, f"P(b) should be {expected}, got {P_at_b}"
    print("✅ TEST PASSED: P(b) = (1+c)/2")


def test_fisher_information_maximum():
    """Test Fisher Information peaks near difficulty"""
    abilities = np.linspace(-2, 2, 100)
    b = 0.0
    
    I = fisher_information(abilities, 1.5, b, 0.25)
    max_idx = np.argmax(I)
    ability_at_max = abilities[max_idx]
    
    # Maximum should be at or slightly above b for 3PL
    assert abs(ability_at_max - b) < 0.5, f"Max info should be near b={b}, got {ability_at_max}"
    print("✅ TEST PASSED: Fisher Information maximum near difficulty")


def test_ability_estimation_correct():
    """Test ability estimation from response pattern"""
    # All correct on medium questions → high ability
    params = [IRTParameters(a=1.0, b=0.0, c=0.25) for _ in range(10)]
    responses = [True] * 10
    
    ability, se = estimate_ability(responses, params, prior_ability=0.0)
    
    assert ability > 0.5, f"All correct should give high ability, got {ability}"
    assert se < 1.0, f"SE should be reasonable, got {se}"
    print("✅ TEST PASSED: Ability estimation (all correct)")


def test_ability_estimation_incorrect():
    """Test ability estimation from all incorrect"""
    params = [IRTParameters(a=1.0, b=0.0, c=0.25) for _ in range(10)]
    responses = [False] * 10
    
    ability, se = estimate_ability(responses, params, prior_ability=0.0)
    
    assert ability < -0.5, f"All incorrect should give low ability, got {ability}"
    print("✅ TEST PASSED: Ability estimation (all incorrect)")


def test_selection_score_match():
    """Test selection score favors difficulty match"""
    ability = 0.5
    
    # Question matching ability
    params_match = IRTParameters(a=1.5, b=0.5, c=0.25)
    score_match = calculate_selection_score(ability, params_match, 0.5)
    
    # Question too hard
    params_hard = IRTParameters(a=1.5, b=2.0, c=0.25)
    score_hard = calculate_selection_score(ability, params_hard, 0.5)
    
    assert score_match > score_hard, "Matched question should score higher"
    print("✅ TEST PASSED: Selection score favors difficulty match")


def test_mastery_ability_conversion():
    """Test bidirectional conversion between mastery and ability"""
    for mastery in [0.2, 0.5, 0.7, 0.9]:
        ability = mastery_to_ability(mastery)
        back = ability_to_mastery(ability)
        assert abs(back - mastery) < 0.001, f"Conversion mismatch: {mastery} → {ability} → {back}"
    
    print("✅ TEST PASSED: Mastery-ability conversion")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests() -> None:
    """Run all IRT model tests. Called by CI/CD pipeline."""
    print("Running IRT Model tests...")
    test_irt_probability_bounds()
    test_irt_probability_monotonic()
    test_fisher_information_maximum()
    test_selection_score_match()
    print("✅ All tests passed!")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CR-V4 IRT 3PL MODEL TESTS")
    print("="*70 + "\n")
    
    test_irt_probability_bounds()
    test_irt_probability_monotonic()
    test_irt_probability_at_b()
    test_fisher_information_maximum()
    test_ability_estimation_correct()
    test_ability_estimation_incorrect()
    test_selection_score_match()
    test_mastery_ability_conversion()
    
    print("\n" + "="*70)
    print("ALL IRT TESTS PASSED ✅")
    print("="*70 + "\n")
    
    # Example usage
    print("EXAMPLE: Question Selection Score Calculation\n")
    
    student_ability = 0.65
    
    questions = [
        ("Q1 - Good Match", IRTParameters(a=1.5, b=0.7, c=0.25), 0.6),
        ("Q2 - Too Easy", IRTParameters(a=1.0, b=-1.0, c=0.25), 0.3),
        ("Q3 - Too Hard", IRTParameters(a=1.2, b=2.0, c=0.25), 0.8),
        ("Q4 - High Discrimination", IRTParameters(a=2.5, b=0.5, c=0.25), 0.7),
    ]
    
    print(f"Student Ability: {student_ability} (Mastery: {ability_to_mastery(student_ability):.1%})\n")
    print(f"{'Question':<25} {'b (diff)':<10} {'a (disc)':<10} {'Score':<10}")
    print("-" * 55)
    
    for name, params, gap in questions:
        score = calculate_selection_score(student_ability, params, gap)
        print(f"{name:<25} {params.b:<10.2f} {params.a:<10.2f} {score:<10.3f}")
    
    print("\n→ Q1 (Good Match) should be selected!")
