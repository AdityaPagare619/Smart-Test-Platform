"""
CR-V4 STRESS TEST SUITE
=======================

COUNCIL REVIEW: VERCEL OPTIMIZATION & SCALABILITY

Purpose:
1. Benchmark engine performance under load
2. Identify bottlenecks before production
3. Verify Vercel serverless compatibility
4. Provide honest council assessment

Vercel Constraints:
- Serverless functions (10s max execution time free tier)
- Edge functions (50ms target, 25MB size limit)
- Cold start penalty (~500ms first invocation)
- No persistent memory between requests
- CPU limited (not compute-heavy workloads)

Testing Approach:
1. Single request latency (should be <100ms)
2. Batch processing (1000+ students)
3. Memory usage (should be <50MB per function)
4. Cold start simulation
"""

import time
import sys
import tracemalloc
from typing import Dict, List, Tuple
from datetime import datetime
import random

# Add parent path for imports
sys.path.insert(0, '.')

from app.engine.algorithms.irt_model import (
    IRTParameters, irt_probability, fisher_information,
    estimate_ability, calculate_selection_score
)
from app.engine.algorithms.knowledge_state import (
    StudentKnowledgeState, create_student_state, process_interaction
)
from app.engine.algorithms.question_selector import (
    Question, QuestionSelector, SelectionResult
)
from app.engine.algorithms.misconception_detector import (
    MisconceptionDetector, analyze_and_intervene
)
from app.engine.engine_orchestrator import (
    CognitiveResonanceEngine, create_engine
)

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

# Vercel limits
VERCEL_FREE_TIMEOUT_MS = 10_000  # 10 seconds
VERCEL_EDGE_TARGET_MS = 50       # Edge function target
API_TARGET_LATENCY_MS = 100      # Council requirement

# Test sizes
SMALL_BATCH = 100
MEDIUM_BATCH = 1_000
LARGE_BATCH = 10_000
STRESS_BATCH = 100_000

# Memory limits
MAX_MEMORY_MB = 50  # Serverless constraint

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

class PerformanceMetrics:
    """Track performance metrics for council review"""
    
    def __init__(self):
        self.results = []
        self.warnings = []
        self.failures = []
    
    def add_result(self, test_name: str, duration_ms: float, 
                   memory_mb: float, ops_per_sec: float,
                   passed: bool, notes: str = ""):
        self.results.append({
            'test': test_name,
            'duration_ms': round(duration_ms, 2),
            'memory_mb': round(memory_mb, 2),
            'ops_per_sec': round(ops_per_sec, 1),
            'passed': passed,
            'notes': notes
        })
        
        if not passed:
            self.failures.append(f"{test_name}: {notes}")
        elif duration_ms > API_TARGET_LATENCY_MS:
            self.warnings.append(f"{test_name}: {duration_ms}ms exceeds {API_TARGET_LATENCY_MS}ms target")
    
    def print_report(self):
        print("\n" + "="*80)
        print("COUNCIL STRESS TEST REPORT")
        print("Vercel Optimization & Scalability Assessment")
        print("="*80)
        
        print("\n📊 PERFORMANCE RESULTS:\n")
        print(f"{'Test':<40} {'Time (ms)':<12} {'Memory (MB)':<12} {'Ops/sec':<12} {'Status':<8}")
        print("-" * 84)
        
        for r in self.results:
            status = "✅ PASS" if r['passed'] else "❌ FAIL"
            print(f"{r['test']:<40} {r['duration_ms']:<12} {r['memory_mb']:<12} {r['ops_per_sec']:<12} {status}")
        
        print("\n" + "-"*80)
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        
        print(f"\n📈 SUMMARY: {passed}/{total} tests passed")
        
        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for w in self.warnings:
                print(f"   - {w}")
        
        if self.failures:
            print("\n❌ FAILURES:")
            for f in self.failures:
                print(f"   - {f}")
        
        # Council verdict
        print("\n" + "="*80)
        print("COUNCIL VERDICT:")
        
        if len(self.failures) == 0 and len(self.warnings) <= 2:
            print("🟢 GREEN - Ready for Vercel production deployment")
        elif len(self.failures) == 0:
            print("🟡 YELLOW - Acceptable with optimizations")
        else:
            print("🔴 RED - NOT READY - Critical issues must be fixed")
        
        print("="*80 + "\n")

