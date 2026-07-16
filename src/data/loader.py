"""
loader.py
=========

Centralized data loading utilities.

Responsibilities
----------------
- Load processed parquet datasets.
- Optionally filter by date.
- Return a clean pandas DataFrame.

All other modules should import this loader instead of reading files
directly.
"""

from pathlib import Path

import pandas as pd

from src.config.settings import (
    DATA_DIR,
    SYMBOL,
    INTERVAL,
)


def load_data(
    symbol: str = SYMBOL,
    interval: str = INTERVAL,
    start=None,
    end=None,
) -> pd.DataFrame:
    """
    Load a processed parquet dataset.

    Parameters
    ----------
    symbol : str
        Trading symbol.

    interval : str
        Candle interval.

    start : str or Timestamp, optional
        Start date.

    end : str or Timestamp, optional
        End date.

    Returns
    -------
    pandas.DataFrame
    """

    file = DATA_DIR / "parquet" / f"{symbol}_{interval}.parquet"

    df = pd.read_parquet(file)

    df = df.sort_values("open_time").reset_index(drop=True)

    if start is not None:
        df = df[df["open_time"] >= pd.Timestamp(start, tz="UTC")]

    if end is not None:
        df = df[df["open_time"] <= pd.Timestamp(end, tz="UTC")]

    return df.reset_index(drop=True)