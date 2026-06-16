"""End-to-end run: Excel -> enriched trades -> EAD/RWA summaries."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .aggregate import (
    addon_aggregates,
    ead_and_rwa,
    pfe_by_netting_set,
    rc_by_netting_set,
    summary_asset_class,
    summary_counterparty,
)
from .config import CORE_COLUMNS
from .io import load_trades
from .transform import enrich_trades


@dataclass(frozen=True)
class SaccrOutputs:
    """Main tables produced by the exposure pipeline."""

    trades_raw: pd.DataFrame
    trades_core: pd.DataFrame
    trades_enriched: pd.DataFrame
    addon_by_hedging_set: pd.DataFrame
    addon_by_asset_class: pd.DataFrame
    addon_by_netting_set: pd.DataFrame
    netting_set_ead: pd.DataFrame
    summary_by_counterparty: pd.DataFrame
    summary_by_asset_class: pd.DataFrame


def run_saccr(
    excel_path: str | Path,
    *,
    sheet_name: str = "Data_Input",
    header: int = 8,
) -> SaccrOutputs:
    """
    Load Excel trade data, enrich features, aggregate Add-on exposure, and compute
    PFE, RC, EAD, and RWA through netting-set and counterparty summaries.
    """
    trades_raw = load_trades(excel_path, sheet_name=sheet_name, header=header)
    missing = [c for c in CORE_COLUMNS if c not in trades_raw.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    trades_core = trades_raw[list(CORE_COLUMNS)].copy()
    trades_enriched = enrich_trades(trades_raw)

    addon_hs, addon_ac, addon_ns = addon_aggregates(trades_enriched)
    addon_pfe = pfe_by_netting_set(addon_ns)
    rc = rc_by_netting_set(trades_enriched)
    netting_set_ead = ead_and_rwa(addon_pfe, rc)

    return SaccrOutputs(
        trades_raw=trades_raw,
        trades_core=trades_core,
        trades_enriched=trades_enriched,
        addon_by_hedging_set=addon_hs,
        addon_by_asset_class=addon_ac,
        addon_by_netting_set=addon_ns,
        netting_set_ead=netting_set_ead,
        summary_by_counterparty=summary_counterparty(netting_set_ead),
        summary_by_asset_class=summary_asset_class(addon_ac),
    )
