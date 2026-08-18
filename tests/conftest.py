"""Datos compartidos por las pruebas del pipeline."""

import pandas as pd
import pytest


@pytest.fixture
def transaction_records() -> list[dict[str, object]]:
    """Crea registros representativos de las transacciones.

    Returns:
        Registros de entrada para las pruebas.
    """
    records = [
        {
            "id": "transaction-1",
            "created_at": "2026-08-15T10:00:00Z",
            "status": " approved ",
            "payment_method_type": {"extra": {"bin": "123456"}},
            "amount_in_cents": "1000",
        },
        {
            "id": "transaction-2",
            "created_at": "2026-08-15T11:00:00Z",
            "status": "DECLINED",
            "payment_method_type": {"extra": {"bin": "123456"}},
            "amount_in_cents": 2000,
        },
        {
            "id": "transaction-3",
            "created_at": "2026-08-16T09:00:00Z",
            "status": "APPROVED",
            "payment_method_type": {"extra": {"bin": "654321"}},
            "amount_in_cents": 3000,
        },
        {
            "id": "transaction-4",
            "created_at": "2026-08-16T12:00:00Z",
            "status": "approved",
            "payment_method_type": {"extra": {"bin": "654321"}},
            "amount_in_cents": 500,
        },
    ]

    return records


@pytest.fixture
def raw_transactions(
    transaction_records: list[dict[str, object]],
) -> pd.DataFrame:
    """Construye el DataFrame de entrada.

    Args:
        transaction_records: Registros representativos.

    Returns:
        DataFrame sin limpiar.
    """
    transactions = pd.DataFrame(transaction_records)

    return transactions
