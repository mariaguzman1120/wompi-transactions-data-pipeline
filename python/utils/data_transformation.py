"""Funciones para transformar las transacciones."""

import pandas as pd

from python.metadata import APPROVED_STATUS, GROUP_COLUMNS


def build_transaction_summary(transactions: pd.DataFrame) -> pd.DataFrame:
    """Agrega la cantidad y el monto de las transacciones aprobadas.

    Args:
        transactions: Transacciones limpias.

    Returns:
        Vista agregada por fecha y BIN.
    """
    approved_transactions = transactions.loc[
        transactions["status"].eq(APPROVED_STATUS)
    ].assign(
        transaction_date=lambda data_frame: data_frame["created_at"].dt.date,
        month=lambda data_frame: data_frame["created_at"].dt.month.astype("int8"),
        year=lambda data_frame: data_frame["created_at"].dt.year.astype("int16"),
    )

    transaction_summary = approved_transactions.groupby(
        GROUP_COLUMNS,
        as_index=False,
        sort=True,
    ).agg(
        approved_transaction_count=("id", "size"),
        approved_amount_in_cents=("amount_in_cents", "sum"),
    )

    sorted_summary = transaction_summary.sort_values(
        GROUP_COLUMNS,
        ignore_index=True,
    )

    return sorted_summary
