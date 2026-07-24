"""
engine.py

Generic event-driven backtest engine.
"""

import pandas as pd


class BacktestEngine:

    def __init__(
        self,
        strategy,
        initial_capital,
        commission=0.0,
        slippage=0.0,
        risk_per_trade=0.01,
    ):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.risk_per_trade = risk_per_trade

    def run(self, df):

        df = self.strategy.prepare_data(df.copy())

        capital = self.initial_capital

        position = False
        units = 0.0

        entry_price = 0.0
        entry_time = None

        stop_price = 0.0
        highest_price = 0.0

        trail_active = False
        entry_atr = 0.0

        trades = []
        stop_trace = []

        current_trade_id = -1

        for i in range(len(df) - 1):

            row = df.iloc[i]
            next_row = df.iloc[i + 1]

            next_open = next_row["open"]
            next_time = next_row["open_time"]

            # ==================================================
            # ENTRY
            # ==================================================

            if (not position) and row["long_signal"]:

                current_trade_id += 1

                entry_price = next_open * (
                    1
                    + self.commission
                    + self.slippage
                )

                entry_atr = row["atr"]

                stop_price = (
                    entry_price
                    - self.strategy.atr_multiple
                    * entry_atr
                )

                highest_price = entry_price

                trail_active = False

                risk_amount = (
                    capital
                    * self.risk_per_trade
                )

                risk_per_unit = (
                    entry_price
                    - stop_price
                )

                units = (
                    risk_amount / risk_per_unit
                    if risk_per_unit > 0
                    else 0
                )

                entry_time = next_time

                position = True

            # ==================================================
            # POSITION MANAGEMENT
            # ==================================================

            elif position:

                highest_price = max(
                    highest_price,
                    row["high"],
                )

                if (
                    (not trail_active)
                    and (
                        highest_price
                        >= entry_price
                        + self.strategy.trail_start_atr
                        * entry_atr
                    )
                ):
                    trail_active = True

                if trail_active:

                    candidate = (
                        highest_price
                        - self.strategy.atr_multiple
                        * row["atr"]
                    )

                    stop_price = max(
                        stop_price,
                        candidate,
                    )

                stop_trace.append(
                    {
                        "trade_id": current_trade_id,
                        "time": row["open_time"],
                        "stop": stop_price,
                    }
                )

                exit_trade = False
                                # ---------------- EXIT CONDITIONS ----------------

                if row["low"] <= stop_price:

                    exit_price = stop_price
                    exit_trade = True                

                # ---------------- CLOSE TRADE ----------------

                if exit_trade:

                    pnl = units * (
                        exit_price
                        - entry_price
                    )

                    capital += pnl

                    trades.append(
                        {
                            "trade_id": current_trade_id,
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

                    entry_price = 0.0
                    entry_time = None

                    stop_price = 0.0
                    highest_price = 0.0

                    trail_active = False
                    entry_atr = 0.0

        return (
            pd.DataFrame(trades),
            pd.DataFrame(stop_trace),
        )