# ============================================================================
# STRESS TESTS
# ============================================================================

def measure_time(func):
    """Measure execution time in milliseconds"""
    start = time.perf_counter()
    result = func()
    end = time.perf_counter()
    return result, (end - start) * 1000

def measure_memory(func):
    """Measure peak memory usage in MB"""
    tracemalloc.start()
    result = func()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024 / 1024

def test_single_irt_probability(metrics: PerformanceMetrics):
    """Test: Single IRT probability calculation"""
    print("Testing: Single IRT probability...")
    
    def run():
        for _ in range(1000):
            irt_probability(0.5, 1.5, 0.0, 0.25)
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 1000 / (duration / 1000)
    
    passed = duration < 10  # Should be <10ms for 1000 ops
    metrics.add_result(
        "IRT Probability (1000 calls)",
        duration, memory, ops_per_sec, passed,
        "Core math operation"
    )

def test_fisher_information_batch(metrics: PerformanceMetrics):
    """Test: Fisher Information for question pool"""
    print("Testing: Fisher Information batch...")
    
    import numpy as np
    abilities = np.linspace(-3, 3, 1000)
    
    def run():
        for _ in range(100):
            fisher_information(abilities, 1.5, 0.0, 0.25)
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 100 / (duration / 1000)
    
    passed = duration < 100  # Should be <100ms
    metrics.add_result(
        "Fisher Info (100 × 1000 abilities)",
        duration, memory, ops_per_sec, passed,
        "Question selection core"
    )

def test_ability_estimation(metrics: PerformanceMetrics):
    """Test: Student ability estimation"""
    print("Testing: Ability estimation...")
    
    params = [IRTParameters(a=1.0 + i*0.1, b=i*0.2 - 1, c=0.25) for i in range(20)]
    responses = [i % 3 != 0 for i in range(20)]  # ~67% correct
    
    def run():
        for _ in range(100):
            estimate_ability(responses, params)
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 100 / (duration / 1000)
    
    passed = duration < 500  # 100 estimations in <500ms
    metrics.add_result(
        "Ability Estimation (100 students × 20 Q)",
        duration, memory, ops_per_sec, passed,
        "Newton-Raphson iteration"
    )

def test_knowledge_state_update(metrics: PerformanceMetrics):
    """Test: Knowledge state update throughput"""
    print("Testing: Knowledge state updates...")
    
    def run():
        state = create_student_state("STRESS_TEST_001")
        for i in range(500):
            state = process_interaction(
                state,
                concept_id=f"MATH_{i % 50:03d}",
                question_id=f"Q_{i}",
                correct=i % 3 != 0,
                time_taken=60 + (i % 60),
                difficulty=0.3 + (i % 5) * 0.1,
                timestamp=datetime.now()
            )
        return state
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 500 / (duration / 1000)
    
    passed = duration < 500  # 500 updates in <500ms
    metrics.add_result(
        "Knowledge State (500 interactions)",
        duration, memory, ops_per_sec, passed,
        "3 time-scale tracking"
    )

def test_question_selection_batch(metrics: PerformanceMetrics):
    """Test: Batch question selection"""
    print("Testing: Question selection batch...")
    
    # Create test questions
    questions = [
        Question(
            question_id=f"Q_{i}",
            concept_id=f"MATH_{i % 50:03d}",
            subject="MATH",
            irt_params=IRTParameters(
                a=0.8 + (i % 10) * 0.2,
                b=-2 + (i % 20) * 0.2,
                c=0.25
            )
        )
        for i in range(500)
    ]
    
    selector = QuestionSelector(questions, {})
    
    def run():
        results = []
        for _ in range(50):
            state = create_student_state(f"TEST_{_}")
            state.ability = random.uniform(-2, 2)
            result = selector.select_next_question(state)
            results.append(result)
        return results
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 50 / (duration / 1000)
    
    passed = duration < 1000  # 50 selections in <1s
    metrics.add_result(
        "Question Selection (50 students × 500 Q)",
        duration, memory, ops_per_sec, passed,
        "Multi-criteria optimization"
    )

