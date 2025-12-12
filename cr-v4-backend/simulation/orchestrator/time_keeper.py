"""
CR-V4 Time Keeper Module

This module manages time compression and simulation period logic.

COUNCIL DECISIONS IMPLEMENTED:
1. Simulation is EXAM-BOUND (not endless)
2. Time compression configurable (1x, 100x, 1000x)
3. Each agent has a target_exam_date
4. Agent stops when exam date passes (graduates)
5. Simulation ends when all agents graduate or churn
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set
import time


# =============================================================================
# ENUMS
# =============================================================================

class SimulationPhase(Enum):
    """Phases of simulation execution."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETING = "completing"
    FINISHED = "finished"


class TimeScale(Enum):
    """Time compression presets."""
    REALTIME = 1.0        # 1 second = 1 second
    FAST = 10.0           # 1 second = 10 seconds
    TURBO = 100.0         # 1 second = 100 seconds (default)
    ULTRA = 1000.0        # 1 second = 1000 seconds
    HYPERDRIVE = 10000.0  # 1 second = 10000 seconds (2.7 hours)


# =============================================================================
# TIME KEEPER
# =============================================================================

@dataclass
class TimeState:
    """Current state of simulation time."""
    # Real time tracking
    real_start_time: datetime = field(default_factory=datetime.now)
    real_elapsed_seconds: float = 0.0
    
    # Simulated time tracking
    sim_start_date: date = field(default_factory=date.today)
    sim_current_datetime: datetime = field(default_factory=datetime.now)
    sim_elapsed_days: float = 0.0
    
    # Progress
    tick_count: int = 0
    phase: SimulationPhase = SimulationPhase.INITIALIZING
    
    # Bounds
    sim_end_date: Optional[date] = None  # Latest exam date
    
    @property
    def sim_current_date(self) -> date:
        """Get current simulated date."""
        return self.sim_current_datetime.date()


