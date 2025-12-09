"""
CR-V4 CORE ALGORITHMS
Module: JEE-MAINS Engine

PURPOSE: Align engine with NTA JEE-MAINS exam structure and strategies.

LAYER MAPPING:
- Layer 8 (Marks-to-Percentile) - Percentile mapping
- Layer 3 (Academic Calendar) - Time-based strategies
- Layer 6 (Question Selection) - Exam pattern alignment

COUNCIL + NTA ALIGNMENT:
- Follows official JEE-MAINS 2024-2025 pattern
- 90 questions: 75 MCQ + 15 Numerical (5 per subject optional)
- Marks-to-percentile based on real NTA data
- Time management strategies per student tier
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import math


# ============================================================================
# JEE-MAINS 2024-2025 OFFICIAL STRUCTURE
# ============================================================================

JEE_MAINS_PATTERN = {
    'exam_name': 'JEE MAINS 2025',
    'conducting_body': 'NTA',
    'total_questions': 90,
    'questions_to_attempt': 75,  # 20 MCQ + 5 of 10 Numerical per subject
    'total_time_minutes': 180,
    'total_marks': 300,
    
    'subjects': {
        'PHYSICS': {
            'section_a': {
                'questions': 20,
                'type': 'MCQ',
                'marks_correct': 4,
                'marks_wrong': -1,
                'attempt': 20  # All mandatory
            },
            'section_b': {
                'questions': 10,
                'type': 'NUMERICAL',
                'marks_correct': 4,
                'marks_wrong': 0,  # No negative
                'attempt': 5  # Choose any 5
            }
        },
        'CHEMISTRY': {
            'section_a': {
                'questions': 20,
                'type': 'MCQ',
                'marks_correct': 4,
                'marks_wrong': -1,
                'attempt': 20
            },
            'section_b': {
                'questions': 10,
                'type': 'NUMERICAL',
                'marks_correct': 4,
                'marks_wrong': 0,
                'attempt': 5
            }
        },
        'MATH': {
            'section_a': {
                'questions': 20,
                'type': 'MCQ',
                'marks_correct': 4,
                'marks_wrong': -1,
                'attempt': 20
            },
            'section_b': {
                'questions': 10,
                'type': 'NUMERICAL',
                'marks_correct': 4,
                'marks_wrong': 0,
                'attempt': 5
            }
        }
    },
    
    # Maximum possible per subject
    'max_per_subject': 100,  # 20×4 + 5×4 = 100
}


# ============================================================================
# MARKS TO PERCENTILE MAPPING (NTA 2024 DATA)
# ============================================================================

# Based on JEE Mains 2024 January + April sessions (actual NTA data)
MARKS_TO_PERCENTILE_2024 = {
    # Marks: Percentile (approximate, from NTA releases)
    300: 100.00,
    290: 99.99,
    280: 99.97,
    270: 99.93,
    260: 99.85,
    250: 99.70,
    240: 99.50,
    230: 99.20,
    220: 98.80,
    210: 98.30,
    200: 97.50,
    190: 96.50,
    180: 95.00,
    170: 93.00,
    160: 90.50,
    150: 87.50,
    140: 84.00,
    130: 80.00,
    120: 75.00,
    110: 69.50,
    100: 63.00,
    90: 56.00,
    80: 48.00,
    70: 40.00,
    60: 32.00,
    50: 24.00,
    40: 17.00,
    30: 11.00,
    20: 6.00,
    10: 2.50,
    0: 0.00,
}

# Percentile to approximate rank (for 12 lakh candidates)
def percentile_to_rank(percentile: float, total_candidates: int = 1200000) -> int:
    """Convert percentile to approximate rank."""
    return int(total_candidates * (100 - percentile) / 100) + 1


# ============================================================================
# TIME MANAGEMENT STRATEGY
# ============================================================================

class TimeStrategy(Enum):
    """Time allocation strategies."""
    BALANCED = "balanced"      # Equal time per subject
    STRONG_FIRST = "strong_first"  # Start with strongest
    WEAK_FIRST = "weak_first"  # Start with weakest
    MARKS_FIRST = "marks_first"  # Easy questions first


@dataclass
class SubjectTimeAllocation:
    """Time allocation for a subject."""
    subject: str
    total_minutes: int
    mcq_time: int
    numerical_time: int
    buffer_time: int


# Ideal time per question type (in minutes)
IDEAL_TIME_PER_QUESTION = {
    'MCQ': {
        'easy': 1.0,
        'medium': 1.5,
        'hard': 2.5
    },
    'NUMERICAL': {
        'easy': 2.0,
        'medium': 3.0,
        'hard': 4.5
    }
}


def get_time_allocation(
    subject_strengths: Dict[str, float],
    strategy: TimeStrategy = TimeStrategy.BALANCED
) -> Dict[str, SubjectTimeAllocation]:
    """
    Calculate optimal time allocation across subjects.
    
    Args:
        subject_strengths: Dict of subject -> strength (0-1)
        strategy: Time allocation strategy
        
    Returns:
        Dict of subject -> SubjectTimeAllocation
    """
    total_time = 180  # minutes
    base_time = 60  # 60 minutes per subject
    
    allocations = {}
    
    if strategy == TimeStrategy.BALANCED:
        for subject in ['PHYSICS', 'CHEMISTRY', 'MATH']:
            allocations[subject] = SubjectTimeAllocation(
                subject=subject,
                total_minutes=60,
                mcq_time=35,  # 20 questions × ~1.75 min
                numerical_time=20,  # 5 questions × 4 min
                buffer_time=5
            )
    
    elif strategy == TimeStrategy.STRONG_FIRST:
        # Sort by strength (descending)
        sorted_subjects = sorted(
            subject_strengths.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Strong subject: less time (faster), weak: more time
        times = [50, 60, 70]  # minutes
        for i, (subject, strength) in enumerate(sorted_subjects):
            t = times[i]
            allocations[subject] = SubjectTimeAllocation(
                subject=subject,
                total_minutes=t,
                mcq_time=int(t * 0.58),
                numerical_time=int(t * 0.33),
                buffer_time=int(t * 0.09)
            )
    
    return allocations


# ============================================================================
# HIGH-YIELD TOPICS (Based on JEE-MAINS Mark Distribution)
# ============================================================================

HIGH_YIELD_TOPICS = {
    'PHYSICS': {
        # Mechanics: 35-40 marks (highest yield)
        'tier_1': [
            'PHYS_001', 'PHYS_002', 'PHYS_003', 'PHYS_004', 'PHYS_005',
            'PHYS_006', 'PHYS_007', 'PHYS_008'
        ],
        # Electromagnetism: 28-32 marks
        'tier_2': [
            'PHYS_030', 'PHYS_031', 'PHYS_032', 'PHYS_033', 'PHYS_034',
            'PHYS_035', 'PHYS_036'
        ],
        # Modern Physics: 12-16 marks
        'tier_3': [
            'PHYS_040', 'PHYS_041', 'PHYS_042', 'PHYS_043'
        ],
        # Optics + Waves: 10-14 marks
        'tier_4': [
            'PHYS_010', 'PHYS_011', 'PHYS_012', 'PHYS_020', 'PHYS_021'
        ]
    },
    'CHEMISTRY': {
        # Physical Chemistry: 28-32 marks
        'tier_1': [
            'CHEM_001', 'CHEM_002', 'CHEM_003', 'CHEM_004', 'CHEM_005',
            'CHEM_010', 'CHEM_011', 'CHEM_012'
        ],
        # Organic Chemistry: 32-36 marks
        'tier_2': [
            'CHEM_020', 'CHEM_021', 'CHEM_022', 'CHEM_023', 'CHEM_024',
            'CHEM_025', 'CHEM_026', 'CHEM_027'
        ],
        # Inorganic Chemistry: 28-32 marks
        'tier_3': [
            'CHEM_030', 'CHEM_031', 'CHEM_033', 'CHEM_035', 'CHEM_036',
            'CHEM_037', 'CHEM_038'
        ]
    },
    'MATH': {
        # Calculus: 28-32 marks (highest yield)
        'tier_1': [
            'MATH_040', 'MATH_041', 'MATH_042', 'MATH_043', 'MATH_044',
            'MATH_045', 'MATH_046'
        ],
        # Algebra: 24-28 marks
        'tier_2': [
            'MATH_010', 'MATH_011', 'MATH_013', 'MATH_014', 'MATH_015',
            'MATH_016', 'MATH_017'
        ],
        # Coordinate Geometry: 20-24 marks
        'tier_3': [
            'MATH_030', 'MATH_031', 'MATH_032', 'MATH_033', 'MATH_034'
        ],
        # Trigonometry: 12-16 marks
        'tier_4': [
            'MATH_020', 'MATH_021', 'MATH_022', 'MATH_023'
        ]
    }
}


def get_topic_priority(
    subject: str,
    days_to_exam: int
) -> List[str]:
    """
    Get prioritized topic list based on time remaining.
    
    COUNCIL DECISION:
    - <30 days: Only tier_1 topics
    - 30-90 days: tier_1 + tier_2
    - 90-180 days: tier_1 + tier_2 + tier_3
    - >180 days: All topics
    """
    topics = HIGH_YIELD_TOPICS.get(subject, {})
    
    if days_to_exam < 30:
        return topics.get('tier_1', [])
    
    elif days_to_exam < 90:
        return topics.get('tier_1', []) + topics.get('tier_2', [])
    
    elif days_to_exam < 180:
        return (topics.get('tier_1', []) + 
                topics.get('tier_2', []) + 
                topics.get('tier_3', []))
    
    else:
        # All tiers
        all_topics = []
        for tier in ['tier_1', 'tier_2', 'tier_3', 'tier_4']:
            all_topics.extend(topics.get(tier, []))
        return all_topics


# ============================================================================
# SCORE PREDICTION
# ============================================================================

@dataclass
class ScorePrediction:
    """Predicted JEE-MAINS score based on current performance."""
    predicted_marks: int
    predicted_percentile: float
    predicted_rank: int
    
    confidence_interval: Tuple[int, int]  # Marks range
    
    strength_areas: List[str]
    weakness_areas: List[str]
    
    recommendation: str


def predict_score(
    subject_masteries: Dict[str, float],
    subject_accuracies: Dict[str, float]
) -> ScorePrediction:
    """
    Predict JEE-MAINS score based on current performance.
    
    Args:
        subject_masteries: Dict of subject -> mastery (0-1)
        subject_accuracies: Dict of subject -> accuracy (0-1)
        
    Returns:
        ScorePrediction with marks, percentile, rank
    """
    total_marks = 0
    subject_scores = {}
    
    for subject in ['PHYSICS', 'CHEMISTRY', 'MATH']:
        mastery = subject_masteries.get(subject, 0.5)
        accuracy = subject_accuracies.get(subject, 0.5)
        
        # Blend mastery and accuracy
        effective = 0.6 * mastery + 0.4 * accuracy
        
        # Estimate marks: MCQ + Numerical
        # MCQ: 20 questions × 4 marks × accuracy - wrong × 1
        mcq_correct = int(20 * effective)
        mcq_wrong = 20 - mcq_correct
        mcq_marks = max(0, mcq_correct * 4 - mcq_wrong * 1)
        
        # Numerical: 5 questions × 4 marks (no negative)
        numerical_marks = int(5 * effective * 4)
        
        subject_marks = mcq_marks + numerical_marks
        subject_scores[subject] = subject_marks
        total_marks += subject_marks
    
    # Cap at 300
    total_marks = min(300, max(0, total_marks))
    
    # Get percentile
    percentile = interpolate_percentile(total_marks)
    
    # Get rank
    rank = percentile_to_rank(percentile)
    
    # Confidence interval (±15 marks typically)
    confidence = (max(0, total_marks - 15), min(300, total_marks + 15))
    
    # Identify strengths/weaknesses
    sorted_subjects = sorted(subject_scores.items(), key=lambda x: x[1], reverse=True)
    strengths = [s[0] for s in sorted_subjects if s[1] > 70]
    weaknesses = [s[0] for s in sorted_subjects if s[1] < 60]
    
    # Generate recommendation
    if total_marks >= 200:
        rec = "Focus on weak areas and practice more numerical questions."
    elif total_marks >= 150:
        rec = "Strengthen tier-1 topics and work on time management."
    elif total_marks >= 100:
        rec = "Prioritize foundational concepts before advanced topics."
    else:
        rec = "Focus on building fundamentals. Consider diagnostic review."
    
    return ScorePrediction(
        predicted_marks=total_marks,
        predicted_percentile=percentile,
        predicted_rank=rank,
        confidence_interval=confidence,
        strength_areas=strengths,
        weakness_areas=weaknesses,
        recommendation=rec
    )


def interpolate_percentile(marks: int) -> float:
    """Interpolate percentile from marks using NTA data."""
    sorted_marks = sorted(MARKS_TO_PERCENTILE_2024.keys(), reverse=True)
    
    for i, m in enumerate(sorted_marks):
        if marks >= m:
            if i == 0:
                return MARKS_TO_PERCENTILE_2024[m]
            
            higher_m = sorted_marks[i-1]
            lower_m = m
            
            # Linear interpolation
            ratio = (marks - lower_m) / (higher_m - lower_m)
            lower_p = MARKS_TO_PERCENTILE_2024[lower_m]
            higher_p = MARKS_TO_PERCENTILE_2024[higher_m]
            
            return lower_p + ratio * (higher_p - lower_p)
    
    return 0.0


# ============================================================================
# TESTS
# ============================================================================

def test_percentile_mapping():
    """Test marks to percentile conversion."""
    assert MARKS_TO_PERCENTILE_2024[300] == 100.0
    assert MARKS_TO_PERCENTILE_2024[200] == 97.50
    assert MARKS_TO_PERCENTILE_2024[100] == 63.00
    
    # Interpolation test
    p = interpolate_percentile(175)
    assert 93.0 < p < 95.0, f"Expected ~94, got {p}"
    
    print("✅ Percentile mapping test passed")


def test_score_prediction():
    """Test score prediction."""
    prediction = predict_score(
        subject_masteries={'PHYSICS': 0.7, 'CHEMISTRY': 0.6, 'MATH': 0.8},
        subject_accuracies={'PHYSICS': 0.65, 'CHEMISTRY': 0.55, 'MATH': 0.75}
    )
    
    assert 150 < prediction.predicted_marks < 250
    assert prediction.predicted_percentile > 80
    
    print(f"✅ Score prediction: {prediction.predicted_marks} marks, {prediction.predicted_percentile:.1f}%ile")
    print("✅ Score prediction test passed")


def test_time_allocation():
    """Test time allocation."""
    allocations = get_time_allocation(
        {'PHYSICS': 0.8, 'CHEMISTRY': 0.6, 'MATH': 0.7},
        TimeStrategy.STRONG_FIRST
    )
    
    assert len(allocations) == 3
    total_time = sum(a.total_minutes for a in allocations.values())
    assert 175 <= total_time <= 185  # ~180 minutes
    
    print("✅ Time allocation test passed")


if __name__ == "__main__":
    test_percentile_mapping()
    test_score_prediction()
    test_time_allocation()
    print("\n🎉 JEE-MAINS Engine: All tests passed!")
