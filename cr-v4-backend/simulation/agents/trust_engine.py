"""
CR-V4 Trust Engine Module

This module implements the trust and compliance dynamics
for simulated students.

COUNCIL DECISIONS IMPLEMENTED:
1. Trust is asymmetric (lost faster than gained)
2. First impressions are weighted 2x
3. Low-grit students are more sensitive to negative
4. Trust zones determine behavioral compliance
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple
import random

from .genome import StudentGenome


# =============================================================================
# ENUMS
# =============================================================================

class TrustZone(Enum):
    """Trust level zones."""
    HIGH = "high"           # T > 0.8 - Very compliant
    SKEPTIC = "skeptic"     # 0.4 < T < 0.8 - Sometimes non-compliant
    DANGER = "danger"       # 0.1 < T < 0.4 - High non-compliance
    CHURN = "churn"         # T < 0.1 - Leaving platform


class AgentAction(Enum):
    """Possible agent actions."""
    FOLLOW_RECOMMENDATION = "follow"
    BROWSE_MANUALLY = "browse"
    SKIP_SESSION = "skip"
    RAPID_GUESS = "game"
    DO_MINIMUM = "minimum"
    LEAVE_PLATFORM = "churn"


class RecommendationQuality(Enum):
    """Quality of platform recommendation."""
    FLOW = "flow"                    # Optimal challenge
    NEUTRAL = "neutral"              # Acceptable
    INSULT = "insult"                # Too easy
    FRUSTRATION = "frustration"      # Too hard


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TrustState:
    """Agent's trust in the platform."""
    trust_score: float = 1.0
    insult_count: int = 0
    frustration_count: int = 0
    flow_count: int = 0
    neutral_count: int = 0
    interactions_total: int = 0
    last_update: datetime = field(default_factory=datetime.now)
    churn_triggered: bool = False
    churn_timestamp: Optional[datetime] = None
    
    # History for analysis
    trust_history: List[Tuple[datetime, float]] = field(default_factory=list)
    
    @property
    def zone(self) -> TrustZone:
        """Get current trust zone."""
        if self.trust_score > 0.8:
            return TrustZone.HIGH
        elif self.trust_score > 0.4:
            return TrustZone.SKEPTIC
        elif self.trust_score > 0.1:
            return TrustZone.DANGER
        else:
            return TrustZone.CHURN
    
    @property
    def at_risk(self) -> bool:
        """Is agent at risk of churning?"""
        return self.zone in (TrustZone.DANGER, TrustZone.CHURN)
    
    @property
    def positive_ratio(self) -> float:
        """Ratio of positive (flow) interactions."""
        if self.interactions_total == 0:
            return 0.5
        return self.flow_count / self.interactions_total
    
    def record_trust(self, timestamp: datetime):
        """Record trust for history."""
        self.trust_history.append((timestamp, self.trust_score))
        # Keep only last 100 entries
        if len(self.trust_history) > 100:
            self.trust_history = self.trust_history[-100:]


@dataclass
class Recommendation:
    """A recommendation from the platform."""
    question_id: str
    concept_id: str
    difficulty: float          # IRT b parameter
    subject: str
    is_primary: bool = True
    is_12th_content: bool = False


# =============================================================================
# TRUST ENGINE
# =============================================================================

