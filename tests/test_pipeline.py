"""Pruebas del pipeline completo."""

import hashlib
import json
from pathlib import Path

import pandas as pd

from main import main


def test_pipeline_is_idempotent(
    tmp_path: Path,
    transaction_records: list[dict[str, object]],
) -> None:
    """Comprueba dos ejecuciones consecutivas con la misma entrada."""
    input_path = tmp_path / "transactions.jsonl"
    output_path = tmp_path / "transactions_summary.parquet"
    file_content = "\n".join(json.dumps(record) for record in transaction_records)
    input_path.write_text(file_content, encoding="utf-8")
    arguments = [
        "--input-path",
        str(input_path),
        "--output-path",
        str(output_path),
    ]

    main(arguments)
    first_summary = pd.read_parquet(output_path, engine="pyarrow")
    first_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()

    main(arguments)
    second_summary = pd.read_parquet(output_path, engine="pyarrow")
    second_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()

    pd.testing.assert_frame_equal(first_summary, second_summary)
    assert first_hash == second_hash
    assert len(second_summary) == 2
    assert second_summary["approved_transaction_count"].sum() == 3
    assert second_summary["approved_amount_in_cents"].sum() == 4500
