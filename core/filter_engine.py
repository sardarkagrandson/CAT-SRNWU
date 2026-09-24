from datetime import date, datetime
import math


# =============================================================
# FILTER OPERATORS
# =============================================================

FILTER_OPERATORS = [
    "Equals",
    "Not Equals",
    "Contains",
    "Does Not Contain",
    "Starts With",
    "Ends With",
    "Greater Than",
    "Greater Than or Equal",
    "Less Than",
    "Less Than or Equal",
    "Between",
    "Is Empty",
    "Is Not Empty",
]


# =============================================================
# APPLY FILTERS
# =============================================================

def apply_filters(
    headers,
    rows,
    conditions
):

    if not conditions:

        return list(rows)

    filtered_rows = []

    for row in rows:

        if row_matches_conditions(
            headers,
            row,
            conditions
        ):

            filtered_rows.append(
                row
            )

    return filtered_rows


# =============================================================
# ROW MATCH
# =============================================================

def row_matches_conditions(
    headers,
    row,
    conditions
):

    if not conditions:
        return True

    results = []

    for condition in conditions:

        result = evaluate_condition(
            headers,
            row,
            condition
        )

        results.append(
            result
        )

    # ---------------------------------------------------------
    # ALL conditions currently use AND logic.
    #
    # OR groups can be added later without changing the
    # individual condition engine.
    # ---------------------------------------------------------

    return all(
        results
    )


# =============================================================
# EVALUATE CONDITION
# =============================================================

def evaluate_condition(
    headers,
    row,
    condition
):

    column = condition.get(
        "column"
    )

    operator = condition.get(
        "operator"
    )

    value = condition.get(
        "value"
    )

    second_value = condition.get(
        "second_value"
    )

    if column not in headers:

        return False

    column_index = headers.index(
        column
    )

    if column_index >= len(row):

        cell_value = ""

    else:

        cell_value = row[
            column_index
        ]

    # ---------------------------------------------------------
    # EMPTY
    # ---------------------------------------------------------

    if operator == "Is Empty":

        return is_empty(
            cell_value
        )

    if operator == "Is Not Empty":

        return not is_empty(
            cell_value
        )

    # ---------------------------------------------------------
    # TEXT OPERATORS
    # ---------------------------------------------------------

    if operator == "Contains":

        return normalize_text(
            value
        ) in normalize_text(
            cell_value
        )

    if operator == "Does Not Contain":

        return normalize_text(
            value
        ) not in normalize_text(
            cell_value
        )

    if operator == "Starts With":

        return normalize_text(
            cell_value
        ).startswith(
            normalize_text(value)
        )

    if operator == "Ends With":

        return normalize_text(
            cell_value
        ).endswith(
            normalize_text(value)
        )

    # ---------------------------------------------------------
    # EQUALITY
    # ---------------------------------------------------------

    if operator == "Equals":

        return values_equal(
            cell_value,
            value
        )

    if operator == "Not Equals":

        return not values_equal(
            cell_value,
            value
        )

    # ---------------------------------------------------------
    # NUMERIC / DATE COMPARISON
    # ---------------------------------------------------------

    if operator == "Greater Than":

        return compare_values(
            cell_value,
            value,
            lambda a, b: a > b
        )

    if operator == "Greater Than or Equal":

        return compare_values(
            cell_value,
            value,
            lambda a, b: a >= b
        )

    if operator == "Less Than":

        return compare_values(
            cell_value,
            value,
            lambda a, b: a < b
        )

    if operator == "Less Than or Equal":

        return compare_values(
            cell_value,
            value,
            lambda a, b: a <= b
        )

    # ---------------------------------------------------------
    # BETWEEN
    # ---------------------------------------------------------

    if operator == "Between":

        first_result = compare_values(
            cell_value,
            value,
            lambda a, b: a >= b
        )

        second_result = compare_values(
            cell_value,
            second_value,
            lambda a, b: a <= b
        )

        return (
            first_result
            and second_result
        )

    return False


# =============================================================
# VALUE COMPARISON
# =============================================================

def compare_values(
    actual,
    expected,
    comparison
):

    actual_value = convert_comparable(
        actual
    )

    expected_value = convert_comparable(
        expected
    )

    if actual_value is None:
        return False

    if expected_value is None:
        return False

    try:

        return comparison(
            actual_value,
            expected_value
        )

    except (
        TypeError,
        ValueError
    ):

        return False


# =============================================================
# EQUALITY
# =============================================================

def values_equal(
    first,
    second
):

    first_value = convert_comparable(
        first
    )

    second_value = convert_comparable(
        second
    )

    if (
        first_value is None
        or second_value is None
    ):

        return (
            normalize_text(first)
            ==
            normalize_text(second)
        )

    return first_value == second_value


# =============================================================
# CONVERT COMPARABLE VALUE
# =============================================================

def convert_comparable(
    value
):

    if is_empty(value):

        return None

    if isinstance(
        value,
        bool
    ):

        return value

    if isinstance(
        value,
        datetime
    ):

        return value

    if isinstance(
        value,
        date
    ):

        return value

    if isinstance(
        value,
        (int, float)
    ):

        if (
            isinstance(value, float)
            and math.isnan(value)
        ):

            return None

        return value

    text = str(
        value
    ).strip()

    # ---------------------------------------------------------
    # NUMBER
    # ---------------------------------------------------------

    number_text = (
        text
        .replace(",", "")
        .replace(" ", "")
    )

    try:

        if "." in number_text:

            return float(
                number_text
            )

        return int(
            number_text
        )

    except ValueError:

        pass

    # ---------------------------------------------------------
    # DATE
    # ---------------------------------------------------------

    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
    ]

    for date_format in date_formats:

        try:

            return datetime.strptime(
                text,
                date_format
            )

        except ValueError:

            continue

    # ---------------------------------------------------------
    # TEXT
    # ---------------------------------------------------------

    return text.casefold()


# =============================================================
# TEXT NORMALIZATION
# =============================================================

def normalize_text(
    value
):

    if value is None:

        return ""

    return str(
        value
    ).strip().casefold()


# =============================================================
# EMPTY VALUE
# =============================================================

def is_empty(
    value
):

    if value is None:

        return True

    if isinstance(
        value,
        float
    ):

        if math.isnan(value):

            return True

    if isinstance(
        value,
        str
    ):

        return not value.strip()

    return False