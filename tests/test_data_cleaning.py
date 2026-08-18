"""Pruebas para la limpieza de transacciones."""

import pandas as pd
import pytest

from python.metadata import CLEANED_COLUMNS
from python.utils.data_cleaning import clean_transactions


def test_clean_transactions_normalizes_required_columns(
    raw_transactions: pd.DataFrame,
) -> None:
    """Comprueba la selección, normalización y tipado."""
    cleaned_transactions = clean_transactions(raw_transactions)

    assert cleaned_transactions.columns.tolist() == CLEANED_COLUMNS
    assert cleaned_transactions["status"].tolist() == [
        "APPROVED",
        "DECLINED",
        "APPROVED",
        "APPROVED",
    ]
    assert cleaned_transactions["amount_in_cents"].tolist() == [1000, 2000, 3000, 500]
    assert cleaned_transactions["bin"].tolist() == [
        "123456",
        "123456",
        "654321",
        "654321",
    ]
    assert isinstance(cleaned_transactions["status"].dtype, pd.StringDtype)
    assert cleaned_transactions["amount_in_cents"].dtype == "int64"
    assert isinstance(cleaned_transactions["bin"].dtype, pd.StringDtype)
    assert pd.api.types.is_datetime64_any_dtype(cleaned_transactions["created_at"])


def test_clean_transactions_does_not_modify_input(
    raw_transactions: pd.DataFrame,
) -> None:
    """Comprueba que la función no modifica el DataFrame recibido."""
    clean_transactions(raw_transactions)

    assert raw_transactions.loc[0, "status"] == " approved "
    assert raw_transactions.loc[0, "amount_in_cents"] == "1000"
    assert "bin" not in raw_transactions.columns


def test_clean_transactions_rejects_missing_columns(
    raw_transactions: pd.DataFrame,
) -> None:
    """Comprueba el error cuando falta una columna requerida."""
    incomplete_transactions = raw_transactions.loc[
        :, raw_transactions.columns != "amount_in_cents"
    ]

    with pytest.raises(
        ValueError,
        match=r"Faltan columnas requeridas: \['amount_in_cents'\]",
    ):
        clean_transactions(incomplete_transactions)
