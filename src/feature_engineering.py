"""
Feature Extraction and Engineering Engine
For Honeywell AI Behavioral Anomaly Detection System
"""

import math
import numpy as np
import pandas as pd

try:
    from haversine import haversine, Unit
    HAVERSINE_AVAILABLE = True
except ImportError:
    HAVERSINE_AVAILABLE = False


SENSITIVE_KEYWORDS = [
    "admin", "shadow", "vault", "secret", "override", "privilege",
    "exfiltrate", "dumping", "firewall", "root", "keys"
]


def calculate_haversine(lat1, lon1, lat2, lon2):
    """
    Computes distance in kilometers between two (lat, lon) points.
    """
    if HAVERSINE_AVAILABLE:
        try:
            return haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)
        except Exception:
            pass
    
    # Fallback formula
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class FeatureExtractor:
    def __init__(self):
        self.entity_history = {}
        self.ip_history = {}
        self.resource_freq_by_entity = {}
        self.primary_fingerprints = {}

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts engineered feature matrix from raw log dataframe.
        """
        df = df.copy()
        df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by=['timestamp_dt'], inplace=True)

        features_list = []

        for idx, row in df.iterrows():
            feat = self._extract_row_features(row)
            features_list.append(feat)

        feat_df = pd.DataFrame(features_list)
        return pd.concat([df.reset_index(drop=True), feat_df.reset_index(drop=True)], axis=1)

    def _extract_row_features(self, row) -> dict:
        entity_id = row['entry_id']
        etype = row['entity_type']
        ts = row['timestamp_dt']
        ip = row['source_ip']
        fp = row['device_fingerprint']
        resource = row['resource_accessed']
        cmd_seq = row['command_sequence']
        auth_status = row['auth_status']

        # 1. Parse Lat / Lon
        city, coords = row['geo_location'].split('|') if '|' in row['geo_location'] else ("Unknown", row['geo_location'])
        lat, lon = map(float, coords.split(','))

        # 2. Entity History Lookup & Velocity
        entity_hist = self.entity_history.get(entity_id, [])
        if len(entity_hist) > 0:
            last_event = entity_hist[-1]
            time_delta_sec = (ts - last_event['ts']).total_seconds()
            time_delta_sec = max(time_delta_sec, 0.1)  # avoid div by zero
            dist_km = calculate_haversine(last_event['lat'], last_event['lon'], lat, lon)
            geo_velocity_kmh = dist_km / (time_delta_sec / 3600.0)
        else:
            time_delta_sec = 86400.0  # 1 day default for first event
            dist_km = 0.0
            geo_velocity_kmh = 0.0

        # Update entity history
        self.entity_history.setdefault(entity_id, []).append({
            'ts': ts, 'lat': lat, 'lon': lon, 'ip': ip, 'fp': fp, 'resource': resource
        })

        # 3. IP Rolling Window Statistics (Credential Stuffing & Brute Force Signals)
        ip_hist = self.ip_history.get(ip, [])
        # Prune older than 5 minutes (300s)
        ip_hist = [ev for ev in ip_hist if (ts - ev['ts']).total_seconds() <= 300]
        ip_failed_auths_5m = sum(1 for ev in ip_hist if ev['status'] == 'FAILED')
        ip_unique_entities_5m = len(set(ev['entity_id'] for ev in ip_hist))
        
        self.ip_history[ip] = ip_hist + [{'ts': ts, 'entity_id': entity_id, 'status': auth_status}]

        # 4. Fingerprint Mismatch Detection
        if entity_id not in self.primary_fingerprints:
            self.primary_fingerprints[entity_id] = fp
            is_fp_mismatch = 0
        else:
            is_fp_mismatch = 1 if fp != self.primary_fingerprints[entity_id] else 0

        # 5. Resource Access Novelty & Frequency
        res_freq_map = self.resource_freq_by_entity.setdefault(entity_id, {})
        resource_seen_count = res_freq_map.get(resource, 0)
        is_unseen_resource = 1 if resource_seen_count == 0 else 0
        res_freq_map[resource] = resource_seen_count + 1

        # Check if sensitive resource
        is_sensitive_res = 1 if any(kw in resource.lower() for kw in SENSITIVE_KEYWORDS) else 0

        # 6. Command Sequence Risk Score
        cmd_risk = 0.0
        for kw in SENSITIVE_KEYWORDS:
            if kw in cmd_seq.lower():
                cmd_risk += 1.0

        # 7. Temporal & Circadian Features
        hour = ts.hour
        sin_hour = math.sin(2 * math.pi * hour / 24.0)
        cos_hour = math.cos(2 * math.pi * hour / 24.0)
        is_weekend = 1 if ts.weekday() >= 5 else 0
        is_off_hours = 1 if (hour < 7 or hour > 19) else 0

        # 8. Numeric Encodings
        etype_code = {"user": 0, "service_account": 1, "edge_device": 2}.get(etype, 0)
        auth_code = {"password": 0, "token": 1, "certificate": 2, "biometric": 3}.get(row['auth_method'], 0)
        auth_failed = 1 if auth_status == "FAILED" else 0

        return {
            'lat': lat,
            'lon': lon,
            'time_delta_sec': time_delta_sec,
            'dist_km': dist_km,
            'geo_velocity_kmh': geo_velocity_kmh,
            'ip_failed_auths_5m': ip_failed_auths_5m,
            'ip_unique_entities_5m': ip_unique_entities_5m,
            'is_fp_mismatch': is_fp_mismatch,
            'is_unseen_resource': is_unseen_resource,
            'resource_seen_count': resource_seen_count,
            'is_sensitive_res': is_sensitive_res,
            'cmd_risk_score': cmd_risk,
            'hour_of_day': hour,
            'sin_hour': sin_hour,
            'cos_hour': cos_hour,
            'is_weekend': is_weekend,
            'is_off_hours': is_off_hours,
            'session_duration': float(row['session_duration']),
            'etype_code': etype_code,
            'auth_code': auth_code,
            'auth_failed': auth_failed
        }


# Feature columns list for ML models
FEATURE_COLUMNS = [
    'time_delta_sec', 'dist_km', 'geo_velocity_kmh',
    'ip_failed_auths_5m', 'ip_unique_entities_5m', 'is_fp_mismatch',
    'is_unseen_resource', 'resource_seen_count', 'is_sensitive_res',
    'cmd_risk_score', 'hour_of_day', 'sin_hour', 'cos_hour',
    'is_weekend', 'is_off_hours', 'session_duration',
    'etype_code', 'auth_code', 'auth_failed'
]


if __name__ == "__main__":
    from src.generator import SyntheticDataGenerator
    gen = SyntheticDataGenerator(num_entities=10)
    raw_df = gen.generate_dataset(num_events=100)
    fe = FeatureExtractor()
    processed_df = fe.fit_transform(raw_df)
    print("Processed DataFrame columns:", processed_df.columns.tolist())
    print("Sample features:\n", processed_df[FEATURE_COLUMNS].head())
