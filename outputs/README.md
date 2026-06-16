# Outputs directory

This folder holds **generated** results from the pipeline (CSV, XLSX, HTML, PNG, PDF exports).

## How to produce files here

From the repository root:

```bash
python scripts/run_saccr.py --output-dir outputs --plot
```

Regenerated artifacts are listed in `.gitignore` so they are **not committed** (keeps the repo small and avoids noisy diffs). This `README.md` is committed so the `outputs/` directory is visible on GitHub.
