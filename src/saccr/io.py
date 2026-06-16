"""Load trade input from Excel."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_trades(
    excel_path: str | Path,
    *,
    sheet_name: str = "Data_Input",
    header: int = 8,
) -> pd.DataFrame:
    """Read the main trade sheet and drop all-empty columns."""
    path = Path(excel_path)
    df = pd.read_excel(path, sheet_name=sheet_name, header=header)
    return df.dropna(axis=1, how="all")
