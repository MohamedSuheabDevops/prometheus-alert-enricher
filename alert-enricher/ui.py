import json
import os

import streamlit as st

OUT_FILE = "enriched_alerts.jsonl"
ICON = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}

st.title("Alert Enricher")
st.caption("Alerts from Prometheus/Alertmanager, explained by AI. Always verify before acting.")
st.button("Refresh")

records = []
if os.path.exists(OUT_FILE):
    with open(OUT_FILE, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

if not records:
    st.info("No alerts yet. Start the webhook, then wait for an alert or run test_alert.py.")

for r in reversed(records[-20:]):
    icon = ICON.get(r["urgency"], "⚪")
    with st.expander(f"{icon} {r['alertname']}  |  {r['urgency']}  |  {r['time']}"):
        st.write(r["summary"])
        if r["likely_causes"]:
            st.markdown("**Likely causes**")
            for c in r["likely_causes"]:
                st.markdown(f"- {c}")
        if r["runbook_steps"]:
            st.markdown("**Runbook steps**")
            for i, step in enumerate(r["runbook_steps"], 1):
                st.markdown(f"{i}. {step}")
        st.caption(f"Labels: {r['labels']}")
