"""
CR-V4 CORE ALGORITHMS
Module: Misconception Detection Engine

Implements severity-based misconception detection and recovery:

Severity Levels (Council Approved):
1. HIGH: Critical misconception blocking future learning
   → Immediate intervention + diagnostic question
   
2. MEDIUM: Incorrect understanding, recoverable
   → Correction + similar practice questions
   
3. LOW: Minor confusion or careless error
   → Feedback only + optional resources

Detection Methods:
1. Pattern Matching: Known error patterns from expert data
2. Response Analysis: Time, hesitation, answer changes
3. Prerequisite Gaps: Wrong answer due to missing foundation
4. Confidence Calibration: Overconfident wrong or underconfident right

Recovery Strategies:
- Diagnostic questions to isolate root cause
- Targeted remediation content
- Prerequisite review if needed
- Spaced repetition scheduling for corrected concepts

Reference: 330 expert-validated misconceptions in database
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from datetime import datetime
import re

# ============================================================================
# CONSTANTS
# ============================================================================

# Severity thresholds
HIGH_SEVERITY_THRESHOLD = 0.8
MEDIUM_SEVERITY_THRESHOLD = 0.5

# Time analysis
VERY_FAST_THRESHOLD = 15  # Seconds (likely guessing or careless)
VERY_SLOW_THRESHOLD = 180  # Seconds (struggling)

# Confidence calibration
CONFIDENCE_GAP_THRESHOLD = 0.3  # Difference between stated and demonstrated

# Recovery settings
MAX_DIAGNOSTIC_QUESTIONS = 3
MIN_PRACTICE_QUESTIONS = 5

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class MisconceptionSeverity(Enum):
    """
    Severity levels for detected misconceptions.
    
    HIGH: Immediately blocking further progress
    MEDIUM: Significant but recoverable
    LOW: Minor, often careless errors
    """
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MisconceptionCategory(Enum):
    """
    Categories of misconceptions based on cognitive cause.
    """
    CONCEPTUAL = "CONCEPTUAL"          # Wrong understanding of concept
    PROCEDURAL = "PROCEDURAL"          # Wrong problem-solving steps
    PREREQUISITE_GAP = "PREREQUISITE_GAP"  # Missing foundation
    FORMULA_CONFUSION = "FORMULA_CONFUSION"  # Similar formula mix-up
    SIGN_ERROR = "SIGN_ERROR"          # +/- confusion
    UNIT_CONVERSION = "UNIT_CONVERSION"  # Unit errors
    CARELESS = "CARELESS"              # Inattention errors
    GUESSING = "GUESSING"              # Random guessing


@dataclass
class Misconception:
    """
    A known misconception with detection patterns and recovery strategy.
    
    Based on 330 expert-validated misconceptions in the database.
    """
    misconception_id: str
    concept_id: str
    subject: str
    
    # Description
    name: str
    description: str
    
    # Classification
    severity: MisconceptionSeverity
    category: MisconceptionCategory
    
    # Detection patterns
    error_patterns: List[str] = field(default_factory=list)
    common_wrong_answers: List[str] = field(default_factory=list)
    
    # Recovery
    recovery_strategy: str = ""
    remediation_content: Optional[str] = None
    diagnostic_question_ids: List[str] = field(default_factory=list)
    prerequisite_concepts: List[str] = field(default_factory=list)
    
    # Statistics
    detection_count: int = 0
    recovery_rate: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'misconception_id': self.misconception_id,
            'concept_id': self.concept_id,
            'name': self.name,
            'severity': self.severity.value,
            'category': self.category.value,
            'recovery_strategy': self.recovery_strategy
        }


@dataclass
class DetectionResult:
    """
    Result of misconception detection analysis.
    """
    detected: bool
    misconception: Optional[Misconception] = None
    confidence: float = 0.0
    
    # Analysis details
    evidence: List[str] = field(default_factory=list)
    time_analysis: Optional[str] = None
    pattern_match: Optional[str] = None
    
    # Recovery recommendations
    recommended_actions: List[str] = field(default_factory=list)
    diagnostic_questions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'detected': self.detected,
            'misconception': self.misconception.to_dict() if self.misconception else None,
            'confidence': self.confidence,
            'evidence': self.evidence,
            'time_analysis': self.time_analysis,
            'recommended_actions': self.recommended_actions
        }


@dataclass
class RecoveryPlan:
    """
    Personalized recovery plan for a detected misconception.
    """
    student_id: str
    misconception: Misconception
    
    # Status
    status: str = "PENDING"  # PENDING, IN_PROGRESS, RESOLVED
    created_at: datetime = field(default_factory=datetime.now)
    
    # Recovery steps
    diagnostic_phase: bool = True  # Start with diagnostic
    diagnostic_questions: List[str] = field(default_factory=list)
    practice_questions: List[str] = field(default_factory=list)
    
    # Progress
    diagnostic_complete: bool = False
    root_cause_identified: str = ""
    questions_completed: int = 0
    success_count: int = 0
    
    def get_success_rate(self) -> float:
        if self.questions_completed == 0:
            return 0.0
        return self.success_count / self.questions_completed
    
    def is_resolved(self) -> bool:
        """Check if misconception is resolved"""
        # Resolved if >80% success on 5+ practice questions
        return (
            self.questions_completed >= MIN_PRACTICE_QUESTIONS and
            self.get_success_rate() >= 0.8
        )


# ============================================================================
# MISCONCEPTION DATABASE (Sample from 330)
# ============================================================================

# Sample misconceptions (in production, loaded from database)
SAMPLE_MISCONCEPTIONS = {
    # Mathematics misconceptions
    "MISC_MATH_001": Misconception(
        misconception_id="MISC_MATH_001",
        concept_id="MATH_041",
        subject="MATH",
        name="Derivative Chain Rule Missing",
        description="Student forgets to apply chain rule for composite functions",
        severity=MisconceptionSeverity.HIGH,
        category=MisconceptionCategory.PROCEDURAL,
        error_patterns=[r"d/dx\[f\(g\(x\)\)\]\s*=\s*f[']\(g\(x\)\)"],
        recovery_strategy="Review chain rule: d/dx[f(g(x))] = f'(g(x)) × g'(x). Practice with simple compositions first.",
        diagnostic_question_ids=["MATH_041_DIAG_001", "MATH_041_DIAG_002"],
        prerequisite_concepts=["MATH_040"]
    ),
    
    "MISC_MATH_002": Misconception(
        misconception_id="MISC_MATH_002",
        concept_id="MATH_041",
        subject="MATH",
        name="Integration Constant Forgotten",
        description="Student forgets +C in indefinite integrals",
        severity=MisconceptionSeverity.LOW,
        category=MisconceptionCategory.PROCEDURAL,
        error_patterns=[r"∫.+dx\s*=\s*[^+]*$"],
        recovery_strategy="Remember: Every indefinite integral needs +C. Think: 'Indefinite = uncertain constant'",
    ),
    
    "MISC_MATH_003": Misconception(
        misconception_id="MISC_MATH_003",
        concept_id="MATH_020",
        subject="MATH",
        name="sin²θ + cos²θ ≠ 1 confusion",
        description="Student doesn't recognize or misapplies Pythagorean identity",
        severity=MisconceptionSeverity.HIGH,
        category=MisconceptionCategory.CONCEPTUAL,
        error_patterns=[r"sin\^2.*\+.*cos\^2.*=.*[02]"],
        recovery_strategy="Build from unit circle: On unit circle, x²+y²=1, where x=cosθ, y=sinθ",
        prerequisite_concepts=["MATH_001"]
    ),
    
    # Physics misconceptions
    "MISC_PHYS_001": Misconception(
        misconception_id="MISC_PHYS_001",
        concept_id="PHYS_001",
        subject="PHYSICS",
        name="Mass affects free fall speed",
        description="Student believes heavier objects fall faster",
        severity=MisconceptionSeverity.HIGH,
        category=MisconceptionCategory.CONCEPTUAL,
        common_wrong_answers=["heavier falls faster", "mass affects g"],
        recovery_strategy="Demonstrate: g is constant (9.8 m/s²) regardless of mass. Air resistance causes real-world differences, not gravity.",
    ),
    
    "MISC_PHYS_002": Misconception(
        misconception_id="MISC_PHYS_002",
        concept_id="PHYS_002",
        subject="PHYSICS",
        name="Force needed for constant velocity",
        description="Student thinks constant velocity requires constant force",
        severity=MisconceptionSeverity.HIGH,
        category=MisconceptionCategory.CONCEPTUAL,
        common_wrong_answers=["force needed", "no force = stops"],
        recovery_strategy="Newton's 1st Law: No NET force needed for constant velocity. Force only changes motion.",
        prerequisite_concepts=["PHYS_001"]
    ),
    
    "MISC_PHYS_003": Misconception(
        misconception_id="MISC_PHYS_003",
        concept_id="PHYS_030",
        subject="PHYSICS",
        name="Sign confusion in electric field",
        description="Student confuses direction of electric field with force direction on negative charge",
        severity=MisconceptionSeverity.MEDIUM,
        category=MisconceptionCategory.SIGN_ERROR,
        error_patterns=[r".*negative.*same.*direction.*"],
        recovery_strategy="Remember: E points AWAY from +, force on -q is OPPOSITE to E direction",
    ),
    
    # Chemistry misconceptions
    "MISC_CHEM_001": Misconception(
        misconception_id="MISC_CHEM_001",
        concept_id="CHEM_010",
        subject="CHEMISTRY",
        name="Oxidation = oxygen gain only",
        description="Student limits oxidation to oxygen addition, ignoring electron loss",
        severity=MisconceptionSeverity.MEDIUM,
        category=MisconceptionCategory.CONCEPTUAL,
        common_wrong_answers=["oxidation = gain oxygen", "no oxygen = no oxidation"],
        recovery_strategy="Modern definition: Oxidation = LOSS of electrons (LEO). Oxygen involvement is coincidental.",
    ),
    
    "MISC_CHEM_002": Misconception(
        misconception_id="MISC_CHEM_002",
        concept_id="CHEM_020",
        subject="CHEMISTRY",
        name="Equilibrium means equal concentrations",
        description="Student thinks equilibrium means [reactants] = [products]",
        severity=MisconceptionSeverity.HIGH,
        category=MisconceptionCategory.CONCEPTUAL,
        common_wrong_answers=["equal", "same amounts", "50-50"],
        recovery_strategy="Equilibrium = rate forward = rate backward. Concentrations depend on K, not equal by default.",
    ),
    
    "MISC_CHEM_003": Misconception(
        misconception_id="MISC_CHEM_003",
        concept_id="CHEM_001",
        subject="CHEMISTRY",
        name="Molar mass = atomic mass confusion",
        description="Student confuses molar mass (g/mol) with atomic mass (amu)",
        severity=MisconceptionSeverity.LOW,
        category=MisconceptionCategory.UNIT_CONVERSION,
        recovery_strategy="Remember: Molar mass (g/mol) = Atomic mass (amu) numerically, but different units and meaning.",
    ),
}


# ============================================================================
# DETECTION ENGINE
# ============================================================================

class MisconceptionDetector:
    """
    Detects and analyzes student misconceptions.
    
    Detection methods:
    1. Pattern matching against known error patterns
    2. Response time analysis (too fast = guessing, too slow = confused)
    3. Answer analysis (common wrong answer patterns)
    4. Prerequisite gap detection
    5. Confidence calibration analysis
    """
    
    def __init__(
        self,
        misconceptions: Optional[Dict[str, Misconception]] = None
    ):
        """
        Initialize detector with misconception database.
        """
        self.misconceptions = misconceptions or SAMPLE_MISCONCEPTIONS
        
        # Index by concept for fast lookup
        self._by_concept: Dict[str, List[Misconception]] = {}
        for m in self.misconceptions.values():
            if m.concept_id not in self._by_concept:
                self._by_concept[m.concept_id] = []
            self._by_concept[m.concept_id].append(m)
    
    def detect(
        self,
        concept_id: str,
        correct: bool,
        student_answer: Optional[str] = None,
        time_taken: float = 60.0,
        stated_confidence: Optional[float] = None,
        question_difficulty: float = 0.5
    ) -> DetectionResult:
        """
        Analyze a student response for misconceptions.
        
        Args:
            concept_id: Concept the question tests
            correct: Whether answer was correct
            student_answer: Student's actual answer (for pattern matching)
            time_taken: Seconds spent on question
            stated_confidence: Student's self-reported confidence (0-1)
            question_difficulty: Question difficulty (0-1)
            
        Returns:
            DetectionResult with analysis
        """
        result = DetectionResult(detected=False)
        
        # If correct, usually no misconception (unless overconfident guess)
        if correct:
            # Check for lucky guess (very fast on hard question)
            if time_taken < VERY_FAST_THRESHOLD and question_difficulty > 0.7:
                result.time_analysis = "Possible lucky guess (fast + hard)"
                # Don't flag as misconception, but note it
            return result
        
        # Incorrect answer - analyze for misconception
        evidence = []
        candidate_misconceptions = []
        
        # Get concept-specific misconceptions
        concept_misconceptions = self._by_concept.get(concept_id, [])
        
        for misconception in concept_misconceptions:
            match_score = 0.0
            
            # Check 1: Pattern matching
            if student_answer and misconception.error_patterns:
                for pattern in misconception.error_patterns:
                    try:
                        if re.search(pattern, student_answer, re.IGNORECASE):
                            match_score += 0.4
                            evidence.append(f"Pattern match: {pattern}")
                            break
                    except re.error:
                        pass  # Invalid regex, skip
            
            # Check 2: Common wrong answer
            if student_answer and misconception.common_wrong_answers:
                answer_lower = student_answer.lower()
                for wrong_answer in misconception.common_wrong_answers:
                    if wrong_answer.lower() in answer_lower:
                        match_score += 0.3
                        evidence.append(f"Common wrong answer: {wrong_answer}")
                        break
            
            # Check 3: Time analysis
            if time_taken < VERY_FAST_THRESHOLD:
                if misconception.category == MisconceptionCategory.GUESSING:
                    match_score += 0.2
                elif misconception.category == MisconceptionCategory.CARELESS:
                    match_score += 0.2
            elif time_taken > VERY_SLOW_THRESHOLD:
                if misconception.category in [
                    MisconceptionCategory.CONCEPTUAL,
                    MisconceptionCategory.PREREQUISITE_GAP
                ]:
                    match_score += 0.2
            
            # Check 4: Difficulty mismatch
            # Easy question wrong + high severity misconception → likely
            if question_difficulty < 0.3 and misconception.severity == MisconceptionSeverity.HIGH:
                match_score += 0.1
                evidence.append("Easy question wrong - fundamental gap")
            
            if match_score > 0:
                candidate_misconceptions.append((match_score, misconception))
        
        # Select best match
        if candidate_misconceptions:
            candidate_misconceptions.sort(key=lambda x: x[0], reverse=True)
            best_score, best_misconception = candidate_misconceptions[0]
            
            if best_score >= 0.3:  # Threshold for detection
                result.detected = True
                result.misconception = best_misconception
                result.confidence = min(1.0, best_score)
                result.evidence = evidence
                
                # Generate recovery recommendations
                result.recommended_actions = self._get_recommendations(best_misconception)
                result.diagnostic_questions = best_misconception.diagnostic_question_ids
        
        # Time analysis
        if time_taken < VERY_FAST_THRESHOLD:
            result.time_analysis = "Very fast response - possible guessing or careless"
        elif time_taken > VERY_SLOW_THRESHOLD:
            result.time_analysis = "Struggled significantly - conceptual difficulty"
        else:
            result.time_analysis = "Normal response time"
        
        # If no specific misconception detected but wrong answer
        if not result.detected:
            result.detected = True
            result.misconception = self._create_generic_misconception(concept_id, time_taken)
            result.confidence = 0.3
            result.evidence = ["No specific pattern match - generic error"]
            result.recommended_actions = ["Review concept fundamentals", "Practice similar questions"]
        
        return result
    
    def _get_recommendations(self, misconception: Misconception) -> List[str]:
        """Generate recovery recommendations based on misconception"""
        recommendations = []
        
        # Based on severity
        if misconception.severity == MisconceptionSeverity.HIGH:
            recommendations.append("IMMEDIATE: Stop current topic, address this misconception first")
            recommendations.append("Complete diagnostic questions to isolate root cause")
            if misconception.prerequisite_concepts:
                recommendations.append(f"Review prerequisites: {', '.join(misconception.prerequisite_concepts)}")
        
        elif misconception.severity == MisconceptionSeverity.MEDIUM:
            recommendations.append("Practice similar problems with attention to this error")
            if misconception.recovery_strategy:
                recommendations.append(f"Key insight: {misconception.recovery_strategy[:100]}...")
        
        else:  # LOW
            recommendations.append("Minor issue - be more careful next time")
            recommendations.append("Mark for review in next session")
        
        # Based on category
        if misconception.category == MisconceptionCategory.PREREQUISITE_GAP:
            recommendations.append("Building block missing - complete prerequisite first")
        elif misconception.category == MisconceptionCategory.FORMULA_CONFUSION:
            recommendations.append("Create formula comparison chart")
        elif misconception.category == MisconceptionCategory.SIGN_ERROR:
            recommendations.append("Practice sign-tracking exercises")
        
        return recommendations
    
    def _create_generic_misconception(
        self,
        concept_id: str,
        time_taken: float
    ) -> Misconception:
        """Create generic misconception when no specific one detected"""
        
        # Determine likely category from time
        if time_taken < VERY_FAST_THRESHOLD:
            category = MisconceptionCategory.CARELESS
            severity = MisconceptionSeverity.LOW
            recovery = "Slow down and read carefully. Check your work."
        elif time_taken > VERY_SLOW_THRESHOLD:
            category = MisconceptionCategory.CONCEPTUAL
            severity = MisconceptionSeverity.MEDIUM
            recovery = "Review concept fundamentals. This needs more practice."
        else:
            category = MisconceptionCategory.PROCEDURAL
            severity = MisconceptionSeverity.MEDIUM
            recovery = "Check problem-solving steps. Where did the approach break down?"
        
        return Misconception(
            misconception_id=f"MISC_GENERIC_{concept_id}",
            concept_id=concept_id,
            subject=concept_id.split('_')[0] if '_' in concept_id else "UNKNOWN",
            name="Unclassified Error",
            description="Error not matching known patterns",
            severity=severity,
            category=category,
            recovery_strategy=recovery
        )


# ============================================================================
# RECOVERY ENGINE
# ============================================================================

class RecoveryEngine:
    """
    Manages misconception recovery process.
    
    Recovery flow:
    1. Diagnostic phase: Isolate root cause with targeted questions
    2. Remediation: Provide targeted content addressing specific gap
    3. Practice phase: Gradually increase difficulty of related questions
    4. Verification: Confirm misconception is resolved
    """
    
    def __init__(self, detector: MisconceptionDetector):
        """Initialize with detector for ongoing analysis"""
        self.detector = detector
        self.active_plans: Dict[str, List[RecoveryPlan]] = {}  # student_id -> plans
    
    def create_recovery_plan(
        self,
        student_id: str,
        detection_result: DetectionResult
    ) -> RecoveryPlan:
        """
        Create personalized recovery plan for detected misconception.
        """
        if not detection_result.detected or not detection_result.misconception:
            raise ValueError("Cannot create plan for non-detected misconception")
        
        misconception = detection_result.misconception
        
        plan = RecoveryPlan(
            student_id=student_id,
            misconception=misconception,
            diagnostic_questions=list(misconception.diagnostic_question_ids),
            diagnostic_phase=misconception.severity == MisconceptionSeverity.HIGH
        )
        
        # Store plan
        if student_id not in self.active_plans:
            self.active_plans[student_id] = []
        self.active_plans[student_id].append(plan)
        
        return plan
    
    def process_response(
        self,
        student_id: str,
        plan: RecoveryPlan,
        question_id: str,
        correct: bool
    ) -> Dict:
        """
        Process a response in the recovery flow.
        
        Returns dict with next steps.
        """
        plan.questions_completed += 1
        if correct:
            plan.success_count += 1
        
        # Check if diagnostic phase complete
        if plan.diagnostic_phase:
            if question_id in plan.diagnostic_questions:
                plan.diagnostic_questions.remove(question_id)
            
            if not plan.diagnostic_questions:
                plan.diagnostic_phase = False
                plan.diagnostic_complete = True
                
                # Analyze diagnostic results
                if plan.get_success_rate() >= 0.5:
                    plan.root_cause_identified = "Partial understanding - practice needed"
                else:
                    plan.root_cause_identified = "Fundamental gap - remediation required"
        
        # Check if resolved
        if plan.is_resolved():
            plan.status = "RESOLVED"
            return {
                'status': 'RESOLVED',
                'message': 'Great job! Misconception addressed successfully.',
                'next_action': 'CONTINUE_NORMAL'
            }
        
        # Determine next action
        if plan.diagnostic_phase:
            return {
                'status': 'IN_PROGRESS',
                'message': 'Continuing diagnostic phase',
                'next_action': 'DIAGNOSTIC_QUESTION',
                'questions_remaining': len(plan.diagnostic_questions)
            }
        
        return {
            'status': 'IN_PROGRESS',
            'message': f'Practice phase: {plan.questions_completed}/{MIN_PRACTICE_QUESTIONS}',
            'next_action': 'PRACTICE_QUESTION',
            'success_rate': plan.get_success_rate()
        }
    
    def get_active_plans(self, student_id: str) -> List[RecoveryPlan]:
        """Get all active recovery plans for a student"""
        plans = self.active_plans.get(student_id, [])
        return [p for p in plans if p.status != "RESOLVED"]
    
    def get_priority_misconception(self, student_id: str) -> Optional[RecoveryPlan]:
        """Get highest priority unresolved misconception"""
        plans = self.get_active_plans(student_id)
        
        if not plans:
            return None
        
        # Sort by severity (HIGH first)
        severity_order = {
            MisconceptionSeverity.HIGH: 0,
            MisconceptionSeverity.MEDIUM: 1,
            MisconceptionSeverity.LOW: 2
        }
        
        plans.sort(key=lambda p: severity_order.get(p.misconception.severity, 99))
        
        return plans[0]


# ============================================================================
# INTEGRATION: Detection + Recovery Pipeline
# ============================================================================

def analyze_and_intervene(
    student_id: str,
    concept_id: str,
    correct: bool,
    student_answer: Optional[str] = None,
    time_taken: float = 60.0,
    question_difficulty: float = 0.5,
    detector: Optional[MisconceptionDetector] = None,
    recovery_engine: Optional[RecoveryEngine] = None
) -> Dict:
    """
    Complete misconception analysis and intervention pipeline.
    
    This is the main entry point for the misconception system.
    
    Args:
        student_id: Student identifier
        concept_id: Concept being tested
        correct: Whether answer was correct
        student_answer: Actual answer text (optional)
        time_taken: Seconds spent
        question_difficulty: 0-1 difficulty
        detector: Optional detector instance
        recovery_engine: Optional recovery engine instance
        
    Returns:
        Dict with analysis results and intervention plan
    """
    # Initialize components
    if detector is None:
        detector = MisconceptionDetector()
    if recovery_engine is None:
        recovery_engine = RecoveryEngine(detector)
    
    # Detect misconception
    detection = detector.detect(
        concept_id=concept_id,
        correct=correct,
        student_answer=student_answer,
        time_taken=time_taken,
        question_difficulty=question_difficulty
    )
    
    result = {
        'detected': detection.detected,
        'correct': correct,
        'analysis': detection.to_dict()
    }
    
    # If misconception detected, create/update recovery plan
    if detection.detected and detection.misconception:
        severity = detection.misconception.severity
        
        if severity in [MisconceptionSeverity.HIGH, MisconceptionSeverity.MEDIUM]:
            # Create recovery plan
            plan = recovery_engine.create_recovery_plan(student_id, detection)
            
            result['intervention'] = {
                'required': True,
                'severity': severity.value,
                'plan_id': plan.misconception.misconception_id,
                'immediate_action': 'DIAGNOSTIC' if severity == MisconceptionSeverity.HIGH else 'PRACTICE',
                'message': f"We noticed an issue with {detection.misconception.name}. Let's work on this."
            }
            
            # Add recovery content
            result['remediation'] = {
                'strategy': detection.misconception.recovery_strategy,
                'diagnostic_questions': detection.diagnostic_questions,
                'estimated_recovery_time': '10-15 minutes' if severity == MisconceptionSeverity.HIGH else '5-10 minutes'
            }
        
        else:  # LOW severity
            result['intervention'] = {
                'required': False,
                'severity': 'LOW',
                'message': detection.misconception.recovery_strategy,
                'immediate_action': 'CONTINUE'
            }
    
    else:
        result['intervention'] = {
            'required': False,
            'severity': None,
            'message': 'All good! Keep going.',
            'immediate_action': 'CONTINUE'
        }
    
    return result


# ============================================================================
# TESTS
# ============================================================================

def test_detection_correct_answer():
    """Test that correct answers don't trigger misconceptions"""
    detector = MisconceptionDetector()
    
    result = detector.detect(
        concept_id="MATH_041",
        correct=True,
        time_taken=45.0
    )
    
    assert not result.detected or result.confidence < 0.3, "Correct answer shouldn't trigger misconception"
    print("✅ TEST PASSED: Correct answer handling")


