"""
Cold Start Entity & Concept Drift Adaptation Engine
For Honeywell AI Behavioral Anomaly Detection System
"""

import numpy as np
import pandas as pd


class ColdStartAndDriftManager:
    """
    Handles:
    1. Cold-start entity initialization using hierarchical entity-type priors.
    2. Exponential Moving Average (EMA) baseline updates for legitimate concept drift.
    """
    def __init__(self, min_events_for_full_baseline=20, alpha_drift=0.05):
        self.min_events = min_events_for_full_baseline
        self.alpha_drift = alpha_drift  # EMA update weight
        
        # Entity-type global prior means & stds
        self.type_priors = {
            "user": {
                "mean_duration": 1800.0,
                "off_hours_prob": 0.1,
                "geo_velocity_max": 200.0,
                "auth_failed_rate": 0.02
            },
            "service_account": {
                "mean_duration": 30.0,
                "off_hours_prob": 0.5,
                "geo_velocity_max": 500.0,
                "auth_failed_rate": 0.001
            },
            "edge_device": {
                "mean_duration": 10.0,
                "off_hours_prob": 0.5,
                "geo_velocity_max": 50.0,
                "auth_failed_rate": 0.005
            }
        }
        
        # Per-entity state
        self.entity_stats = {}

    def get_entity_weight(self, event_count: int) -> float:
        """
        Calculates interpolation weight between individual entity history and global type prior.
        Returns weight alpha in [0.0, 1.0].
        """
        return min(1.0, float(event_count) / float(self.min_events))

    def evaluate_cold_start_risk(self, entity_id: str, etype: str, feature_vector: dict) -> float:
        """
        Evaluates risk contribution for cold start entities using type priors.
        Returns a cold-start risk modifier [0.0, 1.0].
        """
        state = self.entity_stats.get(entity_id, {'count': 0, 'feature_means': {}})
        count = state['count']
        weight = self.get_entity_weight(count)

        prior = self.type_priors.get(etype, self.type_priors['user'])

        # Compare session duration against blended mean
        current_dur = feature_vector.get('session_duration', 300.0)
        expected_dur = weight * state['feature_means'].get('session_duration', prior['mean_duration']) + (1 - weight) * prior['mean_duration']

        # If cold-start entity, compute deviation against blended prior
        duration_ratio = abs(current_dur - expected_dur) / (expected_dur + 1.0)
        risk_modifier = min(1.0, duration_ratio / 10.0) * (1.0 - weight)

        return float(risk_modifier)

    def update_entity_baseline(self, entity_id: str, etype: str, feature_vector: dict, is_anomaly: bool):
        """
        Updates running baseline stats via EMA if the event is non-anomalous (concept drift adaptation).
        """
        if is_anomaly:
            # Do NOT update baseline with malicious events
            return

        if entity_id not in self.entity_stats:
            self.entity_stats[entity_id] = {
                'count': 1,
                'etype': etype,
                'feature_means': {k: float(v) for k, v in feature_vector.items() if isinstance(v, (int, float, np.number))}
            }
        else:
            state = self.entity_stats[entity_id]
            state['count'] += 1
            means = state['feature_means']
            
            for k, v in feature_vector.items():
                if isinstance(v, (int, float, np.number)):
                    val = float(v)
                    if k in means:
                        # EMA update formula: mu_t = (1 - alpha)*mu_{t-1} + alpha * x_t
                        means[k] = (1.0 - self.alpha_drift) * means[k] + self.alpha_drift * val
                    else:
                        means[k] = val

    def get_summary(self) -> dict:
        return {
            "tracked_entities": len(self.entity_stats),
            "cold_entities_count": sum(1 for s in self.entity_stats.values() if s['count'] < self.min_events),
            "mature_entities_count": sum(1 for s in self.entity_stats.values() if s['count'] >= self.min_events)
        }


if __name__ == "__main__":
    mgr = ColdStartAndDriftManager()
    feat = {'session_duration': 5000.0, 'geo_velocity_kmh': 15.0}
    r = mgr.evaluate_cold_start_risk("USR_999", "user", feat)
    print("Cold start risk modifier:", r)
    mgr.update_entity_baseline("USR_999", "user", feat, is_anomaly=False)
    print("Manager summary:", mgr.get_summary())
