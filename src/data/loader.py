from pathlib import Path
import pandas as pd


DATA_DIR = Path("data/parquet")


def load_data(
    symbol: str,
    interval: str,
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    """
    Load OHLCV data from a Parquet file.
    """

    file = DATA_DIR / f"{symbol}_{interval}.parquet"

    if not file.exists():
        raise FileNotFoundError(file)

    df = pd.read_parquet(file)

    if start is not None:
        df = df[df["open_time"] >= pd.Timestamp(start, tz="UTC")]

    if end is not None:
        df = df[df["open_time"] <= pd.Timestamp(end, tz="UTC")]

    return df.reset_index(drop=True)


if __name__ == "__main__":
    df = load_data(
        symbol="ETHUSDT",
        interval="1h",
        start="2024-01-01",
        end="2024-12-31",
    )

    print(df.head())
    print(df.tail())
    print(f"Rows: {len(df)}")