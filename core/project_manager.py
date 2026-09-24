
from pathlib import Path
import json
import shutil
from datetime import datetime


class ProjectManager:

    def __init__(self, base_path=None):

        if base_path is None:

            base_path = (
                Path(__file__).resolve().parent.parent
                / "projects"
            )

        self.base_path = Path(base_path)

        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )

    # =========================================================
    # CREATE PROJECT
    # =========================================================

    def create_project(
        self,
        name,
        description=""
    ):

        name = name.strip()

        if not name:

            raise ValueError(
                "Project name cannot be empty."
            )

        project_folder = (
            self.base_path / name
        )

        if project_folder.exists():

            raise FileExistsError(
                f"Project already exists: {name}"
            )

        project_folder.mkdir(
            parents=True
        )

        # -----------------------------------------------------
        # PROJECT SUBFOLDERS
        # -----------------------------------------------------

        (project_folder / "data").mkdir()
        (project_folder / "mappings").mkdir()
        (project_folder / "results").mkdir()
        (project_folder / "reports").mkdir()
        (project_folder / "archive").mkdir()

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        project = {

            "name": name,

            "description": description.strip(),

            "created": now,

            "last_opened": now,

            "files": [],

            "mappings": {},

            "filters": [],

            "analysis": {},

            "results": [],

            "reports": [],
        }

        self.save_project(
            name,
            project
        )

        return project

    # =========================================================
    # SAVE PROJECT
    # =========================================================

    def save_project(
        self,
        name,
        project
    ):

        project_folder = (
            self.base_path / name
        )

        project_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        project_file = (
            project_folder / "project.json"
        )

        with open(
            project_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                project,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =========================================================
    # OPEN PROJECT
    # =========================================================

    def open_project(
        self,
        name
    ):

        project_file = (
            self.base_path
            / name
            / "project.json"
        )

        if not project_file.exists():

            raise FileNotFoundError(
                f"Project not found: {name}"
            )

        with open(
            project_file,
            "r",
            encoding="utf-8"
        ) as file:

            project = json.load(file)

        project["last_opened"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        self.save_project(
            name,
            project
        )

        return project

    # =========================================================
    # LIST PROJECTS
    # =========================================================

    def list_projects(self):

        projects = []

        if not self.base_path.exists():

            return projects

        for folder in self.base_path.iterdir():

            if not folder.is_dir():

                continue

            project_file = (
                folder / "project.json"
            )

            if not project_file.exists():

                continue

            try:

                with open(
                    project_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    project = json.load(file)

                projects.append(
                    project
                )

            except (
                OSError,
                json.JSONDecodeError
            ):

                continue

        projects.sort(
            key=lambda project:
                project.get(
                    "last_opened",
                    ""
                ),
            reverse=True
        )

        return projects

    # =========================================================
    # RENAME PROJECT
    # =========================================================

    def rename_project(
        self,
        old_name,
        new_name
    ):

        old_name = old_name.strip()
        new_name = new_name.strip()

        # -----------------------------------------------------
        # VALIDATE NAMES
        # -----------------------------------------------------

        if not old_name:

            raise ValueError(
                "Current project name cannot be empty."
            )

        if not new_name:

            raise ValueError(
                "New project name cannot be empty."
            )

        # Nothing to do
        if old_name == new_name:

            return self.open_project(
                old_name
            )

        # -----------------------------------------------------
        # PROJECT FOLDERS
        # -----------------------------------------------------

        old_folder = (
            self.base_path / old_name
        )

        new_folder = (
            self.base_path / new_name
        )

        # -----------------------------------------------------
        # CHECK OLD PROJECT
        # -----------------------------------------------------

        if not old_folder.exists():

            raise FileNotFoundError(
                f"Project not found: {old_name}"
            )

        if not old_folder.is_dir():

            raise ValueError(
                f"Project path is not a folder: {old_name}"
            )

        # -----------------------------------------------------
        # PREVENT OVERWRITING ANOTHER PROJECT
        # -----------------------------------------------------

        if new_folder.exists():

            raise FileExistsError(
                f"A project already exists with the name: "
                f"{new_name}"
            )

        # -----------------------------------------------------
        # CHECK PROJECT FILE
        # -----------------------------------------------------

        old_project_file = (
            old_folder / "project.json"
        )

        if not old_project_file.exists():

            raise FileNotFoundError(
                "The project.json file could not be found."
            )

        # -----------------------------------------------------
        # READ PROJECT
        # -----------------------------------------------------

        try:

            with open(
                old_project_file,
                "r",
                encoding="utf-8"
            ) as file:

                project = json.load(file)

        except (
            OSError,
            json.JSONDecodeError
        ) as error:

            raise RuntimeError(
                f"Could not read project configuration:\n{error}"
            )

        # -----------------------------------------------------
        # RENAME ENTIRE PROJECT FOLDER
        # -----------------------------------------------------

        try:

            old_folder.rename(
                new_folder
            )

        except OSError as error:

            raise RuntimeError(
                f"Could not rename the project folder:\n{error}"
            )

        # -----------------------------------------------------
        # UPDATE PROJECT INFORMATION
        # -----------------------------------------------------

        project["name"] = new_name

        project["last_opened"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        new_project_file = (
            new_folder / "project.json"
        )

        try:

            with open(
                new_project_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    project,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except (
            OSError,
            TypeError
        ) as error:

            # -------------------------------------------------
            # ROLLBACK IF PROJECT.JSON CANNOT BE UPDATED
            # -------------------------------------------------

            try:

                new_folder.rename(
                    old_folder
                )

            except OSError:

                pass

            raise RuntimeError(
                f"Could not update project configuration:\n{error}"
            )

        return project

    # =========================================================
    # DELETE PROJECT
    # =========================================================

    def delete_project(
        self,
        name
    ):

        project_folder = (
            self.base_path / name
        )

        if not project_folder.exists():

            raise FileNotFoundError(
                f"Project not found: {name}"
            )

        if not project_folder.is_dir():

            raise ValueError(
                f"Project path is not a folder: {name}"
            )

        shutil.rmtree(
            project_folder
        )

    # =========================================================
    # PROJECT PATH
    # =========================================================

    def get_project_path(
        self,
        name
    ):

        return (
            self.base_path / name
        )

    # =========================================================
    # DATA PATH
    # =========================================================

    def get_data_path(
        self,
        name
    ):

        path = (
            self.get_project_path(name)
            / "data"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # =========================================================
    # MAPPING PATH
    # =========================================================

    def get_mapping_path(
        self,
        name
    ):

        path = (
            self.get_project_path(name)
            / "mappings"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # =========================================================
    # RESULTS PATH
    # =========================================================

    def get_results_path(
        self,
        name
    ):

        path = (
            self.get_project_path(name)
            / "results"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # =========================================================
    # REPORTS PATH
    # =========================================================

    def get_reports_path(
        self,
        name
    ):

        path = (
            self.get_project_path(name)
            / "reports"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # =========================================================
    # ARCHIVE PATH
    # =========================================================

    def get_archive_path(
        self,
        name
    ):

        path = (
            self.get_project_path(name)
            / "archive"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

