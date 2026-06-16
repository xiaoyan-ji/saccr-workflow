#!/usr/bin/env python3
"""
Command-line entry point for the SA-CCR exposure pipeline.

Run from the repository root (recommended):

    python scripts/run_saccr.py
    python scripts/run_saccr.py --input data/your_trades.xlsx --output-dir outputs/latest

Writes CSVs, ``summary.xlsx``, ``report.html``, and optionally ``rwa_by_counterparty.png`` (``--plot``).

Adds ``src/`` to ``sys.path`` so you do not need ``pip install -e .`` first.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _ensure_src_on_path() -> None:
    src = _repo_root() / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def main() -> int:
    root = _repo_root()
    default_input = root / "data" / "SA-CCR Sample IR Calculations.xlsx"

    parser = argparse.ArgumentParser(
        description="Run SA-CCR-style exposure pipeline (Excel → EAD / RWA tables).",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help=f"Path to input Excel (default: {default_input})",
    )
    parser.add_argument(
        "--sheet",
        default="Data_Input",
        help="Excel sheet name (default: Data_Input)",
    )
    parser.add_argument(
        "--header",
        type=int,
        default=8,
        help="Header row index for pd.read_excel (default: 8)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs",
        help="Directory for CSV exports (default: ./outputs)",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Save RWA-by-counterparty bar chart as PNG in output-dir",
    )
    args = parser.parse_args()

    excel_path = args.input
    if not excel_path.is_file():
        print(f"Error: input file not found: {excel_path}", file=sys.stderr)
        return 1

    _ensure_src_on_path()
    from saccr.pipeline import run_saccr
    from saccr.plots import rwa_by_counterparty_figure
    from saccr.reporting import write_excel_summary, write_html_report

    out = run_saccr(excel_path, sheet_name=args.sheet, header=args.header)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    out.summary_by_counterparty.to_csv(
        args.output_dir / "summary_by_counterparty.csv", index=False
    )
    out.summary_by_asset_class.to_csv(
        args.output_dir / "summary_by_asset_class.csv", index=False
    )
    out.netting_set_ead.to_csv(args.output_dir / "netting_set_ead.csv", index=False)

    plot_path = args.output_dir / "rwa_by_counterparty.png"
    if args.plot:
        import matplotlib.pyplot as plt

        fig = rwa_by_counterparty_figure(out.summary_by_counterparty)
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)
        print(f"Wrote plot: {plot_path.resolve()}")

    xlsx_path = args.output_dir / "summary.xlsx"
    write_excel_summary(xlsx_path, out)
    print(f"Wrote workbook: {xlsx_path.resolve()}")

    html_path = args.output_dir / "report.html"
    write_html_report(
        html_path,
        out,
        plot_path=plot_path if args.plot else None,
    )
    print(f"Wrote report: {html_path.resolve()}")

    print(f"Input:  {excel_path.resolve()}")
    print(f"Trades (enriched rows): {len(out.trades_enriched)}")
    print(f"Netting sets: {len(out.netting_set_ead)}")
    print(f"Artifacts under: {args.output_dir.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
