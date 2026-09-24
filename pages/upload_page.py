from pathlib import Path
import shutil

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLabel,
    QPushButton,
    QCheckBox,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QFrame,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
)

from core.file_loader import load_file
from core import folder_manager
from widgets.common import NO_PROJECT_MESSAGE


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

        self.current_folder_id = folder_manager.ROOT_FOLDER_ID

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

        self.project_label.setWordWrap(
            True
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
        # SPLITTER: FOLDERS (LEFT) / FILES (RIGHT)
        # -----------------------------------------------------

        splitter = QSplitter(
            Qt.Horizontal
        )

        splitter.setObjectName(
            "dataManagementSplitter"
        )

        # -------------------------------------------------
        # FOLDERS PANEL
        # -------------------------------------------------

        folders_panel = QWidget()

        folders_layout = QVBoxLayout(
            folders_panel
        )

        folders_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        folders_layout.setSpacing(
            8
        )

        folders_title = QLabel(
            "Data Management"
        )

        folders_title.setObjectName(
            "panelTitle"
        )

        folders_layout.addWidget(
            folders_title
        )

        self.folder_tree = QTreeWidget()

        self.folder_tree.setObjectName(
            "folderTree"
        )

        self.folder_tree.setHeaderHidden(
            True
        )

        self.folder_tree.itemSelectionChanged.connect(
            self.folder_selection_changed
        )

        folders_layout.addWidget(
            self.folder_tree,
            1
        )

        folder_toolbar = QHBoxLayout()

        folder_toolbar.setSpacing(
            6
        )

        self.new_folder_button = QPushButton(
            "New Folder"
        )

        self.new_folder_button.setObjectName(
            "secondaryButton"
        )

        self.new_folder_button.clicked.connect(
            self.create_new_folder
        )

        folder_toolbar.addWidget(
            self.new_folder_button
        )

        self.rename_folder_button = QPushButton(
            "Rename"
        )

        self.rename_folder_button.setObjectName(
            "secondaryButton"
        )

        self.rename_folder_button.clicked.connect(
            self.rename_selected_folder
        )

        folder_toolbar.addWidget(
            self.rename_folder_button
        )

        self.delete_folder_button = QPushButton(
            "Delete"
        )

        self.delete_folder_button.setObjectName(
            "dangerButton"
        )

        self.delete_folder_button.clicked.connect(
            self.delete_selected_folder
        )

        folder_toolbar.addWidget(
            self.delete_folder_button
        )

        folders_layout.addLayout(
            folder_toolbar
        )

        second_toolbar = QHBoxLayout()

        second_toolbar.setSpacing(
            6
        )

        self.add_button = QPushButton(
            "Upload"
        )

        self.add_button.setObjectName(
            "primaryButton"
        )

        self.add_button.clicked.connect(
            self.select_files
        )

        second_toolbar.addWidget(
            self.add_button
        )

        refresh_button = QPushButton(
            "Refresh"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        second_toolbar.addWidget(
            refresh_button
        )

        folders_layout.addLayout(
            second_toolbar
        )

        splitter.addWidget(
            folders_panel
        )

        # -------------------------------------------------
        # FILES PANEL
        # -------------------------------------------------

        files_panel = QWidget()

        files_layout = QVBoxLayout(
            files_panel
        )

        files_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        files_layout.setSpacing(
            10
        )

        self.breadcrumb_label = QLabel(
            "Location: Root"
        )

        self.breadcrumb_label.setObjectName(
            "breadcrumbLabel"
        )

        files_layout.addWidget(
            self.breadcrumb_label
        )

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

        files_layout.addWidget(
            self.scroll_area,
            1
        )

        splitter.addWidget(
            files_panel
        )

        splitter.setStretchFactor(
            0,
            0
        )

        splitter.setStretchFactor(
            1,
            1
        )

        splitter.setSizes(
            [
                260,
                640
            ]
        )

        layout.addWidget(
            splitter,
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

        project = self.get_current_project()

        self.update_project_information(
            project
        )

        if not project:

            self.current_folder_id = (
                folder_manager.ROOT_FOLDER_ID
            )

        self.refresh_folder_tree(
            project
        )

        self.load_project_files(
            project
        )

        self.refresh_file_cards(
            project
        )

    # =========================================================
    # GET CURRENT PROJECT
    # =========================================================

    def get_current_project(self):

        return getattr(
            self.main_window,
            "current_project",
            None
        )

    # =========================================================
    # UPDATE PROJECT INFORMATION
    # =========================================================

    def update_project_information(
        self,
        project
    ):

        if project:

            self.project_label.setText(
                f"Current Project: "
                f"{project.get('name', '')}"
            )

            self.add_button.setEnabled(
                True
            )

            self.new_folder_button.setEnabled(
                True
            )

            self.rename_folder_button.setEnabled(
                True
            )

            self.delete_folder_button.setEnabled(
                True
            )

        else:

            self.project_label.setText(
                NO_PROJECT_MESSAGE
            )

            self.add_button.setEnabled(
                False
            )

            self.new_folder_button.setEnabled(
                False
            )

            self.rename_folder_button.setEnabled(
                False
            )

            self.delete_folder_button.setEnabled(
                False
            )

    # =========================================================
    # LOAD PROJECT FILES
    # =========================================================

    def load_project_files(
        self,
        project
    ):

        self.uploaded_files = []

        if not project:

            self.state.uploaded_files = []

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
    # FOLDER TREE
    # =========================================================

    def refresh_folder_tree(
        self,
        project
    ):

        self.folder_tree.blockSignals(
            True
        )

        self.folder_tree.clear()

        root_item = QTreeWidgetItem(
            [
                "\U0001F4C1  All Files"
            ]
        )

        root_item.setData(
            0,
            Qt.UserRole,
            folder_manager.ROOT_FOLDER_ID
        )

        self.folder_tree.addTopLevelItem(
            root_item
        )

        selected_item = root_item

        if project:

            tree = folder_manager.build_folder_tree(
                project
            )

            selected_item = (
                self.populate_folder_items(
                    root_item,
                    tree
                )
                or root_item
            )

        self.folder_tree.expandAll()

        self.folder_tree.setCurrentItem(
            selected_item
        )

        self.folder_tree.blockSignals(
            False
        )

        self.current_folder_id = selected_item.data(
            0,
            Qt.UserRole
        )

    # =========================================================
    # POPULATE FOLDER ITEMS (RECURSIVE)
    # =========================================================

    def populate_folder_items(
        self,
        parent_item,
        nodes
    ):

        match = None

        for node in nodes:

            item = QTreeWidgetItem(
                [
                    f"\U0001F4C1  {node['name']}"
                ]
            )

            item.setData(
                0,
                Qt.UserRole,
                node["id"]
            )

            parent_item.addChild(
                item
            )

            if node["id"] == self.current_folder_id:

                match = item

            child_match = self.populate_folder_items(
                item,
                node["children"]
            )

            if child_match:

                match = child_match

        return match

    # =========================================================
    # FOLDER SELECTION CHANGED
    # =========================================================

    def folder_selection_changed(self):

        items = self.folder_tree.selectedItems()

        if not items:

            return

        self.current_folder_id = items[0].data(
            0,
            Qt.UserRole
        )

        project = self.get_current_project()

        self.refresh_file_cards(
            project
        )

    # =========================================================
    # CURRENT FOLDER ID FROM SELECTION (FOR CREATING SUBFOLDERS)
    # =========================================================

    def get_selected_folder_id(self):

        items = self.folder_tree.selectedItems()

        if not items:

            return folder_manager.ROOT_FOLDER_ID

        return items[0].data(
            0,
            Qt.UserRole
        )

    # =========================================================
    # CREATE NEW FOLDER
    # =========================================================

    def create_new_folder(self):

        project = self.get_current_project()

        if not project:

            QMessageBox.warning(
                self,
                "No Project Selected",
                "Please open a project first."
            )

            return

        parent_id = self.get_selected_folder_id()

        name, accepted = QInputDialog.getText(
            self,
            "New Folder",
            "Folder name:"
        )

        if not accepted:

            return

        try:

            folder_manager.create_folder(
                project,
                name,
                parent_id=parent_id
            )

        except (
            ValueError,
            FileExistsError
        ) as error:

            QMessageBox.warning(
                self,
                "New Folder",
                str(error)
            )

            return

        self.save_project(
            project
        )

        self.refresh_folder_tree(
            project
        )

        self.refresh_file_cards(
            project
        )

        self.status_label.setText(
            f"Folder '{name.strip()}' created."
        )

    # =========================================================
    # RENAME SELECTED FOLDER
    # =========================================================

    def rename_selected_folder(self):

        project = self.get_current_project()

        if not project:

            return

        folder_id = self.get_selected_folder_id()

        if folder_id is None:

            QMessageBox.information(
                self,
                "Rename Folder",
                "Select a folder to rename (the 'All Files' "
                "root cannot be renamed)."
            )

            return

        folder = folder_manager.find_folder(
            project,
            folder_id
        )

        if not folder:

            return

        new_name, accepted = QInputDialog.getText(
            self,
            "Rename Folder",
            "Folder name:",
            text=folder.get("name", "")
        )

        if not accepted:

            return

        try:

            folder_manager.rename_folder(
                project,
                folder_id,
                new_name
            )

        except (
            ValueError,
            FileExistsError
        ) as error:

            QMessageBox.warning(
                self,
                "Rename Folder",
                str(error)
            )

            return

        self.save_project(
            project
        )

        self.refresh_folder_tree(
            project
        )

        self.status_label.setText(
            "Folder renamed."
        )

    # =========================================================
    # DELETE SELECTED FOLDER
    # =========================================================

    def delete_selected_folder(self):

        project = self.get_current_project()

        if not project:

            return

        folder_id = self.get_selected_folder_id()

        if folder_id is None:

            QMessageBox.information(
                self,
                "Delete Folder",
                "Select a folder to delete (the 'All Files' "
                "root cannot be deleted)."
            )

            return

        folder = folder_manager.find_folder(
            project,
            folder_id
        )

        if not folder:

            return

        answer = QMessageBox.question(
            self,
            "Delete Folder",
            (
                f"Delete the folder '{folder.get('name')}'?\n\n"
                "Any files and subfolders directly inside it "
                "will be moved up one level rather than being "
                "deleted."
            ),
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        parent_id = folder.get(
            "parent_id"
        )

        folder_manager.delete_folder(
            project,
            folder_id
        )

        self.current_folder_id = parent_id

        self.save_project(
            project
        )

        self.refresh_folder_tree(
            project
        )

        self.refresh_file_cards(
            project
        )

        self.status_label.setText(
            "Folder deleted."
        )

    # =========================================================
    # SAVE PROJECT (AND KEEP MAIN WINDOW / STATE IN SYNC)
    # =========================================================

    def save_project(
        self,
        project
    ):

        self.main_window.project_manager.save_project(
            project["name"],
            project
        )

        self.main_window.current_project = project

        self.state.uploaded_files = (
            project.get(
                "files",
                []
            ).copy()
        )

    # =========================================================
    # SELECT FILES (UPLOAD INTO CURRENT FOLDER)
    # =========================================================

    def select_files(self):

        project = self.get_current_project()

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
                    project,
                    file_path,
                    self.current_folder_id
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
        project,
        file_path,
        folder_id
    ):

        source = Path(
            file_path
        )

        # -----------------------------------------------------
        # CHECK DUPLICATE (SAME NAME, SAME FOLDER)
        # -----------------------------------------------------

        for existing in project.get(
            "files",
            []
        ):

            if (
                existing.get("original_name") == source.name
                and existing.get("folder_id") == folder_id
            ):

                QMessageBox.information(
                    self,
                    "File Already Added",
                    (
                        f"The file '{source.name}' "
                        f"is already in this folder."
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

        destination = self.unique_destination(
            data_path,
            source.name
        )

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

            "folder_id":
                folder_id,
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

        self.save_project(
            project
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
    # UNIQUE DESTINATION FILENAME
    # =========================================================

    def unique_destination(
        self,
        data_path,
        file_name
    ):

        source = Path(
            file_name
        )

        destination = (
            data_path / source.name
        )

        if not destination.exists():

            return destination

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

                return destination

            counter += 1

    # =========================================================
    # REMOVE FILE
    # =========================================================

    def remove_file(
        self,
        stored_name
    ):

        project = self.get_current_project()

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

        self.save_project(
            project
        )

        self.state.selected_file = None
        self.state.selected_sheet = None
        self.state.selected_data = None

        self.refresh_file_cards(
            project
        )

        self.status_label.setText(
            "File removed from project."
        )

    # =========================================================
    # OPEN FILE
    # =========================================================

    def open_file(
        self,
        file_record
    ):

        stored_path = file_record.get(
            "stored_path",
            ""
        )

        if not stored_path or not Path(
            stored_path
        ).exists():

            QMessageBox.warning(
                self,
                "Open File",
                "The stored file could not be found on disk."
            )

            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                stored_path
            )
        )

    # =========================================================
    # SHOW FILE INFORMATION
    # =========================================================

    def show_file_information(
        self,
        project,
        file_record
    ):

        tables = file_record.get(
            "tables",
            []
        )

        folder_path = folder_manager.get_folder_path(
            project,
            file_record.get("folder_id")
        )

        location = (
            " / ".join(
                [
                    "Root"
                ]
                + folder_path
            )
        )

        message = (
            f"Name: {file_record.get('original_name', '')}\n"
            f"Location: {location}\n"
            f"Type: {file_record.get('extension', '').upper()}\n"
            f"Size: {self.format_file_size(file_record.get('size', 0))}\n"
            f"Added: {file_record.get('added', '')}\n"
            f"Sheets/Tables: {len(tables)}\n"
            f"Stored path: {file_record.get('stored_path', '')}"
        )

        QMessageBox.information(
            self,
            "File Information",
            message
        )

    # =========================================================
    # MOVE / COPY FILE — CHOOSE DESTINATION FOLDER
    # =========================================================

    def choose_destination_folder(
        self,
        project,
        title
    ):

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            title
        )

        dialog.setMinimumWidth(
            400
        )

        dialog.setModal(
            True
        )

        layout = QVBoxLayout(
            dialog
        )

        label = QLabel(
            "Destination folder:"
        )

        layout.addWidget(
            label
        )

        combo = QComboBox()

        combo.addItem(
            "Root (no folder)",
            folder_manager.ROOT_FOLDER_ID
        )

        for folder_id, display_name in (
            self.flatten_folder_names(
                project
            )
        ):

            combo.addItem(
                display_name,
                folder_id
            )

        layout.addWidget(
            combo
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
            | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(
            buttons
        )

        if dialog.exec() != QDialog.Accepted:

            return None, False

        return combo.currentData(), True

    # =========================================================
    # FLATTEN FOLDER NAMES (FOR THE DESTINATION PICKER)
    # =========================================================

    def flatten_folder_names(
        self,
        project,
        parent_id=None,
        depth=0
    ):

        result = []

        for folder in folder_manager.get_child_folders(
            project,
            parent_id
        ):

            indent = "    " * depth

            result.append(
                (
                    folder["id"],
                    f"{indent}{folder['name']}"
                )
            )

            result.extend(
                self.flatten_folder_names(
                    project,
                    folder["id"],
                    depth + 1
                )
            )

        return result

    # =========================================================
    # MOVE FILE
    # =========================================================

    def move_file(
        self,
        file_record
    ):

        project = self.get_current_project()

        if not project:

            return

        target_folder_id, accepted = (
            self.choose_destination_folder(
                project,
                "Move File"
            )
        )

        if not accepted:

            return

        folder_manager.move_file_to_folder(
            project,
            file_record,
            target_folder_id
        )

        self.save_project(
            project
        )

        self.refresh_file_cards(
            project
        )

        self.status_label.setText(
            f"'{file_record.get('original_name')}' moved."
        )

    # =========================================================
    # COPY FILE
    # =========================================================

    def copy_file(
        self,
        file_record
    ):

        project = self.get_current_project()

        if not project:

            return

        target_folder_id, accepted = (
            self.choose_destination_folder(
                project,
                "Copy File"
            )
        )

        if not accepted:

            return

        source_path = Path(
            file_record.get(
                "stored_path",
                ""
            )
        )

        if not source_path.exists():

            QMessageBox.warning(
                self,
                "Copy File",
                "The stored file could not be found on disk."
            )

            return

        data_path = (
            self.main_window
            .project_manager
            .get_data_path(
                project["name"]
            )
        )

        destination = self.unique_destination(
            data_path,
            source_path.name
        )

        shutil.copy2(
            source_path,
            destination
        )

        try:

            tables = load_file(
                str(destination)
            )

        except Exception as error:

            if destination.exists():

                destination.unlink()

            QMessageBox.critical(
                self,
                "Copy File",
                f"Could not load the copied file:\n\n{error}"
            )

            return

        file_information = {

            "original_name":
                file_record.get("original_name", destination.name),

            "stored_name":
                destination.name,

            "original_path":
                file_record.get("original_path", str(source_path)),

            "stored_path":
                str(destination),

            "extension":
                destination.suffix.lower(),

            "size":
                destination.stat().st_size,

            "added":
                self.get_current_datetime(),

            "tables":
                tables,

            "loaded":
                True,

            "folder_id":
                target_folder_id,
        }

        project.setdefault(
            "files",
            []
        ).append(
            file_information
        )

        self.save_project(
            project
        )

        self.refresh_file_cards(
            project
        )

        self.status_label.setText(
            f"'{file_record.get('original_name')}' copied."
        )

    # =========================================================
    # TOGGLE FILE SELECTION FOR ANALYSIS
    # =========================================================

    def toggle_analysis_selection(
        self,
        stored_name,
        checked
    ):

        selected = self.state.selected_analysis_files

        if checked:

            if stored_name not in selected:

                selected.append(
                    stored_name
                )

        else:

            if stored_name in selected:

                selected.remove(
                    stored_name
                )

    # =========================================================
    # REFRESH FILE CARDS
    # =========================================================

    def refresh_file_cards(
        self,
        project
    ):

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

                # Detach immediately so it disappears from view
                # right away rather than waiting for the deferred
                # deleteLater() cleanup to run.

                widget.setParent(
                    None
                )

                widget.deleteLater()

        if not project:

            self.breadcrumb_label.setText(
                "Location: —"
            )

            return

        folder_path = folder_manager.get_folder_path(
            project,
            self.current_folder_id
        )

        self.breadcrumb_label.setText(
            "Location: "
            + " / ".join(
                [
                    "Root"
                ]
                + folder_path
            )
        )

        files = folder_manager.get_files_in_folder(
            project,
            self.current_folder_id
        )

        if not files:

            empty = QLabel(
                "No files in this folder yet."
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
                project,
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
        project,
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

        # -----------------------------------------------------
        # SELECT FOR ANALYSIS
        # -----------------------------------------------------

        select_box = QCheckBox()

        select_box.setObjectName(
            "analysisCheckbox"
        )

        select_box.setToolTip(
            "Select for analysis"
        )

        select_box.setChecked(
            file_record.get("stored_name")
            in self.state.selected_analysis_files
        )

        select_box.toggled.connect(
            lambda checked=False,
            stored_name=file_record.get("stored_name"):
                self.toggle_analysis_selection(
                    stored_name,
                    checked
                )
        )

        card_layout.addWidget(
            select_box
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

        # -----------------------------------------------------
        # ACTION BUTTONS
        # -----------------------------------------------------

        open_button = QPushButton(
            "Open"
        )

        open_button.setObjectName(
            "secondaryButton"
        )

        open_button.clicked.connect(
            lambda checked=False,
            record=file_record:
                self.open_file(
                    record
                )
        )

        card_layout.addWidget(
            open_button
        )

        info_button = QPushButton(
            "Info"
        )

        info_button.setObjectName(
            "secondaryButton"
        )

        info_button.clicked.connect(
            lambda checked=False,
            record=file_record:
                self.show_file_information(
                    project,
                    record
                )
        )

        card_layout.addWidget(
            info_button
        )

        move_button = QPushButton(
            "Move"
        )

        move_button.setObjectName(
            "secondaryButton"
        )

        move_button.clicked.connect(
            lambda checked=False,
            record=file_record:
                self.move_file(
                    record
                )
        )

        card_layout.addWidget(
            move_button
        )

        copy_button = QPushButton(
            "Copy"
        )

        copy_button.setObjectName(
            "secondaryButton"
        )

        copy_button.clicked.connect(
            lambda checked=False,
            record=file_record:
                self.copy_file(
                    record
                )
        )

        card_layout.addWidget(
            copy_button
        )

        remove_button = QPushButton(
            "Remove"
        )

        remove_button.setObjectName(
            "dangerButton"
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

            #panelTitle {{
                color: {theme.color("primary_text")};
                font-size: 13px;
                font-weight: 700;
            }}

            #breadcrumbLabel {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
                font-weight: 600;
            }}

            #folderTree {{
                background-color: {theme.color("card_background")};
                color: {theme.color("primary_text")};
                border: 1px solid {theme.color("border")};
                border-radius: 6px;
                font-size: 12px;
            }}

            #folderTree::item {{
                padding: 5px;
            }}

            #folderTree::item:selected {{
                background-color: {theme.color("table_selected")};
                color: {theme.color("primary_text")};
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
                padding: 6px 12px;
            }}

            #secondaryButton:hover {{
                background-color: {theme.color("table_header")};
            }}

            #secondaryButton:disabled {{
                color: {theme.color("muted_text")};
            }}

            #dangerButton {{
                background-color: {theme.color("input_background")};
                color: {theme.color("danger_text")};
                border: 1px solid {theme.color("danger_border")};
                border-radius: 6px;
                padding: 6px 12px;
            }}

            #dangerButton:hover {{
                background-color: #f7eeee;
            }}

            #dangerButton:disabled {{
                color: {theme.color("muted_text")};
                border: 1px solid {theme.color("input_border")};
            }}
            """
        )
