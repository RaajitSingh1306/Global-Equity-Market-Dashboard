# Global Equity Market Heatmap & Risk-Return Dashboard

[![Streamlit Dashboard](https://img.shields.io/badge/Streamlit-Interactive%20Web%20App-red)](#step-3a-launch-streamlit-web-dashboard)
[![Power BI](https://img.shields.io/badge/Power%20BI-dashboard.pbix-yellow)](#step-3b-open-power-bi-dashboard)
[![Data Pipeline](https://img.shields.io/badge/Data-Yahoo%20Finance%20Live-blue)](#5-data)
[![Universe](https://img.shields.io/badge/Coverage-35%20Equities%20(IN%20%2B%20US)-green)](#5-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#16-license--disclaimer)

An institutional-grade interactive market monitoring system that visualizes **35 Indian (NSE) and US equities** across 10 sectors using hierarchical treemaps combined with multi-year risk-return analytics. The system fetches live intraday pricing and 3-year daily OHLCV history via Yahoo Finance, computes core quantitative performance metrics (CAGR, Annualized Sharpe Ratio, Maximum Drawdown, Liquidity), and serves analytics through dual frontends: a **Streamlit Web Application** with Plotly visualizations and a native **Power BI Desktop Report** (`.pbix`).

---

## Table of Contents

- [1. What This Project Does](#1-what-this-project-does)
- [2. Why It Was Built](#2-why-it-was-built)
- [3. System Architecture](#3-system-architecture)
- [4. Tech Stack & Libraries](#4-tech-stack--libraries)
- [5. Data](#5-data)
- [6. Step-by-Step Pipeline](#6-step-by-step-pipeline)
- [7. Problems Faced & How We Solved Them](#7-problems-faced--how-we-solved-them)
- [8. Results & Evaluation](#8-results--evaluation)
- [9. Project Structure](#9-project-structure)
- [10. Getting Started](#10-getting-started)
- [11. Dashboard Capabilities & Views](#11-dashboard-capabilities--views)
- [12. Deployment](#12-deployment)
- [13. Connected Portfolio Projects](#13-connected-portfolio-projects)
- [14. Limitations & Known Issues](#14-limitations--known-issues)
- [15. Roadmap / Future Expansion](#15-roadmap--future-expansion)
- [16. License & Disclaimer](#16-license--disclaimer)

---

## 1. What This Project Does

Given a diversified universe of cross-border equities, the system delivers:

- **Cross-Market Data Ingestion**: Reads symbols from `tickers.txt` and queries Yahoo Finance for both real-time intraday quotes (last price, change %, market cap) and 3-year daily trading histories.
- **Institutional Risk-Return KPIs**:
  - **3-Year CAGR** (Compound Annual Growth Rate) measuring structural business-cycle appreciation.
  - **Annualized Sharpe Ratio** ($R_f = 6.5\%$ benchmark yield) to quantify return per unit of volatility risk.
  - **Maximum Peak-to-Trough Drawdown** evaluating historical capital preservation.
  - **30-Day Average Volume** as an institutional liquidity indicator.
- **Unified Analytics Persistence**: Normalizes Indian (`.NS`) and US equities into a clean schema stored at `data/heatmap_data.csv`.
- **Dual Visual Frontend Strategy**:
  - **Streamlit Web App**: Real-time cross-filtering, interactive Plotly treemaps by sector and country, risk-return scatter plots, and sorted data tables.
  - **Power BI Report (`dashboard.pbix`)**: Executive desktop report with slicers, sector summary cards, and visual drill-downs.

---

## 2. Why It Was Built

- **Cross-Border Monitoring**: Enables simultaneous side-by-side comparison between high-growth Indian emerging market leaders and mature US mega-cap technology and industrial titans.
- **Beyond Pure 1-Day Price Noise**: Financial news heatmaps typically show only today's 1-day percentage movement, obscuring structural volatility and drawdown risk. This platform layers 3-year risk-adjusted returns (Sharpe ratio) and downside exposure directly onto the visual representation.
- **Multi-Modal Enterprise Consumption**: Bridges Python-native ad-hoc data science exploration (via Streamlit + Plotly) with corporate business intelligence environments (via Microsoft Power BI Desktop).

---

## 3. System Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        TICKER CONFIGURATION                            │
│                                                                        │
│   tickers.txt (35 Indian NSE & US equity symbols across 10 sectors)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION ENGINE                           │
│                      (main.py / fetch_data.py)                         │
│                                                                        │
│   ├── yfinance .info     ──► Intraday quotes (Last, Change %, MktCap)  │
│   └── yfinance .history  ──► 3-Year Daily OHLCV Time Series            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      QUANTITATIVE KPI CALCULATOR                       │
│                                                                        │
│   ├── 3-Year Compounded CAGR: (P_end / P_start)^(1/3) - 1              │
│   ├── Annualized Sharpe Ratio: (mean(r_log) * 252 - R_f) / Ann_Vol     │
│   ├── Max Peak-to-Trough Drawdown: min((P_t - cummax(P)) / cummax(P))  │
│   └── 30-Day Average Share Volume: sum(Vol_30d) / 30                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       PERSISTED DATA LAYER                             │
│                                                                        │
│   data/heatmap_data.csv (Clean unified cross-border schema)            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
┌───────────────────────────────────────┐ ┌──────────────────────────────┐
│        STREAMLIT WEB DASHBOARD        │ │       POWER BI REPORT        │
│        (dashboard_streamlit.py)       │ │       (dashboard.pbix)       │
│               Port :8501              │ │       (Desktop Engine)       │
│                                       │ │                              │
│  - Hierarchical Plotly Treemaps       │ │  - Executive KPI Cards       │
│  - Risk-Return Scatter Matrix         │ │  - Interactive Slicers       │
│  - Country & Sector Drill-Downs       │ │  - Cross-Filtering Charts    │
│  - Searchable Screener Table          │ │  - Direct CSV Refresh Hook   │
└───────────────────────────────────────┘ └──────────────────────────────┘
```

---

## 4. Tech Stack & Libraries

| Library / Tool | Version | Purpose | Rationale |
|---|---|---|---|
| **Python** | `>=3.10` | Core programming runtime | High-performance ecosystem for financial time series and scripting |
| **yfinance** | `^0.2.36` | Market data ingestion | Access to global equities across NSE and US exchanges with split/dividend adjustment |
| **pandas** | `^2.1.0` | Tabular data processing | Time-series slicing, rolling window math, and unified CSV persistence |
| **numpy** | `^1.26.0` | Vectorized numerical computing | Logarithmic return transforms, annualization scaling, and array operations |
| **streamlit** | `^1.31.0` | Interactive web dashboard | Rapid, reactive analytical dashboarding without complex frontend boilerplate |
| **plotly** | `^5.18.0` | Interactive chart generation | Dynamic zooming treemaps, tooltips, and risk-return scatter plots |
| **Power BI Desktop** | `^2.126.0` | Enterprise business intelligence | Corporate data visualization model (`.pbix`) with native DAX slicing |

---

## 5. Data

- **Configured Universe**: 35 industry-leading blue chips spanning 10 major economic sectors (defined in `tickers.txt`).
  - **Indian Equities (NSE: 25)**:
    - *IT & Technology*: TCS, Infosys (`INFY`), Wipro (`WIPRO`), HCL Tech (`HCLTECH`), Tech Mahindra (`TECHM`)
    - *Banking & Finance*: HDFC Bank (`HDFCBANK`), ICICI Bank (`ICICIBANK`), Kotak Mahindra (`KOTAKBANK`), Axis Bank (`AXISBANK`), SBI (`SBIN`)
    - *Energy & Utilities*: Reliance Industries (`RELIANCE`), ONGC (`ONGC`), NTPC (`NTPC`), Power Grid (`POWERGRID`)
    - *Consumer Staples*: Hindustan Unilever (`HINDUNILVR`), ITC (`ITC`), Nestle India (`NESTLEIND`)
    - *Automotive*: Maruti Suzuki (`MARUTI`), Tata Motors (`TATAMOTORS`), Bajaj Auto (`BAJAJ-AUTO`)
    - *Healthcare & Pharma*: Sun Pharma (`SUNPHARMA`), Dr. Reddy's (`DRREDDY`), Cipla (`CIPLA`)
    - *Metals & Mining*: Tata Steel (`TATASTEEL`), JSW Steel (`JSWSTEEL`)
  - **US Equities (10)**:
    - *Technology*: Apple (`AAPL`), Microsoft (`MSFT`), NVIDIA (`NVDA`), Alphabet (`GOOGL`), Meta (`META`)
    - *Automotive*: Tesla (`TSLA`)
    - *Financial Services*: JPMorgan Chase (`JPM`), Bank of America (`BAC`), Goldman Sachs (`GS`)
    - *Healthcare*: Johnson & Johnson (`JNJ`), Pfizer (`PFE`)
    - *Energy*: ExxonMobil (`XOM`), Chevron (`CVX`)
- **Data Attributes Collected**: Intraday Price, Day Change %, Market Cap, 3-Year Daily OHLCV, 30-Day Volume.
- **Output Artifact**: Structured tabular dataset materialized to `data/heatmap_data.csv`.

---

## 6. Step-by-Step Pipeline

1. **Universe Ingestion**: Parse `tickers.txt` and load sector and country taxonomy mapping.
2. **Sequential API Extraction**:
   - Query `yfinance.Ticker(symbol).info` for current price, previous close, market cap, and trading currency.
   - Query `yfinance.Ticker(symbol).history(period="3y")` for daily OHLCV bars.
3. **Price Normalization & Log Returns**: Extract dividend-adjusted prices and compute daily logarithmic returns:
   $$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)$$
4. **Multi-Year KPI Computation**:
   - Compound annual growth rate: $\text{CAGR} = (P_{\text{end}} / P_{\text{start}})^{1/3} - 1$
   - Annualized volatility: $\sigma_{\text{ann}} = \text{std}(r_{\text{log}}) \times \sqrt{252}$
   - Annualized Sharpe ratio: $\text{Sharpe} = \frac{\bar{r}_{\text{log}} \times 252 - 0.065}{\sigma_{\text{ann}}}$
   - Max peak-to-trough drawdown: $\text{Max DD} = \min_t \left(\frac{P_t - \max_{\tau \le t} P_\tau}{\max_{\tau \le t} P_\tau}\right)$
5. **CSV Materialization**: Merge calculated metrics into a unified schema and write to `data/heatmap_data.csv`.
6. **Frontend Consumption**: Launch Streamlit web app (`dashboard_streamlit.py`) or open Power BI model (`dashboard.pbix`) pointing to the refreshed CSV.

---

## 7. Problems Faced & How We Solved Them

| Problem | Impact | How We Got Around It |
|---|---|---|
| **yfinance throttling** when fetching 35+ tickers sequentially | Intermittent connection timeouts and incomplete data for several tickers during batch updates | Added per-ticker try/except error handling with graceful skipping; decoupled the `.info` live snapshot call from `.history` batch download to reduce per-request payload size and API pressure |
| **Power BI requires manual refresh clicks** | Generated data went stale in the dashboard unless someone manually clicked Refresh in Power BI Desktop | Decoupled data generation (`main.py` writes to `data/heatmap_data.csv`) from visualization; Power BI points directly to the persistent CSV and can be refreshed on demand, while Streamlit reads the fresh CSV dynamically on load |
| **INR vs USD currency mismatch** | Comparing Indian and US equities directly mixed currencies, making Sharpe and CAGR comparisons potentially misleading | Acknowledged limitation explicitly; used a single standardized $R_f = 6.5\%$ (India 10Y G-Sec) as baseline benchmark across all equities. Documented the trade-off and scheduled multi-currency risk-free adjustments for the roadmap |
| **Missing market cap data** for some tickers | `yfinance .info` occasionally returned `None` or omitted market cap, crashing the Plotly treemap hierarchy sizing | Added defensive null-check fallback logic that substitutes median sector market cap values when the API returns incomplete financial summaries |
| **Treemap color scaling** across mixed KPIs | Daily change %, CAGR, and Sharpe have completely different scales (-5% to +5% vs -20% to +90% vs -0.6 to +1.2), making a static color gradient meaningless | Implemented **per-metric dynamic color normalization** in Plotly — each KPI view dynamically recalculates min/max percentile bounds and maps to a diverging red-to-green gradient independently |

---

## 8. Results & Evaluation

Empirical metrics recorded across the 35+ asset universe in `data/heatmap_data.csv`:

### Cross-Asset Performance Overview

| Category / Metric | Top Performers | Benchmark / Median | Laggards / Drawdown Leaders |
|---|---|---|---|
| **3-Year CAGR** | **Nvidia (+91.3%)**, Alphabet (+45.0%), Meta (+43.9%), Bajaj Auto (+37.9%) | Nifty 50 (~11.4%), US S&P 500 (~12.8%) | Pfizer (-8.3%), TCS (-5.7%), HUL (-3.5%) |
| **Sharpe Ratio ($R_f=6.5\%$)** | **Nvidia (1.21)**, JPMorgan (1.10), Goldman Sachs (1.09), Bajaj Auto (1.02) | Indian Large-Cap Avg (~0.45) | Pfizer (-0.62), TCS (-0.60), HUL (-0.54) |
| **Max Peak-to-Trough Drawdown** | **JSW Steel (-15.6%)**, J&J (-16.3%), ICICI Bank (-19.2%) | Market Index Drawdown (~-22% to -38%) | Tesla (-57.6%), TCS (-47.3%), Pfizer (-45.0%) |
| **Daily Volatility Span** | Sun Pharma (-3.62%) to ICICI Bank (+3.17%) | Daily Interquartile Range: ±0.85% | High Beta Growth Equities |

---

## 9. Project Structure

```text
Global Market HeatMap/
├── main.py                 # Pipeline trigger script
├── fetch_data.py           # Core ingestion & KPI computation engine
├── dashboard_streamlit.py  # Interactive Streamlit + Plotly web frontend
├── dashboard.pbix          # Power BI Desktop report
├── tickers.txt             # 35 configured asset symbols across 10 sectors
├── how to run.txt          # Quick execution notes
├── requirements.txt        # Python dependencies (yfinance, streamlit, plotly, pandas)
├── Readme.md               # Project documentation
└── data/
    └── heatmap_data.csv    # Generated analytics dataset
```

---

## 10. Getting Started

### Step 1: Environment Setup

```bash
cd "Global Market HeatMap"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Generate / Refresh Dataset

Execute the pipeline to query Yahoo Finance and generate `data/heatmap_data.csv`:

```bash
python main.py
# or
python fetch_data.py
```

*The script iterates over all 35 tickers, prints progress logs, and persists the unified analytics table.*

### Step 3A: Launch Streamlit Web Dashboard

Start the local web server:

```bash
streamlit run dashboard_streamlit.py
```

- Access the dashboard at: **`http://localhost:8501`**
- Use the sidebar to filter by country (All, India, United States) or sector.
- Switch metric color modes: Daily Change %, 3-Year CAGR, Sharpe Ratio, or Max Drawdown.

### Step 3B: Open Power BI Dashboard

1. Launch **Power BI Desktop**.
2. Open `dashboard.pbix`.
3. To refresh data with the latest generated dataset:
   - Click **Home** → **Refresh** (points directly to `data/heatmap_data.csv`).
4. Interact with slicers, sector cards, and drill-downs.

---

## 11. Dashboard Capabilities & Views

- **Market Treemap View**: Tile dimensions scale proportional to market capitalization; colors dynamically reflect selected KPI (Daily Change, CAGR, or Sharpe Ratio).
- **Risk vs. Return Matrix**: Scatter plot correlating 3-year volatility and maximum drawdown against CAGR, immediately identifying alpha leaders and downside vulnerabilities.
- **Top Movers Leaderboard**: Rapid rankings of the day's top gainers and losers across both Indian and US equities.
- **Searchable Screener Table**: Interactive tabular view with formatted currencies, percentage returns, and volume metrics.

---

## 12. Deployment

- **Streamlit Community Cloud**: Connect the repository to Streamlit Cloud with `dashboard_streamlit.py` as entrypoint.
- **Scheduled Automated Refresh**: Set up a GitHub Actions workflow or Linux cron job to run `main.py` at daily exchange close (16:00 IST / 16:00 EST) and commit the updated `data/heatmap_data.csv`.

---

## 13. Connected Portfolio Projects

- **[Finance KPI](https://github.com/RaajitSingh1306/Finance_Kpi)**: Single-ticker 4-panel diagnostic equity generator that provided the foundational calculation formulas.
- **[Nifty Sector Rotation](https://github.com/RaajitSingh1306/Nifty-Sector-Rotation)**: Quantitative momentum allocation system rotating across 10 Indian sector indices.
- **[Volatility Intelligence Platform](https://github.com/RaajitSingh1306/volatility-intelligence-platform)**: Flagship econometrics and ML platform predicting volatility regimes for Indian indices.

---

## 14. Limitations & Known Issues

- **Upstream Rate Throttling**: Fetching 35+ tickers sequentially via Yahoo Finance can experience occasional latency spikes or rate limiting.
- **Power BI Desktop Dependency**: `.pbix` report requires Power BI Desktop on Windows and manual refresh; automated cloud refresh requires Power BI Service and Gateway licensing.
- **Single Risk-Free Rate**: Applies a single $R_f = 6.5\%$ (India 10Y Benchmark) across all assets rather than using US 10Y Treasury rates for USD equities.
- **Unadjusted FX Returns**: Indian Rupee and US Dollar returns are evaluated in their native quote currencies without subtracting USD/INR exchange rate fluctuations.

---

## 15. Roadmap / Future Expansion

- [ ] **Jurisdiction-Specific Risk-Free Benchmarks**: Implement dual $R_f$ selection (10Y US Treasury for USD equities, 10Y G-Sec for INR equities).
- [ ] **FX-Adjusted Unified Portfolio Return**: Add currency-normalized USD and INR returns to assess true cross-border performance.
- [ ] **Automated GitHub Actions Ingestion**: Schedule `main.py` via GitHub Actions on market close to commit fresh `data/heatmap_data.csv` snapshots daily.
- [ ] **Sector-Level Aggregation Rollups**: Add rollup cards for sector-wide median Sharpe, aggregate market capitalization, and market breadth.

---

## 16. License & Disclaimer

### License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

### Disclaimer
This software is built for educational, research, and portfolio monitoring purposes only. It does not constitute investment advice or solicitation.