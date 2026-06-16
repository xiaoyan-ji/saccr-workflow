# Input data

## File

| File | Description |
|------|-------------|
| `SA-CCR Sample IR Calculations.xlsx` | Sample OTC-style trade workbook used by the pipeline and notebooks. |

## Workbook layout

- **Primary sheet:** `Data_Input`  
- **Header row:** row index **8** (0-based) when read with `pandas.read_excel(..., header=8)` — matches the layout of the reference workbook.

## Key columns (non-exhaustive)

The pipeline expects at least the columns listed in `src/saccr/config.py` (`CORE_COLUMNS`), including:

- `COB Date`, `Counterparty ID`, `Netting Set ID`, `Ticket Number`, `Trade Type`, `Asset Class`
- `Base Notional`, `Margined/ Unmargined`, `Buy/Sell Indicator`, `Maturity Date`, `MtM`

Additional columns used for **hedging set** construction include, among others:

- `Base Currency`, `Trade Leg 1 Currency`, `Trade Leg 2 Currency`, `Sub Class`, `Underlying Entity Name`

## Asset classes in this sample

The sample file includes rows with `Asset Class` in:

`Interest Rate`, `FX`, `Credit`, `Equity`, `Commodity`.

## Source

Workbook structure and sample content are aligned with the public reference:

- [rohank170403/SA-CCR](https://github.com/rohank170403/SA-CCR)

Place any replacement input files in this directory and point `scripts/run_saccr.py --input` (or `run_saccr(...)`) at the new path.
