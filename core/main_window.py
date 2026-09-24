from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFrame,
    QComboBox,
    QMessageBox,
)

from core.theme_manager import ThemeManager

from pages.projects_page import ProjectsPage
from pages.upload_page import UploadPage
from pages.preview_page import PreviewPage
from pages.mapping_page import MappingPage


class MainWindow(QMainWindow):

    def __init__(
        self,
        state,
        project_manager
    ):

        super().__init__()

        self.state = state
        self.project_manager = project_manager

        # =====================================================
        # THEME MANAGER
        # =====================================================

        self.theme_manager = ThemeManager()

        self.theme_manager.theme_changed.connect(
           self.apply_current_theme
        )
        self.theme_manager.theme_changed.connect(
        self.refresh_page_themes
)

        self.current_project = None

        # Project menu state
        self.projects_expanded = True
        self.project_buttons = {}

        self.setWindowTitle(
            "Audit Data Analysis"
        )

        self.setMinimumSize(
            1200,
            750
        )

        self.resize(
            1400,
            850
        )

        self.create_interface()

        # Apply initial theme
        self.apply_current_theme(
            self.theme_manager.name()
        )

        # Load project names into sidebar
        self.refresh_project_list()

    # =========================================================
    # CREATE INTERFACE
    # =========================================================

    def create_interface(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar = QFrame()

        sidebar.setObjectName(
            "sidebar"
        )

        sidebar.setFixedWidth(
            245
        )

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            15,
            20,
            15,
            20
        )

        sidebar_layout.setSpacing(
            7
        )

        # -----------------------------------------------------
        # LOGO
        # -----------------------------------------------------

        logo = QLabel(
            "AUDIT DATA\nANALYSIS"
        )

        logo.setObjectName(
            "logo"
        )

        sidebar_layout.addWidget(
            logo
        )

        subtitle = QLabel(
            "Local Data Analysis"
        )

        subtitle.setObjectName(
            "logoSubtitle"
        )

        sidebar_layout.addWidget(
            subtitle
        )

        sidebar_layout.addSpacing(
            25
        )

        # -----------------------------------------------------
        # MENU
        # -----------------------------------------------------

        self.menu_buttons = {}

        # -----------------------------------------------------
        # PROJECTS HEADER
        # -----------------------------------------------------

        self.projects_button = QPushButton(
            "Projects  ▲"
        )

        self.projects_button.setObjectName(
            "menuButton"
        )

        self.projects_button.setCheckable(
            True
        )

        self.projects_button.clicked.connect(
            self.projects_menu_clicked
        )

        self.menu_buttons[
            "projects"
        ] = self.projects_button

        sidebar_layout.addWidget(
            self.projects_button
        )

        # -----------------------------------------------------
        # PROJECT LIST CONTAINER
        # -----------------------------------------------------

        self.project_list_widget = QWidget()

        self.project_list_widget.setObjectName(
            "projectListWidget"
        )

        self.project_list_layout = QVBoxLayout(
            self.project_list_widget
        )

        self.project_list_layout.setContentsMargins(
            8,
            0,
            0,
            0
        )

        self.project_list_layout.setSpacing(
            2
        )

        sidebar_layout.addWidget(
            self.project_list_widget
        )

        # -----------------------------------------------------
        # OTHER MENU ITEMS
        # -----------------------------------------------------

        menu_items = [
            ("Upload Files", "upload"),
            ("Data Preview", "preview"),
            ("Data Mapping", "mapping"),
            ("Filters", "filters"),
            ("Analysis", "analysis"),
            ("Results", "results"),
            ("Reports", "reports"),
        ]

        for text, page_name in menu_items:

            button = QPushButton(
                text
            )

            button.setObjectName(
                "menuButton"
            )

            button.setCheckable(
                True
            )

            button.clicked.connect(
                lambda checked=False,
                name=page_name:
                    self.show_page(name)
            )

            self.menu_buttons[
                page_name
            ] = button

            sidebar_layout.addWidget(
                button
            )

        sidebar_layout.addStretch()

        # -----------------------------------------------------
        # OFFLINE INDICATOR
        # -----------------------------------------------------

        offline_label = QLabel(
            "●  LOCAL • OFFLINE"
        )

        offline_label.setObjectName(
            "offlineLabel"
        )

        offline_label.setAlignment(
            Qt.AlignCenter
        )

        sidebar_layout.addWidget(
            offline_label
        )

        main_layout.addWidget(
            sidebar
        )

        # =====================================================
        # WORKSPACE
        # =====================================================

        workspace = QWidget()

        workspace.setObjectName(
            "workspace"
        )

        workspace_layout = QVBoxLayout(
            workspace
        )

        workspace_layout.setContentsMargins(
            28,
            24,
            28,
            24
        )

        workspace_layout.setSpacing(
            18
        )

        # -----------------------------------------------------
        # WORKSPACE HEADER
        # -----------------------------------------------------

        workspace_header = QHBoxLayout()

        self.workspace_title = QLabel(
            "My Projects"
        )

        self.workspace_title.setObjectName(
            "workspaceTitle"
        )

        workspace_header.addWidget(
            self.workspace_title
        )

        workspace_header.addStretch()

        # -----------------------------------------------------
        # THEME SELECTOR
        # -----------------------------------------------------

        theme_label = QLabel(
            "Theme:"
        )

        theme_label.setObjectName(
            "themeLabel"
        )

        workspace_header.addWidget(
            theme_label
        )

        self.theme_selector = QComboBox()

        self.theme_selector.setObjectName(
            "themeSelector"
        )

        self.theme_selector.addItems(
            self.theme_manager.available_themes()
        )

        self.theme_selector.setCurrentText(
            self.theme_manager.name()
        )

        self.theme_selector.currentTextChanged.connect(
            self.change_theme
        )

        workspace_header.addWidget(
            self.theme_selector
        )

        workspace_header.addSpacing(
            20
        )

        self.project_status = QLabel(
            "No project open"
        )

        self.project_status.setObjectName(
            "projectStatus"
        )

        workspace_header.addWidget(
            self.project_status
        )

        self.file_status = QLabel(
            "0 files loaded"
        )

        self.file_status.setObjectName(
            "fileStatus"
        )

        workspace_header.addSpacing(
            15
        )

        workspace_header.addWidget(
            self.file_status
        )

        workspace_layout.addLayout(
            workspace_header
        )

        # -----------------------------------------------------
        # STACKED PAGES
        # -----------------------------------------------------

        self.stack = QStackedWidget()

        workspace_layout.addWidget(
            self.stack,
            1
        )

        main_layout.addWidget(
            workspace,
            1
        )

        # -----------------------------------------------------
        # CREATE PAGES
        # -----------------------------------------------------

        self.create_pages()

        # -----------------------------------------------------
        # DEFAULT PAGE
        # -----------------------------------------------------

        self.show_page(
            "projects"
        )

    # =========================================================
    # PROJECT MENU
    # =========================================================

    def projects_menu_clicked(
        self
    ):

        self.projects_expanded = (
            not self.projects_expanded
        )

        self.update_project_menu_visibility()

        self.show_page(
            "projects"
        )

    # =========================================================
    # PROJECT MENU VISIBILITY
    # =========================================================

    def update_project_menu_visibility(
        self
    ):

        if self.projects_expanded:

            self.projects_button.setText(
                "Projects  ▲"
            )

            self.project_list_widget.show()

        else:

            self.projects_button.setText(
                "Projects  ▼"
            )

            self.project_list_widget.hide()

    # =========================================================
    # REFRESH PROJECT LIST
    # =========================================================

    def refresh_project_list(
        self
    ):

        # Remove existing project buttons
        for button in self.project_buttons.values():

            button.deleteLater()

        self.project_buttons.clear()

        projects = (
            self.project_manager.list_projects()
        )

        for project in projects:

            project_name = project.get(
                "name",
                ""
            )

            if not project_name:
                continue

            button = QPushButton(
                project_name
            )

            button.setObjectName(
                "projectMenuButton"
            )

            button.setCheckable(
                True
            )

            button.clicked.connect(
                lambda checked=False,
                name=project_name:
                    self.open_project_from_menu(name)
            )

            self.project_list_layout.addWidget(
                button
            )

            self.project_buttons[
                project_name
            ] = button

        self.update_project_button_states()

        self.update_project_menu_visibility()

    # =========================================================
    # OPEN PROJECT FROM SIDEBAR
    # =========================================================

    def open_project_from_menu(
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

            self.project_status.setText(
                f"Could not open project: {error}"
            )

            return

        self.project_opened(
            project
        )

        self.update_project_button_states()

    # =========================================================
    # UPDATE PROJECT BUTTON STATES
    # =========================================================

    def update_project_button_states(
        self
    ):

        current_name = ""

        if self.current_project:

            current_name = (
                self.current_project.get(
                    "name",
                    ""
                )
            )

        for name, button in (
            self.project_buttons.items()
        ):

            button.setChecked(
                name == current_name
            )

    # =========================================================
    # CREATE PAGES
    # =========================================================

    def create_pages(self):

        # -----------------------------------------------------
        # PROJECTS
        # -----------------------------------------------------

        self.projects_page = ProjectsPage(
            self.project_manager,
            self
        )

        self.stack.addWidget(
            self.projects_page
        )

        # -----------------------------------------------------
        # UPLOAD
        # -----------------------------------------------------

        self.upload_page = UploadPage(
            self.state,
            self
        )

        self.stack.addWidget(
            self.upload_page
        )

        # -----------------------------------------------------
        # PREVIEW
        # -----------------------------------------------------

        self.preview_page = PreviewPage(
            self.state,
            self
        )

        self.stack.addWidget(
            self.preview_page
        )

        # -----------------------------------------------------
        # MAPPING
        # -----------------------------------------------------

        self.mapping_page = MappingPage(
            self.state,
            self
        )

        self.stack.addWidget(
            self.mapping_page
        )

        # -----------------------------------------------------
        # PLACEHOLDER PAGES
        # -----------------------------------------------------

        self.placeholder_pages = {}

        placeholder_information = {
            "filters": "Filters will be developed next.",
            "analysis": "Analysis will be developed next.",
            "results": "Results will be developed next.",
            "reports": "Reports will be developed next.",
        }

        for page_name, message in (
            placeholder_information.items()
        ):

            page = self.create_placeholder_page(
                message
            )

            self.placeholder_pages[
                page_name
            ] = page

            self.stack.addWidget(
                page
            )

    # =========================================================
    # PROJECT OPENED
    # =========================================================

    def project_opened(
        self,
        project
    ):

        self.current_project = project

        self.project_status.setText(
            f"Project: {project.get('name', '')}"
        )

        file_count = len(
            project.get(
                "files",
                []
            )
        )

        self.update_file_status(
            file_count
        )

        self.state.uploaded_files = (
            project.get(
                "files",
                []
            )
        )

        self.update_project_button_states()

        self.show_page(
            "upload"
        )

    # =========================================================
    # PROJECT CLOSED
    # =========================================================

    def close_project(self):

        self.current_project = None

        self.state.clear()

        self.project_status.setText(
            "No project open"
        )

        self.update_file_status(
            0
        )

        self.update_project_button_states()

        self.show_page(
            "projects"
        )

    # =========================================================
    # PLACEHOLDER PAGE
    # =========================================================

    def create_placeholder_page(
        self,
        message
    ):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setAlignment(
            Qt.AlignCenter
        )

        label = QLabel(
            message
        )

        label.setObjectName(
            "placeholderLabel"
        )

        label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            label
        )

        return page

    # =========================================================
    # SHOW PAGE
    # =========================================================

    def show_page(
        self,
        page_name
    ):

        page_map = {
            "projects": self.projects_page,
            "upload": self.upload_page,
            "preview": self.preview_page,
            "mapping": self.mapping_page,
        }

        if page_name in page_map:

            page = page_map[
                page_name
            ]

        elif page_name in self.placeholder_pages:

            page = self.placeholder_pages[
                page_name
            ]

        else:

            return

        self.stack.setCurrentWidget(
            page
        )

        # -----------------------------------------------------
        # BUTTON STATE
        # -----------------------------------------------------

        for name, button in (
            self.menu_buttons.items()
        ):

            button.setChecked(
                name == page_name
            )

        # -----------------------------------------------------
        # PROJECT BUTTON STATE
        # -----------------------------------------------------

        self.update_project_button_states()

        # -----------------------------------------------------
        # REFRESH PAGES
        # -----------------------------------------------------

        if page_name == "projects":

            self.projects_page.refresh()

            self.refresh_project_list()

        elif page_name == "upload":

            self.upload_page.refresh()

        elif page_name == "preview":

            self.preview_page.refresh()

        elif page_name == "mapping":

            self.mapping_page.refresh()

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        titles = {
            "projects": "My Projects",
            "upload": "Upload Files",
            "preview": "Data Preview",
            "mapping": "Data Mapping",
            "filters": "Filters",
            "analysis": "Analysis",
            "results": "Results",
            "reports": "Reports",
        }

        self.workspace_title.setText(
            titles.get(
                page_name,
                "Data Analysis Workspace"
            )
        )

    # =========================================================
    # FILE STATUS
    # =========================================================

    def update_file_status(
        self,
        number_of_files
    ):

        self.file_status.setText(
            f"{number_of_files} "
            f"{'file' if number_of_files == 1 else 'files'} loaded"
        )

    # =========================================================
    # THEME
    # =========================================================

    def change_theme(
        self,
        theme_name
    ):

        self.theme_manager.set_theme(
            theme_name
        )

    # =========================================================
    # APPLY CURRENT THEME
    # =========================================================

    def apply_current_theme(
        self,
        theme_name=None
    ):

        theme = self.theme_manager

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {theme.color("window_background")};
            }}

            #sidebar {{
                background-color: {theme.color("sidebar_background")};
            }}

            #logo {{
                color: {theme.color("button_text")};
                font-size: 19px;
                font-weight: 800;
                line-height: 1.2;
            }}

            #logoSubtitle {{
                color: {theme.color("sidebar_muted")};
                font-size: 11px;
            }}

            #menuButton {{
                background-color: transparent;
                color: {theme.color("sidebar_text")};
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 11px 13px;
                font-size: 13px;
            }}

            #menuButton:hover {{
                background-color: {theme.color("menu_hover")};
                color: {theme.color("button_text")};
            }}

            #menuButton:checked {{
                background-color: {theme.color("menu_selected")};
                color: {theme.color("button_text")};
                font-weight: 600;
            }}

            #projectListWidget {{
                background-color: transparent;
            }}

            #projectMenuButton {{
                background-color: transparent;
                color: {theme.color("sidebar_muted")};
                border: none;
                border-radius: 5px;
                text-align: left;
                padding: 8px 10px;
                font-size: 12px;
            }}

            #projectMenuButton:hover {{
                background-color: {theme.color("menu_hover")};
                color: {theme.color("button_text")};
            }}

            #projectMenuButton:checked {{
                background-color: {theme.color("menu_selected")};
                color: {theme.color("button_text")};
                font-weight: 600;
            }}

            #offlineLabel {{
                color: {theme.color("sidebar_muted")};
                font-size: 10px;
                padding: 8px;
            }}

            #workspace {{
                background-color: {theme.color("workspace_background")};
            }}

            #workspaceTitle {{
                color: {theme.color("primary_text")};
                font-size: 20px;
                font-weight: 700;
            }}

            #projectStatus {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
                font-weight: 600;
            }}

            #fileStatus {{
                color: {theme.color("muted_text")};
                font-size: 12px;
            }}

            #themeLabel {{
                color: {theme.color("secondary_text")};
                font-size: 12px;
                font-weight: 600;
            }}

            #themeSelector {{
                background-color: {theme.color("input_background")};
                color: {theme.color("input_text")};
                border: 1px solid {theme.color("input_border")};
                border-radius: 5px;
                padding: 6px 10px;
                min-width: 145px;
            }}

            #themeSelector:hover {{
                border: 1px solid {theme.color("accent")};
            }}

            #placeholderLabel {{
                color: {theme.color("muted_text")};
                font-size: 16px;
            }}
            """
        )

    # =========================================================
    # REFRESH PAGE THEMES
    # =========================================================

    def refresh_page_themes(
        self
    ):

        if hasattr(
            self,
            "projects_page"
        ):

            self.projects_page.apply_theme()

        if hasattr(
            self,
            "upload_page"
        ):

            self.upload_page.apply_theme()

        if hasattr(
            self,
            "preview_page"
        ):

            self.preview_page.apply_theme()

        if hasattr(
            self,
            "mapping_page"
        ):

            self.mapping_page.apply_theme()
