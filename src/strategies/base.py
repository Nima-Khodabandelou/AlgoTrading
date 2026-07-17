"""
base.py

Purpose
-------
Defines the abstract interface for every trading strategy.

Why?
----
The backtesting engine should never know whether it is running
a breakout strategy, moving-average crossover, RSI strategy,
or anything else.

Every strategy must implement the same interface.

Future strategies
-----------------
- Breakout
- Moving Average
- RSI
- MACD
- Bollinger Bands
- Mean Reversion
- Machine Learning
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Base class for every trading strategy.
    """

    @abstractmethod
    def entry_signal(
        self,
        row: pd.Series,
    ) -> bool:
        """
        Return True if a long position should be opened.
        """
        pass

    @abstractmethod
    def exit_signal(
        self,
        row: pd.Series,
    ) -> bool:
        """
        Return True if the current position should be closed.
        """
        pass