"""
CR-V4 Simulation Orchestrator

This module is the central control system that runs the simulation,
coordinating all agents, time, data collection, and validation.

COUNCIL DECISIONS IMPLEMENTED:
1. Exam-bound simulation (ends when all agents graduate/churn)
2. Smart time compression (100x default)
3. Standard-wise content validation
4. Incomplete data handling
5. Parquet data storage
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import logging
import uuid

from ..agents.genome import StudentGenome, generate_genome_pool, PersonaType
from ..agents.cognitive_core import (
    CognitiveLogicCore, SessionState, QuestionContext, AnswerResult
)
from ..agents.trust_engine import (
    TrustEngine, TrustState, AgentAction, Recommendation, RecommendationQuality
)
from ..observer.god_view import GodViewObserver, Violation, TruthFidelityMetrics
from ..data.storage import DataWriter, DataReader, CheckpointManager
from .time_keeper import TimeKeeper, SimulationPhase
from ..config import (
    SimulationConfig, INCOMPLETE_DATA_CONFIG, 
    JEE_EXAM_DATES, PARQUET_DIR, CONTENT_RULES
)

logger = logging.getLogger(__name__)


# =============================================================================
# STUDENT AGENT
# =============================================================================

@dataclass
class StudentAgent:
    """
    Complete student agent with all components.
    
    This wraps genome, CLC, and trust engine together.
    """
    genome: StudentGenome
    clc: CognitiveLogicCore
    trust_engine: TrustEngine
    
    # Runtime state
    current_session: Optional[SessionState] = None
    total_interactions: int = 0
    total_correct: int = 0
    last_interaction_time: Optional[datetime] = None
    
    @property
    def agent_id(self) -> str:
        return self.genome.genome_id
    
    @property
    def is_active(self) -> bool:
        return self.genome.is_active and not self.trust_engine.state.churn_triggered
    
    @property
    def has_graduated(self) -> bool:
        return self.genome.has_graduated
    
    @property
    def trust_score(self) -> float:
        return self.trust_engine.state.trust_score
    
    @property
    def average_accuracy(self) -> float:
        if self.total_interactions == 0:
            return 0.0
        return self.total_correct / self.total_interactions
    
    def start_session(self) -> SessionState:
        """Start a new study session."""
        self.current_session = self.clc.start_session()
        return self.current_session
    
    def end_session(self):
        """End current session."""
        self.clc.end_session()
        self.current_session = None
    
    def attempt_question(
        self,
        question: QuestionContext,
        recommendation: Optional[Recommendation] = None
    ) -> Tuple[AnswerResult, Optional[RecommendationQuality]]:
        """
        Agent attempts a question.
        
        Returns:
            (answer_result, recommendation_quality)
        """
        if self.current_session is None:
            self.start_session()
        
        # Generate answer
        result = self.clc.generate_answer(question, self.current_session)
        
        # Update stats
        self.total_interactions += 1
        if result.is_correct:
            self.total_correct += 1
        self.last_interaction_time = datetime.now()
        
        # Apply learning
        self.clc.apply_learning(
            question.concept_id,
            result.is_correct
        )
        
        # Update trust if we have a recommendation
        quality = None
        if recommendation:
            quality = self.trust_engine.process_recommendation(recommendation)[0]
        
        return result, quality
    
    def decide_action(self) -> AgentAction:
        """Decide next action."""
        return self.trust_engine.decide_action()
    
    def to_state_dict(self, sim_date: date) -> dict:
        """Get state for logging."""
        return {
            "snapshot_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "sim_date": sim_date.isoformat(),
            "persona_type": self.genome.persona_type.name,
            "standard": self.genome.standard,
            "is_active": self.is_active,
            "has_graduated": self.has_graduated,
            "trust_score": self.trust_score,
            "trust_zone": self.trust_engine.state.zone.value,
            "days_to_exam": self.genome.temporal.days_to_exam,
            "total_interactions": self.total_interactions,
            "average_accuracy": self.average_accuracy,
            "average_mastery": sum(
                self.genome.knowledge.kc_mastery_map.values()
            ) / max(1, len(self.genome.knowledge.kc_mastery_map)),
            "churn_reason": self.genome.churn_reason or "",
        }


# =============================================================================
# MOCK QUESTION PROVIDER
# =============================================================================

class MockQuestionProvider:
    """
    Provides mock questions for simulation.
    
    In real implementation, this would connect to the actual
    question bank. For simulation, we generate mock questions.
    
    AUDIT FIX: Added adversarial_mode for trust decay testing.
    """
    
    def __init__(
        self, 
        available_concepts: Optional[List[str]] = None,
        adversarial_mode: bool = False,
        adversarial_rate: float = 0.20  # 20% bad recommendations
    ):
        """
        Initialize question provider.
        
        Args:
            available_concepts: List of concept IDs
            adversarial_mode: If True, intentionally provide bad matches
            adversarial_rate: Fraction of questions that are poorly matched
        """
        self.concepts = available_concepts or self._generate_default_concepts()
        self._question_counter = 0
        self.adversarial_mode = adversarial_mode
        self.adversarial_rate = adversarial_rate
        self.adversarial_count = 0
        self.total_count = 0
    
    def _generate_default_concepts(self) -> List[str]:
        """Generate default concept list."""
        concepts = []
        
        # 11th grade concepts (1-75)
        for i in range(1, 76):
            concepts.append(f"MATH_11_{i:03d}")
            concepts.append(f"PHYS_11_{i:03d}")
            concepts.append(f"CHEM_11_{i:03d}")
        
        # 12th grade concepts (76-165)
        for i in range(76, 166):
            concepts.append(f"MATH_12_{i:03d}")
            concepts.append(f"PHYS_12_{i:03d}")
            concepts.append(f"CHEM_12_{i:03d}")
        
        return concepts
    
    def get_question_for_agent(
        self,
        agent: StudentAgent,
        target_difficulty: Optional[float] = None
    ) -> Tuple[QuestionContext, Recommendation]:
        """
        Get a question appropriate for the agent.
        
        CRITICAL: Must respect standard-wise content rules.
        
        AUDIT FIX: In adversarial mode, some questions are intentionally
        too easy (insult zone) or too hard (frustration zone) to test
        trust decay mechanisms.
        
        Args:
            agent: The student agent
            target_difficulty: Target difficulty, or match to ability
            
        Returns:
            (question_context, recommendation)
        """
        import random
        
        self.total_count += 1
        
        # Filter concepts by standard
        allowed_concepts = [
            c for c in self.concepts
            if agent.genome.can_access_concept(c)
        ]
        
        if not allowed_concepts:
            # Fallback to any 11th concept
            allowed_concepts = [c for c in self.concepts if "_11_" in c]
        
        # Select random concept
        concept_id = random.choice(allowed_concepts)
        
        # Determine subject
        if "MATH" in concept_id:
            subject = "MATH"
        elif "PHYS" in concept_id:
            subject = "PHYSICS"
        else:
            subject = "CHEMISTRY"
        
        # Determine if 12th content
        is_12th = "_12_" in concept_id
        
        # Get agent's mastery for difficulty targeting
        agent_mastery = agent.genome.knowledge.get_mastery(concept_id)
        
        # AUDIT FIX: Adversarial mode - intentionally mismatch difficulty
        is_adversarial = False
        if self.adversarial_mode and random.random() < self.adversarial_rate:
            is_adversarial = True
            self.adversarial_count += 1
            
            # Choose adversarial type
            if random.random() < 0.5:
                # INSULT ZONE: Way too easy (will lose trust)
                target = -2.5  # Very easy
            else:
                # FRUSTRATION ZONE: Way too hard (will lose trust faster)
                target = 2.5  # Very hard
        else:
            # Normal matching
            if target_difficulty is None:
                # Match to ability with some variance
                target = (agent_mastery * 6 - 3) + random.gauss(0, 0.5)
            else:
                target = target_difficulty
        
        # Clamp to valid range
        difficulty = max(-3.0, min(3.0, target))
        
        # Generate question ID
        self._question_counter += 1
        question_id = f"Q{self._question_counter:08d}"
        
        # Create question context
        question = QuestionContext(
            question_id=question_id,
            concept_id=concept_id,
            subject=subject,
            difficulty_b=difficulty,
            discrimination_a=random.uniform(0.5, 2.0),
            guessing_c=0.25,  # 4-option MCQ
            is_high_stakes=False,
            is_12th_content=is_12th,
        )
        
        # Create recommendation
        recommendation = Recommendation(
            question_id=question_id,
            concept_id=concept_id,
            difficulty=difficulty,
            subject=subject,
            is_12th_content=is_12th,
        )
        
        return question, recommendation
    
    def get_adversarial_stats(self) -> dict:
        """Get adversarial mode statistics."""
        return {
            "adversarial_mode": self.adversarial_mode,
            "adversarial_rate": self.adversarial_rate,
            "adversarial_count": self.adversarial_count,
            "total_count": self.total_count,
            "actual_rate": self.adversarial_count / max(1, self.total_count),
        }



# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================

class SimulationOrchestrator:
    """
    Master controller for the simulation.
    
    Manages:
    - Agent lifecycle (creation, interaction, graduation, churn)
    - Time advancement
    - Data collection
    - Observer validation
    - Checkpointing
    """
    
    def __init__(
        self,
        config: Optional[SimulationConfig] = None,
        available_concepts: Optional[List[str]] = None,
        adversarial_mode: bool = False  # AUDIT FIX: For trust decay testing
    ):
        """
        Initialize orchestrator.
        
        Args:
            config: Simulation configuration
            available_concepts: Available concept IDs
            adversarial_mode: If True, 20% of recommendations are intentionally poor
        """
        self.config = config or SimulationConfig.standard()
        self.adversarial_mode = adversarial_mode
        
        # Components
        self.time_keeper = TimeKeeper(
            compression_ratio=self.config.time.compression_ratio,
        )
        self.data_writer = DataWriter(
            batch_size=self.config.storage.write_batch_size
        )
        self.checkpoint_manager = CheckpointManager()
        self.observer = GodViewObserver(data_writer=self.data_writer)
        self.question_provider = MockQuestionProvider(
            available_concepts,
            adversarial_mode=adversarial_mode,  # AUDIT FIX
            adversarial_rate=0.20  # 20% bad recommendations
        )
        
        # Agents
        self.agents: Dict[str, StudentAgent] = {}
        self.available_concepts = available_concepts
        
        # Runtime state
        self.is_running = False
        self.step_count = 0
        self.interactions_count = 0
        
        if adversarial_mode:
            logger.info("SimulationOrchestrator initialized in ADVERSARIAL MODE")
        else:
            logger.info("SimulationOrchestrator initialized")
    
    # =========================================================================
    # INITIALIZATION
    # =========================================================================
    
    def initialize(
        self,
        agent_count: Optional[int] = None,
        target_exam_date: Optional[date] = None
    ):
        """
        Initialize simulation with agents.
        
        Args:
            agent_count: Number of agents (uses config if None)
            target_exam_date: JEE exam date
        """
        count = agent_count or self.config.agents.total_agents
        exam_date = target_exam_date or JEE_EXAM_DATES.get(2025, date(2025, 1, 22))
        
        logger.info(f"Initializing simulation with {count} agents")
        logger.info(f"Target exam date: {exam_date}")
        
        # Generate genomes
        genomes = generate_genome_pool(
            count=count,
            target_exam_date=exam_date,
            available_concepts=self.available_concepts,
            random_seed=self.config.random_seed,
        )
        
        # Create agents
        for genome in genomes:
            agent = StudentAgent(
                genome=genome,
                clc=CognitiveLogicCore(genome),
                trust_engine=TrustEngine(genome),
            )
            self.agents[genome.genome_id] = agent
            
            # Register with time keeper and observer
            self.time_keeper.register_agent(
                genome.genome_id,
                genome.temporal.target_exam_date
            )
            self.observer.register_genome(genome)
        
        logger.info(f"Created {len(self.agents)} agents")
        
        # Log persona distribution
        persona_counts = {}
        for agent in self.agents.values():
            ptype = agent.genome.persona_type.name
            persona_counts[ptype] = persona_counts.get(ptype, 0) + 1
        logger.info(f"Persona distribution: {persona_counts}")
        
        # Log standard distribution
        standard_counts = {11: 0, 12: 0}
        for agent in self.agents.values():
            standard_counts[agent.genome.standard] += 1
        logger.info(f"Standard distribution: {standard_counts}")
    
    # =========================================================================
    # MAIN LOOP
    # =========================================================================
    
    def run(self, max_steps: Optional[int] = None) -> TruthFidelityMetrics:
        """
        Run the simulation.
        
        Args:
            max_steps: Maximum steps to run (None = until completion)
            
        Returns:
            Final validation metrics
        """
        self.is_running = True
        self.time_keeper.start()
        
        logger.info("=" * 60)
        logger.info("SIMULATION STARTED")
        logger.info(f"Compression ratio: {self.config.time.compression_ratio}x")
        logger.info("=" * 60)
        
        try:
            while self.is_running and not self.time_keeper.is_finished:
                # Check step limit
                if max_steps and self.step_count >= max_steps:
                    logger.info(f"Reached max steps: {max_steps}")
                    break
                
                # Run one step
                self._run_step()
                self.step_count += 1
                
                # Log progress periodically
                if self.step_count % 100 == 0:
                    self._log_progress()
                
                # Checkpoint periodically
                if self.step_count % self.config.storage.checkpoint_interval == 0:
                    self._save_checkpoint()
        
        except KeyboardInterrupt:
            logger.info("Simulation interrupted by user")
        
        finally:
            self.is_running = False
            self._finalize()
        
        # Get final metrics
        trust_scores = {
            aid: agent.trust_score 
            for aid, agent in self.agents.items()
        }
        metrics = self.observer.calculate_metrics(trust_scores)
        
        logger.info("=" * 60)
        logger.info("SIMULATION COMPLETED")
        logger.info(self.observer.generate_report(trust_scores))
        logger.info("=" * 60)
        
        return metrics
    
    def _run_step(self):
        """Run one simulation step (1 simulated hour)."""
        # Advance time
        self.time_keeper.advance_hours(1.0)
        current_date = self.time_keeper.current_date
        
        # COUNCIL DECISION: Update all agents with current simulation date
        # This ensures complete time isolation from real-world time
        for agent in self.agents.values():
            agent.genome.temporal.set_sim_date(current_date)
        
        # Check for graduations
        new_graduates = self.time_keeper.check_graduations()
        for agent_id in new_graduates:
            agent = self.agents.get(agent_id)
            if agent:
                agent.genome.mark_graduated(current_date)
                logger.info(f"Agent {agent_id} graduated (exam passed)")
        
        # Process active agents
        active_agents = [
            agent for agent in self.agents.values()
            if agent.is_active and not agent.has_graduated
        ]
        
        for agent in active_agents:
            self._process_agent(agent, current_date)

    
    def _process_agent(self, agent: StudentAgent, current_date: date):
        """Process one agent for this step."""
        import random
        
        # Decide if agent is active this hour (based on preferences)
        if not self._should_agent_be_active(agent, current_date):
            return
        
        # Decide action
        action = agent.decide_action()
        
        if action == AgentAction.LEAVE_PLATFORM:
            agent.genome.mark_churned("trust_too_low")
            self.time_keeper.mark_churned(agent.agent_id)
            logger.info(f"Agent {agent.agent_id} churned (trust: {agent.trust_score:.2f})")
            return
        
        if action == AgentAction.SKIP_SESSION:
            return  # Do nothing this hour
        
        # Get a question
        question, recommendation = self.question_provider.get_question_for_agent(agent)
        
        # === CRITICAL: Validate content access ===
        violation = self.observer.validate_content_access(
            agent.agent_id,
            question.concept_id,
            question.is_12th_content
        )
        if violation:
            logger.error(f"STANDARD VIOLATION: {violation.message}")
        
        # Attempt question
        result, quality = agent.attempt_question(question, recommendation)
        self.interactions_count += 1
        
        # Validate with observer
        self.observer.validate_interaction(
            agent_id=agent.agent_id,
            concept_id=question.concept_id,
            inferred_mastery=agent.genome.knowledge.get_mastery(question.concept_id),
            interaction_count=agent.total_interactions,
            response_time_seconds=result.response_time_seconds,
            is_12th_content=question.is_12th_content,
            fatigue_level=result.fatigue_at_answer,
        )
        
        # Log interaction - AUDIT FIX: Added persona_type for per-persona analytics
        self.data_writer.log_interaction({
            "interaction_id": str(uuid.uuid4()),
            "agent_id": agent.agent_id,
            "persona_type": agent.genome.persona_type.name,  # AUDIT FIX
            "standard": agent.genome.standard,  # AUDIT FIX
            "is_dropper": agent.genome.is_dropper,  # AUDIT FIX
            "days_to_exam": agent.genome.temporal.days_to_exam,  # AUDIT FIX
            "timestamp": datetime.now().isoformat(),
            "sim_timestamp": self.time_keeper.current_datetime.isoformat(),
            "question_id": question.question_id,
            "concept_id": question.concept_id,
            "subject": question.subject,
            "is_correct": result.is_correct,
            "outcome": result.outcome.value,
            "response_time_seconds": result.response_time_seconds,
            "theta_effective": result.theta_effective,
            "probability_correct": result.probability_correct,
            "fatigue_level": result.fatigue_at_answer,
            "anxiety_level": result.anxiety_at_answer,
            "confidence_self_report": result.confidence_self_report,
            "session_questions_count": agent.current_session.questions_attempted if agent.current_session else 0,
            "session_accuracy": agent.current_session.current_accuracy if agent.current_session else 0,
            "trust_score": agent.trust_score,
            "trust_zone": agent.trust_engine.state.zone.value,
            "standard_violation": result.standard_violation,
        })
    
    def _should_agent_be_active(self, agent: StudentAgent, current_date: date) -> bool:
        """Check if agent should be active this hour."""
        import random
        
        # Base probability from consistency
        base_prob = agent.genome.behavioral.consistency_factor * 0.3
        
        # Higher on weekdays
        if current_date.weekday() < 5:
            base_prob *= 1.2
        else:
            base_prob *= agent.genome.behavioral.weekend_multiplier
        
        return random.random() < base_prob
    
    # =========================================================================
    # UTILITIES
    # =========================================================================
    
    def _log_progress(self):
        """Log progress update."""
        status = self.time_keeper.get_status()
        active = len([a for a in self.agents.values() if a.is_active])
        
        logger.info(
            f"Step {self.step_count}: "
            f"SimDay={status['sim_elapsed_days']:.1f}, "
            f"Active={active}/{status['agents_total']}, "
            f"Graduated={status['agents_graduated']}, "
            f"Churned={status['agents_churned']}, "
            f"Interactions={self.interactions_count}"
        )
    
    def _save_checkpoint(self):
        """Save simulation checkpoint."""
        checkpoint_id = f"checkpoint_{self.step_count}"
        
        # Collect state
        state = {
            "step_count": self.step_count,
            "interactions_count": self.interactions_count,
            "time_keeper_status": self.time_keeper.get_status(),
            "observer_summary": self.observer.get_summary(),
            "agent_stats": {
                "active": len([a for a in self.agents.values() if a.is_active]),
                "graduated": len([a for a in self.agents.values() if a.has_graduated]),
                "churned": len([a for a in self.agents.values() if a.genome.churn_reason]),
            }
        }
        
        self.checkpoint_manager.save_checkpoint(checkpoint_id, state)
        
        # Also flush data
        self.data_writer.flush_all()
    
    def _finalize(self):
        """Finalize simulation."""
        # Flush all data
        self.data_writer.flush_all()
        
        # Save final checkpoint
        self.checkpoint_manager.save_checkpoint(
            "final",
            {
                "completed_at": datetime.now().isoformat(),
                "total_steps": self.step_count,
                "total_interactions": self.interactions_count,
                "observer_summary": self.observer.get_summary(),
            }
        )
        
        logger.info("Simulation finalized")
    
    def stop(self):
        """Stop the simulation."""
        self.is_running = False
    
    def get_status(self) -> dict:
        """Get current simulation status."""
        return {
            "is_running": self.is_running,
            "step_count": self.step_count,
            "interactions_count": self.interactions_count,
            "time_keeper": self.time_keeper.get_status(),
            "observer": self.observer.get_summary(),
            "data_writer": self.data_writer.get_stats(),
        }
