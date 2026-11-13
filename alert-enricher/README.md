# Alert Enricher

Turns raw Prometheus alerts into plain-English explanations with likely causes and runbook steps, using Azure OpenAI (gpt-4o-mini).

## How it works

```mermaid
flowchart LR
    P[Prometheus] -->|fires alert| A[Alertmanager]
    A -->|webhook| W[FastAPI enricher]
    W -->|prompt| L[Azure OpenAI]
    L -->|JSON| W
    W --> U[Streamlit UI]
    W -->|/metrics| P
    P --> G[Grafana dashboard]
```

1. Prometheus evaluates alert rules and sends firing alerts to Alertmanager.
2. Alertmanager posts them to the enricher webhook.
3. The enricher asks the model for a summary, likely causes, runbook steps and urgency.
4. Results are saved and shown in a Streamlit page. Pipeline health (alerts processed, latency, failures) is shown in Grafana.

## Features

- Alertmanager webhook receiver built with FastAPI
- AI-generated summary, likely causes, runbook steps and urgency
- Alert text treated as untrusted input (length limits, prompt tells the model to ignore instructions inside alerts)
- Safe suggestions only (checks, not destructive actions)
- Own Prometheus metrics and a provisioned Grafana dashboard
- Failures are recorded, not lost

## Quick start

Requirements: Python 3.11+, Docker, an Azure OpenAI endpoint and key.

```bash
cp .env.example .env          # then add your endpoint and key
pip install -r requirements.txt

# terminal 1
uvicorn webhook:app --host 0.0.0.0 --port 8001
# terminal 2
docker compose up -d
# terminal 3
streamlit run ui.py
```

Send a fake alert without any outage:

```bash
python test_alert.py
```

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |
| Grafana | http://localhost:3000 (admin / admin, change it) |

## Tests (manual)

| Case | Expected |
|---|---|
| Run `test_alert.py` | Enriched alert appears in the UI |
| `DemoAlwaysFiring` rule | Alert flows through Alertmanager automatically |
| Stop node-exporter | `TargetDown` fires and is enriched |
| Wrong API key | Alert saved with "failed" status, no crash |

## Security notes

- Secrets live in `.env`, which is git-ignored.
- `--host 0.0.0.0` is for local or lab use only. Do not expose the webhook publicly without authentication.
- AI output can be wrong. Verify before acting on it.

## Screenshots
### Enriched alert in the UI
![Alert card]<img width="1285" height="594" alt="ui-alert-card" src="https://github.com/user-attachments/assets/899cb833-9a9f-4350-a98e-9757fd072ec5" />

### Another example: a down target
![TargetDown alert]<img width="784" height="457" alt="ui-target-down" src="https://github.com/user-attachments/assets/9466f991-d2e9-434d-83b7-6c47e9efa527" />

### Grafana dashboard
![Grafana dashboard]<img width="1350" height="579" alt="grafana-dashboard" src="https://github.com/user-attachments/assets/61b92335-b09c-4588-9a64-9d8cb642da01" />

### Prometheus alert rules
![Prometheus alerts]<img width="1319" height="573" alt="prometheus-alerts" src="https://github.com/user-attachments/assets/ab5464a9-c25e-4067-8627-35fd584e200f" />

### Prometheus targets
![Prometheus targets]<img width="1354" height="519" alt="prometheus-targets" src="https://github.com/user-attachments/assets/5a050153-3223-42ee-a764-369f883ffc88" />







## Tech stack

Python, FastAPI, Streamlit, Prometheus, Alertmanager, Grafana, Docker Compose, Azure OpenAI.
