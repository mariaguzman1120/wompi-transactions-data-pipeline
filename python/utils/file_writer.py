"""Funciones para escribir los archivos de salida."""

import os

import pandas as pd


def write_parquet(data_frame: pd.DataFrame, file_path: str) -> None:
    """Escribe un DataFrame en formato Parquet.

    Args:
        data_frame: Datos que se escribirán.
        file_path: Ruta del archivo de salida.
    """
    output_directory = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(output_directory, exist_ok=True)
    data_frame.to_parquet(file_path, engine="pyarrow", index=False)
