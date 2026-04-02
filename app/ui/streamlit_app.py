from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.analysis.diagnostics import diagnose
from app.simulation.scenario_factory import SCENARIOS, ScenarioConfig, ScenarioFactory

st.set_page_config(page_title="False-Green Dashboard Simulator", layout="wide")
st.title("False-Green Dashboard Simulator")
st.caption("Deterministic simulation of green-looking dashboards hiding failure drift.")
st.link_button("Home", "https://ops-demo-launchpad-9fd4e1ed9e00.herokuapp.com/")

scenario = st.selectbox("Scenario", sorted(SCENARIOS))
intensity = st.slider("Intensity", 0.2, 1.0, 0.7, 0.05)
points = st.slider("Time Window (points)", 12, 60, 24, 1)
seed = st.number_input("Seed", min_value=1, max_value=9999, value=42)

if st.button("Reset Scenario"):
    st.experimental_rerun()

cfg = ScenarioConfig(scenario=scenario, intensity=float(intensity), points=int(points), seed=int(seed))
bundle = ScenarioFactory().generate(cfg)
diag = diagnose(cfg, bundle)

left, right = st.columns(2)

with left:
    st.subheader("What Leadership Sees")
    exec_df = pd.DataFrame({"t": bundle.time_index, **bundle.executive_metrics})
    for metric in [m for m in exec_df.columns if m != "t"]:
        fig = px.line(exec_df, x="t", y=metric, title=metric)
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("What Operators Should See")
    truth_df = pd.DataFrame({"t": bundle.time_index, **bundle.truth_metrics})
    for metric in [m for m in truth_df.columns if m != "t"]:
        fig = px.line(truth_df, x="t", y=metric, title=metric)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Why This Is Dangerous")
st.write(diag["false_green_explanation"])

st.subheader("Signals I Would Add")
for signal in diag["recommended_signals"]:
    st.write(f"- {signal}")
