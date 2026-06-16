"""Smoke and regression checks for the end-to-end SA-CCR exposure pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest

from saccr.pipeline import run_saccr

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_XLSX = REPO_ROOT / "data" / "SA-CCR Sample IR Calculations.xlsx"


@pytest.fixture(scope="module")
def sample_output():
    assert SAMPLE_XLSX.is_file(), f"Missing sample data: {SAMPLE_XLSX}"
    return run_saccr(SAMPLE_XLSX)


def test_run_saccr_produces_non_empty_outputs(sample_output):
    out = sample_output
    assert len(out.trades_enriched) > 0
    assert len(out.netting_set_ead) > 0
    assert len(out.summary_by_counterparty) > 0


def test_netting_set_ead_has_expected_columns(sample_output):
    cols = set(sample_output.netting_set_ead.columns)
    assert {"Counterparty ID", "Netting Set ID", "PFE", "RC", "EAD", "RWA"}.issubset(cols)


def test_summary_by_counterparty_columns(sample_output):
    cols = sample_output.summary_by_counterparty.columns.tolist()
    assert cols == ["Counterparty ID", "PFE", "RC", "EAD", "RWA"]


def test_sample_workbook_shape_stable(sample_output):
    """Guards against accidental truncation of the committed sample workbook."""
    assert len(sample_output.trades_enriched) == 78
    assert len(sample_output.netting_set_ead) == 5
