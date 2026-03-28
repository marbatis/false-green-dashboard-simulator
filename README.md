# false-green-dashboard-simulator

Interactive simulator showing how top-line metrics can stay green while hidden indicators drift toward failure.

## Why it matters
Teams often over-index on averages and success rate. This project demonstrates failure modes where leadership dashboards look healthy while operators should already be escalating.

## MVP features
- Three deterministic scenarios:
  - `cert_rotation_hidden_failure`
  - `retry_storm_masked_by_averages`
  - `downstream_queue_saturation`
- Controls: intensity, seed, time window
- Two-panel view:
  - what leadership sees
  - what operators should see
- Deterministic diagnostics:
  - why this is dangerous
  - signals to add
- Reproducible outputs from seed values

## Architecture
Scenario generator -> metrics bundle -> diagnostics engine -> Streamlit visualization.

## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/ui/streamlit_app.py
```

## Heroku deploy
```bash
heroku create false-green-dashboard-simulator
git push heroku main
```

## Mock mode
No OpenAI dependency is required in MVP.

## Roadmap
- export scenario reports
- compare monitoring strategies
- optional LLM narration behind provider interface
