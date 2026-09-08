# P4 — Global Equity Market Dashboard

Interactive dashboard visualising **35 Indian and US equities** across 10 sectors using a sector-wise heatmap combined with risk-return analytics.  
Data is fetched live from Yahoo Finance; KPIs are computed from 3 years of daily prices and served via two frontends: Power BI (primary) and Streamlit (fallback).

---

## Architecture

```
tickers.txt  (35 symbols)
      │
fetch_data.py
      ├── yfinance .info     →  live snapshot  (price, change %, market cap)
      └── yfinance .history  →  3yr daily OHLCV  →  CAGR, Sharpe, Max Drawdown
      │
data/heatmap_data.csv
      ├── dashboard.pbix              ← Power BI  (primary)
      └── dashboard_streamlit.py      ← Streamlit (fallback)
```

---

## KPIs

| KPI | Formula | Notes |
|---|---|---|
| CAGR | `(P_end / P_start)^(1/years) − 1` | 3-year window |
| Sharpe Ratio | `(mean(log_ret) − Rf/252) / std(log_ret) × √252` | Rf = 6.5% (India 10yr G-Sec) |
| Max Drawdown | `min((equity − cummax) / cummax)` | Worst peak-to-trough % |
| Avg Vol 30d | Mean of last 30 days' daily volume | Liquidity proxy |

---

## Dataset Columns

| Column | Description |
|---|---|
| Ticker | Short symbol (no exchange suffix) |
| Name | Full company name |
| Sector | Industry classification (yfinance) |
| Country | India / United States |
| MarketCap | Market capitalisation (USD) |
| CurrentPrice | Last traded price |
| ChangePct | Daily % price change |
| CAGR | 3-year compound annual growth rate (%) |
| Sharpe | 3-year annualised Sharpe ratio |
| Max_Drawdown | Worst drawdown % over 3 years |
| Avg_Vol_30d | 30-day average daily volume |

---

## Coverage

**Indian equities (NSE):** TCS, Infosys, Wipro, HCLTech, TechM, HDFC Bank, ICICI Bank, Kotak, Axis, SBI, Reliance, ONGC, NTPC, PowerGrid, HUL, ITC, Nestle, Maruti, Tata Motors, Bajaj Auto, Sun Pharma, Dr Reddy's, Cipla, Tata Steel, JSW Steel

**US equities:** AAPL, MSFT, NVDA, GOOGL, META, TSLA, JPM, BAC, GS, JNJ, PFE, XOM, CVX

---

## Dashboard Features

### Power BI (`dashboard.pbix`)
- Treemap: tile size = Market Cap, colour = daily % change (red/green)
- Risk-return scatter: X = Max Drawdown, Y = CAGR, bubble = Sharpe
- KPI cards: Avg CAGR, Avg Sharpe, Max Drawdown, top stock
- Slicers: Sector, Country

### Streamlit (`dashboard_streamlit.py`)
- Sector heatmap treemap (Plotly)
- Risk-return scatter with country grouping
- 5 live KPI cards
- Avg CAGR and Avg Sharpe bar charts by sector
- Colour-graded sortable data table
- Sidebar filters: Country, Sector, Market Cap floor
- Refresh button (clears cache, re-fetches CSV)

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
# Fetch live data and open Power BI
python main.py

# Fetch only (no Power BI, useful on Linux/CI)
python main.py --no-pbix

# Streamlit fallback dashboard
streamlit run dashboard_streamlit.py
```

---

## File Structure

```
04_market_heatmap/
├── fetch_data.py           ← data pipeline + KPI computation
├── main.py                 ← CLI entry point
├── dashboard_streamlit.py  ← Streamlit fallback dashboard
├── dashboard.pbix          ← Power BI dashboard
├── tickers.txt             ← 35 symbols (Indian + US)
├── requirements.txt
├── LICENSE
├── .gitignore
└── data/                   ← generated (git-ignored)
    └── heatmap_data.csv
```

---
## Frontend

Interactive dashboard built in **Streamlit + Plotly**. A Power BI prototype exists 
locally but is not hosted — Streamlit is the deployed interface.

**Live**: [global-equity-market-dashboard.streamlit.app](https://global-equity-market-dashboard.streamlit.app/)
---

## Data Disclaimer

Market data is sourced from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance).  
This project is for educational and portfolio demonstration purposes only and does not constitute financial advice.

---