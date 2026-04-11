"""
main.py
-------
Pipeline entry point for P4: Global Equity Market Dashboard.

Usage:
    python main.py              # fetch data + attempt to open Power BI
    python main.py --no-pbix    # fetch data only (headless / CI)
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

from fetch_data import fetch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

PBIX_PATH = Path("dashboard.pbix")


def open_pbix(path: Path) -> None:
    """Open a .pbix file with the OS default handler (Power BI Desktop)."""
    if not path.exists():
        log.warning("dashboard.pbix not found at %s", path.resolve())
        log.warning("Open Power BI manually and load data/heatmap_data.csv")
        return

    if sys.platform == "win32":
        os.startfile(str(path))
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        log.info("Linux detected — open %s manually in Power BI Desktop.", path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="P4 Global Market Heatmap — data pipeline"
    )
    parser.add_argument(
        "--no-pbix",
        action="store_true",
        help="Skip opening Power BI after data fetch (useful for headless runs).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log.info("=" * 52)
    log.info("  P4: Global Market Heatmap — Data Pipeline")
    log.info("=" * 52)

    log.info("[1/2] Fetching live data and computing KPIs …")
    fetch()

    if not args.no_pbix:
        log.info("[2/2] Opening Power BI dashboard …")
        open_pbix(PBIX_PATH)

    log.info("Pipeline complete. CSV written to data/heatmap_data.csv")


if __name__ == "__main__":
    main()