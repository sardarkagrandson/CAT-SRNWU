from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QMessageBox,
)

from widgets.common import NO_PROJECT_MESSAGE


class PreviewPage(QWidget):

    def __init__(
        self,
        state,
        main_window
    ):

        super().__init__()

        self.state = state
        self.main_window = main_window

        self.current_file = None
        self.current_table = None

        self.create_interface()

    # =========================================================
    # CREATE INTERFACE
    # =========================================================

    def create_interface(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(15)

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "Data Preview"
        )

        title.setObjectName(
            "sectionTitle"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        refresh_button = QPushButton(
            "Refresh"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        header.addWidget(
            refresh_button
        )

        layout.addLayout(
            header
        )

        # -----------------------------------------------------
        # PROJECT
        # -----------------------------------------------------

        self.project_label = QLabel(
            "No project selected"
        )

        self.project_label.setObjectName(
            "projectLabel"
        )

        layout.addWidget(
            self.project_label
        )

        # -----------------------------------------------------
        # DATA SOURCE
        # -----------------------------------------------------

        source_frame = QFrame()

        source_frame.setObjectName(
            "sourceFrame"
        )

        source_layout = QHBoxLayout(
            source_frame
        )

        source_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        source_label = QLabel(
            "Data Source:"
        )

        source_label.setObjectName(
            "controlLabel"
        )

        source_layout.addWidget(
            source_label
        )

        self.source_selector = QComboBox()

        self.source_selector.setMinimumWidth(
            450
        )

        self.source_selector.currentIndexChanged.connect(
            self.source_changed
        )

        source_layout.addWidget(
            self.source_selector,
            1
        )

        sheet_label = QLabel(
            "Preview rows:"
        )

        sheet_label.setObjectName(
            "controlLabel"
        )

        source_layout.addWidget(
            sheet_label
        )

        self.row_limit = QSpinBox()

        self.row_limit.setMinimum(
            10
        )

        self.row_limit.setMaximum(
            10000
        )

        self.row_limit.setValue(
            500
        )

        self.row_limit.setSingleStep(
            100
        )

        self.row_limit.valueChanged.connect(
            self.refresh_table
        )

        source_layout.addWidget(
            self.row_limit
        )

        layout.addWidget(
            source_frame
        )

        # -----------------------------------------------------
        # INFORMATION BAR
        # -----------------------------------------------------

        self.info_label = QLabel(
            "No data selected."
        )

        self.info_label.setObjectName(
            "infoLabel"
        )

        layout.addWidget(
            self.info_label
        )

        # -----------------------------------------------------
        # TABLE
        # -----------------------------------------------------

        self.table = QTableWidget()

        self.table.setObjectName(
            "previewTable"
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSortingEnabled(
            False
        )

        layout.addWidget(
            self.table,
            1
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = QLabel(
            "No data loaded."
        )

        self.status_label.setObjectName(
            "statusLabel"
        )

        layout.addWidget(
            self.status_label
        )

        self.apply_theme()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            self.project_label.setText(
                NO_PROJECT_MESSAGE
            )

            self.source_selector.blockSignals(
                True
            )

            self.source_selector.clear()

            self.source_selector.blockSignals(
                False
            )

            self.clear_table()

            self.info_label.setText(
                NO_PROJECT_MESSAGE
            )

            self.status_label.setText(
                "No project open."
            )

            return

        self.project_label.setText(
            f"Current Project: "
            f"{project.get('name', '')}"
        )

        self.populate_sources()

    # =========================================================
    # POPULATE DATA SOURCES
    # =========================================================

    def populate_sources(self):

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            return

        files = project.get(
            "files",
            []
        )

        self.source_selector.blockSignals(
            True
        )

        self.source_selector.clear()

        source_items = []

        for file_index, file_record in enumerate(
            files
        ):

            file_name = file_record.get(
                "original_name",
                file_record.get(
                    "stored_name",
                    f"File {file_index + 1}"
                )
            )

            tables = file_record.get(
                "tables",
                []
            )

            if not tables:

                source_items.append(
                    (
                        f"{file_name}",
                        file_index,
                        None
                    )
                )

                continue

            for table_index, table in enumerate(
                tables
            ):

                sheet_name = table.get(
                    "sheet_name",
                    f"Table {table_index + 1}"
                )

                source_items.append(
                    (
                        f"{file_name}  —  {sheet_name}",
                        file_index,
                        table_index
                    )
                )

        for display_name, file_index, table_index in (
            source_items
        ):

            self.source_selector.addItem(
                display_name,
                (
                    file_index,
                    table_index
                )
            )

        self.source_selector.blockSignals(
            False
        )

        if self.source_selector.count() == 0:

            self.current_file = None
            self.current_table = None

            self.clear_table()

            self.info_label.setText(
                "No loaded data sources in this project."
            )

            self.status_label.setText(
                "Upload a data file first."
            )

            return

        self.source_selector.setCurrentIndex(
            0
        )

        self.source_changed(
            0
        )

    # =========================================================
    # SOURCE CHANGED
    # =========================================================

    def source_changed(
        self,
        index
    ):

        if index < 0:

            return

        data = self.source_selector.itemData(
            index
        )

        if not data:

            return

        file_index, table_index = data

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            return

        files = project.get(
            "files",
            []
        )

        if file_index >= len(files):

            return

        file_record = files[
            file_index
        ]

        self.current_file = file_record

        tables = file_record.get(
            "tables",
            []
        )

        if (
            table_index is None
            or table_index >= len(tables)
        ):

            self.current_table = None

            self.clear_table()

            self.info_label.setText(
                "This file does not contain loaded table data."
            )

            return

        self.current_table = tables[
            table_index
        ]

        # -----------------------------------------------------
        # UPDATE CENTRAL STATE
        # -----------------------------------------------------

        self.state.selected_file = (
            file_record
        )

        self.state.selected_sheet = (
            self.current_table.get(
                "sheet_name"
            )
        )

        self.state.selected_data = (
            self.current_table
        )

        self.refresh_table()

    # =========================================================
    # REFRESH TABLE
    # =========================================================

    def refresh_table(self):

        if not self.current_table:

            self.clear_table()

            return

        headers = self.current_table.get(
            "headers",
            []
        )

        rows = self.current_table.get(
            "rows",
            []
        )

        original_row_numbers = (
            self.current_table.get(
                "original_row_numbers",
                []
            )
        )

        if not headers:

            self.clear_table()

            self.info_label.setText(
                "No columns found."
            )

            return

        preview_limit = self.row_limit.value()

        preview_rows = rows[
            :preview_limit
        ]

        self.table.clear()

        # -----------------------------------------------------
        # COLUMNS
        # -----------------------------------------------------

        self.table.setColumnCount(
            len(headers) + 1
        )

        column_headers = [
            "Source Row"
        ] + [
            str(header)
            for header in headers
        ]

        self.table.setHorizontalHeaderLabels(
            column_headers
        )

        # -----------------------------------------------------
        # ROWS
        # -----------------------------------------------------

        self.table.setRowCount(
            len(preview_rows)
        )

        for row_index, row in enumerate(
            preview_rows
        ):

            if row_index < len(
                original_row_numbers
            ):

                source_row = (
                    original_row_numbers[
                        row_index
                    ]
                )

            else:

                source_row = (
                    row_index + 2
                )

            source_item = QTableWidgetItem(
                str(source_row)
            )

            source_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row_index,
                0,
                source_item
            )

            for column_index in range(
                len(headers)
            ):

                if column_index < len(row):

                    value = row[
                        column_index
                    ]

                else:

                    value = ""

                if value is None:

                    value = ""

                item = QTableWidgetItem(
                    str(value)
                )

                self.table.setItem(
                    row_index,
                    column_index + 1,
                    item
                )

        # -----------------------------------------------------
        # RESIZE
        # -----------------------------------------------------

        self.table.resizeColumnsToContents()

        for column_index in range(
            self.table.columnCount()
        ):

            width = (
                self.table.columnWidth(
                    column_index
                )
            )

            if width > 300:

                self.table.setColumnWidth(
                    column_index,
                    300
                )

        # -----------------------------------------------------
        # INFORMATION
        # -----------------------------------------------------

        total_rows = len(
            rows
        )

        total_columns = len(
            headers
        )

        displayed_rows = len(
            preview_rows
        )

        sheet_name = self.current_table.get(
            "sheet_name",
            "Data"
        )

        self.info_label.setText(
            f"Sheet: {sheet_name}"
            f"    •    "
            f"Total Rows: {total_rows:,}"
            f"    •    "
            f"Columns: {total_columns:,}"
            f"    •    "
            f"Displaying: {displayed_rows:,}"
        )

        self.status_label.setText(
            "Data preview loaded successfully."
        )

    # =========================================================
    # CLEAR TABLE
    # =========================================================

    def clear_table(self):

        self.table.clear()

        self.table.setRowCount(
            0
        )

        self.table.setColumnCount(
            0
        )

    # =========================================================
    # THEME
    # =========================================================

    def apply_theme(self):

        theme = self.main_window.theme_manager

        self.setStyleSheet(
            f"""
            #sectionTitle {{
                color: {theme.color("primary_text")};
                font-size: 22px;
                font-weight: 700;
            }}

            #projectLabel {{
                color: {theme.color("secondary_text")};
                font-size: 13px;
                font-weight: 600;
            }}

            #sourceFrame {{
                background-color: {theme.color("card_background")};
                border: 1px solid {theme.color("border")};
                border-radius: 8px;
            }}

            #controlLabel {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
                font-weight: 600;
            }}

            #infoLabel {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
                padding: 3px;
            }}

            #statusLabel {{
                color: {theme.color("muted_text")};
                font-size: 12px;
            }}

            #previewTable {{
                background-color: {theme.color("card_background")};
                alternate-background-color: {theme.color("table_header")};
                color: {theme.color("primary_text")};
                border: 1px solid {theme.color("border")};
                gridline-color: {theme.color("border")};
                font-size: 11px;
            }}

            #previewTable::item {{
                padding: 4px;
            }}

            #previewTable::item:selected {{
                background-color: {theme.color("table_selected")};
                color: {theme.color("primary_text")};
            }}

            QHeaderView::section {{
                background-color: {theme.color("accent")};
                color: {theme.color("button_text")};
                padding: 7px;
                border: none;
                font-size: 11px;
                font-weight: 600;
            }}

            QComboBox {{
                background-color: {theme.color("input_background")};
                border: 1px solid {theme.color("input_border")};
                border-radius: 5px;
                padding: 7px;
                color: {theme.color("input_text")};
            }}

            QComboBox:hover {{
                border: 1px solid {theme.color("accent")};
            }}

            QComboBox QAbstractItemView {{
                background-color: {theme.color("input_background")};
                color: {theme.color("input_text")};
                border: 1px solid {theme.color("input_border")};
                selection-background-color: {theme.color("table_selected")};
                selection-color: {theme.color("primary_text")};
            }}

            QSpinBox {{
                background-color: {theme.color("input_background")};
                border: 1px solid {theme.color("input_border")};
                border-radius: 5px;
                padding: 6px;
                padding-right: 2px;
                color: {theme.color("input_text")};
            }}

            QSpinBox:hover {{
                border: 1px solid {theme.color("accent")};
            }}

            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                height: 12px;
                border: none;
                border-left: 1px solid {theme.color("input_border")};
                border-top-right-radius: 5px;
                background-color: {theme.color("input_background")};
            }}

            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                height: 12px;
                border: none;
                border-left: 1px solid {theme.color("input_border")};
                border-bottom-right-radius: 5px;
                background-color: {theme.color("input_background")};
            }}

            QSpinBox::up-button:hover,
            QSpinBox::down-button:hover {{
                background-color: {theme.color("table_header")};
            }}

            QSpinBox::up-arrow {{
                width: 7px;
                height: 7px;
                image: none;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-bottom: 4px solid {theme.color("secondary_text")};
            }}

            QSpinBox::down-arrow {{
                width: 7px;
                height: 7px;
                image: none;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 4px solid {theme.color("secondary_text")};
            }}

            #secondaryButton {{
                background-color: {theme.color("input_background")};
                color: {theme.color("secondary_text")};
                border: 1px solid {theme.color("input_border")};
                border-radius: 6px;
                padding: 8px 15px;
            }}

            #secondaryButton:hover {{
                background-color: {theme.color("table_header")};
            }}
            """
        )