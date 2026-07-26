"""
Explainable AI (XAI) Engine & Feature Attribution Generator
For Honeywell AI Behavioral Anomaly Detection System
"""

import numpy as np
import pandas as pd
from src.feature_engineering import FEATURE_COLUMNS


FEATURE_HUMAN_NAMES = {
    'geo_velocity_kmh': 'Geo Velocity (km/h)',
    'dist_km': 'Travel Distance (km)',
    'time_delta_sec': 'Time Elapsed (sec)',
    'ip_failed_auths_5m': 'Failed Auths from IP (5m)',
    'ip_unique_entities_5m': 'Targeted Entities from IP (5m)',
    'is_fp_mismatch': 'Device Fingerprint Mismatch',
    'is_unseen_resource': 'Accessing Unseen Resource',
    'resource_seen_count': 'Historical Resource Frequency',
    'is_sensitive_res': 'Accessing Sensitive Endpoint',
    'cmd_risk_score': 'Suspicious Command Sequence Risk',
    'hour_of_day': 'Hour of Day',
    'is_off_hours': 'Off-Hours Access Attempt',
    'session_duration': 'Session Duration (sec)',
    'auth_failed': 'Authentication Status'
}


class AlertExplainer:
    """
    Generates human-readable feature attribution explanations and SHAP-style breakdown
    for security analysts.
    """
    def __init__(self, feature_means: dict = None):
        # Historical normal feature baselines for contrastive explanation
        self.baselines = feature_means or {
            'geo_velocity_kmh': 25.0,
            'dist_km': 10.0,
            'ip_failed_auths_5m': 0.0,
            'ip_unique_entities_5m': 1.0,
            'is_fp_mismatch': 0.0,
            'is_unseen_resource': 0.0,
            'is_sensitive_res': 0.0,
            'cmd_risk_score': 0.0,
            'is_off_hours': 0.0,
            'auth_failed': 0.0
        }

    def explain_alert(self, row: pd.Series or dict) -> dict:
        """
        Calculates feature attributions and generates natural language summary.
        """
        row_dict = row.to_dict() if isinstance(row, pd.Series) else row
        
        attributions = {}
        factors = []

        # 1. Geo Velocity Attribution
        velocity = float(row_dict.get('geo_velocity_kmh', 0.0))
        dist = float(row_dict.get('dist_km', 0.0))
        if velocity > 300.0:
            attributions['geo_velocity_kmh'] = round(velocity / 10.0, 2)
            factors.append(f"Impossible Travel: Speed of {velocity:,.1f} km/h over {dist:,.1f} km exceeds plausible transport limits.")

        # 2. Failed Auth & Credential Stuffing
        failed_5m = float(row_dict.get('ip_failed_auths_5m', 0.0))
        unique_ents = float(row_dict.get('ip_unique_entities_5m', 1.0))
        if failed_5m >= 3:
            attributions['ip_failed_auths_5m'] = round(failed_5m * 12.0, 2)
            factors.append(f"High Authentication Failures: {int(failed_5m)} failed login attempts detected in 5 minutes from source IP.")
        if unique_ents >= 3:
            attributions['ip_unique_entities_5m'] = round(unique_ents * 15.0, 2)
            factors.append(f"Credential Stuffing Signal: Single IP attempting access across {int(unique_ents)} distinct account IDs.")

        # 3. Fingerprint Mismatch
        fp_mismatch = int(row_dict.get('is_fp_mismatch', 0))
        if fp_mismatch == 1:
            attributions['is_fp_mismatch'] = 25.0
            factors.append("Device Spoofing: Session fingerprint (OS/MAC/Protocol) differs from entity's historical device profile.")

        # 4. Resource & Command Risk
        unseen_res = int(row_dict.get('is_unseen_resource', 0))
        sensitive_res = int(row_dict.get('is_sensitive_res', 0))
        cmd_risk = float(row_dict.get('cmd_risk_score', 0.0))
        
        if sensitive_res == 1 or unseen_res == 1:
            attributions['is_unseen_resource'] = 20.0 if unseen_res else 10.0
            attributions['is_sensitive_res'] = 30.0 if sensitive_res else 0.0
            res_name = str(row_dict.get('resource_accessed', 'Endpoint'))
            factors.append(f"Lateral Movement / Policy Violation: Accessed privileged endpoint '{res_name}' for the first time.")

        if cmd_risk > 0:
            attributions['cmd_risk_score'] = round(cmd_risk * 20.0, 2)
            factors.append(f"Suspicious Command Execution: Command sequence contained elevated risk tokens (risk score: {cmd_risk}).")

        # 5. Off Hours
        is_off = int(row_dict.get('is_off_hours', 0))
        if is_off == 1:
            attributions['is_off_hours'] = 10.0
            factors.append("Off-Hours Activity: Access attempt initiated outside standard operating schedule (7:00 - 19:00).")

        # Fallback if no specific factors triggered
        if not factors:
            factors.append("Statistical Anomaly: Multi-dimensional feature vector deviated from entity baseline.")
            attributions['session_duration'] = 15.0

        # Construct Natural Language Analyst Summary
        pred_threat = row_dict.get('predicted_threat', 'anomalous activity')
        severity = row_dict.get('severity', 'HIGH')
        entity_id = row_dict.get('entry_id', 'Entity')

        analyst_summary = (
            f"Alert [{severity}] for {entity_id}: System flagged suspicious {pred_threat.replace('_', ' ')}. "
            f"Primary indicators: {factors[0]}"
        )

        return {
            "contributing_factors": factors,
            "analyst_summary": analyst_summary,
            "feature_attributions": attributions
        }


if __name__ == "__main__":
    explainer = AlertExplainer()
    sample_row = {
        'entry_id': 'USR_102',
        'predicted_threat': 'impossible_travel',
        'severity': 'CRITICAL',
        'geo_velocity_kmh': 1250.4,
        'dist_km': 6200.0,
        'ip_failed_auths_5m': 0,
        'is_fp_mismatch': 1,
        'resource_accessed': '/admin/vault'
    }
    explanation = explainer.explain_alert(sample_row)
    print("Analyst Summary:", explanation["analyst_summary"])
    print("Contributing Factors:", explanation["contributing_factors"])
