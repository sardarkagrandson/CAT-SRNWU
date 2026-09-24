from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtCore import Qt

from core.type_detector import detect_column_type
from widgets.common import NO_PROJECT_MESSAGE


class MappingPage(QWidget):

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

        layout.setSpacing(
            15
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "Data Mapping"
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

        source_layout = QHBoxLayout()

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
            500
        )

        self.source_selector.currentIndexChanged.connect(
            self.source_changed
        )

        source_layout.addWidget(
            self.source_selector,
            1
        )

        layout.addLayout(
            source_layout
        )

        # -----------------------------------------------------
        # INFORMATION
        # -----------------------------------------------------

        self.info_label = QLabel(
            "Select a data source."
        )

        self.info_label.setObjectName(
            "infoLabel"
        )

        layout.addWidget(
            self.info_label
        )

        # -----------------------------------------------------
        # MAPPING TABLE
        # -----------------------------------------------------

        self.mapping_table = QTableWidget()

        self.mapping_table.setObjectName(
            "mappingTable"
        )

        self.mapping_table.setColumnCount(
            5
        )

        self.mapping_table.setHorizontalHeaderLabels(
            [
                "Column",
                "Detected Type",
                "Confidence",
                "Mapped Type",
                "Sample Values",
            ]
        )

        self.mapping_table.setAlternatingRowColors(
            True
        )

        self.mapping_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.mapping_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        header = self.mapping_table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.mapping_table,
            1
        )

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        clear_button = QPushButton(
            "Clear Mapping"
        )

        clear_button.setObjectName(
            "secondaryButton"
        )

        clear_button.clicked.connect(
            self.clear_mapping
        )

        button_layout.addWidget(
            clear_button
        )

        apply_button = QPushButton(
            "Apply Mapping"
        )

        apply_button.setObjectName(
            "primaryButton"
        )

        apply_button.clicked.connect(
            self.apply_mapping
        )

        button_layout.addWidget(
            apply_button
        )

        layout.addLayout(
            button_layout
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = QLabel(
            "Ready."
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
    # POPULATE SOURCES
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

        tables = file_record.get(
            "tables",
            []
        )

        if table_index >= len(tables):

            self.current_file = None
            self.current_table = None

            self.clear_table()

            return

        self.current_file = file_record

        self.current_table = tables[
            table_index
        ]

        # -----------------------------------------------------
        # CENTRAL APPLICATION STATE
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

        # -----------------------------------------------------
        # DETECT / LOAD MAPPING
        # -----------------------------------------------------

        self.load_mapping()

    # =========================================================
    # LOAD MAPPING
    # =========================================================

    def load_mapping(self):

        self.clear_table()

        if not self.current_table:

            self.info_label.setText(
                "No data source selected."
            )

            return

        headers = self.current_table.get(
            "headers",
            []
        )

        rows = self.current_table.get(
            "rows",
            []
        )

        if not headers:

            self.info_label.setText(
                "No columns found."
            )

            return

        # -----------------------------------------------------
        # AUTOMATIC TYPE DETECTION
        # -----------------------------------------------------

        detected_types = {}

        confidence_values = {}

        for column_index, header in enumerate(
            headers
        ):

            values = []

            for row in rows:

                if column_index < len(row):

                    values.append(
                        row[column_index]
                    )

            try:

                result = detect_column_type(
                    values
                )

                if isinstance(
                    result,
                    dict
                ):

                    detected_type = result.get(
                        "type",
                        "Text"
                    )

                    confidence = result.get(
                        "confidence",
                        0
                    )

                else:

                    detected_type = str(
                        result
                    )

                    confidence = 0

            except Exception:

                detected_type = "Text"

                confidence = 0

            detected_types[
                header
            ] = detected_type

            confidence_values[
                header
            ] = confidence

        # -----------------------------------------------------
        # EXISTING MAPPING
        # -----------------------------------------------------

        existing_mapping = (
            self.get_saved_mapping()
        )

        self.mapping_table.setRowCount(
            len(headers)
        )

        for row_index, header in enumerate(
            headers
        ):

            # Column

            column_item = QTableWidgetItem(
                str(header)
            )

            self.mapping_table.setItem(
                row_index,
                0,
                column_item
            )

            # Detected type

            detected_type = detected_types.get(
                header,
                "Text"
            )

            detected_item = QTableWidgetItem(
                str(detected_type)
            )

            self.mapping_table.setItem(
                row_index,
                1,
                detected_item
            )

            # Confidence

            confidence = confidence_values.get(
                header,
                0
            )

            if isinstance(
                confidence,
                (int, float)
            ):

                confidence_text = (
                    f"{confidence:.0f}%"
                )

            else:

                confidence_text = str(
                    confidence
                )

            confidence_item = QTableWidgetItem(
                confidence_text
            )

            confidence_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.mapping_table.setItem(
                row_index,
                2,
                confidence_item
            )

            # Mapped type

            selector = QComboBox()

            selector.addItems(
                [
                    "Text",
                    "Integer",
                    "Decimal",
                    "Date",
                    "DateTime",
                    "Boolean"
                ]
            )

            saved_type = existing_mapping.get(
                header
            )

            if saved_type in [
                "Text",
                "Integer",
                "Decimal",
                "Date",
                "DateTime",
                "Boolean"
            ]:

                selector.setCurrentText(
                    saved_type
                )

            else:

                selector.setCurrentText(
                    str(detected_type)
                )

            self.mapping_table.setCellWidget(
                row_index,
                3,
                selector
            )

            # Sample values

            samples = []

            for value in values[:3]:

                if value is None:
                    continue

                text = str(
                    value
                ).strip()

                if text and text not in samples:

                    samples.append(
                        text
                    )

            sample_text = " | ".join(
                samples
            )

            sample_item = QTableWidgetItem(
                sample_text
            )

            self.mapping_table.setItem(
                row_index,
                4,
                sample_item
            )

        self.info_label.setText(
            f"Columns: {len(headers):,}"
            f"    •    "
            f"Rows analysed: {len(rows):,}"
        )

        self.status_label.setText(
            "Automatic data type detection completed."
        )

        self.mapping_table.resizeRowsToContents()

    # =========================================================
    # GET SAVED MAPPING
    # =========================================================

    def get_saved_mapping(self):

        if not self.current_file:
            return {}

        if not self.current_table:
            return {}

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:
            return {}

        mappings = project.get(
            "mappings",
            {}
        )

        if not isinstance(
            mappings,
            dict
        ):
            return {}

        original_name = self.current_file.get(
            "original_name",
            self.current_file.get(
                "stored_name",
                ""
            )
        )

        sheet_name = self.current_table.get(
            "sheet_name",
            "Data"
        )

        mapping_key = (
            f"{original_name}||{sheet_name}"
        )

        saved = mappings.get(
            mapping_key,
            {}
        )

        if not isinstance(
            saved,
            dict
        ):
            return {}

        return saved

    # =========================================================
    # APPLY MAPPING
    # =========================================================

    def apply_mapping(self):

        if not self.state.selected_data:

            self.status_label.setText(
                "No data source selected."
            )

            return

        headers = self.state.selected_data.get(
            "headers",
            []
        )

        if not headers:

            self.status_label.setText(
                "No columns available for mapping."
            )

            return

        mapping = {}

        for row_index, header in enumerate(
            headers
        ):

            selector = self.mapping_table.cellWidget(
                row_index,
                3
            )

            if selector is not None:

                mapping[
                    header
                ] = selector.currentText()

        if not mapping:

            self.status_label.setText(
                "No mapping values found."
            )

            return

        # -----------------------------------------------------
        # UPDATE CENTRAL STATE
        # -----------------------------------------------------

        self.state.column_types = mapping

        # -----------------------------------------------------
        # SAVE TO PROJECT
        # -----------------------------------------------------

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if project:

            mappings = project.setdefault(
                "mappings",
                {}
            )

            original_name = self.current_file.get(
                "original_name",
                self.current_file.get(
                    "stored_name",
                    ""
                )
            )

            sheet_name = self.current_table.get(
                "sheet_name",
                "Data"
            )

            mapping_key = (
                f"{original_name}||{sheet_name}"
            )

            mappings[
                mapping_key
            ] = mapping

            try:

                self.main_window.project_manager.save_project(
                    project.get("name", ""),
                    project
                )

            except Exception as error:

                self.status_label.setText(
                    f"Mapping applied, but could not be saved: {error}"
                )

                return

        message = (
            f"Mapping applied successfully for "
            f"{len(mapping):,} columns."
        )

        self.status_label.setText(
            message
        )

        QMessageBox.information(
            self,
            "Mapping Applied",
            message
        )
    # =========================================================
    # CLEAR MAPPING
    # =========================================================

    def clear_mapping(self):

        if self.mapping_table.rowCount() == 0:

            return

        reply = QMessageBox.question(
            self,
            "Clear Mapping",
            "Clear the mapping for this data source?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:

            return

        for row_index in range(
            self.mapping_table.rowCount()
        ):

            selector = self.mapping_table.cellWidget(
                row_index,
                3
            )

            if selector is not None:

                selector.setCurrentText(
                    "Text"
                )

        # Clear saved project mapping

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if project and self.current_file and self.current_table:

            mappings = project.setdefault(
                "mappings",
                {}
            )

            original_name = self.current_file.get(
                "original_name",
                self.current_file.get(
                    "stored_name",
                    ""
                )
            )

            sheet_name = self.current_table.get(
                "sheet_name",
                "Data"
            )

            mapping_key = (
                f"{original_name}||{sheet_name}"
            )

            mappings.pop(
                mapping_key,
                None
            )

            try:

                self.main_window.project_manager.save_project(
                    project.get("name", ""),
                    project
                )

            except Exception:

                pass

        self.state.column_types = {}

        self.status_label.setText(
            "Mapping cleared."
        )

    # =========================================================
    # CLEAR TABLE
    # =========================================================

    def clear_table(self):

        self.mapping_table.clearContents()

        self.mapping_table.setRowCount(
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

            #mappingTable {{
                background-color: {theme.color("card_background")};
                alternate-background-color: {theme.color("table_header")};
                color: {theme.color("primary_text")};
                border: 1px solid {theme.color("border")};
                gridline-color: {theme.color("border")};
                font-size: 11px;
            }}

            #mappingTable::item {{
                padding: 4px;
            }}

            #mappingTable::item:selected {{
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
                padding: 6px;
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

            #primaryButton {{
                background-color: {theme.color("accent")};
                color: {theme.color("button_text")};
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: 600;
            }}

            #primaryButton:hover {{
                background-color: {theme.color("accent_hover")};
            }}
            """
        )