"""
base.py

Defines the interface that every trading strategy must implement.

A strategy is responsible for

- computing its own indicators
- generating entry/exit signals
- deciding whether to enter
- deciding whether to exit

The BacktestEngine never knows how the signals are produced.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Base class for all trading strategies.
    """

    @abstractmethod
    def prepare_data(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Compute indicators and signals.

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        DataFrame
            DataFrame containing every column required by
            this strategy.
        """
        pass

    @abstractmethod
    def entry_signal(
        self,
        row: pd.Series,
    ) -> bool:
        """
        Return True when a long position should be opened.
        """
        pass

    @abstractmethod
    def exit_signal(
        self,
        row: pd.Series,
    ) -> bool:
        """
        Return True when a long position should be closed.
        """
        pass