class TimeKeeper:
    """
    Manages time compression and simulation period.
    
    Key Responsibilities:
    1. Advance simulated time at compressed rate
    2. Track which agents have passed their exam dates
    3. Signal when simulation should end
    4. Provide time context to all components
    
    CRITICAL: Simulation is EXAM-BOUND:
    - Each agent has a target_exam_date
    - When sim_current_date >= target_exam_date, agent "graduates"
    - Simulation ends when all agents are done (graduated or churned)
    """
    
    def __init__(
        self,
        compression_ratio: float = 100.0,
        sim_start_date: Optional[date] = None,
        max_sim_days: int = 730  # Max 2 years
    ):
        """
        Initialize time keeper.
        
        Args:
            compression_ratio: How much faster sim time runs
                              100.0 = 1 real second = 100 sim seconds
            sim_start_date: When simulation starts (default: today)
            max_sim_days: Maximum simulated days (safety limit)
        """
        self.compression_ratio = compression_ratio
        self.max_sim_days = max_sim_days
        
        # Initialize state
        now = datetime.now()
        self.state = TimeState(
            real_start_time=now,
            sim_start_date=sim_start_date or date.today(),
            sim_current_datetime=datetime.combine(
                sim_start_date or date.today(),
                datetime.min.time()
            ),
        )
        
        # Track agent exam dates
        self.agent_exam_dates: Dict[str, date] = {}
        self.graduated_agents: Set[str] = set()
        self.churned_agents: Set[str] = set()
        
        # Performance tracking
        self._last_tick_real_time = time.time()
    
    @property
    def current_date(self) -> date:
        """Get current simulated date."""
        return self.state.sim_current_date
    
    @property
    def current_datetime(self) -> datetime:
        """Get current simulated datetime."""
        return self.state.sim_current_datetime
    
    @property
    def elapsed_sim_days(self) -> float:
        """Get elapsed simulated days."""
        return self.state.sim_elapsed_days
    
    @property
    def elapsed_real_seconds(self) -> float:
        """Get elapsed real seconds."""
        return self.state.real_elapsed_seconds
    
    @property
    def is_finished(self) -> bool:
        """Check if simulation should end."""
        return self.state.phase == SimulationPhase.FINISHED
    
    # =========================================================================
    # AGENT MANAGEMENT
    # =========================================================================
    
    def register_agent(self, agent_id: str, target_exam_date: date):
        """
        Register an agent with their exam date.
        
        Args:
            agent_id: Unique agent identifier
            target_exam_date: When agent's exam is
        """
        self.agent_exam_dates[agent_id] = target_exam_date
        
        # Update simulation end date to latest exam
        if self.state.sim_end_date is None:
            self.state.sim_end_date = target_exam_date
        else:
            self.state.sim_end_date = max(
                self.state.sim_end_date, 
                target_exam_date
            )
    
    def mark_graduated(self, agent_id: str):
        """Mark agent as graduated (exam passed)."""
        self.graduated_agents.add(agent_id)
    
    def mark_churned(self, agent_id: str):
        """Mark agent as churned (left platform)."""
        self.churned_agents.add(agent_id)
    
    def get_active_agents(self) -> Set[str]:
        """Get agents that are still active."""
        all_agents = set(self.agent_exam_dates.keys())
        done = self.graduated_agents | self.churned_agents
        return all_agents - done
    
    def check_graduations(self) -> List[str]:
        """
        Check which agents should graduate (exam date passed).
        
        Returns:
            List of agent IDs that just graduated
        """
        new_graduates = []
        current = self.current_date
        
        for agent_id, exam_date in self.agent_exam_dates.items():
            if agent_id not in self.graduated_agents:
                if agent_id not in self.churned_agents:
                    if current >= exam_date:
                        self.graduated_agents.add(agent_id)
                        new_graduates.append(agent_id)
        
        return new_graduates
    
    # =========================================================================
    # TIME ADVANCEMENT
    # =========================================================================
    
    def tick(self, real_elapsed_seconds: Optional[float] = None) -> datetime:
        """
        Advance simulation time by one tick.
        
        Args:
            real_elapsed_seconds: Real time since last tick
                                 (auto-calculated if None)
        
        Returns:
            New simulated datetime
        """
        # Calculate real elapsed
        now = time.time()
        if real_elapsed_seconds is None:
            real_elapsed_seconds = now - self._last_tick_real_time
        self._last_tick_real_time = now
        
        # Calculate simulated elapsed
        sim_elapsed_seconds = real_elapsed_seconds * self.compression_ratio
        
        # Update state
        self.state.real_elapsed_seconds += real_elapsed_seconds
        self.state.tick_count += 1
        
        # Advance simulated time
        self.state.sim_current_datetime += timedelta(seconds=sim_elapsed_seconds)
        self.state.sim_elapsed_days = (
            self.state.sim_current_datetime - 
            datetime.combine(self.state.sim_start_date, datetime.min.time())
        ).total_seconds() / 86400
        
        # Check for simulation end conditions
        self._check_end_conditions()
        
        return self.state.sim_current_datetime
    
    def advance_hours(self, hours: float) -> datetime:
        """
        Advance simulation by specified hours.
        
        Useful for discrete-time simulation mode.
        
        Args:
            hours: Simulated hours to advance
            
        Returns:
            New simulated datetime
        """
        self.state.sim_current_datetime += timedelta(hours=hours)
        self.state.sim_elapsed_days += hours / 24
        self.state.tick_count += 1
        
        # Calculate equivalent real time
        sim_seconds = hours * 3600
        real_seconds = sim_seconds / self.compression_ratio
        self.state.real_elapsed_seconds += real_seconds
        
        self._check_end_conditions()
        return self.state.sim_current_datetime
    
    def _check_end_conditions(self):
        """Check if simulation should end."""
        # Safety limit
        if self.state.sim_elapsed_days >= self.max_sim_days:
            self.state.phase = SimulationPhase.FINISHED
            return
        
        # All agents done
        active = self.get_active_agents()
        if len(active) == 0 and len(self.agent_exam_dates) > 0:
            self.state.phase = SimulationPhase.FINISHED
            return
        
        # Past all exam dates
        if self.state.sim_end_date:
            if self.current_date > self.state.sim_end_date + timedelta(days=7):
                # Week after last exam, definitely done
                self.state.phase = SimulationPhase.FINISHED
                return
    
    # =========================================================================
    # STATUS AND REPORTING
    # =========================================================================
    
    def start(self):
        """Mark simulation as started."""
        self.state.phase = SimulationPhase.RUNNING
        self.state.real_start_time = datetime.now()
        self._last_tick_real_time = time.time()
    
    def pause(self):
        """Pause simulation."""
        self.state.phase = SimulationPhase.PAUSED
    
    def resume(self):
        """Resume simulation."""
        self.state.phase = SimulationPhase.RUNNING
        self._last_tick_real_time = time.time()
    
    def get_status(self) -> dict:
        """Get current time keeper status."""
        active = len(self.get_active_agents())
        total = len(self.agent_exam_dates)
        
        return {
            "phase": self.state.phase.value,
            "compression_ratio": self.compression_ratio,
            "real_elapsed_seconds": self.state.real_elapsed_seconds,
            "real_elapsed_hours": self.state.real_elapsed_seconds / 3600,
            "sim_current_date": self.current_date.isoformat(),
            "sim_elapsed_days": round(self.state.sim_elapsed_days, 2),
            "sim_elapsed_months": round(self.state.sim_elapsed_days / 30, 2),
            "tick_count": self.state.tick_count,
            "agents_total": total,
            "agents_active": active,
            "agents_graduated": len(self.graduated_agents),
            "agents_churned": len(self.churned_agents),
            "progress_percent": round(
                (len(self.graduated_agents) + len(self.churned_agents)) / max(1, total) * 100,
                1
            ),
        }
    
    def estimate_completion(self) -> Optional[timedelta]:
        """
        Estimate remaining real time to completion.
        
        Returns:
            Estimated remaining time, or None if can't estimate
        """
        if len(self.graduated_agents) == 0:
            return None
        
        if self.state.sim_end_date is None:
            return None
        
        # Days remaining in simulation
        remaining_sim_days = (self.state.sim_end_date - self.current_date).days
        if remaining_sim_days <= 0:
            return timedelta(seconds=0)
        
        # Real seconds per sim day (based on current rate)
        if self.state.sim_elapsed_days > 0:
            real_seconds_per_sim_day = (
                self.state.real_elapsed_seconds / self.state.sim_elapsed_days
            )
            remaining_real_seconds = remaining_sim_days * real_seconds_per_sim_day
            return timedelta(seconds=remaining_real_seconds)
        
        return None
