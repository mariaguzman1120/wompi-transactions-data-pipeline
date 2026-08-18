"""Pruebas del pipeline completo."""

import hashlib
import json
import logging
from pathlib import Path

import pandas as pd
import pytest

from main import main


def test_pipeline_is_idempotent(
    tmp_path: Path,
    transaction_records: list[dict[str, object]],
) -> None:
    """Comprueba dos ejecuciones consecutivas con la misma entrada."""
    input_path = tmp_path / "transactions.jsonl"
    output_path = tmp_path / "transactions_summary.parquet"
    log_path = tmp_path / "pipeline.log"
    file_content = "\n".join(json.dumps(record) for record in transaction_records)
    input_path.write_text(file_content, encoding="utf-8")
    arguments = [
        "--input-path",
        str(input_path),
        "--output-path",
        str(output_path),
        "--log-path",
        str(log_path),
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


def test_pipeline_logs_each_stage(
    tmp_path: Path,
    transaction_records: list[dict[str, object]],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Comprueba que el pipeline registra sus etapas principales."""
    input_path = tmp_path / "transactions.jsonl"
    output_path = tmp_path / "transactions_summary.parquet"
    log_path = tmp_path / "pipeline.log"
    file_content = "\n".join(json.dumps(record) for record in transaction_records)
    input_path.write_text(file_content, encoding="utf-8")
    arguments = [
        "--input-path",
        str(input_path),
        "--output-path",
        str(output_path),
        "--log-path",
        str(log_path),
    ]

    with caplog.at_level(logging.INFO, logger="main"):
        main(arguments)

    log_messages = [record.getMessage() for record in caplog.records]

    assert any("Iniciando el pipeline" in message for message in log_messages)
    assert any("Lectura completada" in message for message in log_messages)
    assert any("Limpieza completada" in message for message in log_messages)
    assert any("Transformación completada" in message for message in log_messages)
    assert any("Escritura completada" in message for message in log_messages)
    assert any("Pipeline finalizado" in message for message in log_messages)

    log_content = log_path.read_text(encoding="utf-8")

    assert "Iniciando el pipeline" in log_content
    assert "Pipeline finalizado" in log_content
