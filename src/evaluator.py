"""
Evaluation Suite & Benchmark Metrics Engine
For Honeywell AI Behavioral Anomaly Detection System
"""

import time
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, precision_recall_fscore_support, roc_auc_score

from src.generator import SyntheticDataGenerator
from src.feature_engineering import FeatureExtractor
from src.models.profiler import UnsupervisedBehaviorProfiler
from src.models.classifier import ThreatCategoryClassifier
from src.models.risk_engine import UnifiedRiskEngine


class ModelEvaluator:
    def __init__(self, engine: UnifiedRiskEngine):
        self.engine = engine

    def run_full_evaluation(self, test_df: pd.DataFrame) -> dict:
        """
        Executes comprehensive evaluation on test dataset.
        """
        start_time = time.time()

        # Feature engineering & scoring
        if 'geo_velocity_kmh' in test_df.columns:
            processed_df = test_df.copy()
        else:
            fe = FeatureExtractor()
            processed_df = fe.fit_transform(test_df)

        scored_df = self.engine.evaluate(processed_df)

        elapsed_sec = time.time() - start_time
        throughput = len(test_df) / (elapsed_sec + 1e-6)

        # 1. Binary Detection Metrics (Normal vs Any Anomaly)
        y_true_binary = (scored_df['label'] != 'normal').astype(int)
        # Threshold risk score >= 55 as anomaly prediction
        y_pred_binary = (scored_df['risk_score'] >= 55.0).astype(int)

        prec, rec, f1, _ = precision_recall_fscore_support(y_true_binary, y_pred_binary, average='binary')

        # 2. Multi-Class Threat Classification Metrics
        y_true_class = scored_df['label']
        y_pred_class = scored_df['predicted_threat']
        cls_report = classification_report(y_true_class, y_pred_class, output_dict=True, zero_division=0)

        # 3. Alert Budget FPR Analysis (Top 1% Alert Budget)
        top_1_percent_count = max(1, int(len(scored_df) * 0.01))
        top_alerts = scored_df.sort_values(by='risk_score', ascending=False).head(top_1_percent_count)
        
        # Calculate FPR at top 1% threshold
        negatives = scored_df[scored_df['label'] == 'normal']
        fp_count = (top_alerts['label'] == 'normal').sum()
        fpr_top_1pct = fp_count / (len(negatives) + 1e-6)

        # 4. Cold Start & Drift Analysis
        cold_events = scored_df[scored_df['cold_start_modifier'] > 0.2]
        if len(cold_events) > 0:
            cold_fp = (cold_events['risk_score'] >= 55.0) & (cold_events['label'] == 'normal')
            cold_fpr = cold_fp.sum() / len(cold_events)
        else:
            cold_fpr = 0.0

        results = {
            "total_events": len(test_df),
            "evaluation_time_sec": round(elapsed_sec, 3),
            "throughput_events_per_sec": round(throughput, 1),
            "binary_detection": {
                "precision": round(float(prec), 4),
                "recall": round(float(rec), 4),
                "f1_score": round(float(f1), 4)
            },
            "alert_budget_1pct": {
                "budget_alert_count": top_1_percent_count,
                "false_positive_rate": round(float(fpr_top_1pct), 4),
                "top_alerts_precision": round(float((top_alerts['label'] != 'normal').sum() / top_1_percent_count), 4)
            },
            "cold_start": {
                "cold_events_evaluated": len(cold_events),
                "cold_start_fpr": round(float(cold_fpr), 4)
            },
            "per_class_f1": {k: round(v['f1-score'], 3) for k, v in cls_report.items() if isinstance(v, dict)}
        }

        return results, scored_df


if __name__ == "__main__":
    print("Running evaluation suite test...")
    gen = SyntheticDataGenerator(num_entities=30, seed=123)
    train_raw = gen.generate_dataset(num_events=1000, anomaly_rate=0.03)
    test_raw = gen.generate_dataset(num_events=500, anomaly_rate=0.04)

    fe = FeatureExtractor()
    train_proc = fe.fit_transform(train_raw)

    profiler = UnsupervisedBehaviorProfiler()
    profiler.fit(train_proc)

    clf = ThreatCategoryClassifier()
    clf.fit(train_proc, train_proc['label'])

    engine = UnifiedRiskEngine(profiler, clf)
    evaluator = ModelEvaluator(engine)

    metrics, scored_df = evaluator.run_full_evaluation(test_raw)
    import json
    print(json.dumps(metrics, indent=2))
