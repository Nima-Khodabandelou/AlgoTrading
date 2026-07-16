"""
portfolio.py

Purpose
-------
Stores the current portfolio state used by the backtesting engine.

The portfolio tracks:
- Current capital
- Position status
- Number of units held
- Entry price
- Entry time

The engine updates this object during simulation.
"""

from dataclasses import dataclass
import pandas as pd


@dataclass
class Portfolio:

    initial_capital: float = 10_000.0

    capital: float = 10_000.0

    position: bool = False

    units: float = 0.0

    entry_price: float = 0.0

    entry_time: pd.Timestamp | None = None