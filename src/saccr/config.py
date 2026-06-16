"""Supervisory parameters and core trade column schema for the SA-CCR exposure pipeline."""

from __future__ import annotations

from typing import Final

CORE_COLUMNS: Final[tuple[str, ...]] = (
    "COB Date",
    "Counterparty ID",
    "Netting Set ID",
    "Ticket Number",
    "Trade Type",
    "Asset Class",
    "Base Notional",
    "Margined/ Unmargined",
    "Buy/Sell Indicator",
    "Maturity Date",
    "MtM",
)

SUPERVISORY_FACTORS: Final[dict[str, float]] = {
    "Interest Rate": 0.005,
    "FX": 0.04,
    "Credit": 0.0054,
    "Equity": 0.32,
    "Commodity": 0.18,
}

DELTA_MAP: Final[dict[str, int]] = {"B": 1, "S": -1}

EAD_ALPHA: Final[float] = 1.4
DEFAULT_MULTIPLIER: Final[float] = 1.0
DEFAULT_RISK_WEIGHT: Final[float] = 1.0
