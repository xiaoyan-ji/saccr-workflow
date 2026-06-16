"""Reporting charts (matplotlib)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def rwa_by_counterparty_figure(summary_by_counterparty: pd.DataFrame) -> "Figure":
    """Bar chart of total RWA by counterparty."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary_by_counterparty["Counterparty ID"], summary_by_counterparty["RWA"])
    ax.set_xlabel("Counterparty ID")
    ax.set_ylabel("Total RWA")
    ax.set_title("RWA by Counterparty")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig
