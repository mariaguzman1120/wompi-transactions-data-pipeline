<div align="center">

# Wompi Transactions Data Pipeline

Pipeline reproducible para convertir transacciones en una vista analítica de operaciones aprobadas.

**50.000 transacciones · 42.427 aprobadas · 21.529 filas agregadas**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-3.0.5-150458?style=for-the-badge&logo=pandas&logoColor=white)
![PyArrow](https://img.shields.io/badge/PyArrow-25.0.1-2F6F9F?style=for-the-badge&logo=apache&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.1.1-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Parquet](https://img.shields.io/badge/Salida-Parquet-50ABF1?style=for-the-badge&logo=apache&logoColor=white)

[Pipeline](#pipeline) · [Arquitectura](#arquitectura) · [Instalación](#instalación) · [Ejecución](#ejecución) · [Pruebas](#pruebas) · [Notebook](#notebook) · [Salida](#esquema-de-salida)

</div>

## Qué resuelve

El proyecto lee transacciones en formato JSON Lines, normaliza los campos necesarios y genera un archivo Parquet agregado por fecha y BIN. Solo las operaciones con estado `APPROVED` participan en el resultado.

| Entrada | Procesamiento | Salida |
| --- | --- | --- |
| JSONL o TXT con contenido JSON Lines | Lectura, limpieza, filtrado y agregación | Parquet ordenado por fecha y BIN |

## Pipeline

```mermaid
flowchart LR
    A["JSONL o TXT"] --> B["read_file"]
    B --> C["clean_transactions"]
    C --> D["build_transaction_summary"]
    D --> E["write_parquet"]
    E --> F["Parquet agregado"]
```

1. Lee el archivo de entrada y construye un DataFrame.
2. Selecciona las columnas requeridas y normaliza fecha, estado y monto.
3. Extrae el BIN desde `payment_method_type.extra.bin`.
4. Filtra las transacciones aprobadas.
5. Calcula la cantidad y el monto aprobado por fecha y BIN.
6. Ordena el resultado y lo escribe en formato Parquet.

## Arquitectura

`main.py` orquesta el flujo y mantiene la lectura, la escritura y el registro de eventos en los límites del pipeline. Las transformaciones se concentran en funciones que reciben y retornan DataFrames, mientras que `python/metadata/` centraliza columnas, estados y claves de agrupación.

```text
.
├── main.py
├── notebooks/
│   └── transactions_exploration.ipynb
├── python/
│   ├── metadata/
│   │   └── transaction_metadata.py
│   └── utils/
│       ├── data_cleaning.py
│       ├── data_transformation.py
│       ├── file_reader.py
│       └── file_writer.py
├── tests/
│   ├── conftest.py
│   ├── test_data_cleaning.py
│   ├── test_data_transformation.py
│   ├── test_file_reader.py
│   ├── test_file_writer.py
│   └── test_pipeline.py
├── output/
│   └── transactions_summary.parquet
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## Instalación

Requisitos: Python 3.12 y `pip`.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Las dependencias principales son `pandas`, para procesar los datos; `pyarrow`, como motor de escritura y lectura de Parquet; y `pytest`, para ejecutar las pruebas automatizadas.

## Preparación de los datos

El archivo se recibe descomprimido y debe ubicarse en:

```text
data/transactions_50k.jsonl
```

La carpeta `data/` está excluida del control de versiones porque contiene información personal, operacional y documentos locales del reto.

## Ejecución

Desde la raíz del proyecto:

```powershell
python main.py
```

| Parámetro | Valor predeterminado |
| --- | --- |
| `--input-path` | `data/transactions_50k.jsonl` |
| `--output-path` | `output/transactions_summary.parquet` |

También se pueden indicar rutas diferentes sin modificar el código:

```powershell
python main.py --input-path data/transactions_50k.jsonl --output-path output/transactions_summary.parquet
```

El logger informa el inicio del proceso, las filas leídas, las transacciones aprobadas, las filas agregadas y la ruta del resultado.

## Pruebas

La suite valida la lectura, la limpieza, la transformación, la escritura y la ejecución completa del pipeline. También comprueba su idempotencia: con la misma entrada y los mismos parámetros, dos ejecuciones consecutivas generan el mismo esquema, orden, contenido y SHA-256, sin acumular filas o montos.

Con el entorno virtual activo, todas las pruebas se ejecutan desde la raíz del proyecto:

```powershell
python -m pytest
```

Para mostrar únicamente el resumen:

```powershell
python -m pytest -q
```

También se puede ejecutar un archivo específico. Por ejemplo, la prueba de idempotencia de extremo a extremo:

```powershell
python -m pytest tests/test_pipeline.py -q
```

Las pruebas usan directorios temporales proporcionados por `pytest`; no leen el archivo de `data/` ni sobrescriben el resultado almacenado en `output/`.

## Notebook

El notebook [`notebooks/transactions_exploration.ipynb`](notebooks/transactions_exploration.ipynb) reproduce el pipeline en el mismo orden que `main.py`. Presenta la entrada, las decisiones de limpieza, las transformaciones y el resultado sin implementar una lógica paralela.

## Esquema de salida

| Columna | Descripción |
| --- | --- |
| `transaction_date` | Fecha de creación de la transacción. |
| `month` | Mes de la transacción. |
| `year` | Año de la transacción. |
| `bin` | Bank Identification Number asociado al método de pago. |
| `approved_transaction_count` | Cantidad de transacciones aprobadas. |
| `approved_amount_in_cents` | Suma de los montos aprobados en centavos. |

## Decisiones y supuestos

- `created_at` define la fecha de la transacción.
- El estado se normaliza eliminando espacios y convirtiéndolo a mayúsculas.
- Solo el valor exacto `APPROVED` representa una aprobación después de normalizarlo.
- El BIN se obtiene de `payment_method_type.extra.bin`.
- Los montos se convierten a enteros y se conservan en centavos porque la fuente no informa una moneda.
- Las columnas de entrada requeridas deben existir; si falta alguna, el pipeline se detiene.
- El resultado se ordena por fecha, mes, año y BIN para mantener una salida determinista.

## Resultado validado

| Métrica | Resultado |
| --- | ---: |
| Transacciones leídas | 50.000 |
| Transacciones aprobadas | 42.427 |
| Filas agregadas | 21.529 |
| Monto aprobado en centavos | 1.965.579.524.955 |
| Valores nulos en la salida | 0 |
| Claves agregadas duplicadas | 0 |

Con la misma entrada, dos ejecuciones consecutivas generan el mismo esquema, orden, contenido y SHA-256.

## Desactivación del entorno

```powershell
deactivate
```
