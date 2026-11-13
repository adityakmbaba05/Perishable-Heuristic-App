# Perishable Inventory Heuristic Simulator

Interactive Streamlit simulator for perishable inventory management under non-stationary demand.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the displayed local URL, normally `http://localhost:8501`.

## Deploy with Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Open [share.streamlit.io](https://share.streamlit.io).
3. Choose **Create app** and select the repository and branch.
4. Set the main file path to `app.py`.
5. Click **Deploy**.

The resulting `https://*.streamlit.app` URL can be shared for remote access.

## Project structure

- `app.py` — Streamlit interface
- `heuristic.py` — replenishment heuristic and simulation
- `demand.py` — demand distributions
- `sdp.py` — benchmark interface
- `paper_data.py` — example and experiment data
- `run_experiments.py` — regenerate experiment CSV files
- `results/` — generated result tables
