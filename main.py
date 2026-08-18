"""Orquesta el pipeline de transacciones."""

import argparse
import logging
import os
from collections.abc import Sequence
from time import perf_counter

from python.utils import (
    build_transaction_summary,
    clean_transactions,
    read_file,
    write_parquet,
)


logger = logging.getLogger(__name__)


def main(arguments: Sequence[str] | None = None) -> None:
    """Ejecuta el pipeline de transacciones.

    Args:
        arguments: Argumentos opcionales de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Genera la vista agregada de transacciones aprobadas."
    )
    parser.add_argument(
        "--input-path",
        default=os.path.join("data", "transactions_50k.jsonl"),
        help="Ruta del archivo JSONL o TXT de entrada.",
    )
    parser.add_argument(
        "--output-path",
        default=os.path.join("output", "transactions_summary.parquet"),
        help="Ruta del archivo Parquet de salida.",
    )
    parser.add_argument(
        "--log-path",
        default=os.path.join("logs", "pipeline.log"),
        help="Ruta del archivo de logs.",
    )
    parsed_arguments = parser.parse_args(arguments)

    log_directory = os.path.dirname(os.path.abspath(parsed_arguments.log_path))
    os.makedirs(log_directory, exist_ok=True)

    log_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler = logging.FileHandler(
        parsed_arguments.log_path,
        mode="a",
        encoding="utf-8",
    )
    stream_handler = logging.StreamHandler()
    file_handler.setFormatter(log_formatter)
    stream_handler.setFormatter(log_formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    pipeline_start = perf_counter()

    try:
        logger.info(
            "Iniciando el pipeline | entrada=%s | salida=%s",
            parsed_arguments.input_path,
            parsed_arguments.output_path,
        )

        stage_start = perf_counter()
        transactions = read_file(parsed_arguments.input_path)
        logger.info(
            "Lectura completada | registros=%s | duracion_segundos=%.3f",
            len(transactions),
            perf_counter() - stage_start,
        )

        stage_start = perf_counter()
        cleaned_transactions = clean_transactions(transactions)
        logger.info(
            "Limpieza completada | registros=%s | duracion_segundos=%.3f",
            len(cleaned_transactions),
            perf_counter() - stage_start,
        )

        stage_start = perf_counter()
        transaction_summary = build_transaction_summary(cleaned_transactions)
        logger.info(
            "Transformación completada | transacciones_aprobadas=%s | "
            "filas_agregadas=%s | duracion_segundos=%.3f",
            int(transaction_summary["approved_transaction_count"].sum()),
            len(transaction_summary),
            perf_counter() - stage_start,
        )

        stage_start = perf_counter()
        write_parquet(transaction_summary, parsed_arguments.output_path)
        logger.info(
            "Escritura completada | filas=%s | ruta=%s | duracion_segundos=%.3f",
            len(transaction_summary),
            parsed_arguments.output_path,
            perf_counter() - stage_start,
        )
        logger.info(
            "Pipeline finalizado | duracion_segundos=%.3f",
            perf_counter() - pipeline_start,
        )
    except Exception:
        logger.exception(
            "El pipeline terminó con un error | duracion_segundos=%.3f",
            perf_counter() - pipeline_start,
        )
        raise
    finally:
        logger.removeHandler(file_handler)
        logger.removeHandler(stream_handler)
        file_handler.close()
        stream_handler.close()


if __name__ == "__main__":
    main()
