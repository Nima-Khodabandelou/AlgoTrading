"""
loader.py
"""

import pandas as pd

from src.config.settings import (
    DATA_DIR,
    SYMBOL,
    TIMEFRAME,
)


def load_data(
    symbol: str = SYMBOL,
    timeframe: str = TIMEFRAME,
    start=None,
    end=None,
):

    file = (
        DATA_DIR
        / "parquet"
        / f"{symbol}_{timeframe}.parquet"
    )

    df = pd.read_parquet(file)

    df = (
        df.sort_values("open_time")
        .reset_index(drop=True)
    )

    if start is not None:
        df = df[
            df["open_time"] >= pd.Timestamp(
                start,
                tz="UTC",
            )
        ]

    if end is not None:
        df = df[
            df["open_time"] <= pd.Timestamp(
                end,
                tz="UTC",
            )
        ]

    return df.reset_index(drop=True)