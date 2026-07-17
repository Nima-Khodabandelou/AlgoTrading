"""
base.py

Abstract base class for every trading strategy.

Every strategy must implement generate_signals().
"""

from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    @abstractmethod
    def generate_signals(self, df):
        """
        Returns a DataFrame containing trading signals.
        """
        pass