def test_misconception_detection(metrics: PerformanceMetrics):
    """Test: Misconception detection throughput"""
    print("Testing: Misconception detection...")
    
    def run():
        results = []
        for i in range(200):
            result = analyze_and_intervene(
                student_id=f"STU_{i}",
                concept_id=f"PHYS_{i % 50:03d}",
                correct=i % 4 != 0,
                student_answer="test answer with some patterns",
                time_taken=30 + (i % 150),
                question_difficulty=0.3 + (i % 5) * 0.15
            )
            results.append(result)
        return results
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 200 / (duration / 1000)
    
    passed = duration < 500  # 200 detections in <500ms
    metrics.add_result(
        "Misconception Detection (200 responses)",
        duration, memory, ops_per_sec, passed,
        "Pattern matching + recovery"
    )

def test_full_pipeline_single(metrics: PerformanceMetrics):
    """Test: Full pipeline single request (API latency)"""
    print("Testing: Full pipeline single request...")
    
    # Create engine with questions
    questions = [
        Question(
            question_id=f"Q_{i}",
            concept_id=f"MATH_{i % 50:03d}",
            subject="MATH",
            irt_params=IRTParameters(b=-2 + i*0.1)
        )
        for i in range(100)
    ]
    engine = create_engine(questions)
    engine.initialize_student("API_TEST")
    
    def run():
        # Simulate full API request
        response = engine.get_next_question("API_TEST")
        return response
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 1 / (duration / 1000)
    
    passed = duration < API_TARGET_LATENCY_MS  # <100ms requirement
    metrics.add_result(
        "Full Pipeline (single request)",
        duration, memory, ops_per_sec, passed,
        f"API latency target: <{API_TARGET_LATENCY_MS}ms"
    )

def test_full_pipeline_with_answer(metrics: PerformanceMetrics):
    """Test: Full pipeline with answer processing"""
    print("Testing: Full pipeline with answer...")
    
    questions = [
        Question(
            question_id=f"Q_{i}",
            concept_id=f"MATH_{i % 50:03d}",
            subject="MATH",
            irt_params=IRTParameters(b=-2 + i*0.1)
        )
        for i in range(100)
    ]
    engine = create_engine(questions)
    engine.initialize_student("ANSWER_TEST")
    
    def run():
        response = engine.process_answer(
            "ANSWER_TEST", "Q_5", True, 45.0, "test answer"
        )
        return response
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 1 / (duration / 1000)
    
    passed = duration < API_TARGET_LATENCY_MS * 1.5  # Allow slightly more for answer processing
    metrics.add_result(
        "Answer Processing (single)",
        duration, memory, ops_per_sec, passed,
        "Knowledge update + misconception check"
    )

def test_cold_start_simulation(metrics: PerformanceMetrics):
    """Test: Cold start simulation (Vercel serverless)"""
    print("Testing: Cold start simulation...")
    
    def run():
        # Simulate cold start: import all modules + create engine
        from app.engine.algorithms import (
            irt_probability, fisher_information,
            StudentKnowledgeState, QuestionSelector,
            MisconceptionDetector
        )
        from app.engine.engine_orchestrator import CognitiveResonanceEngine
        
        # Create engine with realistic question bank
        questions = [
            Question(
                question_id=f"Q_{i}",
                concept_id=f"MATH_{i % 50:03d}",
                subject="MATH",
                irt_params=IRTParameters(b=-2 + i*0.1)
            )
            for i in range(200)
        ]
        engine = CognitiveResonanceEngine(questions)
        engine.initialize_student("COLD_START")
        response = engine.get_next_question("COLD_START")
        return response
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    
    passed = duration < VERCEL_FREE_TIMEOUT_MS  # Must complete within timeout
    metrics.add_result(
        "Cold Start (import + init + request)",
        duration, memory, 1,
        passed,
        f"Vercel timeout: {VERCEL_FREE_TIMEOUT_MS}ms"
    )

