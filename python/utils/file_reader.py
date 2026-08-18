"""Funciones para leer los archivos de entrada."""

import os

import pandas as pd


def read_file(file_path: str) -> pd.DataFrame:
    """Lee transacciones desde un archivo compatible.

    Los archivos TXT se interpretan como JSON Lines.

    Args:
        file_path: Ruta del archivo de entrada.

    Returns:
        DataFrame con los registros del archivo.

    Raises:
        ValueError: Si la extensión no está soportada.
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".jsonl":
        data_frame = pd.read_json(file_path, lines=True)
    elif file_extension == ".txt":
        data_frame = pd.read_json(file_path, lines=True)
    else:
        raise ValueError(f"Extensión de archivo no soportada: {file_extension}")

    return data_frame
