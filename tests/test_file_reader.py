"""Pruebas para la lectura de archivos."""

import json
from pathlib import Path

import pytest

from python.utils.file_reader import read_file


@pytest.mark.parametrize("file_extension", [".jsonl", ".txt"])
def test_read_file_reads_json_lines(
    tmp_path: Path,
    transaction_records: list[dict[str, object]],
    file_extension: str,
) -> None:
    """Comprueba la lectura de los formatos soportados."""
    input_path = tmp_path / f"transactions{file_extension}"
    file_content = "\n".join(json.dumps(record) for record in transaction_records)
    input_path.write_text(file_content, encoding="utf-8")

    transactions = read_file(str(input_path))

    assert len(transactions) == len(transaction_records)
    assert transactions["id"].tolist() == [
        record["id"] for record in transaction_records
    ]
    assert transactions.loc[0, "payment_method_type"] == {
        "extra": {"bin": "123456"}
    }


def test_read_file_rejects_unsupported_extension(tmp_path: Path) -> None:
    """Comprueba el error para una extensión no soportada."""
    input_path = tmp_path / "transactions.csv"

    with pytest.raises(ValueError, match="Extensión de archivo no soportada: .csv"):
        read_file(str(input_path))
