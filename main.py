import sys

from PySide6.QtWidgets import QApplication

from core.app_state import AppState
from core.main_window import MainWindow
from core.project_manager import ProjectManager


def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Audit Data Analysis"
    )

    app.setOrganizationName(
        "Local Audit Tools"
    )

    # ---------------------------------------------------------
    # CENTRAL APPLICATION STATE
    # ---------------------------------------------------------

    state = AppState()

    # ---------------------------------------------------------
    # PROJECT MANAGER
    # ---------------------------------------------------------

    project_manager = ProjectManager()

    # ---------------------------------------------------------
    # MAIN WINDOW
    # ---------------------------------------------------------

    window = MainWindow(
        state,
        project_manager
    )

    window.show()

    # ---------------------------------------------------------
    # START APPLICATION
    # ---------------------------------------------------------

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()