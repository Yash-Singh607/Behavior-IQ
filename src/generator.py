"""
Synthetic Access Log Data Generator with Attack Taxonomy & Behavioral Profiles
For Honeywell AI Behavioral Anomaly Detection System
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Cities with geographical coordinates (Latitude, Longitude)
CITIES_GEO = {
    "New York, US": (40.7128, -74.0060),
    "San Francisco, US": (37.7749, -122.4194),
    "Chicago, US": (41.8781, -87.6298),
    "London, UK": (51.5074, -0.1278),
    "Frankfurt, DE": (50.1109, 8.6821),
    "Tokyo, JP": (35.6762, 139.6503),
    "Singapore, SG": (1.3521, 103.8198),
    "Sydney, AU": (-33.8688, 151.2093),
    "Bangalore, IN": (12.9716, 77.5946),
    "Sao Paulo, BR": (-23.5505, -46.6333)
}

RESOURCES_BY_TYPE = {
    "user": [
        "/dashboard/home", "/email/inbox", "/document/view", "/report/download",
        "/user/profile", "/api/v1/user/settings", "/tools/analytics"
    ],
    "service_account": [
        "/api/v1/auth/token", "/service/sync", "/db/backup/run",
        "/metrics/export", "/queue/consume", "/storage/blob/read"
    ],
    "edge_device": [
        "/sensor/telemetry/push", "/device/heartbeat", "/firmware/status",
        "/edge/config/fetch", "/plc/register/read"
    ]
}

SENSITIVE_RESOURCES = [
    "/admin/database/export", "/iam/keys/rotate", "/prod/secrets/vault",
    "/root/shadow/read", "/plc/override/control", "/network/firewall/disable"
]

DEVICE_FINGERPRINTS = {
    "user": [
        "OS:Windows11|Browser:Chrome120|MAC:AC:DE:48:11:22:33|Proto:HTTPS",
        "OS:MacOS14|Browser:Safari17|MAC:F0:18:98:44:55:66|Proto:HTTPS",
        "OS:Ubuntu22|Browser:Firefox121|MAC:00:1A:2B:3C:4D:5E|Proto:HTTPS"
    ],
    "service_account": [
        "OS:Linux-Kernel6.1|Client:Go-http-client/2.0|MAC:52:54:00:12:34:56|Proto:gRPC",
        "OS:Linux-Kernel5.15|Client:Python-requests/2.31|MAC:52:54:00:98:76:54|Proto:HTTP/2"
    ],
    "edge_device": [
        "OS:FreeRTOS-v10|Firmware:v3.4.1|MAC:00:80:E1:AA:BB:CC|Proto:MQTT",
        "OS:EmbeddedLinux|Firmware:v2.1.0|MAC:70:B3:D5:11:22:33|Proto:ModbusTCP"
    ]
}

AUTH_METHODS = ["password", "token", "certificate", "biometric"]


class SyntheticDataGenerator:
    def __init__(self, num_entities=50, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        self.num_entities = num_entities
        self.entities = self._generate_entity_profiles()

    def _generate_entity_profiles(self):
        profiles = {}
        # 60% users, 25% edge devices, 15% service accounts
        entity_types = (
            ["user"] * int(self.num_entities * 0.6) +
            ["edge_device"] * int(self.num_entities * 0.25) +
            ["service_account"] * (self.num_entities - int(self.num_entities * 0.6) - int(self.num_entities * 0.25))
        )

        cities = list(CITIES_GEO.keys())

        for idx, etype in enumerate(entity_types):
            prefix = "USR" if etype == "user" else ("DEV" if etype == "edge_device" else "SVC")
            entity_id = f"{prefix}_{idx+101:03d}"

            # Home geo
            home_city = random.choice(cities)
            home_geo = CITIES_GEO[home_city]

            # Primary IP pool
            base_ip = f"192.168.{random.randint(1, 250)}."
            ip_pool = [base_ip + str(random.randint(1, 254)) for _ in range(3)]

            # Default fingerprint
            fingerprint = random.choice(DEVICE_FINGERPRINTS[etype])

            # Preferred resources
            resources = RESOURCES_BY_TYPE[etype]

            profiles[entity_id] = {
                "entity_id": entity_id,
                "entity_type": etype,
                "home_city": home_city,
                "home_geo": home_geo,
                "ip_pool": ip_pool,
                "fingerprint": fingerprint,
                "resources": resources,
                "preferred_auth": "password" if etype == "user" else ("certificate" if etype == "edge_device" else "token")
            }

        return profiles

    def generate_dataset(self, num_events=10000, start_time=None, anomaly_rate=0.02, cold_start_rate=0.05):
        """
        Generates synthetic logs over time with injected anomalies.
        """
        if start_time is None:
            start_time = datetime(2026, 7, 1, 8, 0, 0)

        logs = []
        entity_ids = list(self.entities.keys())
        
        # Cold start entities (created without initial history)
        num_cold = int(len(entity_ids) * cold_start_rate)
        cold_start_entities = set(entity_ids[-num_cold:]) if num_cold > 0 else set()

        current_time = start_time
        events_generated = 0

        # Dedicated anomaly injectors setup
        anomaly_count = int(num_events * anomaly_rate)
        # Distribute anomaly counts across 7 attack types + insider drift
        attack_types = [
            "brute_force", "impossible_travel", "credential_stuffing",
            "lateral_movement", "device_spoofing", "low_and_slow", "insider_drift"
        ]
        
        # Inject anomalies at specific step indices adaptively
        start_idx = max(5, int(num_events * 0.05))
        end_idx = max(start_idx + 10, int(num_events * 0.95))
        sample_pop = list(range(start_idx, end_idx))
        actual_anomaly_count = min(anomaly_count, len(sample_pop))
        
        anomaly_indices = set(random.sample(sample_pop, actual_anomaly_count))
        anomaly_assignments = {idx: random.choice(attack_types) for idx in anomaly_indices}

        while events_generated < num_events:
            # Time progression (between 1 to 30 seconds per event step)
            current_time += timedelta(seconds=random.randint(1, 30))

            if events_generated in anomaly_assignments:
                attack_type = anomaly_assignments[events_generated]
                attack_logs, extra_steps = self._inject_attack(attack_type, current_time)
                logs.extend(attack_logs)
                events_generated += len(attack_logs)
                current_time += timedelta(seconds=extra_steps * 5)
            else:
                # Normal event generation
                entity_id = random.choice(entity_ids)
                
                # Check if cold start entity (suppress early events to keep it cold start)
                if entity_id in cold_start_entities and events_generated < num_events * 0.7:
                    # Pick another non-cold entity
                    entity_id = random.choice([e for e in entity_ids if e not in cold_start_entities])

                profile = self.entities[entity_id]
                log_entry = self._generate_normal_event(profile, current_time)
                logs.append(log_entry)
                events_generated += 1

        df = pd.DataFrame(logs)
        df.sort_values(by="timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def _generate_normal_event(self, profile, timestamp):
        # Work hour noise
        if profile["entity_type"] == "user":
            hour = timestamp.hour
            # Higher probability during 8:00 - 18:00
            if 8 <= hour <= 18:
                session_duration = random.randint(120, 3600)
            else:
                session_duration = random.randint(10, 300)
        else:
            session_duration = random.randint(5, 60)

        city = profile["home_city"]
        lat, lon = profile["home_geo"]
        # Add slight GPS jitter (< 2km)
        lat_jitter = lat + np.random.normal(0, 0.005)
        lon_jitter = lon + np.random.normal(0, 0.005)

        resource = random.choice(profile["resources"])
        cmd_seq = ["connect", f"access_{resource.split('/')[-1]}", "disconnect"]

        return {
            "entry_id": profile["entity_id"],
            "entity_type": profile["entity_type"],
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": random.choice(profile["ip_pool"]),
            "geo_location": f"{city}|{lat_jitter:.4f},{lon_jitter:.4f}",
            "resource_accessed": resource,
            "auth_method": profile["preferred_auth"],
            "session_duration": session_duration,
            "command_sequence": " -> ".join(cmd_seq),
            "device_fingerprint": profile["fingerprint"],
            "auth_status": "SUCCESS",
            "label": "normal"
        }

    def _inject_attack(self, attack_type, timestamp):
        logs = []
        entity_id = random.choice(list(self.entities.keys()))
        profile = self.entities[entity_id]
        steps = 1

        if attack_type == "brute_force":
            # Rapid failed login attempts from external IP
            attacker_ip = f"45.142.{random.randint(1, 250)}.{random.randint(1, 250)}"
            for i in range(random.randint(8, 15)):
                t = timestamp + timedelta(seconds=i * 2)
                logs.append({
                    "entry_id": entity_id,
                    "entity_type": profile["entity_type"],
                    "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                    "source_ip": attacker_ip,
                    "geo_location": "Moscow, RU|55.7558,37.6173",
                    "resource_accessed": "/api/v1/auth/login",
                    "auth_method": "password",
                    "session_duration": 1,
                    "command_sequence": "login_attempt -> auth_failed",
                    "device_fingerprint": "OS:Unknown|Client:Hydra-v9.2|MAC:00:00:00:00:00:00|Proto:HTTP",
                    "auth_status": "FAILED",
                    "label": "brute_force"
                })
            steps = len(logs)

        elif attack_type == "impossible_travel":
            # Login from Home City, then 10 mins later from Tokyo/Sydney
            t1 = timestamp
            t2 = timestamp + timedelta(minutes=random.randint(5, 15))
            
            far_city = "Tokyo, JP" if profile["home_city"] != "Tokyo, JP" else "London, UK"
            far_geo = CITIES_GEO[far_city]

            logs.append(self._generate_normal_event(profile, t1))
            logs.append({
                "entry_id": entity_id,
                "entity_type": profile["entity_type"],
                "timestamp": t2.strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": f"103.252.{random.randint(1,250)}.{random.randint(1,250)}",
                "geo_location": f"{far_city}|{far_geo[0]:.4f},{far_geo[1]:.4f}",
                "resource_accessed": profile["resources"][0],
                "auth_method": profile["preferred_auth"],
                "session_duration": 300,
                "command_sequence": "connect -> query -> disconnect",
                "device_fingerprint": profile["fingerprint"],
                "auth_status": "SUCCESS",
                "label": "impossible_travel"
            })
            steps = 2

        elif attack_type == "credential_stuffing":
            # Single attacker IP trying multiple user IDs
            attacker_ip = f"185.220.{random.randint(1, 250)}.{random.randint(1, 250)}"
            target_ids = random.sample(list(self.entities.keys()), min(6, len(self.entities)))
            for i, tid in enumerate(target_ids):
                t = timestamp + timedelta(seconds=i * 3)
                p = self.entities[tid]
                logs.append({
                    "entry_id": tid,
                    "entity_type": p["entity_type"],
                    "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                    "source_ip": attacker_ip,
                    "geo_location": "Bucharest, RO|44.4323,26.1063",
                    "resource_accessed": "/api/v1/auth/login",
                    "auth_method": "password",
                    "session_duration": 2,
                    "command_sequence": "credential_stuff -> auth_failed",
                    "device_fingerprint": "OS:Linux|Client:Python-urllib|MAC:00:11:22:33:44:55|Proto:HTTPS",
                    "auth_status": "FAILED",
                    "label": "credential_stuffing"
                })
            steps = len(logs)

        elif attack_type == "lateral_movement":
            # Entity accessing restricted / sensitive resources never touched before
            t = timestamp
            sensitive_res = random.choice(SENSITIVE_RESOURCES)
            logs.append({
                "entry_id": entity_id,
                "entity_type": profile["entity_type"],
                "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": profile["ip_pool"][0],
                "geo_location": f"{profile['home_city']}|{profile['home_geo'][0]:.4f},{profile['home_geo'][1]:.4f}",
                "resource_accessed": sensitive_res,
                "auth_method": profile["preferred_auth"],
                "session_duration": 1800,
                "command_sequence": "escalate_privilege -> dumping_hashes -> exfiltrate",
                "device_fingerprint": profile["fingerprint"],
                "auth_status": "SUCCESS",
                "label": "lateral_movement"
            })
            steps = 1

        elif attack_type == "device_spoofing":
            # Matching entity ID but completely altered OS/MAC fingerprint
            t = timestamp
            spoofed_fp = "OS:Android14|Browser:MobileSafari|MAC:DE:AD:BE:EF:00:01|Proto:HTTP/1.1"
            logs.append({
                "entry_id": entity_id,
                "entity_type": profile["entity_type"],
                "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": f"198.51.100.{random.randint(1, 254)}",
                "geo_location": f"{profile['home_city']}|{profile['home_geo'][0]:.4f},{profile['home_geo'][1]:.4f}",
                "resource_accessed": profile["resources"][0],
                "auth_method": "token",
                "session_duration": 450,
                "command_sequence": "connect -> replay_token -> query",
                "device_fingerprint": spoofed_fp,
                "auth_status": "SUCCESS",
                "label": "device_spoofing"
            })
            steps = 1

        elif attack_type == "low_and_slow":
            # Off-hours small volume access over time
            for day in range(3):
                t = timestamp + timedelta(days=day, hours=random.randint(1, 4))  # 1 AM to 4 AM
                logs.append({
                    "entry_id": entity_id,
                    "entity_type": profile["entity_type"],
                    "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                    "source_ip": profile["ip_pool"][0],
                    "geo_location": f"{profile['home_city']}|{profile['home_geo'][0]:.4f},{profile['home_geo'][1]:.4f}",
                    "resource_accessed": random.choice(SENSITIVE_RESOURCES),
                    "auth_method": profile["preferred_auth"],
                    "session_duration": 40,
                    "command_sequence": "stealth_probe -> read_chunk -> exit",
                    "device_fingerprint": profile["fingerprint"],
                    "auth_status": "SUCCESS",
                    "label": "low_and_slow"
                })
            steps = 3

        elif attack_type == "insider_drift":
            # Ambiguous edge case: Legitimate expansion of job duties
            t = timestamp
            new_res = "/report/quarterly_audit"
            logs.append({
                "entry_id": entity_id,
                "entity_type": profile["entity_type"],
                "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": profile["ip_pool"][0],
                "geo_location": f"{profile['home_city']}|{profile['home_geo'][0]:.4f},{profile['home_geo'][1]:.4f}",
                "resource_accessed": new_res,
                "auth_method": profile["preferred_auth"],
                "session_duration": 600,
                "command_sequence": "connect -> view_audit -> disconnect",
                "device_fingerprint": profile["fingerprint"],
                "auth_status": "SUCCESS",
                "label": "insider_drift"
            })
            steps = 1

        return logs, steps


if __name__ == "__main__":
    generator = SyntheticDataGenerator(num_entities=50, seed=42)
    df = generator.generate_dataset(num_events=1000, anomaly_rate=0.03)
    print(f"Generated dataset shape: {df.shape}")
    print("Label distribution:\n", df['label'].value_counts())