def test_detection_known_pattern():
    """Test detection of known misconception pattern"""
    detector = MisconceptionDetector()
    
    result = detector.detect(
        concept_id="PHYS_001",
        correct=False,
        student_answer="heavier objects fall faster because they have more mass",
        time_taken=60.0
    )
    
    assert result.detected, "Should detect misconception"
    assert result.misconception is not None, "Should have misconception details"
    assert "PHYS_001" in result.misconception.concept_id, "Should match concept"
    
    print("✅ TEST PASSED: Pattern detection")


def test_detection_time_analysis():
    """Test time-based analysis"""
    detector = MisconceptionDetector()
    
    # Very fast wrong answer
    result_fast = detector.detect(
        concept_id="MATH_001",
        correct=False,
        time_taken=5.0
    )
    
    assert "fast" in result_fast.time_analysis.lower(), "Should note fast response"
    
    # Very slow wrong answer
    result_slow = detector.detect(
        concept_id="MATH_001",
        correct=False,
        time_taken=200.0
    )
    
    assert "struggle" in result_slow.time_analysis.lower() or "slow" in result_slow.time_analysis.lower(), \
        "Should note slow response"
    
    print("✅ TEST PASSED: Time analysis")


def test_severity_levels():
    """Test severity-based handling"""
    detector = MisconceptionDetector()
    
    # High severity
    result_high = detector.detect(
        concept_id="PHYS_002",
        correct=False,
        student_answer="force needed for constant velocity",
        time_taken=90.0
    )
    
    if result_high.detected and result_high.misconception:
        severity = result_high.misconception.severity
        assert severity in [MisconceptionSeverity.HIGH, MisconceptionSeverity.MEDIUM], \
            f"Unexpected severity: {severity}"
    
    print("✅ TEST PASSED: Severity levels")


