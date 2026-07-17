"""
breakout.py

Purpose
-------
Implementation of the 20-period breakout strategy.

Trading Rules
-------------
Entry
-----
Buy when a breakout long signal is True.

Exit
----
Exit when a breakout short signal is True.

Notes
-----
The strategy itself does not execute trades.
It only answers two questions:

1. Should we enter?
2. Should we exit?

The BacktestEngine handles:
- capital
- position sizing
- PnL
- trade execution

This separation allows the same engine to run any strategy.
"""

import pandas as pd

from src.strategies.base import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """
    20-period breakout strategy.
    """

    def __init__(self):
        """
        No parameters yet.

        Future examples
        ---------------
        lookback=20
        stop_loss=0.03
        take_profit=0.08
        """
        pass

    def entry_signal(
        self,
        row: pd.Series,
    ) -> bool:
        """
        Return True when a long entry should occur.
        """

        return bool(row["long_signal"])

    def exit_signal(
        self,
        row: pd.Series,
    ) -> bool:
        """
        Return True when the current long position
        should be closed.
        """

        return bool(row["short_signal"])