"""
CR-V4 Per-Persona Analytics Generator

This script analyzes simulation data to generate per-persona behavior reports.

AUDIT FIX: Created to address the "Per-Persona Analytics Missing" gap.

Usage:
    python -m simulation.analyze_personas
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import statistics
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pyarrow.parquet as pq
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False


def load_all_interactions(data_dir: str = "simulation/data/parquet/interactions"):
    """Load all interaction data from Parquet files."""
    if not HAS_PYARROW:
        print("ERROR: PyArrow not installed. Run: pip install pyarrow")
        return []
    
    all_records = []
    
    if not os.path.exists(data_dir):
        print(f"ERROR: Data directory not found: {data_dir}")
        return []
    
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.parquet')])
    print(f"Loading {len(files)} Parquet files...")
    
    for f in files:
        try:
            table = pq.read_table(os.path.join(data_dir, f))
            all_records.extend(table.to_pylist())
        except Exception as e:
            print(f"Warning: Could not read {f}: {e}")
    
    print(f"Loaded {len(all_records):,} total interactions")
    return all_records


def analyze_by_persona(records: list) -> dict:
    """Analyze records grouped by persona type."""
    
    persona_stats = defaultdict(lambda: {
        "count": 0,
        "correct": 0,
        "response_times": [],
        "trust_scores": [],
        "outcomes": defaultdict(int),
        "subjects": defaultdict(int),
        "trust_zones": defaultdict(int),
        "agents": set(),
        "standard_violations": 0,
        "days_to_exam": [],
    })
    
    for r in records:
        persona = r.get("persona_type", "UNKNOWN")
        stats = persona_stats[persona]
        
        stats["count"] += 1
        if r.get("is_correct"):
            stats["correct"] += 1
        
        stats["response_times"].append(r.get("response_time_seconds", 0) or 0)
        stats["trust_scores"].append(r.get("trust_score", 1) or 1)
        stats["outcomes"][r.get("outcome", "unknown")] += 1
        stats["subjects"][r.get("subject", "unknown")] += 1
        stats["trust_zones"][r.get("trust_zone", "unknown")] += 1
        stats["agents"].add(r.get("agent_id", ""))
        
        if r.get("standard_violation"):
            stats["standard_violations"] += 1
        
        dte = r.get("days_to_exam")
        if dte is not None:
            stats["days_to_exam"].append(dte)
    
    # Calculate summary metrics
    results = {}
    for persona, stats in persona_stats.items():
        count = stats["count"]
        results[persona] = {
            "total_interactions": count,
            "unique_agents": len(stats["agents"]),
            "avg_interactions_per_agent": count / max(1, len(stats["agents"])),
            "accuracy": stats["correct"] / max(1, count),
            "avg_response_time": statistics.mean(stats["response_times"]) if stats["response_times"] else 0,
            "response_time_std": statistics.stdev(stats["response_times"]) if len(stats["response_times"]) > 1 else 0,
            "avg_trust_score": statistics.mean(stats["trust_scores"]) if stats["trust_scores"] else 0,
            "min_trust_score": min(stats["trust_scores"]) if stats["trust_scores"] else 0,
            "outcomes": dict(stats["outcomes"]),
            "subjects": dict(stats["subjects"]),
            "trust_zones": dict(stats["trust_zones"]),
            "standard_violations": stats["standard_violations"],
            "avg_days_to_exam": statistics.mean(stats["days_to_exam"]) if stats["days_to_exam"] else 0,
            
            # Calculate outcome percentages
            "guess_rate": stats["outcomes"].get("guessed_right", 0) / max(1, count),
            "knew_it_rate": stats["outcomes"].get("knew_it", 0) / max(1, count),
            "careless_error_rate": stats["outcomes"].get("careless_error", 0) / max(1, count),
        }
    
    return results


def generate_report(persona_stats: dict, output_file: str = None):
    """Generate human-readable report."""
    
    lines = [
        "=" * 70,
        "CR-V4 SIMULATION - PER-PERSONA ANALYTICS REPORT",
        "=" * 70,
        "",
    ]
    
    # Sort personas by interaction count
    sorted_personas = sorted(
        persona_stats.items(), 
        key=lambda x: x[1]["total_interactions"], 
        reverse=True
    )
    
    for persona, stats in sorted_personas:
        lines.extend([
            f"📊 {persona}",
            "-" * 50,
            f"   Agents: {stats['unique_agents']}",
            f"   Total Interactions: {stats['total_interactions']:,}",
            f"   Avg per Agent: {stats['avg_interactions_per_agent']:.1f}",
            "",
            f"   Accuracy: {stats['accuracy']*100:.2f}%",
            f"   Avg Response Time: {stats['avg_response_time']:.1f}s (±{stats['response_time_std']:.1f}s)",
            f"   Avg Trust Score: {stats['avg_trust_score']:.4f}",
            f"   Min Trust Score: {stats['min_trust_score']:.4f}",
            "",
            f"   Outcomes:",
            f"      - knew_it: {stats['knew_it_rate']*100:.1f}%",
            f"      - guessed_right: {stats['guess_rate']*100:.1f}%",
            f"      - careless_error: {stats['careless_error_rate']*100:.1f}%",
            "",
            f"   Standard Violations: {stats['standard_violations']}",
            f"   Avg Days to Exam: {stats['avg_days_to_exam']:.0f}",
            "",
        ])
        
        # PERSONA-SPECIFIC VALIDATIONS
        lines.append("   Validation Checks:")
        
        if persona == "DISENGAGED_GAMER":
            # Should have high guessing rate
            if stats["guess_rate"] > 0.25:
                lines.append("      ✅ High guessing rate confirmed (>25%)")
            else:
                lines.append(f"      ⚠️ Guessing rate lower than expected: {stats['guess_rate']*100:.1f}%")
        
        elif persona == "ANXIOUS_PERFECTIONIST":
            # Should have high accuracy despite anxiety
            if stats["accuracy"] > 0.5:
                lines.append("      ✅ High accuracy confirmed (>50%)")
            else:
                lines.append(f"      ⚠️ Accuracy lower than expected: {stats['accuracy']*100:.1f}%")
        
        elif persona == "STRUGGLING_PERSISTER":
            # Should have lower accuracy but high engagement
            if stats["avg_interactions_per_agent"] > 150:
                lines.append("      ✅ High engagement (persistence) confirmed")
            else:
                lines.append(f"      ⚠️ Engagement lower than expected: {stats['avg_interactions_per_agent']:.0f}")
        
        elif persona == "FAST_TRACKER":
            # Should have fast response times
            if stats["avg_response_time"] < 80:
                lines.append("      ✅ Fast response times confirmed (<80s)")
            else:
                lines.append(f"      ⚠️ Response time higher than expected: {stats['avg_response_time']:.1f}s")
        
        lines.append("")
    
    # Summary
    lines.extend([
        "=" * 70,
        "SUMMARY",
        "=" * 70,
        f"Total Personas: {len(persona_stats)}",
        f"Total Interactions: {sum(s['total_interactions'] for s in persona_stats.values()):,}",
        f"Total Agents: {sum(s['unique_agents'] for s in persona_stats.values())}",
        f"Total Standard Violations: {sum(s['standard_violations'] for s in persona_stats.values())}",
        "",
    ])
    
    report = "\n".join(lines)
    print(report)
    
    # Save report
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {output_file}")
    
    return report


def main():
    """Main entry point."""
    print("CR-V4 Per-Persona Analytics Generator")
    print("=" * 50)
    
    # Load data
    records = load_all_interactions()
    
    if not records:
        print("No data to analyze.")
        return 1
    
    # Check if persona_type is in the data
    sample = records[0]
    if "persona_type" not in sample:
        print("\nERROR: persona_type not found in interaction logs.")
        print("This data was logged before the audit fix was applied.")
        print("\nTo fix: Run a new simulation with the updated code:")
        print("  python -m simulation.main --agents 100 --turbo --exam-date 2026-01-20")
        return 1
    
    # Analyze
    print("\nAnalyzing by persona type...")
    persona_stats = analyze_by_persona(records)
    
    # Generate report
    output_dir = "simulation/data/reports"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "per_persona_analytics.txt")
    
    generate_report(persona_stats, output_file)
    
    # Also save JSON for programmatic access
    json_file = os.path.join(output_dir, "per_persona_analytics.json")
    with open(json_file, 'w') as f:
        json.dump(persona_stats, f, indent=2)
    print(f"JSON data saved to: {json_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