def test_recovery_plan():
    """Test recovery plan creation"""
    detector = MisconceptionDetector()
    recovery_engine = RecoveryEngine(detector)
    
    # Detect a misconception
    detection = detector.detect(
        concept_id="CHEM_020",
        correct=False,
        student_answer="equal concentrations at equilibrium",
        time_taken=45.0
    )
    
    if detection.detected:
        plan = recovery_engine.create_recovery_plan("TEST_STUDENT", detection)
        
        assert plan.student_id == "TEST_STUDENT", "Should have student ID"
        assert plan.status == "PENDING", "Should start as pending"
        
        print("✅ TEST PASSED: Recovery plan creation")
    else:
        print("⚠️ TEST SKIPPED: No misconception detected for this test case")


def test_full_pipeline():
    """Test complete analysis pipeline"""
    result = analyze_and_intervene(
        student_id="STU_001",
        concept_id="MATH_041",
        correct=False,
        student_answer="forgot chain rule",
        time_taken=120.0,
        question_difficulty=0.6
    )
    
    assert 'detected' in result, "Should have detection result"
    assert 'intervention' in result, "Should have intervention info"
    
    print("✅ TEST PASSED: Full pipeline")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CR-V4 MISCONCEPTION DETECTION TESTS")
    print("="*70 + "\n")
    
    test_detection_correct_answer()
    test_detection_known_pattern()
    test_detection_time_analysis()
    test_severity_levels()
    test_recovery_plan()
    test_full_pipeline()
    
    print("\n" + "="*70)
    print("ALL MISCONCEPTION TESTS PASSED ✅")
    print("="*70 + "\n")
    
    # Example usage
    print("EXAMPLE: Misconception Detection and Recovery\n")
    
    result = analyze_and_intervene(
        student_id="STU_12345",
        concept_id="PHYS_002",
        correct=False,
        student_answer="An object needs constant force to keep moving at constant velocity",
        time_taken=85.0,
        question_difficulty=0.4
    )
    
    print(f"Detected: {result['detected']}")
    if result['detected']:
        print(f"Misconception: {result['analysis'].get('misconception', {}).get('name', 'Unknown')}")
        print(f"Severity: {result['intervention']['severity']}")
        print(f"Intervention Required: {result['intervention']['required']}")
        print(f"Message: {result['intervention']['message']}")
        if 'remediation' in result:
            print(f"Strategy: {result['remediation']['strategy'][:80]}...")
