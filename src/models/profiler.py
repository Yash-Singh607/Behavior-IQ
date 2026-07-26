"""
Unsupervised Behavioral Anomaly Profiler (Isolation Forest & Statistical Scaling)
For Honeywell AI Behavioral Anomaly Detection System
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

from src.feature_engineering import FEATURE_COLUMNS


class UnsupervisedBehaviorProfiler:
    """
    Fits per-entity or global baseline of 'normal' access behavior.
    Calculates zero-day / novel anomaly score in range [0.0, 1.0].
    """
    def __init__(self, contamination=0.03, random_state=42):
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=150,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X_df: pd.DataFrame):
        X_feats = X_df[FEATURE_COLUMNS].fillna(0).values
        X_scaled = self.scaler.fit_transform(X_feats)
        self.model.fit(X_scaled)
        self.is_fitted = True

    def predict_anomaly_score(self, X_df: pd.DataFrame) -> np.ndarray:
        """
        Returns anomaly scores normalized between 0.0 (normal) and 1.0 (highly anomalous).
        """
        if not self.is_fitted:
            raise ValueError("Profiler model is not fitted yet.")

        X_feats = X_df[FEATURE_COLUMNS].fillna(0).values
        X_scaled = self.scaler.transform(X_feats)
        
        # decision_function returns negative values for anomalies, positive for normal
        raw_scores = self.model.decision_function(X_scaled)
        
        # Convert decision function to [0, 1] anomaly score where 1 is highest anomaly
        min_score = raw_scores.min()
        max_score = raw_scores.max()
        
        if max_score == min_score:
            anomaly_scores = np.zeros(len(raw_scores))
        else:
            # Reverse normalization: lower raw decision -> higher anomaly score
            anomaly_scores = 1.0 - (raw_scores - min_score) / (max_score - min_score + 1e-6)

        return np.clip(anomaly_scores, 0.0, 1.0)

    def save(self, filepath: str):
        joblib.dump({"scaler": self.scaler, "model": self.model}, filepath)

    def load(self, filepath: str):
        data = joblib.load(filepath)
        self.scaler = data["scaler"]
        self.model = data["model"]
        self.is_fitted = True


if __name__ == "__main__":
    from src.generator import SyntheticDataGenerator
    from src.feature_engineering import FeatureExtractor

    gen = SyntheticDataGenerator(num_entities=20)
    df = gen.generate_dataset(num_events=500)
    fe = FeatureExtractor()
    processed_df = fe.fit_transform(df)

    profiler = UnsupervisedBehaviorProfiler()
    profiler.fit(processed_df)
    scores = profiler.predict_anomaly_score(processed_df)
    print("Anomaly scores (first 10):", scores[:10])
