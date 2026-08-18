"""Constantes utilizadas para procesar las transacciones."""

REQUIRED_COLUMNS = [
    "id",
    "created_at",
    "status",
    "payment_method_type",
    "amount_in_cents",
]

CLEANED_COLUMNS = [
    "id",
    "created_at",
    "status",
    "amount_in_cents",
    "bin",
]

GROUP_COLUMNS = [
    "transaction_date",
    "month",
    "year",
    "bin",
]

APPROVED_STATUS = "APPROVED"
