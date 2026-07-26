"""
Composite Risk Engine & Multi-Tier Scoring Pipeline
For Honeywell AI Behavioral Anomaly Detection System
"""

import numpy as np
import pandas as pd

from src.models.profiler import UnsupervisedBehaviorProfiler
from src.models.classifier import ThreatCategoryClassifier
from src.cold_start_drift import ColdStartAndDriftManager
from src.feature_engineering import FeatureExtractor


class UnifiedRiskEngine:
    def __init__(self, profiler: UnsupervisedBehaviorProfiler, classifier: ThreatCategoryClassifier):
        self.profiler = profiler
        self.classifier = classifier
        self.cold_drift_mgr = ColdStartAndDriftManager()

    def evaluate(self, df_processed: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluates a processed DataFrame and returns full scoring, classification, and risk metrics.
        """
        df_eval = df_processed.copy()

        # 1. Profiler Anomaly Score
        anomaly_scores = self.profiler.predict_anomaly_score(df_eval)
        df_eval['profiler_anomaly_score'] = anomaly_scores

        # 2. Threat Classifier Predictions
        pred_labels, confidences = self.classifier.predict_threat_type(df_eval)
        df_eval['predicted_threat'] = pred_labels
        df_eval['classifier_confidence'] = confidences

        # 3. Rule Triggers & Risk Score Calculation
        risk_scores = []
        severities = []
        cold_modifiers = []

        for idx, row in df_eval.iterrows():
            entity_id = row['entry_id']
            etype = row['entity_type']
            feat_vec = row.to_dict()

            # Cold start modifier
            cold_mod = self.cold_drift_mgr.evaluate_cold_start_risk(entity_id, etype, feat_vec)
            cold_modifiers.append(cold_mod)

            # Rule boosts
            rule_score = 0.0
            if row['geo_velocity_kmh'] > 900.0:  # Impossible travel speed
                rule_score += 45.0
            if row['ip_failed_auths_5m'] >= 5:  # Brute force / credential stuffing
                rule_score += 35.0
            if row['is_fp_mismatch'] == 1 and row['is_unseen_resource'] == 1: # Spoofing + Lateral
                rule_score += 30.0
            if row['cmd_risk_score'] > 0:  # Sensitive command execution
                rule_score += 25.0

            # Composite Score formula:
            # Risk = 45 * profiler_score + 35 * (classifier_threat != 'normal') * confidence + rule_score - 15 * cold_mod
            is_predicted_attack = 1.0 if row['predicted_threat'] != 'normal' else 0.0
            
            raw_risk = (
                45.0 * row['profiler_anomaly_score'] +
                30.0 * is_predicted_attack * row['classifier_confidence'] +
                rule_score -
                10.0 * cold_mod
            )

            # Normalize to 0-100
            final_risk = float(np.clip(raw_risk, 0.0, 100.0))
            risk_scores.append(round(final_risk, 1))

            # Severity Tier
            if final_risk >= 75.0:
                severity = "CRITICAL"
            elif final_risk >= 55.0:
                severity = "HIGH"
            elif final_risk >= 35.0:
                severity = "MEDIUM"
            else:
                severity = "LOW"
            severities.append(severity)

            # Update concept drift manager if non-anomalous
            is_anomaly_flag = final_risk >= 55.0 or (row['label'] != 'normal' if 'label' in row else False)
            self.cold_drift_mgr.update_entity_baseline(entity_id, etype, feat_vec, is_anomaly=is_anomaly_flag)

        df_eval['risk_score'] = risk_scores
        df_eval['severity'] = severities
        df_eval['cold_start_modifier'] = cold_modifiers

        return df_eval


if __name__ == "__main__":
    from src.generator import SyntheticDataGenerator
    from src.feature_engineering import FeatureExtractor

    gen = SyntheticDataGenerator(num_entities=20)
    raw_df = gen.generate_dataset(num_events=300, anomaly_rate=0.04)
    fe = FeatureExtractor()
    processed_df = fe.fit_transform(raw_df)

    profiler = UnsupervisedBehaviorProfiler()
    profiler.fit(processed_df)

    clf = ThreatCategoryClassifier()
    clf.fit(processed_df, processed_df['label'])

    engine = UnifiedRiskEngine(profiler, clf)
    results_df = engine.evaluate(processed_df)

    print("Risk scoring summary:")
    print(results_df[['entry_id', 'label', 'predicted_threat', 'risk_score', 'severity']].head(15))
