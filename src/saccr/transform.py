"""Trade-level features: hedging sets, factors, and per-trade AddOn."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import DELTA_MAP, SUPERVISORY_FACTORS


def make_hedging_set(row: pd.Series) -> str:
    """Assign hedging set label by asset class (IR, FX, credit, equity, commodity conventions)."""
    asset = row["Asset Class"]

    if asset == "Interest Rate":
        return f"{row['Base Currency']}_{row['Maturity Bucket']}"

    if asset == "FX":
        return f"{row['Trade Leg 1 Currency']}/{row['Trade Leg 2 Currency']}"

    if asset == "Credit":
        return str(row["Underlying Entity Name"])

    if asset == "Equity":
        return str(row["Underlying Entity Name"])

    if asset == "Commodity":
        return str(row["Sub Class"])

    return "Other"


def enrich_trades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build working frame with maturity bucket, hedging set, delta, maturity factor,
    supervisory factor, and trade-level Add-on.
    """
    df_work = df.copy()

    df_work["Maturity Days"] = (
        pd.to_datetime(df_work["Maturity Date"]) - pd.to_datetime(df_work["COB Date"])
    ).dt.days

    df_work["Maturity Bucket"] = np.select(
        [
            df_work["Maturity Days"] < 365,
            (df_work["Maturity Days"] >= 365) & (df_work["Maturity Days"] <= 365 * 5),
            df_work["Maturity Days"] > 365 * 5,
        ],
        ["<1Y", "1Y-5Y", ">5Y"],
        default="Unknown",
    )

    df_work["Hedging Set"] = df_work.apply(make_hedging_set, axis=1)
    df_work["Adjusted Notional"] = df_work["Base Notional"]
    df_work["Delta"] = df_work["Buy/Sell Indicator"].map(DELTA_MAP)

    df_work = df_work[df_work["Maturity Days"] > 0].copy()
    df_work["Maturity Factor"] = np.sqrt((df_work["Maturity Days"] / 365).clip(upper=1))

    df_work["Supervisory Factor"] = df_work["Asset Class"].map(SUPERVISORY_FACTORS)

    df_work["AddOn"] = (
        df_work["Adjusted Notional"]
        * df_work["Delta"]
        * df_work["Maturity Factor"]
        * df_work["Supervisory Factor"]
    )

    return df_work
