"""
CR-V4 CORE ALGORITHMS
Module: Student Profile System

PURPOSE: Classify students into profiles and tiers for adaptive engine behavior.

LAYER MAPPING:
- Part of Layer 5 (DKT Engine) - Student state classification
- Feeds into Layer 6 (Question Selection) - Dynamic weight adjustment

COUNCIL DECISION: Engine must behave differently for:
- Toppers: Challenge with harder questions, focus weak areas
- Struggling: Build confidence with appropriate difficulty
- New: Comfort zone first, then gradual challenge
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta


# ============================================================================
# STUDENT PROFILE CLASSIFICATIONS
# ============================================================================

class StudentProfile(Enum):
    """
    Experience-based profile (interaction count).
    
    Determines how the engine behaves toward the student.
    """
    ROOKIE = "rookie"           # <50 interactions, learning the system
    DEVELOPING = "developing"   # 50-200, building foundation
    INTERMEDIATE = "intermediate"  # 200-500, focused improvement
    ADVANCED = "advanced"       # 500-1000, fine-tuning
    EXPERT = "expert"           # >1000, exam-ready optimization


class StudentTier(Enum):
    """
    Performance-based tier (accuracy + consistency).
    
    Determines difficulty calibration and support level.
    """
    STRUGGLING = "struggling"   # <40% accuracy, needs support
    DEVELOPING = "developing"   # 40-55% accuracy, building
    AVERAGE = "average"         # 55-70% accuracy, solid
    GOOD = "good"               # 70-85% accuracy, strong
    EXCELLENT = "excellent"     # >85% accuracy, topper path


class LearningStyle(Enum):
    """
    Preferred learning approach (detected from behavior).
    """
    METHODICAL = "methodical"   # Slow, careful, high accuracy
    EXPLORER = "explorer"       # Fast, tries many, learns from errors
    BALANCED = "balanced"       # Mix of both approaches


# ============================================================================
# PROFILE THRESHOLDS
# ============================================================================

PROFILE_THRESHOLDS = {
    'ROOKIE': (0, 50),
    'DEVELOPING': (50, 200),
    'INTERMEDIATE': (200, 500),
    'ADVANCED': (500, 1000),
    'EXPERT': (1000, float('inf'))
}

TIER_THRESHOLDS = {
    'STRUGGLING': (0.0, 0.40),
    'DEVELOPING': (0.40, 0.55),
    'AVERAGE': (0.55, 0.70),
    'GOOD': (0.70, 0.85),
    'EXCELLENT': (0.85, 1.0)
}


# ============================================================================
# STUDENT CLASSIFICATION
# ============================================================================

@dataclass
class StudentClassification:
    """
    Complete student classification with all dimensions.
    """
    profile: StudentProfile
    tier: StudentTier
    learning_style: LearningStyle
    
    # Confidence in classification (0-1)
    confidence: float
    
    # Supporting metrics
    interaction_count: int
    accuracy: float
    consistency: float  # Standard deviation of recent performance
    avg_time_per_question: float
    
    # Timestamps
    last_updated: datetime
    profile_stable_since: Optional[datetime]  # When profile stopped changing
    
    def to_dict(self) -> Dict:
        return {
            'profile': self.profile.value,
            'tier': self.tier.value,
            'learning_style': self.learning_style.value,
            'confidence': round(self.confidence, 2),
            'interaction_count': self.interaction_count,
            'accuracy': round(self.accuracy, 2),
            'consistency': round(self.consistency, 2),
            'avg_time': round(self.avg_time_per_question, 1),
            'last_updated': self.last_updated.isoformat()
        }


# ============================================================================
# PROFILE CLASSIFIER
# ============================================================================

class StudentProfileClassifier:
    """
    Classifies students into profiles and tiers based on behavior.
    
    COUNCIL MANDATE:
    - Must work from first interaction (cold start)
    - Must stabilize after 50+ interactions
    - Must update on every session
    """
    
    def __init__(self):
        self.min_interactions_for_stable = 50
        self.recent_window = 20  # Last 20 for consistency calculation
    
    def classify(
        self,
        interaction_count: int,
        total_correct: int,
        recent_accuracies: list,
        avg_time: float,
        last_active: Optional[datetime] = None
    ) -> StudentClassification:
        """
        Perform full classification.
        
        Args:
            interaction_count: Total interactions ever
            total_correct: Total correct answers
            recent_accuracies: List of recent accuracy values (0-1)
            avg_time: Average time per question in seconds
            last_active: Last activity timestamp
            
        Returns:
            StudentClassification with all dimensions
        """
        # Calculate overall accuracy
        accuracy = total_correct / max(1, interaction_count)
        
        # Determine profile from interaction count
        profile = self._get_profile(interaction_count)
        
        # Determine tier from accuracy
        tier = self._get_tier(accuracy)
        
        # Calculate consistency (lower = more consistent)
        consistency = self._calculate_consistency(recent_accuracies)
        
        # Determine learning style
        learning_style = self._get_learning_style(avg_time, accuracy, consistency)
        
        # Classification confidence
        confidence = self._calculate_confidence(
            interaction_count, consistency, len(recent_accuracies)
        )
        
        # Check if profile is stable
        profile_stable = None
        if interaction_count >= self.min_interactions_for_stable:
            profile_stable = last_active or datetime.now()
        
        return StudentClassification(
            profile=profile,
            tier=tier,
            learning_style=learning_style,
            confidence=confidence,
            interaction_count=interaction_count,
            accuracy=accuracy,
            consistency=consistency,
            avg_time_per_question=avg_time,
            last_updated=datetime.now(),
            profile_stable_since=profile_stable
        )
    
    def _get_profile(self, count: int) -> StudentProfile:
        """Determine profile from interaction count."""
        if count < 50:
            return StudentProfile.ROOKIE
        elif count < 200:
            return StudentProfile.DEVELOPING
        elif count < 500:
            return StudentProfile.INTERMEDIATE
        elif count < 1000:
            return StudentProfile.ADVANCED
        else:
            return StudentProfile.EXPERT
    
    def _get_tier(self, accuracy: float) -> StudentTier:
        """Determine tier from accuracy."""
        if accuracy < 0.40:
            return StudentTier.STRUGGLING
        elif accuracy < 0.55:
            return StudentTier.DEVELOPING
        elif accuracy < 0.70:
            return StudentTier.AVERAGE
        elif accuracy < 0.85:
            return StudentTier.GOOD
        else:
            return StudentTier.EXCELLENT
    
    def _calculate_consistency(self, recent: list) -> float:
        """Calculate performance consistency (0-1)."""
        if len(recent) < 3:
            return 0.5  # Unknown
        
        import numpy as np
        return float(np.std(recent))
    
    def _get_learning_style(
        self, 
        avg_time: float, 
        accuracy: float,
        consistency: float
    ) -> LearningStyle:
        """Infer learning style from behavior."""
        # Methodical: Slow + high accuracy + consistent
        if avg_time > 90 and accuracy > 0.70 and consistency < 0.15:
            return LearningStyle.METHODICAL
        
        # Explorer: Fast + lower accuracy + inconsistent
        if avg_time < 45 and accuracy < 0.65 and consistency > 0.20:
            return LearningStyle.EXPLORER
        
        return LearningStyle.BALANCED
    
    def _calculate_confidence(
        self,
        count: int,
        consistency: float,
        recent_count: int
    ) -> float:
        """Calculate confidence in classification."""
        # More interactions = more confidence
        count_factor = min(1.0, count / 100)
        
        # More consistent = more confident
        consistency_factor = 1 - min(1.0, consistency * 2)
        
        # More recent data = more confident
        recent_factor = min(1.0, recent_count / 20)
        
        return 0.3 * count_factor + 0.4 * consistency_factor + 0.3 * recent_factor


# ============================================================================
# DYNAMIC SELECTION WEIGHTS (COUNCIL APPROVED)
# ============================================================================

def get_selection_weights(
    profile: StudentProfile,
    tier: StudentTier
) -> Dict[str, float]:
    """
    Get question selection weights based on student classification.
    
    COUNCIL DECISION:
    - ROOKIE: Comfort first (high IRT match)
    - STRUGGLING: Build confidence (easier, gap focus)
    - ADVANCED: Challenge more (high Fisher info)
    - EXCELLENT: Fine-tune weaknesses (high gap)
    
    Returns:
        Dict with weights for: irt_match, fisher_info, mastery_gap, competency
    """
    
    # Profile-based adjustments
    if profile == StudentProfile.ROOKIE:
        # New students: comfort zone, don't overwhelm
        base = {'irt_match': 0.45, 'fisher_info': 0.20, 'mastery_gap': 0.25, 'competency': 0.10}
    
    elif profile == StudentProfile.DEVELOPING:
        # Building foundation: balanced approach
        base = {'irt_match': 0.40, 'fisher_info': 0.25, 'mastery_gap': 0.25, 'competency': 0.10}
    
    elif profile == StudentProfile.ADVANCED:
        # Advanced: more challenge
        base = {'irt_match': 0.28, 'fisher_info': 0.32, 'mastery_gap': 0.30, 'competency': 0.10}
    
    elif profile == StudentProfile.EXPERT:
        # Expert: optimize for exam
        base = {'irt_match': 0.25, 'fisher_info': 0.30, 'mastery_gap': 0.35, 'competency': 0.10}
    
    else:  # INTERMEDIATE
        # Default balanced
        base = {'irt_match': 0.35, 'fisher_info': 0.30, 'mastery_gap': 0.25, 'competency': 0.10}
    
    # Tier-based adjustments
    if tier == StudentTier.STRUGGLING:
        # Boost IRT match (easier questions), reduce Fisher
        base['irt_match'] = min(0.50, base['irt_match'] + 0.10)
        base['fisher_info'] = max(0.15, base['fisher_info'] - 0.10)
    
    elif tier == StudentTier.EXCELLENT:
        # Boost mastery gap (target weaknesses)
        base['mastery_gap'] = min(0.40, base['mastery_gap'] + 0.10)
        base['irt_match'] = max(0.20, base['irt_match'] - 0.10)
    
    # Normalize to ensure sum = 1.0
    total = sum(base.values())
    return {k: v/total for k, v in base.items()}


# ============================================================================
# SUBJECT-SPECIFIC ADJUSTMENTS
# ============================================================================

def get_subject_adjustments(
    subject: str,
    tier: StudentTier
) -> Dict[str, float]:
    """
    Get subject-specific weight adjustments.
    
    COUNCIL DECISION:
    - MATH: More mastery gap (need depth)
    - PHYSICS: More Fisher info (discriminating questions help)
    - CHEMISTRY: Add coverage factor
    """
    adjustments = {'irt_match': 0, 'fisher_info': 0, 'mastery_gap': 0, 'competency': 0}
    
    if subject == 'MATH':
        adjustments['mastery_gap'] = 0.05  # Math needs gap focus
        adjustments['irt_match'] = -0.05
    
    elif subject == 'PHYSICS':
        adjustments['fisher_info'] = 0.05  # Physics needs discrimination
        adjustments['irt_match'] = -0.05
    
    elif subject == 'CHEMISTRY':
        # Chemistry needs coverage - handled separately
        pass
    
    return adjustments


# ============================================================================
# TESTS
# ============================================================================

def test_profile_classification():
    """Test profile classification."""
    classifier = StudentProfileClassifier()
    
    # Rookie struggling
    result = classifier.classify(
        interaction_count=25,
        total_correct=8,
        recent_accuracies=[0.3, 0.2, 0.4, 0.3],
        avg_time=120.0
    )
    assert result.profile == StudentProfile.ROOKIE
    assert result.tier == StudentTier.STRUGGLING
    print(f"✅ Rookie Struggling: {result.to_dict()}")
    
    # Advanced excellent
    result = classifier.classify(
        interaction_count=800,
        total_correct=720,
        recent_accuracies=[0.9, 0.88, 0.92, 0.91],
        avg_time=45.0
    )
    assert result.profile == StudentProfile.ADVANCED
    assert result.tier == StudentTier.EXCELLENT
    print(f"✅ Advanced Excellent: {result.to_dict()}")
    
    print("✅ All profile tests passed!")


def test_selection_weights():
    """Test dynamic weight generation."""
    
    # Rookie struggling
    weights = get_selection_weights(StudentProfile.ROOKIE, StudentTier.STRUGGLING)
    assert weights['irt_match'] >= 0.45, "Rookie struggling needs more IRT match"
    assert abs(sum(weights.values()) - 1.0) < 0.01, "Weights must sum to 1"
    print(f"✅ Rookie Struggling weights: {weights}")
    
    # Expert excellent
    weights = get_selection_weights(StudentProfile.EXPERT, StudentTier.EXCELLENT)
    assert weights['mastery_gap'] >= 0.35, "Expert excellent needs gap focus"
    print(f"✅ Expert Excellent weights: {weights}")
    
    print("✅ All weight tests passed!")


if __name__ == "__main__":
    test_profile_classification()
    test_selection_weights()
    print("\n🎉 Student Profile System: All tests passed!")
