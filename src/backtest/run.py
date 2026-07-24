"""
run.py

Run a backtest.
"""

from src.backtest.engine import BacktestEngine
from src.config.settings import (
    TRAIN_START,
    TRAIN_END,
    INITIAL_CAPITAL,
    COMMISSION,
    SLIPPAGE,
)
from src.data.loader import load_data
from src.strategies.breakout import BreakoutStrategy
from src.visualization.plot_trades import plot_trades


def main():

    df = load_data(
        start=TRAIN_START,
        end=TRAIN_END,
    )

    strategy = BreakoutStrategy()

    engine = BacktestEngine(
        strategy=strategy,
        initial_capital=INITIAL_CAPITAL,
        commission=COMMISSION,
        slippage=SLIPPAGE,
        risk_per_trade=0.01,
    )

    trades, stop_trace = engine.run(df)

    print("\n========== TRADE LOG ==========\n")
    print(trades)

    print("\n=============== PERFORMANCE ===============")

    print(f"Trades          : {len(trades)}")

    if len(trades):

        final_capital = trades.iloc[-1]["capital"]
        total_return = (
            (final_capital - INITIAL_CAPITAL)
            / INITIAL_CAPITAL
            * 100
        )

        print(
            f"Initial Capital : ${INITIAL_CAPITAL:,.2f}"
        )
        print(
            f"Final Capital   : ${final_capital:,.2f}"
        )
        print(
            f"Return          : {total_return:.2f}%"
        )

    plot_trades(
        df=df,
        trades=trades,
        stop_trace=stop_trace,
    )


if __name__ == "__main__":
    main()