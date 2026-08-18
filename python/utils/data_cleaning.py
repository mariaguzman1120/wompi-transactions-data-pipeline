"""Funciones para limpiar las transacciones."""

import pandas as pd

from python.metadata import CLEANED_COLUMNS, REQUIRED_COLUMNS


def clean_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """Selecciona, normaliza y valida los campos requeridos.

    Args:
        transactions: Transacciones sin procesar.

    Returns:
        Transacciones limpias con el BIN extraído.

    Raises:
        ValueError: Si faltan columnas o existen valores inválidos.
    """
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(transactions.columns))
    if missing_columns:
        raise ValueError(f"Faltan columnas requeridas: {missing_columns}")

    cleaned_transactions = transactions.loc[:, REQUIRED_COLUMNS]

    cleaned_transactions["created_at"] = pd.to_datetime(
        cleaned_transactions["created_at"],
        errors="coerce",
    )

    cleaned_transactions["status"] = (
        cleaned_transactions["status"].str.strip().str.upper()
    )

    cleaned_transactions["amount_in_cents"] = pd.to_numeric(
        cleaned_transactions["amount_in_cents"],
        errors="coerce",
    )

    cleaned_transactions["bin"] = cleaned_transactions["payment_method_type"].map(
        lambda method: (
            method["extra"].get("bin")
            if isinstance(method, dict) and isinstance(method.get("extra"), dict)
            else pd.NA
        )
    )

    data_types = {
        "status": "string",
        "amount_in_cents": "int64",
        "bin": "string",
    }
    cleaned_transactions = cleaned_transactions.astype(data_types)
    cleaned_transactions = cleaned_transactions.loc[:, CLEANED_COLUMNS]

    return cleaned_transactions
