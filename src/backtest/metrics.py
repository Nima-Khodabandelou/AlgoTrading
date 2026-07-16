"""
metrics.py

Purpose
-------
Computes and prints backtest performance statistics.
"""


def report(trades, initial_capital):

    if trades.empty:
        print("No trades.")
        return

    final_capital = trades.iloc[-1]["capital"]

    print()
    print("========== TRADE LOG ==========")
    print(trades)

    print()
    print(f"Trades       : {len(trades)}")
    print(f"Initial      : ${initial_capital:,.2f}")
    print(f"Final        : ${final_capital:,.2f}")
    print(f"Return       : {(final_capital / initial_capital - 1) * 100:.2f}%")