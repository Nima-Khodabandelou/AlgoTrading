"""
Project-wide configuration.

All constants that are shared across modules should be defined here.
Avoid hardcoding values inside scripts whenever possible.
"""

from pathlib import Path

# ---------------------------------------------------------------------
# Trading
# ---------------------------------------------------------------------

SYMBOL = "ETHUSDT"
TIMEFRAME = "1h"

INITIAL_CAPITAL = 10_000.0
COMMISSION = 0.001      # 0.10%
SLIPPAGE = 0.0005       # 0.05%

# ---------------------------------------------------------------------
# Data split
# ---------------------------------------------------------------------

TRAIN_START = "2024-01-01"
TRAIN_END = "2025-01-01"

# ---------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
PARQUET_DIR = DATA_DIR / "parquet"
FEATURE_DIR = DATA_DIR / "features"
SIGNALS_DIR = DATA_DIR / "signals"
RESULT_DIR = PROJECT_ROOT / "results"