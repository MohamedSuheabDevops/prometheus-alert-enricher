"""Send a fake Alertmanager payload to the webhook (no real outage needed)."""
import requests

payload = {
    "alerts": [{
        "status": "firing",
        "labels": {"alertname": "HighMemoryUsage", "instance": "web-01:9100", "severity": "critical"},
        "annotations": {
            "summary": "Memory usage above 90% for 5 minutes",
            "description": "Instance web-01 has used 93% of its memory.",
        },
    }]
}
r = requests.post("http://localhost:8001/alert", json=payload, timeout=60)
print(r.status_code, r.json())
