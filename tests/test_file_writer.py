"""Pruebas para la escritura de archivos."""

from pathlib import Path

import pandas as pd

from python.utils.file_writer import write_parquet


def test_write_parquet_creates_output_directory(tmp_path: Path) -> None:
    """Comprueba la creación del directorio y del archivo."""
    output_path = tmp_path / "nested" / "transactions.parquet"
    data = {"id": ["transaction-1"], "amount_in_cents": [1000]}
    transactions = pd.DataFrame(data)

    write_parquet(transactions, str(output_path))

    written_transactions = pd.read_parquet(output_path, engine="pyarrow")
    pd.testing.assert_frame_equal(written_transactions, transactions)


def test_write_parquet_overwrites_previous_output(tmp_path: Path) -> None:
    """Comprueba que una nueva ejecución no acumula información."""
    output_path = tmp_path / "transactions.parquet"
    first_data = {"id": ["transaction-1"], "amount_in_cents": [1000]}
    second_data = {"id": ["transaction-2"], "amount_in_cents": [2000]}
    first_transactions = pd.DataFrame(first_data)
    second_transactions = pd.DataFrame(second_data)

    write_parquet(first_transactions, str(output_path))
    write_parquet(second_transactions, str(output_path))

    written_transactions = pd.read_parquet(output_path, engine="pyarrow")
    pd.testing.assert_frame_equal(written_transactions, second_transactions)
