# Binance Perpetual Futures - Funding, Basis, and Carry (Notebook + Code)

A hands-on tutorial that mirrors the options project style, but for **USD-M perpetual futures**.

## What’s inside
- `Binance_Futures_Modeling_Tutorial.ipynb` - walkthrough that:
  - Pulls **live** premium index & funding data (or uses bundled **sample**)
  - Computes **basis** and **annualized premium**
  - Plots **funding rate** history and **cumulative PnL** (long vs short)
  - Simulates a simple **cash-and-carry** (spot vs perp)
  - Shows classic **cost-of-carry** fair pricing for dated futures
- `src/futures_math.py` - utilities: basis/annualization, funding PnL, cash-and-carry PnL, cost-of-carry fair price, and a predicted funding estimator.
- `src/binance_futures_adapter.py` - thin wrappers for:
  - `/fapi/v1/premiumIndex` (mark, index, lastFundingRate, nextFundingTime)
  - `/fapi/v1/fundingRate` (history)
  - `/fapi/v1/exchangeInfo` (symbols/rules)
- `data/sample_*.json` - offline sample data so the notebook runs without internet.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab  # or: jupyter notebook / VS Code
```
Open **`Binance_Futures_Modeling_Tutorial.ipynb`** and run all cells.

- By default the notebook uses **sample data**.  
- To fetch **live** data, set in the first cell:
```python
USE_LIVE = True
SYMBOL = "BTCUSDT"
```

## Requirements
```
python>=3.10
numpy
pandas
matplotlib
requests
jupyter
nbformat
```