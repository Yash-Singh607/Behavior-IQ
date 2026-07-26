"""
Multi-Class Attack Classifier (LightGBM & Sklearn Multi-Class Classifier)
For Honeywell AI Behavioral Anomaly Detection System
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

try:
    import lightgbm as lgb
    LGBM_AVAILABLE = True
except ImportError:
    LGBM_AVAILABLE = False

from src.feature_engineering import FEATURE_COLUMNS


ATTACK_LABELS = [
    "normal",
    "brute_force",
    "impossible_travel",
    "credential_stuffing",
    "lateral_movement",
    "device_spoofing",
    "low_and_slow",
    "insider_drift"
]


class ThreatCategoryClassifier:
    """
    Classifies anomalous feature vectors into specific Honeywell attack taxonomy categories.
    """
    def __init__(self, use_lightgbm=True):
        self.use_lgbm = use_lightgbm and LGBM_AVAILABLE
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(ATTACK_LABELS)
        
        if self.use_lgbm:
            self.model = lgb.LGBMClassifier(
                n_estimators=100,
                learning_rate=0.05,
                num_leaves=31,
                random_state=42,
                class_weight='balanced',
                verbose=-1
            )
        else:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                class_weight='balanced',
                random_state=42,
                n_jobs=-1
            )
        self.is_fitted = False

    def fit(self, X_df: pd.DataFrame, y_labels: pd.Series):
        X_feats = X_df[FEATURE_COLUMNS].fillna(0).values
        # Ensure all unique labels are encoded
        y_encoded = self.label_encoder.transform(y_labels)
        self.model.fit(X_feats, y_encoded)
        self.is_fitted = True

    def predict_threat_type(self, X_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        """
        Predicts threat category strings and class probability distributions.
        Returns (predicted_labels, max_probabilities).
        """
        if not self.is_fitted:
            raise ValueError("Classifier model is not fitted yet.")

        X_feats = X_df[FEATURE_COLUMNS].fillna(0).values
        probs = self.model.predict_proba(X_feats)
        pred_indices = np.argmax(probs, axis=1)
        max_probs = np.max(probs, axis=1)

        pred_labels = self.label_encoder.inverse_transform(pred_indices)
        return pred_labels, max_probs

    def save(self, filepath: str):
        joblib.dump({"encoder": self.label_encoder, "model": self.model, "use_lgbm": self.use_lgbm}, filepath)

    def load(self, filepath: str):
        data = joblib.load(filepath)
        self.label_encoder = data["encoder"]
        self.model = data["model"]
        self.use_lgbm = data["use_lgbm"]
        self.is_fitted = True


if __name__ == "__main__":
    from src.generator import SyntheticDataGenerator
    from src.feature_engineering import FeatureExtractor

    gen = SyntheticDataGenerator(num_entities=30)
    df = gen.generate_dataset(num_events=600, anomaly_rate=0.05)
    fe = FeatureExtractor()
    processed_df = fe.fit_transform(df)

    clf = ThreatCategoryClassifier()
    clf.fit(processed_df, processed_df['label'])
    preds, confs = clf.predict_threat_type(processed_df)
    print("Sample predictions:", preds[:10])
    print("Sample confidences:", confs[:10])
