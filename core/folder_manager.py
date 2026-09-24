import uuid


# =============================================================
# ROOT FOLDER
#
# folder_id == None always means the project's root level (not
# inside any user-created folder). Root itself is never stored
# as an entry in project["folders"].
# =============================================================

ROOT_FOLDER_ID = None


# =============================================================
# GET FOLDERS
# =============================================================

def get_folders(project):

    folders = project.get(
        "folders",
        []
    )

    if not isinstance(
        folders,
        list
    ):
        return []

    return folders


# =============================================================
# FIND FOLDER BY ID
# =============================================================

def find_folder(
    project,
    folder_id
):

    if folder_id is None:
        return None

    for folder in get_folders(project):

        if folder.get("id") == folder_id:

            return folder

    return None


# =============================================================
# GET CHILD FOLDERS
# =============================================================

def get_child_folders(
    project,
    parent_id
):

    children = [
        folder
        for folder in get_folders(project)
        if folder.get("parent_id") == parent_id
    ]

    children.sort(
        key=lambda folder: folder.get("name", "").lower()
    )

    return children


# =============================================================
# GET FILES IN FOLDER
# =============================================================

def get_files_in_folder(
    project,
    folder_id
):

    files = project.get(
        "files",
        []
    )

    return [
        file_record
        for file_record in files
        if file_record.get("folder_id") == folder_id
    ]


# =============================================================
# FOLDER PATH (BREADCRUMB)
# =============================================================

def get_folder_path(
    project,
    folder_id
):

    names = []

    current_id = folder_id

    visited = set()

    while current_id is not None:

        if current_id in visited:
            # Guard against a corrupted/circular parent chain
            break

        visited.add(
            current_id
        )

        folder = find_folder(
            project,
            current_id
        )

        if not folder:
            break

        names.insert(
            0,
            folder.get("name", "")
        )

        current_id = folder.get(
            "parent_id"
        )

    return names


# =============================================================
# DESCENDANT FOLDER IDS (INCLUDING THE FOLDER ITSELF)
# =============================================================

def get_descendant_folder_ids(
    project,
    folder_id
):

    result = {
        folder_id
    }

    changed = True

    while changed:

        changed = False

        for folder in get_folders(project):

            if (
                folder.get("parent_id") in result
                and folder.get("id") not in result
            ):

                result.add(
                    folder.get("id")
                )

                changed = True

    return result


# =============================================================
# NAME ALREADY USED UNDER PARENT
# =============================================================

def name_exists_under_parent(
    project,
    parent_id,
    name,
    ignore_folder_id=None
):

    normalized = name.strip().lower()

    for folder in get_child_folders(
        project,
        parent_id
    ):

        if folder.get("id") == ignore_folder_id:
            continue

        if folder.get("name", "").strip().lower() == normalized:

            return True

    return False


# =============================================================
# CREATE FOLDER
# =============================================================

def create_folder(
    project,
    name,
    parent_id=None
):

    name = name.strip()

    if not name:

        raise ValueError(
            "Folder name cannot be empty."
        )

    if parent_id is not None and not find_folder(
        project,
        parent_id
    ):

        raise ValueError(
            "The parent folder could not be found."
        )

    if name_exists_under_parent(
        project,
        parent_id,
        name
    ):

        raise FileExistsError(
            f"A folder named '{name}' already exists here."
        )

    folder_id = uuid.uuid4().hex

    project.setdefault(
        "folders",
        []
    ).append(
        {
            "id": folder_id,
            "name": name,
            "parent_id": parent_id,
        }
    )

    return folder_id


# =============================================================
# RENAME FOLDER
# =============================================================

def rename_folder(
    project,
    folder_id,
    new_name
):

    new_name = new_name.strip()

    if not new_name:

        raise ValueError(
            "Folder name cannot be empty."
        )

    folder = find_folder(
        project,
        folder_id
    )

    if not folder:

        raise ValueError(
            "The folder could not be found."
        )

    if name_exists_under_parent(
        project,
        folder.get("parent_id"),
        new_name,
        ignore_folder_id=folder_id
    ):

        raise FileExistsError(
            f"A folder named '{new_name}' already exists here."
        )

    folder["name"] = new_name


# =============================================================
# DELETE FOLDER
#
# Any subfolders and files that were directly inside the deleted
# folder are moved up to its parent (or the project root) rather
# than being destroyed.
# =============================================================

def delete_folder(
    project,
    folder_id
):

    folder = find_folder(
        project,
        folder_id
    )

    if not folder:

        raise ValueError(
            "The folder could not be found."
        )

    parent_id = folder.get(
        "parent_id"
    )

    for child_folder in get_child_folders(
        project,
        folder_id
    ):

        child_folder["parent_id"] = parent_id

    for file_record in get_files_in_folder(
        project,
        folder_id
    ):

        file_record["folder_id"] = parent_id

    project["folders"] = [
        existing
        for existing in get_folders(project)
        if existing.get("id") != folder_id
    ]


# =============================================================
# MOVE FILE TO FOLDER
# =============================================================

def move_file_to_folder(
    project,
    file_record,
    target_folder_id
):

    if target_folder_id is not None and not find_folder(
        project,
        target_folder_id
    ):

        raise ValueError(
            "The destination folder could not be found."
        )

    file_record["folder_id"] = target_folder_id


# =============================================================
# BUILD FOLDER TREE
#
# Returns a nested structure of
# {"id", "name", "parent_id", "children": [...]}
# rooted at parent_id (default: the project root).
# =============================================================

def build_folder_tree(
    project,
    parent_id=None
):

    tree = []

    for folder in get_child_folders(
        project,
        parent_id
    ):

        tree.append(
            {
                "id": folder.get("id"),
                "name": folder.get("name"),
                "parent_id": folder.get("parent_id"),
                "children": build_folder_tree(
                    project,
                    folder.get("id")
                ),
            }
        )

    return tree
