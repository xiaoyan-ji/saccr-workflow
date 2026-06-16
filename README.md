# SA-CCR Counterparty Credit Risk Exposure Workflow

Python pipeline from OTC-style trade data in Excel to **Add-on**, **PFE**, **replacement cost (RC)**, **EAD**, and **RWA** at netting-set and counterparty level, following **BCBS SA-CCR** asset-class conventions and grouping logic.

## Cross-role relevance

This project is a **counterparty credit / regulatory exposure** pipeline (SA-CCR-style)—**not** a fraud model, AML engine, or payment-default scorecard. If you are recruiting for **Fraud Analytics**, **Payment Risk**, or **Transaction Risk**, the transferable pieces are:

- **Transaction-level data engineering**: ingest row-level inputs, enforce a **column schema**, and emit reproducible artifacts (CSV / XLSX / HTML).
- **Layered aggregation & monitoring-style reporting**: roll metrics through **entity → portfolio bucket → category** hierarchies (here: counterparty → netting set → asset class)—similar in shape to **merchant / channel / product** rollups used in payment and transaction monitoring.
- **Operational hardening**: CLI batch runs, versioned dependencies, **pytest** + **CI** for regression checks—patterns typical of **production risk and control** workflows.

Point recruiters to this repo for **CCR / capital markets / portfolio credit** depth; use your resume or cover letter to map the above to specific fraud, payment, or transaction-monitoring contexts you have worked on.

## Project structure

```text
.
├── data/                      # Input workbooks (see data/README.md)
├── notebook/                  # Jupyter walkthrough (exploratory + charts)
├── outputs/                   # Sample run artifacts (CSV/XLSX/HTML/PNG); PDFs gitignored (see outputs/README.md)
├── scripts/                   # CLI entry points (batch run + exports)
│   └── run_saccr.py
├── src/
│   └── saccr/                 # Importable package: load → enrich → aggregate → EAD/RWA
│       ├── __init__.py
│       ├── aggregate.py
│       ├── config.py
│       ├── io.py
│       ├── pipeline.py
│       ├── plots.py
│       ├── reporting.py       # summary.xlsx + report.html writers
│       └── transform.py
├── tests/                     # pytest regression checks
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions: pytest on push/PR to main
├── LICENSE                    # MIT
├── pyproject.toml             # Package metadata + optional [dev] extras
├── requirements.txt
└── README.md
```

## What you need

- **Python 3.10+** installed (3.11 is fine)
- Sample data in this repo: `data/SA-CCR Sample IR Calculations.xlsx`

## Install dependencies

Open a terminal in the **project root** (the folder that contains `requirements.txt`), then run:

```bash
pip install -r requirements.txt
```

## How to run

### Notebook

1. Open `notebook/CCR Project.ipynb` in Cursor or Jupyter.
2. **Select Kernel** → **Python Environments** → choose Python 3.
3. Run all code cells **from top to bottom**.
4. If the last cells show tables and an RWA bar chart, the run succeeded.

### Command line (`scripts/`)

From the **repository root** (where `requirements.txt` lives):

```bash
python scripts/run_saccr.py
```

Optional arguments:

```bash
python scripts/run_saccr.py --input "data/SA-CCR Sample IR Calculations.xlsx" --output-dir outputs/run1 --plot
```

Writes:

- `summary_by_counterparty.csv`, `summary_by_asset_class.csv`, `netting_set_ead.csv`
- `summary.xlsx` (multi-sheet workbook)
- `report.html` (tables; include chart if you pass `--plot`)
- `rwa_by_counterparty.png` when using `--plot`

A **sample run** of these files (except PDF) is committed under `outputs/` so others can view results without executing the pipeline.

### Install package (optional)

```bash
pip install -e .
```

Then you can `import saccr` from any working directory without editing `PYTHONPATH`.

## Tests

Install dev dependencies (includes `pytest`), then run from the **repository root**:

```bash
pip install -e ".[dev]"
pytest
```

`pyproject.toml` sets `pythonpath = ["src"]` for pytest, so `import saccr` works without manual `PYTHONPATH`.

On GitHub, **Actions** runs the same test suite on every push to `main` (see `.github/workflows/ci.yml`).

## Data

- File: `data/SA-CCR Sample IR Calculations.xlsx`
- Sheet used: `Data_Input`
- Details: [`data/README.md`](data/README.md)

## Scope

This repository implements a **focused subset** of the SA-CCR exposure chain (trade-level inputs → hedging sets → Add-on aggregation → PFE/RC → EAD → RWA summaries), with **configurable supervisory factors** and a **reproducible** notebook plus importable `src/` package. It is intended for **portfolio analytics, methodology prototyping, and documented end-to-end risk metrics**—not a substitute for a bank’s internal capital engine, model governance, or supervisory filing requirements.

## Sample data reference

Example workbook style: [rohank170403/SA-CCR](https://github.com/rohank170403/SA-CCR)

## License

This project is licensed under the [MIT License](LICENSE).