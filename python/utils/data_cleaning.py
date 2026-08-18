"""Funciones para limpiar las transacciones."""

import pandas as pd


REQUIRED_COLUMNS = [
    "id",
    "created_at",
    "status",
    "payment_method_type",
    "amount_in_cents",
]


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

    cleaned_transactions = transactions.loc[:, REQUIRED_COLUMNS].assign(
        created_at=lambda data_frame: pd.to_datetime(
            data_frame["created_at"], errors="coerce"
        ),
        status=lambda data_frame: (
            data_frame["status"].astype("string").str.strip().str.upper()
        ),
        amount_in_cents=lambda data_frame: pd.to_numeric(
            data_frame["amount_in_cents"], errors="coerce"
        ),
        bin=lambda data_frame: data_frame["payment_method_type"].map(
            lambda method: (
                method.get("extra", {}).get("bin")
                if isinstance(method, dict)
                else pd.NA
            )
        ),
    )

    validated_columns = ["id", "created_at", "status", "amount_in_cents", "bin"]
    if cleaned_transactions.loc[:, validated_columns].isna().any().any():
        raise ValueError("Se encontraron valores nulos o inválidos")

    if not cleaned_transactions["bin"].astype("string").str.fullmatch(r"\d{6}").all():
        raise ValueError("Todos los BIN deben contener seis dígitos")

    if not cleaned_transactions["amount_in_cents"].mod(1).eq(0).all():
        raise ValueError("Los montos en centavos deben ser enteros")

    if cleaned_transactions["amount_in_cents"].le(0).any():
        raise ValueError("Los montos en centavos deben ser positivos")

    return cleaned_transactions.assign(
        amount_in_cents=lambda data_frame: data_frame["amount_in_cents"].astype(
            "int64"
        ),
        bin=lambda data_frame: data_frame["bin"].astype("string"),
    ).loc[:, validated_columns]
