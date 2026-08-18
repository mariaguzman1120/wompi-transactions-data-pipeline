# Pipeline de datos de transacciones Wompi

Pipeline desarrollado en Python para procesar transacciones con tarjeta y generar una vista agregada de las operaciones aprobadas en formato Parquet.

## Flujo del pipeline

1. Lee las transacciones desde un archivo JSONL o TXT con contenido JSON Lines.
2. Valida las columnas requeridas, los tipos, el BIN y los montos.
3. Normaliza el estado y extrae el BIN del método de pago.
4. Conserva únicamente las transacciones con estado `APPROVED`.
5. Agrega la cantidad y el monto aprobado por fecha y BIN.
6. Ordena el resultado y lo guarda en formato Parquet.

Las funciones de limpieza y transformación no modifican los datos recibidos. La lectura, la escritura y el logging se mantienen en los límites del pipeline.

## Estructura del proyecto

```text
main.py
data/
└── transactions_50k.jsonl
python/
├── __init__.py
└── utils/
    ├── __init__.py
    ├── data_cleaning.py
    ├── data_transformation.py
    ├── file_reader.py
    └── file_writer.py
output/
└── transactions_summary.parquet
requirements.txt
```

## Requisitos

- Python 3.12
- `pip`

Dependencias principales:

- `pandas`: lectura, limpieza y agregación de datos.
- `numpy`: soporte para operaciones numéricas.
- `pyarrow`: motor utilizado para escribir y leer Parquet.
- `fastparquet`: compatibilidad adicional con Parquet.

## Instalación

Crear el entorno virtual:

```powershell
py -3.12 -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Preparación de los datos

Ubicar el archivo descomprimido en la siguiente ruta:

```text
data/transactions_50k.jsonl
```

La carpeta `data/` está excluida del control de versiones porque contiene información personal, operacional y documentos locales de referencia.

## Ejecución

Desde la raíz del proyecto, ejecutar:

```powershell
python main.py
```

La ejecución anterior utiliza estas rutas predeterminadas:

| Parámetro | Valor predeterminado | Descripción |
| --- | --- | --- |
| `--input-path` | `data/transactions_50k.jsonl` | Archivo JSONL o TXT de entrada. |
| `--output-path` | `output/transactions_summary.parquet` | Archivo Parquet de salida. |

Para usar rutas diferentes:

```powershell
python main.py --input-path data/transactions_50k.jsonl --output-path output/transactions_summary.parquet
```

El parser de argumentos permite cambiar estas rutas desde la terminal sin modificar el código. Durante la ejecución, el logger informa las filas leídas, aprobadas y agregadas, además de la ubicación del resultado.

## Esquema de salida

| Columna | Descripción |
| --- | --- |
| `transaction_date` | Fecha de creación de la transacción. |
| `month` | Mes de la transacción. |
| `year` | Año de la transacción. |
| `bin` | Bank Identification Number de seis dígitos. |
| `approved_transaction_count` | Cantidad de transacciones aprobadas. |
| `approved_amount_in_cents` | Suma de los montos aprobados en centavos. |

## Supuestos

- `created_at` define la fecha de la transacción.
- Solo el estado `APPROVED`, después de normalizar mayúsculas y espacios, representa una aprobación.
- El BIN se obtiene de `payment_method_type.extra.bin`.
- Los montos se conservan como enteros en centavos porque la fuente no informa una moneda.
- Un registro inválido detiene el pipeline para evitar pérdidas silenciosas de información.
- El resultado se ordena por fecha, mes, año y BIN.

## Idempotencia

Si la entrada no cambia, cada ejecución reemplaza el archivo Parquet con el mismo esquema, orden y contenido.

## Resultado validado

Para el archivo entregado con el reto se obtuvieron los siguientes resultados:

- 50.000 transacciones leídas.
- 42.427 transacciones aprobadas.
- 21.529 filas agregadas.
- 1.965.579.524.955 centavos aprobados.
- Cero valores nulos y cero claves agregadas duplicadas.
- El mismo SHA-256 después de dos ejecuciones consecutivas.

## Desactivación del entorno

```powershell
deactivate
```
