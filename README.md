# Simplified SA-CCR Counterparty Credit Risk Workflow

A short Python demo that walks from trade data in Excel to **EAD** and **RWA** under a **simplified** SA-CCR-style workflow. For learning only—not full regulatory SA-CCR.

## What you need

- **Python 3.10+** installed (3.11 is fine)
- Sample data in this repo: `data/SA-CCR Sample IR Calculations.xlsx`

## Install dependencies

Open a terminal in the **project root** (the folder that contains `requirements.txt`), then run:

```bash
pip install -r requirements.txt
```

## How to run

1. Open `notebook/CCR Project.ipynb` in Cursor or Jupyter.
2. **Select Kernel** → **Python Environments** → choose Python 3.
3. Run all code cells **from top to bottom**.
4. If the last cells show tables and an RWA bar chart, the run succeeded.

## Data

- File: `data/SA-CCR Sample IR Calculations.xlsx`
- Sheet used: `Data_Input`

## Important note

This is a **simplified** educational workflow, not full Basel SA-CCR. **Not for regulatory reporting.**

## Sample data reference

Example workbook style: [rohank170403/SA-CCR](https://github.com/rohank170403/SA-CCR)