def test_memory_under_load(metrics: PerformanceMetrics):
    """Test: Memory usage under heavy load"""
    print("Testing: Memory under load...")
    
    def run():
        # Create many student states
        states = []
        for i in range(100):
            state = create_student_state(f"MEMORY_TEST_{i}")
            # Add many interactions
            for j in range(50):
                state = process_interaction(
                    state,
                    concept_id=f"MATH_{j % 50:03d}",
                    question_id=f"Q_{j}",
                    correct=j % 3 != 0,
                    time_taken=60,
                    difficulty=0.5,
                    timestamp=datetime.now()
                )
            states.append(state)
        return states
    
    _, duration = measure_time(run)
    result, memory = measure_memory(run)
    
    passed = memory < MAX_MEMORY_MB  # <50MB limit
    metrics.add_result(
        "Memory (100 students × 50 interactions)",
        duration, memory, len(result) / (duration / 1000),
        passed,
        f"Limit: {MAX_MEMORY_MB}MB"
    )

def test_concurrent_students(metrics: PerformanceMetrics):
    """Test: Simulate concurrent student requests"""
    print("Testing: Concurrent students simulation...")
    
    questions = [
        Question(
            question_id=f"Q_{i}",
            concept_id=f"MATH_{i % 50:03d}",
            subject="MATH",
            irt_params=IRTParameters(b=-2 + i*0.1)
        )
        for i in range(200)
    ]
    engine = create_engine(questions)
    
    def run():
        # Simulate 100 concurrent requests
        responses = []
        for i in range(100):
            student_id = f"CONCURRENT_{i}"
            engine.initialize_student(student_id)
            
            # Get question
            resp1 = engine.get_next_question(student_id)
            
            # Process answer
            if resp1.next_question:
                q_id = resp1.next_question.get('question_id', 'Q_0')
                resp2 = engine.process_answer(
                    student_id, q_id, random.random() > 0.3, 60.0
                )
                responses.append(resp2)
        
        return responses
    
    _, duration = measure_time(run)
    _, memory = measure_memory(run)
    ops_per_sec = 100 / (duration / 1000)
    
    # Each request (2 operations) should average <100ms
    passed = duration < 15000  # 100 students × 2 ops in <15s
    metrics.add_result(
        "Concurrent (100 students × 2 ops)",
        duration, memory, ops_per_sec,
        passed,
        "Simulates peak load"
    )

# ============================================================================
# SCALABILITY PROJECTION
# ============================================================================

