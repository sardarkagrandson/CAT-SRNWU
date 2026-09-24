from pathlib import Path
import shutil

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
    QScrollArea,
)

from core.file_loader import load_file


class UploadPage(QWidget):

    def __init__(
        self,
        state,
        main_window
    ):

        super().__init__()

        self.state = state
        self.main_window = main_window

        self.uploaded_files = []

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

        layout.setSpacing(18)

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        self.title_label = QLabel(
            "Upload Files"
        )

        self.title_label.setObjectName(
            "sectionTitle"
        )

        header.addWidget(
            self.title_label
        )

        header.addStretch()

        self.add_button = QPushButton(
            "+ Add Files"
        )

        self.add_button.setObjectName(
            "primaryButton"
        )

        self.add_button.clicked.connect(
            self.select_files
        )

        header.addWidget(
            self.add_button
        )

        layout.addLayout(
            header
        )

        # -----------------------------------------------------
        # PROJECT INFORMATION
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
        # INFORMATION
        # -----------------------------------------------------

        information = QLabel(
            "Supported files: CSV, TXT, XLSX and XLS"
        )

        information.setObjectName(
            "description"
        )

        layout.addWidget(
            information
        )

        # -----------------------------------------------------
        # FILE AREA
        # -----------------------------------------------------

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setObjectName(
            "fileScrollArea"
        )

        self.file_container = QWidget()

        self.file_layout = QVBoxLayout(
            self.file_container
        )

        self.file_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.file_layout.setSpacing(
            10
        )

        self.file_layout.addStretch()

        self.scroll_area.setWidget(
            self.file_container
        )

        layout.addWidget(
            self.scroll_area,
            1
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = QLabel(
            "No files uploaded."
        )

        self.status_label.setObjectName(
            "statusLabel"
        )

        layout.addWidget(
            self.status_label
        )

        # Apply central theme
        self.apply_theme()

        self.refresh()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self.update_project_information()

        self.load_project_files()

        self.refresh_file_cards()

    # =========================================================
    # UPDATE PROJECT INFORMATION
    # =========================================================

    def update_project_information(self):

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if project:

            self.project_label.setText(
                f"Current Project: "
                f"{project.get('name', '')}"
            )

            self.add_button.setEnabled(
                True
            )

        else:

            self.project_label.setText(
                "No project selected — "
                "open a project before uploading files."
            )

            self.add_button.setEnabled(
                False
            )

    # =========================================================
    # LOAD PROJECT FILES
    # =========================================================

    def load_project_files(self):

        self.uploaded_files = []

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            return

        self.uploaded_files = list(
            project.get(
                "files",
                []
            )
        )

        # Keep application state in sync

        self.state.uploaded_files = (
            self.uploaded_files.copy()
        )

    # =========================================================
    # SELECT FILES
    # =========================================================

    def select_files(self):

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            QMessageBox.warning(
                self,
                "No Project Selected",
                (
                    "Please open a project before "
                    "uploading files."
                )
            )

            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Data Files",
            "",
            (
                "Data Files "
                "(*.csv *.txt *.xlsx *.xls);;"
                "CSV Files (*.csv);;"
                "Text Files (*.txt);;"
                "Excel Files (*.xlsx *.xls);;"
                "All Files (*.*)"
            )
        )

        if not files:

            return

        successful = 0

        for file_path in files:

            try:

                if self.add_file_to_project(
                    file_path
                ):

                    successful += 1

            except Exception as error:

                QMessageBox.critical(
                    self,
                    "Upload Error",
                    (
                        f"Could not upload:\n\n"
                        f"{file_path}\n\n"
                        f"{error}"
                    )
                )

        self.refresh()

        self.status_label.setText(
            f"{successful} "
            f"{'file' if successful == 1 else 'files'} "
            f"added and loaded into the project."
        )

    # =========================================================
    # ADD FILE TO PROJECT
    # =========================================================

    def add_file_to_project(
        self,
        file_path
    ):

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            return False

        source = Path(
            file_path
        )

        # -----------------------------------------------------
        # CHECK DUPLICATE
        # -----------------------------------------------------

        for existing in project.get(
            "files",
            []
        ):

            if (
                existing.get("original_name")
                == source.name
            ):

                QMessageBox.information(
                    self,
                    "File Already Added",
                    (
                        f"The file '{source.name}' "
                        f"is already part of this project."
                    )
                )

                return False

        # -----------------------------------------------------
        # PROJECT DATA FOLDER
        # -----------------------------------------------------

        data_path = (
            self.main_window
            .project_manager
            .get_data_path(
                project["name"]
            )
        )

        destination = (
            data_path / source.name
        )

        # -----------------------------------------------------
        # HANDLE EXISTING STORED FILE
        # -----------------------------------------------------

        if destination.exists():

            stem = source.stem
            suffix = source.suffix

            counter = 1

            while True:

                new_name = (
                    f"{stem}_{counter}"
                    f"{suffix}"
                )

                destination = (
                    data_path / new_name
                )

                if not destination.exists():

                    break

                counter += 1

        # -----------------------------------------------------
        # COPY FILE
        # -----------------------------------------------------

        shutil.copy2(
            source,
            destination
        )

        # -----------------------------------------------------
        # LOAD THE STORED FILE
        # -----------------------------------------------------

        try:

            tables = load_file(
                str(destination)
            )

        except Exception:

            # Remove the copied file if loading failed

            if destination.exists():

                destination.unlink()

            raise

        # -----------------------------------------------------
        # FILE INFORMATION
        # -----------------------------------------------------

        file_information = {

            "original_name":
                source.name,

            "stored_name":
                destination.name,

            "original_path":
                str(source),

            "stored_path":
                str(destination),

            "extension":
                source.suffix.lower(),

            "size":
                source.stat().st_size,

            "added":
                self.get_current_datetime(),

            "tables":
                tables,

            "loaded":
                True,
        }

        # -----------------------------------------------------
        # ADD TO PROJECT
        # -----------------------------------------------------

        if "files" not in project:

            project["files"] = []

        project["files"].append(
            file_information
        )

        # -----------------------------------------------------
        # SAVE PROJECT
        # -----------------------------------------------------

        self.main_window.project_manager.save_project(
            project["name"],
            project
        )

        # -----------------------------------------------------
        # UPDATE APPLICATION STATE
        # -----------------------------------------------------

        self.main_window.current_project = (
            project
        )

        self.state.uploaded_files = (
            project["files"].copy()
        )

        # -----------------------------------------------------
        # SELECT FIRST TABLE
        # -----------------------------------------------------

        if tables:

            self.state.selected_file = (
                file_information
            )

            self.state.selected_sheet = (
                tables[0]
                .get("sheet_name")
            )

            self.state.selected_data = (
                tables[0]
            )

        return True

    # =========================================================
    # REMOVE FILE
    # =========================================================

    def remove_file(
        self,
        stored_name
    ):

        project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if not project:

            return

        file_record = None

        for record in project.get(
            "files",
            []
        ):

            if record.get(
                "stored_name"
            ) == stored_name:

                file_record = record
                break

        if not file_record:

            return

        answer = QMessageBox.question(
            self,
            "Remove File",
            (
                f"Remove "
                f"'{file_record.get('original_name')}' "
                f"from this project?"
            ),
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        # -----------------------------------------------------
        # DELETE STORED FILE
        # -----------------------------------------------------

        stored_path = Path(
            file_record.get(
                "stored_path",
                ""
            )
        )

        if stored_path.exists():

            stored_path.unlink()

        # -----------------------------------------------------
        # REMOVE RECORD
        # -----------------------------------------------------

        project["files"] = [

            record

            for record in project.get(
                "files",
                []
            )

            if record.get(
                "stored_name"
            ) != stored_name
        ]

        # -----------------------------------------------------
        # SAVE PROJECT
        # -----------------------------------------------------

        self.main_window.project_manager.save_project(
            project["name"],
            project
        )

        self.main_window.current_project = (
            project
        )

        self.state.uploaded_files = (
            project["files"].copy()
        )

        self.state.selected_file = None
        self.state.selected_sheet = None
        self.state.selected_data = None

        self.refresh()

        self.status_label.setText(
            "File removed from project."
        )

    # =========================================================
    # REFRESH FILE CARDS
    # =========================================================

    def refresh_file_cards(self):

        while (
            self.file_layout.count()
            > 1
        ):

            item = (
                self.file_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

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

        if not files:

            empty = QLabel(
                "No files uploaded to this project yet."
            )

            empty.setObjectName(
                "emptyLabel"
            )

            empty.setAlignment(
                Qt.AlignCenter
            )

            self.file_layout.insertWidget(
                0,
                empty
            )

            return

        for file_record in files:

            card = self.create_file_card(
                file_record
            )

            self.file_layout.insertWidget(
                self.file_layout.count() - 1,
                card
            )

    # =========================================================
    # CREATE FILE CARD
    # =========================================================

    def create_file_card(
        self,
        file_record
    ):

        card = QFrame()

        card.setObjectName(
            "fileCard"
        )

        card_layout = QHBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            15,
            12,
            15,
            12
        )

        information = QVBoxLayout()

        name = QLabel(
            file_record.get(
                "original_name",
                ""
            )
        )

        name.setObjectName(
            "fileName"
        )

        information.addWidget(
            name
        )

        extension = file_record.get(
            "extension",
            ""
        ).upper()

        size = self.format_file_size(
            file_record.get(
                "size",
                0
            )
        )

        details = QLabel(
            f"{extension}  •  {size}"
        )

        details.setObjectName(
            "fileDetails"
        )

        information.addWidget(
            details
        )

        tables = file_record.get(
            "tables",
            []
        )

        table_count = len(
            tables
        )

        table_text = (
            f"{table_count} "
            f"{'table' if table_count == 1 else 'tables'}"
        )

        loaded = QLabel(
            f"{table_text}  •  Loaded successfully"
        )

        loaded.setObjectName(
            "fileStored"
        )

        information.addWidget(
            loaded
        )

        card_layout.addLayout(
            information,
            1
        )

        remove_button = QPushButton(
            "Remove"
        )

        remove_button.setObjectName(
            "secondaryButton"
        )

        remove_button.clicked.connect(
            lambda checked=False,
            stored_name=file_record.get(
                "stored_name"
            ):
                self.remove_file(
                    stored_name
                )
        )

        card_layout.addWidget(
            remove_button
        )

        return card

    # =========================================================
    # FORMAT FILE SIZE
    # =========================================================

    def format_file_size(
        self,
        size
    ):

        try:

            size = float(
                size
            )

        except (
            TypeError,
            ValueError
        ):

            return "Unknown size"

        if size < 1024:

            return f"{size:.0f} B"

        if size < 1024 * 1024:

            return (
                f"{size / 1024:.1f} KB"
            )

        if size < 1024 * 1024 * 1024:

            return (
                f"{size / (1024 * 1024):.1f} MB"
            )

        return (
            f"{size / (1024 * 1024 * 1024):.1f} GB"
        )

    # =========================================================
    # CURRENT DATETIME
    # =========================================================

    def get_current_datetime(self):

        from datetime import datetime

        return datetime.now().isoformat(
            timespec="seconds"
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

            #description {{
                color: {theme.color("muted_text")};
                font-size: 12px;
            }}

            #fileScrollArea {{
                background-color: transparent;
                border: none;
            }}

            #fileCard {{
                background-color: {theme.color("card_background")};
                border: 1px solid {theme.color("border")};
                border-radius: 8px;
            }}

            #fileCard:hover {{
                border: 1px solid {theme.color("input_border")};
            }}

            #fileName {{
                color: {theme.color("primary_text")};
                font-size: 14px;
                font-weight: 600;
            }}

            #fileDetails {{
                color: {theme.color("secondary_text")};
                font-size: 11px;
            }}

            #fileStored {{
                color: {theme.color("muted_text")};
                font-size: 10px;
            }}

            #emptyLabel {{
                color: {theme.color("muted_text")};
                font-size: 14px;
                padding: 40px;
            }}

            #statusLabel {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
            }}

            #primaryButton {{
                background-color: {theme.color("accent")};
                color: {theme.color("button_text")};
                border: none;
                border-radius: 6px;
                padding: 9px 18px;
                font-weight: 600;
            }}

            #primaryButton:hover {{
                background-color: {theme.color("accent_hover")};
            }}

            #primaryButton:disabled {{
                background-color: {theme.color("border")};
                color: {theme.color("muted_text")};
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