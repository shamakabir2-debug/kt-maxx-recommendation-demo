# GiftHaven Release 1 Demo — Recommendation Engine

A small Streamlit app that replicates the Release 1 concept: an FP-Growth
market-basket recommendation engine, built on real transaction data from the
UCI "Online Retail" dataset.

## How to run it

1. Install Python 3.9+ if you don't already have it (python.org).
2. Open a terminal in this folder and run:

   pip install -r requirements.txt
   streamlit run app.py

3. It will open automatically in your browser at http://localhost:8501

## What's inside
- `app.py` — the Streamlit app (two tabs: customer-facing product view, and an
  analyst dashboard with charts).
- `app_rules.csv` — 434 real FP-Growth association rules (antecedent,
  consequent, support, confidence, lift), precomputed from 19,833 cleaned
  real orders so the app loads instantly without needing the full dataset.
- `app_rfm_summary.csv` — real RFM customer segment summary (4,338 customers).

No internet connection or database needed — all data is bundled as CSVs.
# kt-maxx-recommendation-demo
