"""
engine.py

Purpose
-------
Generic event-driven backtesting engine.

Responsibilities
----------------
- Execute trades
- Manage capital
- Manage positions
- Calculate PnL
- Record completed trades

Design
------
The engine is strategy-agnostic.

It never checks:
    row["long_signal"]
    row["short_signal"]

Instead, it asks the supplied strategy:

    strategy.entry_signal(row)
    strategy.exit_signal(row)

Any strategy implementing BaseStrategy can therefore be used
without modifying this engine.

Future Improvements
-------------------
- Commission
- Slippage
- Short selling
- Stop-loss
- Take-profit
- Position sizing
- Multiple simultaneous positions
- Portfolio support
"""

import pandas as pd


class BacktestEngine:
    """
    Generic event-driven backtesting engine.
    """

    def __init__(
        self,
        strategy,
        initial_capital: float,
    ):
        self.strategy = strategy
        self.initial_capital = initial_capital

    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute the supplied strategy on the dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            Price data together with any features/signals required
            by the selected strategy.

        Returns
        -------
        pandas.DataFrame
            Completed trades.
        """

        capital = self.initial_capital

        position = False
        units = 0.0

        entry_price = 0.0
        entry_time = None

        trades = []

        # Need next candle open for realistic execution
        for i in range(len(df) - 1):

            row = df.iloc[i]

            next_row = df.iloc[i + 1]

            next_open = next_row["open"]
            next_time = next_row["open_time"]

            # -----------------------------
            # Entry
            # -----------------------------
            if (
                not position
                and self.strategy.entry_signal(row)
            ):

                entry_price = next_open
                entry_time = next_time

                units = capital / entry_price

                position = True

            # -----------------------------
            # Exit
            # -----------------------------
            elif (
                position
                and self.strategy.exit_signal(row)
            ):

                exit_price = next_open
                exit_time = next_time

                pnl = units * (
                    exit_price - entry_price
                )

                capital += pnl

                trades.append(
                    {
                        "entry_time": entry_time,
                        "exit_time": exit_time,
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "pnl": pnl,
                        "capital": capital,
                    }
                )

                position = False
                units = 0.0

        # ---------------------------------
        # Close remaining position
        # ---------------------------------

        if position:

            exit_price = df.iloc[-1]["close"]
            exit_time = df.iloc[-1]["open_time"]

            pnl = units * (
                exit_price - entry_price
            )

            capital += pnl

            trades.append(
                {
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                    "capital": capital,
                }
            )

        return pd.DataFrame(trades)