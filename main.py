"""Orquesta el pipeline de transacciones."""

import argparse
import logging
import os
from collections.abc import Sequence

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
    parsed_arguments = parser.parse_args(arguments)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    try:
        logger.info("Iniciando el pipeline")
        transactions = read_file(parsed_arguments.input_path)
        logger.info("Transacciones leídas: %s", len(transactions))

        cleaned_transactions = clean_transactions(transactions)
        transaction_summary = build_transaction_summary(cleaned_transactions)
        logger.info(
            "Transacciones aprobadas: %s",
            int(transaction_summary["approved_transaction_count"].sum()),
        )
        logger.info("Filas agregadas: %s", len(transaction_summary))

        write_parquet(transaction_summary, parsed_arguments.output_path)
        logger.info("Archivo generado: %s", parsed_arguments.output_path)
    except Exception:
        logger.exception("El pipeline terminó con un error")
        raise


if __name__ == "__main__":
    main()
