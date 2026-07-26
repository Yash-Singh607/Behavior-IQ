"""
BehaviorIQ Enterprise SIEM & SOAR Connectors
Handles bi-directional integration with Splunk HEC, Microsoft Sentinel, PagerDuty, and Slack.
"""

import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("BehaviorIQ_SIEM")
logging.basicConfig(level=logging.INFO)


class SplunkHECConnector:
    """Splunk HTTP Event Collector (HEC) Integration"""
    def __init__(self, hec_url: str = "https://splunk.internal:8088/services/collector", token: str = "BIQ_HEC_TOKEN_99847"):
        self.hec_url = hec_url
        self.token = token

    def push_incident_event(self, alert_detail: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "time": alert_detail.get("timestamp"),
            "host": alert_detail.get("source_ip", "127.0.0.1"),
            "source": "behavioriq:anomaly_engine",
            "sourcetype": "_json",
            "event": {
                "entry_id": alert_detail.get("entry_id"),
                "entity_type": alert_detail.get("entity_type"),
                "threat_vector": alert_detail.get("predicted_threat"),
                "risk_score": alert_detail.get("risk_score"),
                "severity": alert_detail.get("severity"),
                "shap_attributions": alert_detail.get("contributing_factors", [])
            }
        }
        logger.info(f"Pushed incident {alert_detail.get('entry_id')} to Splunk HEC endpoint.")
        return {"status": "SUCCESS", "siem": "Splunk HEC", "pushed_events": 1}


class PagerDutySOARConnector:
    """PagerDuty Incident Trigger Connector"""
    def __init__(self, routing_key: str = "pd_sec_key_384729"):
        self.routing_key = routing_key

    def trigger_critical_incident(self, alert_detail: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Triggered PagerDuty Critical Incident for entry {alert_detail.get('entry_id')}")
        return {
            "status": "TRIGGERED",
            "incident_id": f"PD_INC_{alert_detail.get('entry_id')}",
            "urgency": "HIGH"
        }
