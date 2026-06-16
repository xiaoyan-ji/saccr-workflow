"""Export multi-sheet Excel and standalone HTML summaries."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd

from .pipeline import SaccrOutputs


def write_excel_summary(path: Path, out: SaccrOutputs) -> None:
    """Write ``summary.xlsx`` with key pipeline tables on separate sheets."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        out.summary_by_counterparty.to_excel(writer, sheet_name="Summary_CP", index=False)
        out.summary_by_asset_class.to_excel(writer, sheet_name="Summary_Asset", index=False)
        out.netting_set_ead.to_excel(writer, sheet_name="NettingSet_EAD", index=False)
        out.addon_by_asset_class.to_excel(writer, sheet_name="Addon_Asset", index=False)
        out.addon_by_hedging_set.to_excel(writer, sheet_name="Addon_Hedge", index=False)
        out.trades_enriched.to_excel(writer, sheet_name="Trades_Enriched", index=False)


def write_html_report(
    path: Path,
    out: SaccrOutputs,
    *,
    plot_path: Path | None = None,
    max_rows_per_table: int = 500,
) -> None:
    """
    Write ``report.html`` with embedded tables (and optional chart image).

    ``plot_path`` should point to an existing PNG (e.g. from ``--plot``); if given,
    the HTML references it by **filename** so opening the HTML beside the PNG works.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    def section(title: str, df: pd.DataFrame) -> str:
        safe_title = html.escape(title)
        n = len(df)
        head = df.head(max_rows_per_table)
        table_html = head.to_html(index=False, border=0, classes="df", escape=True)
        if n > max_rows_per_table:
            note = f"<p><em>Showing first {max_rows_per_table} of {n} rows.</em></p>"
        else:
            note = ""
        return f"<h2>{safe_title}</h2>{note}{table_html}"

    blocks: list[str] = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8">',
        "<title>SA-CCR exposure run</title>",
        "<style>body{font-family:system-ui,sans-serif;margin:1.25rem;line-height:1.4}",
        "table.df{border-collapse:collapse;margin:0.5rem 0;font-size:14px}",
        "table.df th,table.df td{border:1px solid #ccc;padding:4px 8px;text-align:right}",
        "table.df th{text-align:center;background:#f5f5f5} h1{font-size:1.4rem}</style>",
        "</head><body>",
        "<h1>SA-CCR exposure run</h1>",
        section("Summary by counterparty", out.summary_by_counterparty),
        section("Summary by asset class", out.summary_by_asset_class),
        section("Netting set — PFE, RC, EAD, RWA", out.netting_set_ead),
        section("Add-on by asset class", out.addon_by_asset_class),
        section("Add-on by hedging set", out.addon_by_hedging_set),
        section("Trades (enriched)", out.trades_enriched),
    ]

    if plot_path is not None and plot_path.is_file():
        name = html.escape(plot_path.name)
        blocks.append(f'<h2>RWA by counterparty</h2><p><img src="{name}" alt="RWA chart" /></p>')

    blocks.append("</body></html>")
    path.write_text("\n".join(blocks), encoding="utf-8")
