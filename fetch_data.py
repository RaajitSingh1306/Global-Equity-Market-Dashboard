"""
fetch_data.py
-------------
Fetches live price snapshots and computes 3-year risk/return KPIs
for a list of Indian (NSE) and US equities via yfinance.

Output: data/heatmap_data.csv
Columns: Ticker, Symbol, Name, Sector, Industry, Country,
         MarketCap, CurrentPrice, ChangePct,
         CAGR, Sharpe, Max_Drawdown, Avg_Vol_30d
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_DIR       = Path("data")
OUTPUT_CSV     = DATA_DIR / "heatmap_data.csv"
TICKERS_FILE   = Path("tickers.txt")

HISTORY_PERIOD = "3y"
HISTORY_INTERVAL = "1d"
MIN_TRADING_DAYS = 63        # ~3 months minimum
TRADING_DAYS_YEAR = 252
RISK_FREE_RATE = 0.065       # India 10yr G-Sec proxy (annualised)
VOL_WINDOW = 30              # days for avg volume

RETRY_ATTEMPTS = 3
RETRY_DELAY    = 2.0         # seconds between retries

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_tickers(path: Path = TICKERS_FILE) -> list[str]:
    """Read ticker symbols from a plain-text file, skipping comments and blanks."""
    with open(path, encoding="utf-8") as fh:
        return [
            line.strip()
            for line in fh
            if line.strip() and not line.startswith("#")
        ]


def compute_kpis(prices: pd.Series) -> dict[str, float | None]:
    """
    Compute CAGR, Sharpe ratio, and Max Drawdown from a daily Close series.

    Parameters
    ----------
    prices : pd.Series
        Daily closing prices (any index).

    Returns
    -------
    dict with keys CAGR, Sharpe, Max_Drawdown.
    All values are rounded floats or None if data is insufficient.
    """
    prices = prices.dropna()
    if len(prices) < MIN_TRADING_DAYS:
        return {"CAGR": None, "Sharpe": None, "Max_Drawdown": None}

    log_ret = np.log(prices / prices.shift(1)).dropna()

    # CAGR
    years = len(prices) / TRADING_DAYS_YEAR
    total_return = prices.iloc[-1] / prices.iloc[0]
    cagr = round((total_return ** (1.0 / years) - 1.0) * 100, 2)

    # Annualised Sharpe (log-return basis)
    daily_rf = RISK_FREE_RATE / TRADING_DAYS_YEAR
    vol = log_ret.std()
    sharpe = (
        round((log_ret.mean() - daily_rf) / vol * np.sqrt(TRADING_DAYS_YEAR), 2)
        if vol > 0
        else None
    )

    # Max Drawdown
    equity   = (1 + log_ret).cumprod()
    drawdown = (equity - equity.cummax()) / equity.cummax()
    max_dd   = round(float(drawdown.min()) * 100, 2)

    return {"CAGR": cagr, "Sharpe": sharpe, "Max_Drawdown": max_dd}


def _fetch_one(symbol: str) -> dict:
    """Fetch snapshot + KPIs for a single ticker with retry logic."""
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            ticker = yf.Ticker(symbol)
            info   = ticker.info or {}

            prev  = info.get("previousClose") or 0
            curr  = info.get("currentPrice") or info.get("regularMarketPrice") or 0
            chg   = round((curr - prev) / prev * 100, 2) if prev else None

            hist   = ticker.history(period=HISTORY_PERIOD, interval=HISTORY_INTERVAL)
            prices = hist["Close"] if not hist.empty else pd.Series(dtype=float)
            kpis   = compute_kpis(prices)

            avg_vol: int | None = None
            if "Volume" in hist.columns and len(hist) >= VOL_WINDOW:
                avg_vol = int(hist["Volume"].tail(VOL_WINDOW).mean())

            country_raw = info.get("country", "Unknown")
            country = (
                "India" if country_raw in ("India", "IN")
                else "United States" if country_raw in ("United States", "US")
                else country_raw
            )

            return {
                "Ticker":       symbol.replace(".NS", "").replace(".BO", ""),
                "Symbol":       symbol,
                "Name":         info.get("longName") or info.get("shortName") or symbol,
                "Sector":       info.get("sector") or "Unknown",
                "Industry":     info.get("industry") or "Unknown",
                "Country":      country,
                "MarketCap":    info.get("marketCap"),
                "CurrentPrice": round(float(curr), 2) if curr else None,
                "ChangePct":    chg,
                "CAGR":         kpis["CAGR"],
                "Sharpe":       kpis["Sharpe"],
                "Max_Drawdown": kpis["Max_Drawdown"],
                "Avg_Vol_30d":  avg_vol,
            }

        except Exception as exc:  # noqa: BLE001
            if attempt < RETRY_ATTEMPTS:
                log.warning("%s – attempt %d failed (%s). Retrying in %.0fs…",
                            symbol, attempt, exc, RETRY_DELAY)
                time.sleep(RETRY_DELAY)
            else:
                log.error("%s – all %d attempts failed: %s", symbol, RETRY_ATTEMPTS, exc)
                return {"Ticker": symbol, "Symbol": symbol}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch(
    tickers_path: Path = TICKERS_FILE,
    output_path: Path  = OUTPUT_CSV,
) -> pd.DataFrame:
    """
    Run the full data pipeline: load tickers → fetch → compute KPIs → save CSV.

    Parameters
    ----------
    tickers_path : Path
        Path to the tickers list file.
    output_path : Path
        Destination CSV path.

    Returns
    -------
    pd.DataFrame with all computed columns.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tickers = load_tickers(tickers_path)
    log.info("Loaded %d tickers from %s", len(tickers), tickers_path)

    rows = []
    for symbol in tickers:
        log.info("Fetching %-20s …", symbol)
        row = _fetch_one(symbol)
        rows.append(row)
        kpis_str = (
            f"CAGR={row.get('CAGR')}%  "
            f"Sharpe={row.get('Sharpe')}  "
            f"MaxDD={row.get('Max_Drawdown')}%"
        )
        log.info("  ✓ %s", kpis_str)

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    log.info("Saved %d rows → %s", len(df), output_path)
    return df


# ---------------------------------------------------------------------------
# CLI usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    result = fetch()
    preview_cols = ["Ticker", "Sector", "CAGR", "Sharpe", "Max_Drawdown", "ChangePct"]
    available = [c for c in preview_cols if c in result.columns]
    print("\n── Preview ─────────────────────────────────────────────────")
    print(result[available].to_string(index=False))