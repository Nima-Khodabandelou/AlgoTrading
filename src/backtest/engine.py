"""
engine.py

Generic event-driven backtest engine.

Responsibilities
----------------
- Execute strategy signals
- Apply commission and slippage
- Support ATR stop-loss
- Record completed trades
"""

import pandas as pd


class BacktestEngine:

    def __init__(
        self,
        strategy,
        initial_capital,
        commission=0.0,
        slippage=0.0,
    ):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

    def run(self, df):

        df = self.strategy.prepare_data(df.copy())

        capital = self.initial_capital

        position = False
        units = 0.0

        entry_price = 0.0
        entry_time = None
        stop_price = None

        trades = []

        for i in range(len(df) - 1):

            row = df.iloc[i]

            next_open = df.iloc[i + 1]["open"]
            next_time = df.iloc[i + 1]["open_time"]

            # ---------------- Entry ----------------

            if (not position) and row["long_signal"]:

                entry_price = next_open * (
                    1 + self.commission + self.slippage
                )

                stop_price = (
                    entry_price
                    - self.strategy.atr_multiple * row["atr"]
                )

                entry_time = next_time
                units = capital / entry_price
                position = True

            # ---------------- Exit -----------------

            elif position:

                exit_trade = False

                if row["low"] <= stop_price:

                    exit_price = stop_price
                    exit_trade = True

                elif row["short_signal"]:

                    exit_price = next_open * (
                        1 - self.commission - self.slippage
                    )

                    exit_trade = True

                if exit_trade:

                    pnl = units * (exit_price - entry_price)

                    capital += pnl

                    trades.append(
                        {
                            "entry_time": entry_time,
                            "exit_time": next_time,
                            "entry_price": entry_price,
                            "exit_price": exit_price,
                            "pnl": pnl,
                            "capital": capital,
                        }
                    )

                    position = False
                    units = 0.0
                    stop_price = None

        # Close remaining position
        if position:

            exit_price = (
                df.iloc[-1]["close"]
                * (1 - self.commission - self.slippage)
            )

            pnl = units * (exit_price - entry_price)

            capital += pnl

            trades.append(
                {
                    "entry_time": entry_time,
                    "exit_time": df.iloc[-1]["open_time"],
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                    "capital": capital,
                }
            )

        return pd.DataFrame(trades)