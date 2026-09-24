from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
)


class FiltersPage(QWidget):

    def __init__(self, state, main_window):

        super().__init__()

        self.state = state
        self.main_window = main_window

        self.conditions = []

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
            "Filters"
        )

        title.setObjectName(
            "sectionTitle"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        self.source_label = QLabel(
            "No data source selected."
        )

        self.source_label.setObjectName(
            "sourceLabel"
        )

        header.addWidget(
            self.source_label
        )

        layout.addLayout(
            header
        )

        # -----------------------------------------------------
        # CONDITION BUILDER
        # -----------------------------------------------------

        builder = QFrame()

        builder.setObjectName(
            "conditionBuilder"
        )

        builder_layout = QVBoxLayout(
            builder
        )

        builder_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        builder_layout.setSpacing(
            10
        )

        builder_title = QLabel(
            "Build Filter Condition"
        )

        builder_title.setObjectName(
            "builderTitle"
        )

        builder_layout.addWidget(
            builder_title
        )

        controls = QHBoxLayout()

        # -----------------------------------------------------
        # COLUMN
        # -----------------------------------------------------

        column_label = QLabel(
            "Column"
        )

        controls.addWidget(
            column_label
        )

        self.column_selector = QComboBox()

        self.column_selector.setMinimumWidth(
            180
        )

        self.column_selector.currentIndexChanged.connect(
            self.column_changed
        )

        controls.addWidget(
            self.column_selector
        )

        # -----------------------------------------------------
        # OPERATOR
        # -----------------------------------------------------

        operator_label = QLabel(
            "Condition"
        )

        controls.addWidget(
            operator_label
        )

        self.operator_selector = QComboBox()

        self.operator_selector.setMinimumWidth(
            190
        )

        self.operator_selector.currentIndexChanged.connect(
            self.operator_changed
        )

        controls.addWidget(
            self.operator_selector
        )

        # -----------------------------------------------------
        # VALUE
        # -----------------------------------------------------

        value_label = QLabel(
            "Value"
        )

        controls.addWidget(
            value_label
        )

        self.value_input = QLineEdit()

        self.value_input.setPlaceholderText(
            "Enter value"
        )

        self.value_input.setMinimumWidth(
            180
        )

        controls.addWidget(
            self.value_input
        )

        # -----------------------------------------------------
        # SECOND VALUE
        # -----------------------------------------------------

        self.second_value_input = QLineEdit()

        self.second_value_input.setPlaceholderText(
            "Second value"
        )

        self.second_value_input.setMinimumWidth(
            150
        )

        self.second_value_input.setVisible(
            False
        )

        controls.addWidget(
            self.second_value_input
        )

        # -----------------------------------------------------
        # ADD BUTTON
        # -----------------------------------------------------

        add_button = QPushButton(
            "Add Condition"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.clicked.connect(
            self.add_condition
        )

        controls.addWidget(
            add_button
        )

        builder_layout.addLayout(
            controls
        )

        layout.addWidget(
            builder
        )

        # -----------------------------------------------------
        # ACTIVE CONDITIONS
        # -----------------------------------------------------

        conditions_title = QLabel(
            "Active Conditions"
        )

        conditions_title.setObjectName(
            "subTitle"
        )

        layout.addWidget(
            conditions_title
        )

        self.conditions_table = QTableWidget()

        self.conditions_table.setColumnCount(
            4
        )

        self.conditions_table.setHorizontalHeaderLabels(
            [
                "Column",
                "Condition",
                "Value",
                "Action",
            ]
        )

        self.conditions_table.setAlternatingRowColors(
            True
        )

        self.conditions_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.conditions_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        table_header = (
            self.conditions_table
            .horizontalHeader()
        )

        table_header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        table_header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        table_header.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        table_header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        layout.addWidget(
            self.conditions_table,
            1
        )

        # -----------------------------------------------------
        # BOTTOM BUTTONS
        # -----------------------------------------------------

        bottom_layout = QHBoxLayout()

        clear_button = QPushButton(
            "Clear Conditions"
        )

        clear_button.setObjectName(
            "secondaryButton"
        )

        clear_button.clicked.connect(
            self.clear_conditions
        )

        bottom_layout.addWidget(
            clear_button
        )

        bottom_layout.addStretch()

        self.apply_button = QPushButton(
            "Apply Filters"
        )

        self.apply_button.setObjectName(
            "primaryButton"
        )

        self.apply_button.clicked.connect(
            self.apply_filters
        )

        bottom_layout.addWidget(
            self.apply_button
        )

        layout.addLayout(
            bottom_layout
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = QLabel(
            ""
        )

        self.status_label.setObjectName(
            "filterStatus"
        )

        layout.addWidget(
            self.status_label
        )

        # -----------------------------------------------------
        # STYLE
        # -----------------------------------------------------

        self.apply_style()

        self.refresh()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self.column_selector.clear()

        table = self.state.selected_data

        if not table:

            self.source_label.setText(
                "No data source selected."
            )

            self.status_label.setText(
                "Select a data source on the Data Preview page."
            )

            return

        headers = table.get(
            "headers",
            []
        )

        self.source_label.setText(
            table.get(
                "sheet_name",
                "Data"
            )
        )

        self.column_selector.addItems(
            [
                str(header)
                for header in headers
            ]
        )

        self.column_changed()

        self.refresh_conditions()

    # =========================================================
    # COLUMN CHANGED
    # =========================================================

    def column_changed(self):

        from core.filter_engine import FILTER_OPERATORS

        self.operator_selector.clear()

        self.operator_selector.addItems(
            FILTER_OPERATORS
        )

        self.operator_changed()

    # =========================================================
    # OPERATOR CHANGED
    # =========================================================

    def operator_changed(self):

        operator = (
            self.operator_selector.currentText()
        )

        needs_second_value = (
            operator == "Between"
        )

        needs_value = operator not in (
            "Is Empty",
            "Is Not Empty",
        )

        self.value_input.setVisible(
            needs_value
        )

        self.second_value_input.setVisible(
            needs_second_value
        )

    # =========================================================
    # ADD CONDITION
    # =========================================================

    def add_condition(self):

        column = (
            self.column_selector.currentText()
        )

        operator = (
            self.operator_selector.currentText()
        )

        value = (
            self.value_input.text()
        )

        second_value = (
            self.second_value_input.text()
        )

        if not column:

            return

        if operator not in (
            "Is Empty",
            "Is Not Empty",
        ):

            if not value.strip():

                self.status_label.setText(
                    "Please enter a value."
                )

                return

        condition = {
            "column": column,

            "operator": operator,

            "value": value,

            "second_value": second_value,
        }

        self.conditions.append(
            condition
        )

        self.refresh_conditions()

        self.value_input.clear()

        self.second_value_input.clear()

        self.status_label.setText(
            f"{len(self.conditions)} condition(s) defined."
        )

    # =========================================================
    # REFRESH CONDITIONS
    # =========================================================

    def refresh_conditions(self):

        self.conditions_table.clearContents()

        self.conditions_table.setRowCount(
            len(self.conditions)
        )

        for row_index, condition in enumerate(
            self.conditions
        ):

            column_item = QTableWidgetItem(
                condition.get(
                    "column",
                    ""
                )
            )

            self.conditions_table.setItem(
                row_index,
                0,
                column_item
            )

            operator_item = QTableWidgetItem(
                condition.get(
                    "operator",
                    ""
                )
            )

            self.conditions_table.setItem(
                row_index,
                1,
                operator_item
            )

            value = condition.get(
                "value",
                ""
            )

            if condition.get(
                "operator"
            ) == "Between":

                value = (
                    f"{value}"
                    f"  →  "
                    f"{condition.get('second_value', '')}"
                )

            value_item = QTableWidgetItem(
                value
            )

            self.conditions_table.setItem(
                row_index,
                2,
                value_item
            )

            remove_button = QPushButton(
                "Remove"
            )

            remove_button.setObjectName(
                "removeConditionButton"
            )

            remove_button.clicked.connect(
                lambda checked=False,
                index=row_index:
                    self.remove_condition(index)
            )

            self.conditions_table.setCellWidget(
                row_index,
                3,
                remove_button
            )

    # =========================================================
    # REMOVE CONDITION
    # =========================================================

    def remove_condition(
        self,
        index
    ):

        if (
            index < 0
            or index >= len(self.conditions)
        ):

            return

        self.conditions.pop(
            index
        )

        self.refresh_conditions()

        self.status_label.setText(
            f"{len(self.conditions)} condition(s) defined."
        )

    # =========================================================
    # CLEAR CONDITIONS
    # =========================================================

    def clear_conditions(self):

        self.conditions.clear()

        self.refresh_conditions()

        self.status_label.setText(
            "All filter conditions cleared."
        )

    # =========================================================
    # APPLY FILTERS
    # =========================================================

    def apply_filters(self):

        if not self.state.selected_data:

            self.status_label.setText(
                "No data source selected."
            )

            return

        self.state.filter_conditions = (
            list(
                self.conditions
            )
        )

        self.status_label.setText(
            f"{len(self.conditions)} condition(s) "
            "ready to be applied."
        )

    # =========================================================
    # STYLE
    # =========================================================

    def apply_style(self):

        self.setStyleSheet("""

        #sectionTitle {

            font-size: 22px;

            font-weight: 700;

            color: #20242a;
        }


        #sourceLabel {

            color: #68717b;

            font-size: 13px;
        }


        #conditionBuilder {

            background-color: white;

            border: 1px solid #dfe3e7;

            border-radius: 8px;
        }


        #builderTitle {

            font-size: 15px;

            font-weight: 600;

            color: #343a40;
        }


        #subTitle {

            font-size: 15px;

            font-weight: 600;

            color: #343a40;
        }


        #filterStatus {

            color: #737c86;

            font-size: 12px;
        }


        QComboBox {

            background-color: white;

            border: 1px solid #d9dde2;

            border-radius: 6px;

            padding: 7px;

            min-height: 20px;
        }


        QComboBox:hover {

            border: 1px solid #bfc5cc;
        }


        QLineEdit {

            background-color: white;

            border: 1px solid #d9dde2;

            border-radius: 6px;

            padding: 8px;
        }


        QLineEdit:focus {

            border: 1px solid #aeb5bc;
        }


        #primaryButton {

            background-color: #343a40;

            color: white;

            border: none;

            border-radius: 6px;

            padding: 9px 18px;

            font-weight: 600;
        }


        #primaryButton:hover {

            background-color: #24282c;
        }


        #secondaryButton {

            background-color: white;

            color: #4d555e;

            border: 1px solid #d7dce1;

            border-radius: 6px;

            padding: 8px 15px;
        }


        #secondaryButton:hover {

            background-color: #f0f2f4;
        }


        #removeConditionButton {

            background-color: white;

            color: #59636d;

            border: 1px solid #d7dce1;

            border-radius: 5px;

            padding: 5px 10px;
        }


        #removeConditionButton:hover {

            background-color: #f0f2f4;
        }


        QTableWidget {

            background-color: white;

            border: 1px solid #dfe3e7;

            gridline-color: #edf0f2;

            alternate-background-color: #f8f9fa;

            selection-background-color: #e5e8eb;

            selection-color: #20242a;
        }


        QHeaderView::section {

            background-color: #eef1f4;

            color: #3c444d;

            padding: 9px;

            border: none;

            border-right: 1px solid #dfe3e7;

            border-bottom: 1px solid #dfe3e7;

            font-weight: 600;
        }

        """)