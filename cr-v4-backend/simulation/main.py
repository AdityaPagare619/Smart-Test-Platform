"""
CR-V4 Simulation Entry Point

Run this file to execute the simulation.

Usage:
    python -m simulation.main [options]
    
Options:
    --agents N       Number of agents (default: 100)
    --compression N  Time compression ratio (default: 100)
    --steps N        Max steps to run (default: unlimited)
    --exam-date      Target exam date YYYY-MM-DD (default: 2025-01-22)
    --adversarial    Enable adversarial mode (20% bad recommendations)
"""

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from simulation.orchestrator.main import SimulationOrchestrator
from simulation.config import SimulationConfig, TimeConfig


def setup_logging(verbose: bool = True):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S',
    )
    
    # Reduce noise from some modules
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='CR-V4 AI Engine Simulation System',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument(
        '--agents', '-a',
        type=int,
        default=100,
        help='Number of student agents to simulate'
    )
    
    parser.add_argument(
        '--compression', '-c',
        type=float,
        default=100.0,
        help='Time compression ratio (100 = 100x faster)'
    )
    
    parser.add_argument(
        '--steps', '-s',
        type=int,
        default=None,
        help='Maximum simulation steps (None = run to completion)'
    )
    
    parser.add_argument(
        '--exam-date', '-e',
        type=str,
        default='2025-01-22',
        help='Target JEE exam date (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--turbo',
        action='store_true',
        help='Use turbo mode (1000x compression)'
    )
    
    # AUDIT FIX: Added adversarial mode for trust decay testing
    parser.add_argument(
        '--adversarial',
        action='store_true',
        help='Enable adversarial mode (20%% bad recommendations to test trust decay)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Parse exam date
    try:
        exam_parts = args.exam_date.split('-')
        exam_date = date(int(exam_parts[0]), int(exam_parts[1]), int(exam_parts[2]))
    except (ValueError, IndexError):
        logger.error(f"Invalid exam date format: {args.exam_date}")
        logger.error("Use YYYY-MM-DD format")
        return 1
    
    # Configure
    compression = 1000.0 if args.turbo else args.compression
    config = SimulationConfig(
        time=TimeConfig(compression_ratio=compression),
    )
    
    logger.info("=" * 60)
    logger.info("CR-V4 HIGH-FIDELITY USER SIMULATION SYSTEM")
    logger.info("=" * 60)
    logger.info(f"Agents: {args.agents}")
    logger.info(f"Compression: {compression}x")
    logger.info(f"Target Exam: {exam_date}")
    logger.info(f"Max Steps: {args.steps or 'unlimited'}")
    if args.adversarial:
        logger.info("Mode: ⚠️ ADVERSARIAL (20% bad recommendations)")
    logger.info("=" * 60)
    
    # Create and initialize orchestrator
    orchestrator = SimulationOrchestrator(
        config=config,
        adversarial_mode=args.adversarial  # AUDIT FIX
    )
    orchestrator.initialize(
        agent_count=args.agents,
        target_exam_date=exam_date,
    )
    
    # Run simulation
    try:
        metrics = orchestrator.run(max_steps=args.steps)
        
        # Summary
        logger.info("")
        logger.info("=" * 60)
        logger.info("SIMULATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Steps: {orchestrator.step_count}")
        logger.info(f"Total Interactions: {orchestrator.interactions_count}")
        logger.info(f"RMSE: {metrics.rmse:.4f}")
        logger.info(f"MAE: {metrics.mae:.4f}")
        logger.info(f"Trust Retention: {metrics.trust_retention_rate*100:.1f}%")
        logger.info(f"Standard Violations: {metrics.standard_violations}")
        
        # AUDIT FIX: Log adversarial stats
        if args.adversarial:
            adv_stats = orchestrator.question_provider.get_adversarial_stats()
            logger.info(f"Adversarial Questions: {adv_stats['adversarial_count']} ({adv_stats['actual_rate']*100:.1f}%)")
        
        logger.info(f"Status: {'✅ PASS' if metrics.is_passing() else '❌ FAIL'}")
        logger.info("=" * 60)
        
        return 0 if metrics.is_passing() else 1
        
    except KeyboardInterrupt:
        logger.info("Simulation interrupted")
        return 130  # Standard interrupt code


if __name__ == "__main__":
    sys.exit(main())

