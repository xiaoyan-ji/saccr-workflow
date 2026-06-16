# Outputs directory

Sample **pipeline results** in this folder (`*.csv`, `summary.xlsx`, `report.html`, `rwa_by_counterparty.png`) are **committed** so visitors can open them without running code.

**PDF exports** (e.g. notebook print-to-PDF) stay **out of Git** via `.gitignore` (`outputs/*.pdf`)—usually large and easy to regenerate.

## How to refresh these files

From the repository root:

```bash
python scripts/run_saccr.py --output-dir outputs --plot
```

After regenerating, commit updated CSV/HTML/PNG/XLSX if you want the repo to reflect a new run (omit PDFs).
