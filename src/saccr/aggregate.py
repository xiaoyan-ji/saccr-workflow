"""Netting-set and counterparty-level aggregation: AddOn, PFE, RC, EAD, RWA."""

from __future__ import annotations

import pandas as pd

from .config import DEFAULT_MULTIPLIER, DEFAULT_RISK_WEIGHT, EAD_ALPHA


def addon_aggregates(df_work: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (by hedging set, by asset class, by netting set) AddOn exposure tables."""
    addon_by_hedging_set = (
        df_work.groupby(["Counterparty ID", "Netting Set ID", "Asset Class", "Hedging Set"])["AddOn"]
        .sum()
        .reset_index()
    )
    addon_by_hedging_set["AddOn Exposure"] = addon_by_hedging_set["AddOn"].abs()

    addon_by_asset_class = (
        addon_by_hedging_set.groupby(["Counterparty ID", "Netting Set ID", "Asset Class"])["AddOn Exposure"]
        .sum()
        .reset_index()
    )

    addon_by_netting_set = (
        addon_by_asset_class.groupby(["Counterparty ID", "Netting Set ID"])["AddOn Exposure"]
        .sum()
        .reset_index()
    )

    return addon_by_hedging_set, addon_by_asset_class, addon_by_netting_set


def pfe_by_netting_set(addon_by_netting_set: pd.DataFrame, *, multiplier: float = DEFAULT_MULTIPLIER) -> pd.DataFrame:
    out = addon_by_netting_set.copy()
    out["Multiplier"] = multiplier
    out["PFE"] = out["Multiplier"] * out["AddOn Exposure"]
    return out


def rc_by_netting_set(df_work: pd.DataFrame) -> pd.DataFrame:
    rc = (
        df_work.groupby(["Counterparty ID", "Netting Set ID"])["MtM"].sum().reset_index()
    )
    rc["RC"] = rc["MtM"].clip(lower=0)
    return rc


def ead_and_rwa(
    addon_with_pfe: pd.DataFrame,
    rc_table: pd.DataFrame,
    *,
    risk_weight: float = DEFAULT_RISK_WEIGHT,
) -> pd.DataFrame:
    ead_input = addon_with_pfe.merge(
        rc_table[["Counterparty ID", "Netting Set ID", "RC"]],
        on=["Counterparty ID", "Netting Set ID"],
        how="left",
    )
    ead_input["EAD"] = EAD_ALPHA * (ead_input["RC"] + ead_input["PFE"])
    ead_input["Risk Weight"] = risk_weight
    ead_input["RWA"] = ead_input["EAD"] * ead_input["Risk Weight"]
    return ead_input


def summary_counterparty(ead_input: pd.DataFrame) -> pd.DataFrame:
    return (
        ead_input.groupby("Counterparty ID")[["PFE", "RC", "EAD", "RWA"]]
        .sum()
        .reset_index()
    )


def summary_asset_class(addon_by_asset_class: pd.DataFrame) -> pd.DataFrame:
    return (
        addon_by_asset_class.groupby("Asset Class")["AddOn Exposure"]
        .sum()
        .reset_index()
    )
