"""Pruebas para la transformación de transacciones."""

from datetime import date

import pandas as pd

from python.utils.data_cleaning import clean_transactions
from python.utils.data_transformation import build_transaction_summary


def test_build_transaction_summary_filters_and_aggregates(
    raw_transactions: pd.DataFrame,
) -> None:
    """Comprueba el filtro, la agrupación y el orden del resultado."""
    cleaned_transactions = clean_transactions(raw_transactions)

    transaction_summary = build_transaction_summary(cleaned_transactions)

    expected_data = {
        "transaction_date": [date(2026, 8, 15), date(2026, 8, 16)],
        "month": [8, 8],
        "year": [2026, 2026],
        "bin": ["123456", "654321"],
        "approved_transaction_count": [1, 2],
        "approved_amount_in_cents": [1000, 3500],
    }
    expected_summary = pd.DataFrame(expected_data)
    expected_types = {
        "month": "int8",
        "year": "int16",
        "bin": "string",
        "approved_transaction_count": "int64",
        "approved_amount_in_cents": "int64",
    }
    expected_summary = expected_summary.astype(expected_types)

    pd.testing.assert_frame_equal(transaction_summary, expected_summary)


def test_build_transaction_summary_is_deterministic(
    raw_transactions: pd.DataFrame,
) -> None:
    """Comprueba que llamadas repetidas producen el mismo resultado."""
    cleaned_transactions = clean_transactions(raw_transactions)

    first_summary = build_transaction_summary(cleaned_transactions)
    second_summary = build_transaction_summary(cleaned_transactions)

    pd.testing.assert_frame_equal(first_summary, second_summary)
