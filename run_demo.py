"""
Master Runner & Demonstration Script
For BehaviorIQ AI Behavioral Anomaly Detection System
"""

import os
import sys
import json
import uvicorn

from src.generator import SyntheticDataGenerator
from src.feature_engineering import FeatureExtractor
from src.models.profiler import UnsupervisedBehaviorProfiler
from src.models.classifier import ThreatCategoryClassifier
from src.models.risk_engine import UnifiedRiskEngine
from src.evaluator import ModelEvaluator


def main():
    print("=" * 70)
    print("  BEHAVIORIQ: AUTONOMOUS BEHAVIORAL ANOMALY DETECTION SYSTEM")
    print("=" * 70)

    # Step 1: Generate Synthetic Access Logs
    print("\n[1/5] Generating Synthetic Access Log Datasets...")
    gen = SyntheticDataGenerator(num_entities=50, seed=42)
    train_raw = gen.generate_dataset(num_events=2500, anomaly_rate=0.03, cold_start_rate=0.08)
    test_raw = gen.generate_dataset(num_events=800, anomaly_rate=0.04, cold_start_rate=0.10)
    
    os.makedirs("data", exist_ok=True)
    train_raw.to_csv("data/synthetic_logs.csv", index=False)
    print(f"      ✓ Generated {len(train_raw)} training events and {len(test_raw)} testing events.")
    print("      ✓ Injected Attack Vectors:", train_raw['label'].unique().tolist())

    # Step 2: Feature Extraction
    print("\n[2/5] Extracting Geo-Velocity, Temporal & Graph Features...")
    fe = FeatureExtractor()
    train_proc = fe.fit_transform(train_raw)
    test_proc = fe.fit_transform(test_raw)
    print(f"      ✓ Feature matrix shape: {train_proc.shape}")

    # Step 3: Model Training
    print("\n[3/5] Training Unsupervised Behavioral Profiler & Multi-Class Classifier...")
    profiler = UnsupervisedBehaviorProfiler(contamination=0.03)
    profiler.fit(train_proc)
    
    classifier = ThreatCategoryClassifier(use_lightgbm=True)
    classifier.fit(train_proc, train_proc['label'])
    print("      ✓ Unsupervised Isolation Profiler and Multi-Class LightGBM Classifier Trained Successfully.")

    # Step 4: System Evaluation & Benchmark
    print("\n[4/5] Running Comprehensive Evaluation Suite...")
    engine = UnifiedRiskEngine(profiler, classifier)
    evaluator = ModelEvaluator(engine)
    metrics, scored_df = evaluator.run_full_evaluation(test_raw)

    print("\n--- BENCHMARK EVALUATION RESULTS ---")
    print(f"  • Binary Anomaly Precision: {metrics['binary_detection']['precision']:.4f}")
    print(f"  • Binary Anomaly Recall:    {metrics['binary_detection']['recall']:.4f}")
    print(f"  • Binary Anomaly F1-Score:  {metrics['binary_detection']['f1_score']:.4f}")
    print(f"  • Alert Budget FPR (Top 1%):{metrics['alert_budget_1pct']['false_positive_rate'] * 100:.2f}%")
    print(f"  • Cold-Start Entity FPR:   {metrics['cold_start']['cold_start_fpr'] * 100:.2f}%")
    print(f"  • Throughput:               {metrics['throughput_events_per_sec']:.1f} events/sec")
    print("------------------------------------")

    # Step 5: Start Web Server
    print("\n[5/5] Launching BehaviorIQ SOC Command Center Web Dashboard...")
    print("      👉 Open your browser at: http://127.0.0.1:8000")
    print("      Press Ctrl+C to stop the server.\n")

    from app.backend import app
    uvicorn.run(app, host="127.0.0.1", port=8000)



if __name__ == "__main__":
    main()
