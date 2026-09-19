# Global Equity Market Heatmap & Risk-Return Dashboard

[![Streamlit Dashboard](https://img.shields.io/badge/Streamlit-Interactive%20Web%20App-red)](#streamlit-dashboard-web)
[![Power BI](https://img.shields.io/badge/Power%20BI-dashboard.pbix-yellow)](#power-bi-dashboard-desktop)
[![Data Pipeline](https://img.shields.io/badge/Data-Yahoo%20Finance%20Live-blue)](#architecture)
[![Coverage](https://img.shields.io/badge/Universe-35%20Equities%20(IN%20%2B%20US)-green)](#coverage)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An institutional-grade interactive market monitoring system that visualizes **35 Indian (NSE) and US equities** across 10 sectors using hierarchical heatmaps combined with multi-year risk-return analytics.

The system connects directly to Yahoo Finance to fetch live intraday pricing and 3-year daily OHLCV history, computes key performance metrics (CAGR, Annualized Sharpe Ratio, Maximum Drawdown, Liquidity), and serves the analytics via two frontends: a **Streamlit Web Application** with Plotly visualizations and a native **Power BI Desktop Report** (`.pbix`).

---

## Table of Contents

1. [What This Project Does](#what-this-project-does)
2. [Why It Was Built](#why-it-was-built)
3. [Architecture & Data Flow](#architecture--data-flow)
4. [Coverage & Universe](#coverage--universe)
5. [KPIs & Formulations](#kpis--formulations)
6. [Project Structure](#project-structure)
7. [Where & How to Start](#where--how-to-start)
   - [Step 1: Environment Setup](#step-1-environment-setup)
   - [Step 2: Generate Dataset](#step-2-generate-dataset)
   - [Step 3A: Launch Streamlit Web Dashboard](#step-3a-launch-streamlit-web-dashboard)
   - [Step 3B: Open Power BI Dashboard](#step-3b-open-power-bi-dashboard)
8. [Dashboard Capabilities](#dashboard-capabilities)
9. [Connected Portfolio Projects](#connected-portfolio-projects)

---

## What This Project Does

Given a diversified basket of cross-border equities, the system:

1. **Ingests Cross-Market Data**: Reads symbols from `tickers.txt` and queries Yahoo Finance (`yfinance`) for both real-time intraday quotes (last price, change %, market cap) and 3-year daily trading histories.
2. **Computes Institutional Risk-Return Metrics**:
   - **CAGR** over a rolling 3-year investment horizon.
   - **Annualized Sharpe Ratio** ($R_f = 6.5\%$ standard benchmark).
   - **Maximum Peak-to-Trough Drawdown**.
   - **30-Day Average Volume** as an institutional liquidity indicator.
3. **Persists Formatted Analytics**: Normalizes Indian (`.NS`) and US equities into a structured schema at `data/heatmap_data.csv`.
4. **Delivers Dual-Frontend Visualization**:
   - **Streamlit Web App**: Real-time cross-filtering, interactive Plotly treemaps by sector and country, risk-return scatter plots, and sorted data tables.
   - **Power BI Report (`dashboard.pbix`)**: Executive dashboard layout with slicers, sector cards, and visual drill-downs.

---

## Why It Was Built

* **Cross-Border Monitoring**: Enables simultaneous comparison between high-growth Indian emerging market leaders and mature US mega-cap technology and industrial titans.
* **Beyond Pure Price Changes**: Standard financial news heatmaps only show today's 1-day percentage fluctuation, hiding underlying structural risk. This dashboard layers 3-year risk-adjusted returns (Sharpe ratio) and downside vulnerability (Max Drawdown) directly onto the visualization.
* **Multi-Modal Consumption**: Provides an accessible Python web dashboard for immediate browser viewing and an enterprise `.pbix` model for corporate business intelligence environments.

---

## Architecture & Data Flow

```text
tickers.txt (35 Indian & US symbols)
      │
      ▼
main.py / fetch_data.py
      ├── yfinance .info     ──► Live snapshot (Price, Change %, Market Cap)
      └── yfinance .history  ──► 3-Year Daily OHLCV (CAGR, Sharpe, Max Drawdown)
      │
      ▼
data/heatmap_data.csv (Clean unified dataset)
      │
      ├───────────────────────────────┐
      ▼                               ▼
Streamlit Web App (Port 8501)    Power BI Desktop (.pbix)
dashboard_streamlit.py           dashboard.pbix
• Plotly Sector Treemaps         • Institutional KPI Cards
• Risk-Return Scatter Matrix     • Interactive Sector Slicers
• Multi-Asset Data Table         • Drill-Through Visuals
```

---

## Coverage & Universe

The universe tracks 35 industry-leading blue chips across 10 major economic sectors:

### Indian Equities (NSE: 25 Stocks)
* **IT & Technology**: TCS, Infosys (`INFY`), Wipro (`WIPRO`), HCL Tech (`HCLTECH`), Tech Mahindra (`TECHM`)
* **Banking & Finance**: HDFC Bank (`HDFCBANK`), ICICI Bank (`ICICIBANK`), Kotak Mahindra (`KOTAKBANK`), Axis Bank (`AXISBANK`), State Bank of India (`SBIN`)
* **Energy & Utilities**: Reliance Industries (`RELIANCE`), ONGC (`ONGC`), NTPC (`NTPC`), Power Grid (`POWERGRID`)
* **Consumer Staples**: Hindustan Unilever (`HINDUNILVR`), ITC (`ITC`), Nestle India (`NESTLEIND`)
* **Automotive**: Maruti Suzuki (`MARUTI`), Tata Motors (`TATAMOTORS`), Bajaj Auto (`BAJAJ-AUTO`)
* **Healthcare & Pharma**: Sun Pharma (`SUNPHARMA`), Dr. Reddy's (`DRREDDY`), Cipla (`CIPLA`)
* **Metals & Mining**: Tata Steel (`TATASTEEL`), JSW Steel (`JSWSTEEL`)

### US Equities (10 Stocks)
* **Technology**: Apple (`AAPL`), Microsoft (`MSFT`), NVIDIA (`NVDA`), Alphabet (`GOOGL`), Meta (`META`)
* **Automotive**: Tesla (`TSLA`)
* **Financial Services**: JPMorgan Chase (`JPM`), Bank of America (`BAC`), Goldman Sachs (`GS`)
* **Healthcare**: Johnson & Johnson (`JNJ`), Pfizer (`PFE`)
* **Energy**: ExxonMobil (`XOM`), Chevron (`CVX`)

---

## KPIs & Formulations

| KPI | Formula | Description |
|---|---|---|
| **CAGR** | $(P_{\text{end}} / P_{\text{start}})^{1/3} - 1$ | 3-year compound annual growth rate |
| **Sharpe Ratio** | $\frac{\text{mean}(r_{\text{log}}) - R_f/252}{\text{std}(r_{\text{log}})} \times \sqrt{252}$ | Risk-adjusted return with $R_f = 6.5\%$ |
| **Max Drawdown** | $\min \left(\frac{P_t - \max_{\tau \le t} P_\tau}{\max_{\tau \le t} P_\tau}\right)$ | Maximum peak-to-trough capital decline over 3 years |
| **Avg Vol (30d)** | $\frac{1}{30} \sum_{i=1}^{30} \text{Volume}_i$ | 30-day average daily share volume (liquidity gauge) |

---

## Key Design Decisions

- **3-Year Lookback Window**: 3 full years captures complete business cycle phases (expansion, tightening, recovery) while maintaining recency for contemporary market conditions.
- **Dual Visual Frontend Strategy**: Streamlit with interactive Plotly provides an instant Python-native browser dashboard; Power BI (`dashboard.pbix`) enables enterprise BI users to perform slicer slicing, drill-down, and corporate reporting.
- **Decoupled Flat-File Architecture**: Configured ticker universe is defined in a plain `tickers.txt` text file, and materialized to `data/heatmap_data.csv`. This avoids database overhead while allowing instant universe additions.
- **Consistent Log Returns for Sharpe**: Logarithmic daily returns are used for annualization ($\text{std}(r_{\text{log}}) \times \sqrt{252}$), maintaining analytical consistency with the `Finance KPI` engine.
- **Lightweight Snapshot Ingestion**: Uses `yfinance` `.info` and historical batch downloads rather than persistent paid streaming feeds (Bloomberg, Refinitiv) to keep the project completely open-source and free to run.

---

## Project Structure

```text
Global Market HeatMap/
├── main.py                 # Pipeline trigger script
├── fetch_data.py           # Core ingestion & KPI computation engine
├── dashboard_streamlit.py  # Interactive Streamlit + Plotly web frontend
├── dashboard.pbix          # Power BI Desktop report
├── tickers.txt             # 35 configured asset symbols
├── how to run.txt          # Quick execution notes
├── requirements.txt        # Python dependencies (yfinance, streamlit, plotly)
├── Readme.md               # Project documentation
└── data/
    └── heatmap_data.csv    # Generated analytics dataset
```

---

## Where & How to Start

### Step 1: Environment Setup

Navigate to the project directory and set up a virtual environment:

```bash
cd "Global Market HeatMap"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Generate Dataset

Execute the pipeline to query Yahoo Finance and write `data/heatmap_data.csv`:

```bash
python main.py
# or
python fetch_data.py
```

*The script fetches live snapshots and 3-year daily price history for all 35 tickers, prints progress logs, and saves the consolidated CSV.*

### Step 3A: Launch Streamlit Web Dashboard

Start the local web server:

```bash
streamlit run dashboard_streamlit.py
```

* Access the interactive dashboard in your browser at: **`http://localhost:8501`**
* Filter by Country (All, India, United States)
* Select Sector drill-downs
* Switch metric views: Daily Change %, 3-Year CAGR, Sharpe Ratio, or Max Drawdown

### Step 3B: Open Power BI Dashboard

1. Launch **Power BI Desktop**.
2. Open `dashboard.pbix`.
3. To refresh the data with newly generated numbers:
   - Click **Home** → **Refresh Data** (Power BI points to `data/heatmap_data.csv`).
4. Interact with slicers, cross-filtering, and dynamic KPI cards.

---

## Dashboard Capabilities

* **Market Treemap**: Tile sizes mapped to Market Capitalization; colors dynamically graded from negative red to positive green based on selected KPI (Daily Change, CAGR, or Sharpe).
* **Risk vs. Return Matrix**: Scatter plot plotting 3-Year Volatility / Max Drawdown against CAGR, instantly separating high-alpha performers from high-risk laggards.
* **Top Movers Bar Charts**: Rapid ranking of the day's biggest gainers and losers across both geographies.
* **Tabular Screener**: Searchable, downloadable table of all 35 assets with formatted currency and percentage indicators.

---

## Results

Empirical distributions materialized across the 37 active global assets in `data/heatmap_data.csv`:

- **Daily Return Performance**: Range spans from **-3.62%** (Sun Pharma) to **+3.17%** (ICICI Bank) and **+3.12%** (Bajaj Auto).
- **3-Year Compound Growth (CAGR)**:
  - Mega-cap US Tech leaders: **+91.32%** (Nvidia), **+45.02%** (Alphabet), **+43.93%** (Meta).
  - Indian Banking & Industrial leaders: **+37.86%** (Bajaj Auto), **+29.55%** (State Bank of India), **+29.12%** (Tata Steel).
  - Laggards / Structural headwind assets: **-8.30%** (Pfizer), **-5.71%** (TCS), **-3.54%** (Hindustan Unilever).
- **Risk-Adjusted Sharpe Ratio ($R_f = 6.5\%$)**:
  - Highest risk-adjusted performers: **1.21** (Nvidia), **1.10** (JPMorgan Chase), **1.09** (Goldman Sachs), **1.05** (Alphabet), **1.02** (Bajaj Auto).
  - Negative Sharpe performers: **-0.62** (Pfizer), **-0.60** (TCS), **-0.54** (Hindustan Unilever), **-0.53** (ITC).
- **Peak-to-Trough Maximum Drawdowns**:
  - Defensive staples and diversified industrials: **-15.56%** (JSW Steel), **-16.27%** (Johnson & Johnson), **-19.17%** (ICICI Bank).
  - High-beta / volatile growth leaders: **-57.60%** (Tesla), **-47.26%** (TCS), **-45.04%** (Pfizer), **-41.14%** (Nvidia).

---

## Connected Portfolio Projects

* **[Finance KPI](https://github.com/RaajitSingh1306/Finance_Kpi)**: Deep-dive single-ticker 4-panel diagnostic equity generator.
* **[Nifty Sector Rotation](https://github.com/RaajitSingh1306/Nifty-Sector-Rotation)**: Dynamic momentum allocation across Indian sector indices.
* **[Volatility Intelligence Platform](https://github.com/RaajitSingh1306/volatility-intelligence-platform)**: Advanced volatility forecasting with econometric GARCH and machine learning.

---

## Limitations & Roadmap

### Known Limitations
- **Upstream Throttle Sensitivity**: Fetching financial summaries and 3-year historical bars sequentially for 35+ global tickers via `yfinance` can experience intermittent throttling or connection timeouts.
- **Static Power BI Refresh**: The `.pbix` report requires Power BI Desktop on Windows and manual "Refresh" clicks; automated cloud scheduled refresh requires Power BI Gateway and Service licensing.
- **Batch Refresh Cadence**: `main.py` runs on-demand; prices do not update continuously during live trading sessions.
- **Unified Risk-Free Assumption**: Uses a single $R_f = 6.5\%$ (India 10Y Benchmark) across all assets. US equities would ideally be benchmarked against the US 10-Year Treasury (~4.2–4.5%).
- **Unadjusted FX Returns**: Indian Rupee and US Dollar returns are evaluated in local quote currencies; currency exchange volatility is not subtracted or hedged.

### Roadmap
- [ ] **Jurisdiction-Specific Risk-Free Rates**: Implement multi-currency $R_f$ selection (e.g. 10Y US Treasury for USD equities, 10Y G-Sec for INR equities).
- [ ] **FX-Adjusted Unified Portfolio Return**: Add currency-normalized USD and INR returns to compare cross-border performance accurately.
- [ ] **Sector-Level Aggregation Layer**: Add rollup views for sector-wide median Sharpe, aggregate market cap, and breadth.
- [ ] **Automated GitHub Actions Ingestion**: Schedule `main.py` via GitHub Actions on market close to commit fresh `data/heatmap_data.csv` snapshots daily.

---

## License & Disclaimer

MIT License. For educational research and market monitoring only. Not investment advice.