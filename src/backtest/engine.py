"""
engine.py

Generic event-driven backtest engine.

Features
--------
- Long-only execution
- Risk-based position sizing
- Commission & slippage
- ATR initial stop
- ATR trailing stop
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

            # -----------------------------
            # ENTRY
            # -----------------------------

            if (not position) and row["long_signal"]:

                entry_price = next_open * (
                    1 + self.commission + self.slippage
                )

                stop_price = (
                    entry_price
                    - self.strategy.atr_multiple * row["atr"]
                )

                risk_per_unit = (
                    entry_price - stop_price
                )

                if (
                    pd.isna(risk_per_unit)
                    or risk_per_unit <= 0
                ):
                    continue

                risk_amount = (
                    capital
                    * self.strategy.risk_per_trade
                )

                units = (
                    risk_amount
                    / risk_per_unit
                )

                max_units = capital / entry_price
                units = min(units, max_units)

                entry_time = next_time
                position = True

            # -----------------------------
            # MANAGE OPEN POSITION
            # -----------------------------

            elif position:

                # ATR trailing stop
                new_stop = (
                    row["close"]
                    - self.strategy.atr_multiple
                    * row["atr"]
                )

                if (
                    not pd.isna(new_stop)
                    and new_stop > stop_price
                ):
                    stop_price = new_stop

                exit_trade = False
                
                # -----------------------------
                # EXIT CONDITIONS
                # -----------------------------

                if row["low"] <= stop_price:

                    exit_price = stop_price
                    exit_trade = True

                elif row["short_signal"]:

                    exit_price = next_open * (
                        1 - self.commission - self.slippage
                    )

                    exit_trade = True

                if exit_trade:

                    pnl = units * (
                        exit_price - entry_price
                    )

                    capital += pnl

                    trades.append(
                        {
                            "entry_time": entry_time,
                            "exit_time": next_time,
                            "entry_price": entry_price,
                            "exit_price": exit_price,
                            "units": units,
                            "pnl": pnl,
                            "capital": capital,
                        }
                    )

                    position = False
                    units = 0.0

                    entry_price = 0.0
                    entry_time = None
                    stop_price = None

        # -----------------------------
        # CLOSE LAST POSITION
        # -----------------------------

        if position:

            exit_price = (
                df.iloc[-1]["close"]
                * (1 - self.commission - self.slippage)
            )

            pnl = units * (
                exit_price - entry_price
            )

            capital += pnl

            trades.append(
                {
                    "entry_time": entry_time,
                    "exit_time": df.iloc[-1]["open_time"],
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "units": units,
                    "pnl": pnl,
                    "capital": capital,
                }
            )

        return pd.DataFrame(trades)