class TrustEngine:
    """
    Manages trust dynamics and compliance decisions.
    
    Council-approved constants:
    - DELTA_FLOW = +0.02 (reward for optimal match)
    - DELTA_NEUTRAL = 0.00
    - DELTA_INSULT = -0.05 (too easy)
    - DELTA_FRUSTRATION = -0.10 (too hard)
    - DECAY_FACTOR = 0.99 (passive decay per interaction)
    - First 10 interactions weighted 2x
    """
    
    # Trust delta values (council-approved)
    DELTA_FLOW: float = +0.02
    DELTA_NEUTRAL: float = 0.00
    DELTA_INSULT: float = -0.05
    DELTA_FRUSTRATION: float = -0.10
    
    # Passive decay
    DECAY_FACTOR: float = 0.99
    
    # Early interaction handling
    FIRST_IMPRESSION_LIMIT: int = 10
    FIRST_IMPRESSION_MULTIPLIER: float = 2.0
    
    # Thresholds for quality evaluation
    FLOW_THRESHOLD: float = 0.3      # |gap| < 0.3 = flow
    INSULT_THRESHOLD: float = 0.5    # difficulty < ability - 0.5 = insult
    FRUSTRATION_THRESHOLD: float = 0.5  # difficulty > ability + 0.5 = frustration
    
    def __init__(self, genome: StudentGenome):
        """
        Initialize trust engine with a student genome.
        
        Args:
            genome: The student's genome
        """
        self.genome = genome
        self.state = TrustState()
    
    def evaluate_recommendation(
        self,
        recommendation: Recommendation
    ) -> RecommendationQuality:
        """
        Evaluate how the agent perceives a recommendation.
        
        Based on gap between agent's ability and recommendation difficulty.
        
        Args:
            recommendation: The platform's recommendation
            
        Returns:
            Quality classification
        """
        # Get agent's true ability for this concept
        theta = self.genome.knowledge.get_mastery(recommendation.concept_id)
        
        # Normalize difficulty to 0-1 scale for comparison
        diff = (recommendation.difficulty + 3) / 6  # Map -3,+3 to 0,1
        
        gap = theta - diff
        
        if abs(gap) < self.FLOW_THRESHOLD:
            return RecommendationQuality.FLOW
        elif gap > self.INSULT_THRESHOLD:
            return RecommendationQuality.INSULT
        elif gap < -self.FRUSTRATION_THRESHOLD:
            return RecommendationQuality.FRUSTRATION
        else:
            return RecommendationQuality.NEUTRAL
    
    def update_trust(
        self,
        quality: RecommendationQuality,
        timestamp: Optional[datetime] = None
    ) -> float:
        """
        Update trust score based on recommendation quality.
        
        Args:
            quality: Quality of the recommendation
            timestamp: Time of update (now if None)
            
        Returns:
            New trust score
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        self.state.interactions_total += 1
        
        # Get base delta
        delta = {
            RecommendationQuality.FLOW: self.DELTA_FLOW,
            RecommendationQuality.NEUTRAL: self.DELTA_NEUTRAL,
            RecommendationQuality.INSULT: self.DELTA_INSULT,
            RecommendationQuality.FRUSTRATION: self.DELTA_FRUSTRATION,
        }[quality]
        
        # First impressions weighted more heavily
        if self.state.interactions_total <= self.FIRST_IMPRESSION_LIMIT:
            delta *= self.FIRST_IMPRESSION_MULTIPLIER
        
        # Low-grit students are more sensitive to negative experiences
        if delta < 0:
            grit_factor = 2.0 - self.genome.psychometric.grit_index
            delta *= grit_factor
        
        # Apply passive decay
        self.state.trust_score *= self.DECAY_FACTOR
        
        # Apply delta
        self.state.trust_score += delta
        self.state.trust_score = max(0.0, min(1.0, self.state.trust_score))
        
        # Track counts
        if quality == RecommendationQuality.FLOW:
            self.state.flow_count += 1
        elif quality == RecommendationQuality.INSULT:
            self.state.insult_count += 1
        elif quality == RecommendationQuality.FRUSTRATION:
            self.state.frustration_count += 1
        else:
            self.state.neutral_count += 1
        
        # Record history
        self.state.record_trust(timestamp)
        self.state.last_update = timestamp
        
        # Check for churn
        if self.state.trust_score < 0.1:
            self.state.churn_triggered = True
            self.state.churn_timestamp = timestamp
        
        return self.state.trust_score
    
    def process_recommendation(
        self,
        recommendation: Recommendation,
        timestamp: Optional[datetime] = None
    ) -> Tuple[RecommendationQuality, float]:
        """
        Evaluate and update trust for a recommendation.
        
        Convenience method combining evaluate and update.
        
        Returns:
            (quality, new_trust_score)
        """
        quality = self.evaluate_recommendation(recommendation)
        new_trust = self.update_trust(quality, timestamp)
        return quality, new_trust
    
    def decide_action(
        self,
        recommendation: Optional[Recommendation] = None
    ) -> AgentAction:
        """
        Decide what action the agent takes.
        
        Depends on trust level and personality.
        
        Args:
            recommendation: Current recommendation (if any)
            
        Returns:
            Action the agent will take
        """
        if self.state.churn_triggered:
            return AgentAction.LEAVE_PLATFORM
        
        zone = self.state.zone
        grit = self.genome.psychometric.grit_index
        
        if zone == TrustZone.HIGH:
            # Very compliant
            return AgentAction.FOLLOW_RECOMMENDATION
        
        elif zone == TrustZone.SKEPTIC:
            # Sometimes non-compliant
            roll = random.random()
            non_compliance_threshold = 0.25 * (1 - grit)
            if roll < non_compliance_threshold:
                return AgentAction.BROWSE_MANUALLY
            return AgentAction.FOLLOW_RECOMMENDATION
        
        elif zone == TrustZone.DANGER:
            # High non-compliance
            roll = random.random()
            
            # Gaming behavior more likely for low-grit gamers
            if self.genome.psychometric.guessing_tendency > 0.5:
                if roll < 0.3:
                    return AgentAction.RAPID_GUESS
            
            if roll < 0.2:
                return AgentAction.SKIP_SESSION
            elif roll < 0.4:
                return AgentAction.DO_MINIMUM
            elif roll < 0.6:
                return AgentAction.BROWSE_MANUALLY
            
            return AgentAction.FOLLOW_RECOMMENDATION
        
        else:  # CHURN
            return AgentAction.LEAVE_PLATFORM
    
    def get_trust_summary(self) -> dict:
        """Get summary of trust state for reporting."""
        return {
            "trust_score": self.state.trust_score,
            "zone": self.state.zone.value,
            "interactions_total": self.state.interactions_total,
            "flow_count": self.state.flow_count,
            "insult_count": self.state.insult_count,
            "frustration_count": self.state.frustration_count,
            "neutral_count": self.state.neutral_count,
            "positive_ratio": self.state.positive_ratio,
            "at_risk": self.state.at_risk,
            "churn_triggered": self.state.churn_triggered,
        }
    
    def reset(self):
        """Reset trust state (for testing)."""
        self.state = TrustState()
