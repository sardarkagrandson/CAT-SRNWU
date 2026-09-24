from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QInputDialog,
    QDialog,
    QLineEdit,
    QTextEdit,
    QDialogButtonBox,
)


class ProjectsPage(QWidget):

    def __init__(
        self,
        project_manager,
        main_window
    ):

        super().__init__()

        self.project_manager = project_manager
        self.main_window = main_window

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
            18
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "My Projects"
        )

        title.setObjectName(
            "sectionTitle"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        new_button = QPushButton(
            "+ New Project"
        )

        new_button.setObjectName(
            "primaryButton"
        )

        new_button.clicked.connect(
            self.create_project
        )

        header.addWidget(
            new_button
        )

        layout.addLayout(
            header
        )

        description = QLabel(
            "Create and manage local audit data analysis projects."
        )

        description.setObjectName(
            "description"
        )

        layout.addWidget(
            description
        )

        # -----------------------------------------------------
        # PROJECT LIST
        # -----------------------------------------------------

        self.project_list_layout = QVBoxLayout()

        self.project_list_layout.setSpacing(
            10
        )

        layout.addLayout(
            self.project_list_layout
        )

        layout.addStretch()

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = QLabel(
            "Projects are stored locally on this computer."
        )

        self.status_label.setObjectName(
            "projectStatus"
        )

        layout.addWidget(
            self.status_label
        )

        # Apply theme
        self.apply_theme()

        self.refresh()

    # =========================================================
    # THEME
    # =========================================================

    def apply_theme(self):

        theme = self.main_window.theme_manager

        self.setStyleSheet(
            f"""
            #sectionTitle {{
                font-size: 22px;
                font-weight: 700;
                color: {theme.color("primary_text")};
            }}

            #description {{
                color: {theme.color("secondary_text")};
                font-size: 13px;
            }}

            #projectCard {{
                background-color: {theme.color("card_background")};
                border: 1px solid {theme.color("border")};
                border-radius: 8px;
            }}

            #projectCard:hover {{
                border: 1px solid {theme.color("accent")};
            }}

            #projectName {{
                color: {theme.color("primary_text")};
                font-size: 15px;
                font-weight: 600;
            }}

            #projectDescription {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
            }}

            #projectMetadata {{
                color: {theme.color("muted_text")};
                font-size: 11px;
            }}

            #emptyLabel {{
                color: {theme.color("muted_text")};
                font-size: 14px;
                padding: 40px;
            }}

            #projectStatus {{
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

            #dangerButton {{
                background-color: {theme.color("input_background")};
                color: {theme.color("danger_text")};
                border: 1px solid {theme.color("danger_border")};
                border-radius: 6px;
                padding: 8px 15px;
            }}

            #dangerButton:hover {{
                background-color: #f7eeee;
            }}

            #dialogLabel {{
                color: {theme.color("primary_text")};
                font-size: 12px;
                font-weight: 600;
            }}

            #dialogInput {{
                background-color: {theme.color("input_background")};
                color: {theme.color("input_text")};
                border: 1px solid {theme.color("input_border")};
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }}

            #dialogInput:focus {{
                border: 1px solid {theme.color("accent")};
            }}

            #dialogTextEdit {{
                background-color: {theme.color("input_background")};
                color: {theme.color("input_text")};
                border: 1px solid {theme.color("input_border")};
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }}

            #dialogTextEdit:focus {{
                border: 1px solid {theme.color("accent")};
            }}
            """
        )

    # =========================================================
    # REFRESH PROJECTS
    # =========================================================

    def refresh(self):

        self.clear_project_cards()

        projects = (
            self.project_manager.list_projects()
        )

        if not projects:

            empty_label = QLabel(
                "No projects created yet."
            )

            empty_label.setObjectName(
                "emptyLabel"
            )

            empty_label.setAlignment(
                Qt.AlignCenter
            )

            self.project_list_layout.addWidget(
                empty_label
            )

            return

        for project in projects:

            self.create_project_card(
                project
            )

    # =========================================================
    # CREATE PROJECT CARD
    # =========================================================

    def create_project_card(
        self,
        project
    ):

        card = QFrame()

        card.setObjectName(
            "projectCard"
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
        # PROJECT INFORMATION
        # -----------------------------------------------------

        information_layout = QVBoxLayout()

        name = QLabel(
            project.get(
                "name",
                ""
            )
        )

        name.setObjectName(
            "projectName"
        )

        information_layout.addWidget(
            name
        )

        description = project.get(
            "description",
            ""
        )

        if not description:

            description = "No description"

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "projectDescription"
        )

        description_label.setWordWrap(
            True
        )

        information_layout.addWidget(
            description_label
        )

        # -----------------------------------------------------
        # FILE COUNT
        # -----------------------------------------------------

        files = project.get(
            "files",
            []
        )

        file_count = len(files)

        file_text = (
            f"{file_count} "
            f"{'file' if file_count == 1 else 'files'}"
        )

        last_opened = project.get(
            "last_opened",
            ""
        )

        metadata = QLabel(
            f"{file_text}"
            f"  •  Last opened: "
            f"{self.format_datetime(last_opened)}"
        )

        metadata.setObjectName(
            "projectMetadata"
        )

        information_layout.addWidget(
            metadata
        )

        card_layout.addLayout(
            information_layout,
            1
        )

        # -----------------------------------------------------
        # OPEN BUTTON
        # -----------------------------------------------------

        open_button = QPushButton(
            "Open"
        )

        open_button.setObjectName(
            "primaryButton"
        )

        open_button.clicked.connect(
            lambda checked=False,
            project_name=project.get("name"):
                self.open_project(project_name)
        )

        card_layout.addWidget(
            open_button
        )

        # -----------------------------------------------------
        # EDIT PROJECT DETAILS BUTTON
        # -----------------------------------------------------

        edit_button = QPushButton(
            "Edit Project Details"
        )

        edit_button.setObjectName(
            "secondaryButton"
        )

        edit_button.clicked.connect(
            lambda checked=False,
            project_data=project:
                self.edit_project_details(project_data)
        )

        card_layout.addWidget(
            edit_button
        )

        # -----------------------------------------------------
        # DELETE BUTTON
        # -----------------------------------------------------

        delete_button = QPushButton(
            "Delete"
        )

        delete_button.setObjectName(
            "dangerButton"
        )

        delete_button.clicked.connect(
            lambda checked=False,
            project_name=project.get("name"):
                self.delete_project(project_name)
        )

        card_layout.addWidget(
            delete_button
        )

        self.project_list_layout.addWidget(
            card
        )

    # =========================================================
    # CREATE PROJECT
    # =========================================================

    def create_project(self):

        name, accepted = QInputDialog.getText(
            self,
            "Create New Project",
            "Project name:"
        )

        if not accepted:

            return

        name = name.strip()

        if not name:

            QMessageBox.warning(
                self,
                "Project Name",
                "Please enter a project name."
            )

            return

        description, accepted = (
            QInputDialog.getMultiLineText(
                self,
                "Project Description",
                "Description:",
                ""
            )
        )

        if not accepted:

            return

        try:

            project = (
                self.project_manager.create_project(
                    name,
                    description
                )
            )

        except FileExistsError:

            QMessageBox.warning(
                self,
                "Project Exists",
                "A project with this name already exists."
            )

            return

        except Exception as error:

            QMessageBox.critical(
                self,
                "Create Project",
                f"Could not create the project:\n\n{error}"
            )

            return

        # -----------------------------------------------------
        # AUTOMATICALLY OPEN NEW PROJECT
        # -----------------------------------------------------

        self.main_window.project_opened(
            project
        )

        self.status_label.setText(
            f"Project '{name}' created and opened."
        )

        self.refresh()

    # =========================================================
    # OPEN PROJECT
    # =========================================================

    def open_project(
        self,
        project_name
    ):

        try:

            project = (
                self.project_manager.open_project(
                    project_name
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Open Project",
                f"Could not open the project:\n\n{error}"
            )

            return

        self.status_label.setText(
            f"Project '{project_name}' opened."
        )

        self.main_window.project_opened(
            project
        )

    # =========================================================
    # EDIT PROJECT DETAILS
    # =========================================================

    def edit_project_details(
        self,
        project
    ):

        old_name = project.get(
            "name",
            ""
        )

        old_description = project.get(
            "description",
            ""
        )

        # -----------------------------------------------------
        # KEEP RE-SHOWING THE DIALOG UNTIL THE USER CANCELS
        # OR THE CHANGES ARE SAVED SUCCESSFULLY
        # -----------------------------------------------------

        prefill_name = old_name
        prefill_description = old_description

        while True:

            accepted, new_name, new_description = (
                self.show_edit_project_dialog(
                    prefill_name,
                    prefill_description
                )
            )

            if not accepted:

                return

            # ---------------------------------------------------
            # VALIDATE NAME
            # ---------------------------------------------------

            if not new_name:

                QMessageBox.warning(
                    self,
                    "Project Name",
                    "Project name cannot be empty."
                )

                prefill_name = new_name
                prefill_description = new_description

                continue

            # ---------------------------------------------------
            # DETERMINE CHANGES
            # ---------------------------------------------------

            name_changed = (
                new_name != old_name
            )

            description_changed = (
                new_description != old_description
            )

            if not name_changed and not description_changed:

                return

            # ---------------------------------------------------
            # CHANGE PROJECT NAME
            # ---------------------------------------------------

            try:

                if name_changed:

                    updated_project = (
                        self.project_manager.rename_project(
                            old_name,
                            new_name
                        )
                    )

                else:

                    updated_project = (
                        self.project_manager.open_project(
                            old_name
                        )
                    )

                # -----------------------------------------------
                # UPDATE DESCRIPTION
                # -----------------------------------------------

                updated_project["description"] = (
                    new_description
                )

                updated_project["last_opened"] = (
                    datetime_now()
                )

                self.project_manager.save_project(
                    new_name,
                    updated_project
                )

            except FileExistsError:

                QMessageBox.warning(
                    self,
                    "Project Exists",
                    (
                        "A project with this name "
                        "already exists."
                    )
                )

                # Reopen the edit dialog so the user can pick a
                # different name without starting over.

                prefill_name = new_name
                prefill_description = new_description

                continue

            except FileNotFoundError:

                QMessageBox.warning(
                    self,
                    "Project Not Found",
                    (
                        f"The project '{old_name}' "
                        "could not be found."
                    )
                )

                return

            except Exception as error:

                QMessageBox.critical(
                    self,
                    "Edit Project Details",
                    (
                        "Could not update the "
                        f"project details:\n\n{error}"
                    )
                )

                return

            break

        # -----------------------------------------------------
        # UPDATE CURRENT PROJECT IF OPEN
        # -----------------------------------------------------

        current_project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if (
            current_project
            and current_project.get("name")
            == old_name
        ):

            self.main_window.current_project = (
                updated_project
            )

            if hasattr(
                self.main_window,
                "project_status"
            ):

                self.main_window.project_status.setText(
                    f"Project: {new_name}"
                )

            # Keep application state in sync
            self.main_window.state.uploaded_files = (
                updated_project.get(
                    "files",
                    []
                )
            )

        # -----------------------------------------------------
        # REFRESH PROJECT LIST
        # -----------------------------------------------------

        self.refresh()

        if hasattr(
            self.main_window,
            "refresh_project_list"
        ):

            self.main_window.refresh_project_list()

        # -----------------------------------------------------
        # SUCCESS MESSAGE
        # -----------------------------------------------------

        self.status_label.setText(
            "Project details updated successfully."
        )

        QMessageBox.information(
            self,
            "Project Details Updated",
            "Project details updated successfully."
        )

    # =========================================================
    # SHOW EDIT PROJECT DIALOG
    # =========================================================

    def show_edit_project_dialog(
        self,
        name,
        description
    ):

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Edit Project Details"
        )

        dialog.setMinimumWidth(
            550
        )

        dialog.setModal(
            True
        )

        layout = QVBoxLayout(
            dialog
        )

        layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        layout.setSpacing(
            12
        )

        # -----------------------------------------------------
        # PROJECT NAME
        # -----------------------------------------------------

        name_label = QLabel(
            "Project Name"
        )

        name_label.setObjectName(
            "dialogLabel"
        )

        layout.addWidget(
            name_label
        )

        name_input = QLineEdit()

        name_input.setText(
            name
        )

        name_input.setObjectName(
            "dialogInput"
        )

        layout.addWidget(
            name_input
        )

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        description_label = QLabel(
            "Description"
        )

        description_label.setObjectName(
            "dialogLabel"
        )

        layout.addWidget(
            description_label
        )

        description_input = QTextEdit()

        description_input.setPlainText(
            description
        )

        description_input.setObjectName(
            "dialogTextEdit"
        )

        description_input.setMinimumHeight(
            120
        )

        layout.addWidget(
            description_input
        )

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save
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

        # -----------------------------------------------------
        # SHOW DIALOG
        # -----------------------------------------------------

        result = dialog.exec()

        if result != QDialog.Accepted:

            return False, "", ""

        new_name = name_input.text().strip()

        new_description = (
            description_input
            .toPlainText()
            .strip()
        )

        return True, new_name, new_description

    # =========================================================
    # DELETE PROJECT
    # =========================================================

    def delete_project(
        self,
        project_name
    ):

        answer = QMessageBox.question(
            self,
            "Delete Project",
            (
                f"Are you sure you want to delete "
                f"the project '{project_name}'?\n\n"
                f"All files, mappings, results and reports "
                f"belonging to this project will be removed."
            ),
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        try:

            self.project_manager.delete_project(
                project_name
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Delete Project",
                f"Could not delete the project:\n\n{error}"
            )

            return

        # -----------------------------------------------------
        # IF THE DELETED PROJECT WAS CURRENTLY OPEN
        # -----------------------------------------------------

        current_project = getattr(
            self.main_window,
            "current_project",
            None
        )

        if (
            current_project
            and current_project.get("name")
            == project_name
        ):

            self.main_window.close_project()

            return

        # -----------------------------------------------------
        # REFRESH
        # -----------------------------------------------------

        self.refresh()

        if hasattr(
            self.main_window,
            "refresh_project_list"
        ):

            self.main_window.refresh_project_list()

        self.status_label.setText(
            f"Project '{project_name}' deleted."
        )

    # =========================================================
    # CLEAR PROJECT CARDS
    # =========================================================

    def clear_project_cards(self):

        while self.project_list_layout.count():

            item = (
                self.project_list_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

    # =========================================================
    # FORMAT DATE/TIME
    # =========================================================

    def format_datetime(
        self,
        value
    ):

        if not value:

            return "Never"

        try:

            date_part, time_part = (
                value.split("T")
            )

            time_part = (
                time_part.split(":")[:2]
            )

            return (
                f"{date_part}"
                f" "
                f"{':'.join(time_part)}"
            )

        except Exception:

            return str(value)


# =============================================================
# DATETIME HELPER
# =============================================================

def datetime_now():

    from datetime import datetime

    return datetime.now().isoformat(
        timespec="seconds"
    )