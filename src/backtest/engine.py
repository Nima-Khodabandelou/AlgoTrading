"""
engine.py
=========

Backtest execution engine.

Responsibilities
----------------
- Iterate over candles
- Query the strategy
- Send orders to the portfolio

The engine knows nothing about indicators or PnL calculations.
"""

from __future__ import annotations

from src.backtest.portfolio import Portfolio


class BacktestEngine:

    def __init__(self, strategy, initial_capital):

        self.strategy = strategy
        self.portfolio = Portfolio(initial_capital)

    # ---------------------------------------------------------

    def run(self, df):

        signals = self.strategy.generate_signals(df)

        for i in range(len(signals) - 1):

            row = signals.iloc[i]

            next_open = signals.iloc[i + 1]["open"]
            next_time = signals.iloc[i + 1]["open_time"]

            # Entry

            if (not self.portfolio.position) and row["long_signal"]:

                self.portfolio.buy(next_open, next_time)

            # Exit

            elif self.portfolio.position and row["short_signal"]:

                self.portfolio.sell(next_open, next_time)

        # Close remaining position

        self.portfolio.close_final(
            signals.iloc[-1]["close"],
            signals.iloc[-1]["open_time"],
        )

        return self.portfolio.trade_log()