def print_scalability_analysis(metrics: PerformanceMetrics):
    """Print scalability projections for council"""
    
    print("\n" + "="*80)
    print("📊 SCALABILITY PROJECTION (COUNCIL ANALYSIS)")
    print("="*80)
    
    # Find single request latency
    single_result = next((r for r in metrics.results if "single request" in r['test'].lower()), None)
    
    if single_result:
        latency_ms = single_result['duration_ms']
        
        print(f"\n🔬 Based on measured single-request latency: {latency_ms}ms")
        print()
        
        # Vercel limits
        print("📌 VERCEL SERVERLESS CHARACTERISTICS:")
        print(f"   - Max concurrent functions: 1000 (Pro plan)")
        print(f"   - Function timeout: 10s (free) / 60s (pro)")
        print(f"   - Cold start: ~500ms (mitigated by edge)")
        print()
        
        # Projections
        print("📈 CAPACITY PROJECTIONS:")
        
        requests_per_instance = 1000 / latency_ms  # Requests per second per instance
        
        scenarios = [
            ("Free tier (10 concurrent)", 10),
            ("Pro tier (100 concurrent)", 100),
            ("Enterprise (1000 concurrent)", 1000),
        ]
        
        for name, instances in scenarios:
            rps = requests_per_instance * instances
            daily = rps * 86400
            monthly = daily * 30
            
            print(f"\n   {name}:")
            print(f"      Requests/sec: {rps:,.0f}")
            print(f"      Daily users (10 req/session): {daily/10:,.0f}")
            print(f"      Monthly users: {monthly/10:,.0f}")
        
        print()
        print("💡 COUNCIL RECOMMENDATION:")
        
        if latency_ms < 50:
            print("   🟢 EXCELLENT - Can handle millions of users with Pro tier")
        elif latency_ms < 100:
            print("   🟢 GOOD - Can handle 100K+ daily users with Pro tier")
        elif latency_ms < 200:
            print("   🟡 ACCEPTABLE - May need caching for peak loads")
        else:
            print("   🔴 NEEDS OPTIMIZATION - Reduce latency before production")
    
    print("\n" + "="*80)

# ============================================================================
# VERCEL OPTIMIZATION RECOMMENDATIONS
# ============================================================================

def print_optimization_recommendations():
    """Print Vercel-specific optimization recommendations"""
    
    print("\n" + "="*80)
    print("🔧 VERCEL OPTIMIZATION RECOMMENDATIONS")
    print("="*80)
    
    recommendations = [
        ("1. Edge Caching", 
         "Cache question metadata at edge. 90% of requests can hit cache.",
         "HIGH"),
        
        ("2. Lazy Loading",
         "Don't load all 1815 questions on cold start. Load on demand.",
         "HIGH"),
        
        ("3. Connection Pooling",
         "Use Supabase connection pooler for PostgreSQL. Avoid cold connections.",
         "HIGH"),
        
        ("4. Serialize State",
         "Store student state in Supabase. Don't rely on in-memory state.",
         "CRITICAL"),
        
        ("5. Precompute IRT Scores",
         "Precompute and cache selection scores nightly. O(1) lookup at runtime.",
         "MEDIUM"),
        
        ("6. Split Functions",
         "Separate functions: get_question, process_answer, get_stats. Smaller = faster.",
         "MEDIUM"),
        
        ("7. Use Edge Runtime",
         "For simple lookups, use Edge Runtime (50ms vs 500ms).",
         "HIGH"),
        
        ("8. Minimize Dependencies",
         "NumPy is heavy (~30MB). Use native Python for simple math when possible.",
         "MEDIUM"),
    ]
    
    for name, desc, priority in recommendations:
        icon = "🔴" if priority == "CRITICAL" else "🟡" if priority == "HIGH" else "🟢"
        print(f"\n{icon} {name} [{priority}]")
        print(f"   {desc}")
    
    print("\n" + "="*80)

# ============================================================================
# MAIN
# ============================================================================

def run_all_tests():
    """Run complete stress test suite"""
    
    print("\n" + "="*80)
    print("🚀 CR-V4 STRESS TEST SUITE")
    print("Council Review: Vercel Optimization & Scalability")
    print("="*80)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    metrics = PerformanceMetrics()
    
    # Run all tests
    test_single_irt_probability(metrics)
    test_fisher_information_batch(metrics)
    test_ability_estimation(metrics)
    test_knowledge_state_update(metrics)
    test_question_selection_batch(metrics)
    test_misconception_detection(metrics)
    test_full_pipeline_single(metrics)
    test_full_pipeline_with_answer(metrics)
    test_cold_start_simulation(metrics)
    test_memory_under_load(metrics)
    test_concurrent_students(metrics)
    
    # Print reports
    metrics.print_report()
    print_scalability_analysis(metrics)
    print_optimization_recommendations()
    
    return metrics

if __name__ == "__main__":
    run_all_tests()
