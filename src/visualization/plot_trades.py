"""
plot_trades.py
"""

from pathlib import Path

import plotly.graph_objects as go


def plot_trades(df, trades, stop_trace):

    fig = go.Figure()

    # ---------------- Candles ----------------

    fig.add_trace(
        go.Candlestick(
            x=df["open_time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price",
        )
    )

    # ---------------- Entries ----------------

    fig.add_trace(
        go.Scatter(
            x=trades["entry_time"],
            y=trades["entry_price"],
            mode="markers",
            name="Entry",
            marker=dict(
                symbol="triangle-up",
                size=18,
                color="blue",
                line=dict(color="black", width=1),
            ),
        )
    )

    # ---------------- Exits ----------------

    fig.add_trace(
        go.Scatter(
            x=trades["exit_time"],
            y=trades["exit_price"],
            mode="markers",
            name="Exit",
            marker=dict(
                symbol="triangle-down",
                size=18,
                color="lime",
                line=dict(color="black", width=1),
            ),
        )
    )

    # ---------------- Trailing Stops ----------------

    if not stop_trace.empty:

        for _, group in stop_trace.groupby("trade_id"):

            fig.add_trace(
                go.Scatter(
                    x=group["time"],
                    y=group["stop"],
                    mode="lines",
                    showlegend=False,
                    line=dict(
                        color="red",
                        width=2,
                    ),
                    hovertemplate="Stop: %{y:.2f}<extra></extra>",
                )
            )

    fig.update_layout(
        template="plotly_dark",
        width=1800,
        height=900,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20,
        ),
        bargap=0,
        xaxis_rangeslider_visible=False,
    )

    fig.update_xaxes(
        type="category",
        showgrid=False,
    )

    Path("results").mkdir(exist_ok=True)

    fig.write_html(
        "results/trades.html",
        auto_open=True,
    )