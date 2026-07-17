"""
metrics.py

Purpose
-------
Performance statistics for backtests.

This module is intentionally independent from the backtesting engine.
It only analyzes completed trades and prints summary statistics.

Input
-----
Trades DataFrame with columns:

- entry_time
- exit_time
- entry_price
- exit_price
- pnl
- capital

Future Improvements
-------------------
- Maximum drawdown
- Sharpe ratio
- Sortino ratio
- CAGR
- Calmar ratio
- Monthly returns
- Equity curve plotting
- Trade duration statistics
"""

import pandas as pd


def report(trades: pd.DataFrame, initial_capital: float) -> None:
    """
    Print a performance report.

    Parameters
    ----------
    trades : pd.DataFrame
        Completed trades.

    initial_capital : float
        Starting account balance.
    """

    if trades.empty:
        print("No trades.")
        return

    final_capital = trades["capital"].iloc[-1]

    winners = trades[trades["pnl"] > 0]
    losers = trades[trades["pnl"] < 0]

    total_trades = len(trades)
    win_rate = len(winners) / total_trades * 100

    gross_profit = winners["pnl"].sum()
    gross_loss = abs(losers["pnl"].sum())

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else float("inf")
    )

    average_win = (
        winners["pnl"].mean()
        if len(winners)
        else 0
    )

    average_loss = (
        losers["pnl"].mean()
        if len(losers)
        else 0
    )

    expectancy = trades["pnl"].mean()

    largest_win = trades["pnl"].max()
    largest_loss = trades["pnl"].min()

    total_return = (
        final_capital / initial_capital - 1
    ) * 100

    print()
    print("=" * 15, "PERFORMANCE", "=" * 15)

    print(f"Trades          : {total_trades}")
    print(f"Winners         : {len(winners)}")
    print(f"Losers          : {len(losers)}")
    print(f"Win Rate        : {win_rate:.2f}%")

    print()

    print(f"Gross Profit    : ${gross_profit:,.2f}")
    print(f"Gross Loss      : ${gross_loss:,.2f}")
    print(f"Profit Factor   : {profit_factor:.2f}")

    print()

    print(f"Average Win     : ${average_win:,.2f}")
    print(f"Average Loss    : ${average_loss:,.2f}")
    print(f"Expectancy      : ${expectancy:,.2f}")

    print()

    print(f"Largest Win     : ${largest_win:,.2f}")
    print(f"Largest Loss    : ${largest_loss:,.2f}")

    print()

    print(f"Initial Capital : ${initial_capital:,.2f}")
    print(f"Final Capital   : ${final_capital:,.2f}")
    print(f"Return          : {total_return:.2f}%")