# Pipeline de datos de transacciones Wompi

Proyecto para desarrollar un pipeline de datos orientado al procesamiento de transacciones de Wompi.

## Requisitos

- Python 3.12
- `pip`

## Configuración del entorno

Crear el entorno virtual:

```powershell
py -3.12 -m venv .venv
```

Activar el entorno en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Dependencias principales

- `pandas`: manipulación y análisis de datos.
- `numpy`: operaciones numéricas.
- `fastparquet`: lectura y escritura de archivos Parquet.
- `pyarrow`: procesamiento columnar y compatibilidad con el formato Parquet.

## Desactivación del entorno

```powershell
deactivate
```
