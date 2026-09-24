from pathlib import Path
import csv


SUPPORTED_EXTENSIONS = {
    ".csv": "CSV",
    ".txt": "Text",
    ".xlsx": "Excel",
    ".xls": "Excel",
}


# =============================================================
# FILE TYPE
# =============================================================

def detect_file_type(file_path):

    extension = Path(file_path).suffix.lower()

    return SUPPORTED_EXTENSIONS.get(
        extension,
        "Unknown"
    )


# =============================================================
# LOAD FILE
# =============================================================

def load_file(file_path):

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".csv":
        return load_csv(file_path)

    if extension == ".txt":
        return load_text(file_path)

    if extension in [".xlsx", ".xls"]:
        return load_excel(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


# =============================================================
# LOAD CSV
# =============================================================

def load_csv(file_path):

    encodings = [
        "utf-8-sig",
        "utf-8",
        "cp1252",
        "latin-1",
    ]

    last_error = None

    for encoding in encodings:

        try:

            with open(
                file_path,
                "r",
                encoding=encoding,
                errors="replace",
                newline=""
            ) as file:

                sample = file.read(
                    10000
                )

                file.seek(0)

                delimiter = detect_delimiter(
                    sample
                )

                reader = csv.reader(
                    file,
                    delimiter=delimiter
                )

                rows = list(
                    reader
                )

            return create_table(
                file_path,
                rows,
                "Data"
            )

        except Exception as error:

            last_error = error

    raise RuntimeError(
        f"Could not read CSV file: {last_error}"
    )


# =============================================================
# LOAD TEXT FILE
# =============================================================

def load_text(file_path):

    encodings = [
        "utf-8-sig",
        "utf-8",
        "cp1252",
        "latin-1",
    ]

    last_error = None

    for encoding in encodings:

        try:

            with open(
                file_path,
                "r",
                encoding=encoding,
                errors="replace",
                newline=""
            ) as file:

                sample = file.read(
                    10000
                )

                file.seek(0)

                delimiter = detect_delimiter(
                    sample
                )

                reader = csv.reader(
                    file,
                    delimiter=delimiter
                )

                rows = list(
                    reader
                )

            return create_table(
                file_path,
                rows,
                "Data"
            )

        except Exception as error:

            last_error = error

    raise RuntimeError(
        f"Could not read text file: {last_error}"
    )


# =============================================================
# DETECT DELIMITER
# =============================================================

def detect_delimiter(sample):

    possible_delimiters = [
        ",",
        ";",
        "\t",
        "|",
    ]

    best_delimiter = ","
    best_score = -1

    lines = sample.splitlines()

    for delimiter in possible_delimiters:

        counts = []

        for line in lines[:50]:

            if not line.strip():
                continue

            counts.append(
                line.count(delimiter)
            )

        if not counts:
            continue

        # Prefer delimiters that occur consistently
        positive_counts = [
            count
            for count in counts
            if count > 0
        ]

        if not positive_counts:
            continue

        average = sum(
            positive_counts
        ) / len(
            positive_counts
        )

        consistency = sum(
            1
            for count in counts
            if count == positive_counts[0]
        )

        score = (
            average
            +
            consistency
        )

        if score > best_score:

            best_score = score

            best_delimiter = delimiter

    return best_delimiter


# =============================================================
# LOAD EXCEL
# =============================================================

def load_excel(file_path):

    import pandas as pd

    try:

        workbook = pd.read_excel(
            file_path,
            sheet_name=None,
            header=0,
            dtype=object
        )

    except Exception as error:

        raise RuntimeError(
            f"Could not read Excel file:\n{error}"
        )

    tables = []

    for sheet_name, dataframe in workbook.items():

        dataframe = dataframe.fillna("")

        headers = [
            clean_header(column)
            for column in dataframe.columns
        ]

        rows = dataframe.astype(
            object
        ).values.tolist()

        table = {
            "sheet_name": str(
                sheet_name
            ),

            "headers": headers,

            "rows": rows,

            "source_path": str(
                file_path
            ),

            "original_row_numbers":
                list(
                    range(
                        2,
                        len(rows) + 2
                    )
                ),
        }

        tables.append(
            table
        )

    return tables


# =============================================================
# CREATE TABLE
# =============================================================

def create_table(
    file_path,
    raw_rows,
    sheet_name
):

    if not raw_rows:

        return []

    # ---------------------------------------------------------
    # FIRST ROW = HEADERS
    # ---------------------------------------------------------

    headers = [
        clean_header(value)
        for value in raw_rows[0]
    ]

    # ---------------------------------------------------------
    # DATA ROWS
    # ---------------------------------------------------------

    rows = []

    for row in raw_rows[1:]:

        normalized_row = normalize_row(
            row,
            len(headers)
        )

        rows.append(
            normalized_row
        )

    # ---------------------------------------------------------
    # SOURCE ROW NUMBERS
    #
    # Row 1 = header
    # Row 2 = first data row
    # ---------------------------------------------------------

    original_row_numbers = list(
        range(
            2,
            len(rows) + 2
        )
    )

    return [
        {
            "sheet_name": sheet_name,

            "headers": headers,

            "rows": rows,

            "source_path": str(
                file_path
            ),

            "original_row_numbers":
                original_row_numbers,
        }
    ]


# =============================================================
# NORMALIZE ROW
# =============================================================

def normalize_row(
    row,
    column_count
):

    row = list(row)

    # ---------------------------------------------------------
    # ADD MISSING CELLS
    # ---------------------------------------------------------

    while len(row) < column_count:

        row.append("")

    # ---------------------------------------------------------
    # REMOVE EXCESS CELLS
    # ---------------------------------------------------------

    if len(row) > column_count:

        row = row[
            :column_count
        ]

    return [
        normalize_value(value)
        for value in row
    ]


# =============================================================
# NORMALIZE VALUE
# =============================================================

def normalize_value(value):

    if value is None:

        return ""

    return value


# =============================================================
# CLEAN HEADER
# =============================================================

def clean_header(value):

    if value is None:

        return "Unnamed Column"

    header = str(
        value
    ).strip()

    if not header:

        return "Unnamed Column"

    return header