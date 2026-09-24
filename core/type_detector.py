from datetime import date, datetime
import math
import re


# =============================================================
# SUPPORTED DATA TYPES
# =============================================================

DATA_TYPES = [
    "Text",
    "Integer",
    "Decimal",
    "Date",
    "DateTime",
    "Boolean",
]


# =============================================================
# DETECT COLUMN TYPE
# =============================================================

def detect_column_type(values):

    cleaned_values = [
        value
        for value in values
        if not is_empty(value)
    ]

    if not cleaned_values:
        return "Text"

    # ---------------------------------------------------------
    # BOOLEAN
    # ---------------------------------------------------------

    if all(is_boolean(value) for value in cleaned_values):
        return "Boolean"

    # ---------------------------------------------------------
    # DATE / DATETIME
    # ---------------------------------------------------------

    if all(is_datetime(value) for value in cleaned_values):

        if any(
            contains_time(value)
            for value in cleaned_values
        ):
            return "DateTime"

        return "Date"

    # ---------------------------------------------------------
    # INTEGER
    # ---------------------------------------------------------

    if all(is_integer(value) for value in cleaned_values):
        return "Integer"

    # ---------------------------------------------------------
    # DECIMAL
    # ---------------------------------------------------------

    if all(is_decimal(value) for value in cleaned_values):
        return "Decimal"

    # ---------------------------------------------------------
    # DEFAULT
    # ---------------------------------------------------------

    return "Text"


# =============================================================
# DETECT ALL COLUMNS
# =============================================================

def detect_table_types(headers, rows):

    detected_types = {}

    for column_index, header in enumerate(headers):

        values = []

        for row in rows:

            if column_index < len(row):

                values.append(
                    row[column_index]
                )

        detected_types[header] = (
            detect_column_type(values)
        )

    return detected_types


# =============================================================
# EMPTY VALUE
# =============================================================

def is_empty(value):

    if value is None:
        return True

    if isinstance(value, float):

        if math.isnan(value):
            return True

    if isinstance(value, str):

        return not value.strip()

    return False


# =============================================================
# BOOLEAN
# =============================================================

def is_boolean(value):

    if isinstance(value, bool):
        return True

    if not isinstance(value, str):
        return False

    normalized = value.strip().lower()

    return normalized in {
        "true",
        "false",
        "yes",
        "no",
        "y",
        "n",
        "1",
        "0",
    }


# =============================================================
# INTEGER
# =============================================================

def is_integer(value):

    if isinstance(value, bool):
        return False

    if isinstance(value, int):
        return True

    if isinstance(value, float):

        return value.is_integer()

    if not isinstance(value, str):
        return False

    text = value.strip()

    if not text:
        return False

    # Remove common thousands separators
    text = text.replace(",", "")

    return bool(
        re.fullmatch(
            r"[+-]?\d+",
            text
        )
    )


# =============================================================
# DECIMAL
# =============================================================

def is_decimal(value):

    if isinstance(value, bool):
        return False

    if isinstance(value, (int, float)):
        return True

    if not isinstance(value, str):
        return False

    text = value.strip()

    if not text:
        return False

    text = text.replace(",", "")

    return bool(
        re.fullmatch(
            r"[+-]?(?:\d+\.\d+|\d+|\.\d+)",
            text
        )
    )


# =============================================================
# DATETIME
# =============================================================

def is_datetime(value):

    if isinstance(value, datetime):
        return True

    if isinstance(value, date):
        return True

    if not isinstance(value, str):
        return False

    text = value.strip()

    if not text:
        return False

    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",

        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",

        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",

        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]

    for fmt in formats:

        try:

            datetime.strptime(
                text,
                fmt
            )

            return True

        except ValueError:

            continue

    return False


# =============================================================
# CONTAINS TIME
# =============================================================

def contains_time(value):

    if isinstance(value, datetime):
        return True

    if isinstance(value, date):
        return False

    if not isinstance(value, str):
        return False

    text = value.strip()

    return bool(
        re.search(
            r"\d{1,2}:\d{2}",
            text
        )
    )


# =============================================================
# TYPE CONFIDENCE
# =============================================================

def calculate_type_confidence(
    values,
    detected_type
):

    cleaned_values = [
        value
        for value in values
        if not is_empty(value)
    ]

    if not cleaned_values:
        return 0.0

    matching_values = 0

    for value in cleaned_values:

        if detected_type == "Boolean":

            valid = is_boolean(value)

        elif detected_type == "Integer":

            valid = is_integer(value)

        elif detected_type == "Decimal":

            valid = is_decimal(value)

        elif detected_type in (
            "Date",
            "DateTime",
        ):

            valid = is_datetime(value)

        else:

            valid = True

        if valid:
            matching_values += 1

    return (
        matching_values
        / len(cleaned_values)
        * 100
    )


# =============================================================
# ANALYSE COLUMN
# =============================================================

def analyse_column(values):

    detected_type = detect_column_type(
        values
    )

    confidence = calculate_type_confidence(
        values,
        detected_type
    )

    return {
        "detected_type": detected_type,
        "confidence": round(
            confidence,
            2
        ),
        "value_count": len(
            [
                value
                for value in values
                if not is_empty(value)
            ]
        ),
    }


# =============================================================
# ANALYSE TABLE
# =============================================================

def analyse_table(headers, rows):

    result = {}

    for column_index, header in enumerate(headers):

        values = []

        for row in rows:

            if column_index < len(row):

                values.append(
                    row[column_index]
                )

        result[header] = analyse_column(
            values
        )

    return result