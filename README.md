# Audit Data Analysis

A local, offline desktop application for auditing and analysing sensitive
institutional data. Built with Python and PySide6.

No AI, no cloud, no automatic upload of any kind. All project data, files,
mappings and results stay on your computer.

## Requirements

- Python 3.10 or newer (tested with 3.11)
- Windows, macOS or Linux with a desktop environment

## Installation

### 1. Get the code

```bash
git clone https://github.com/sardarkagrandson/CAT-SRNWU.git
cd CAT-SRNWU
```

If you already have the project as a folder (e.g. extracted from a `.zip`
or `.7z`), just open a terminal inside that folder instead of cloning.

### 2. Create a virtual environment

A virtual environment keeps this project's dependencies separate from the
rest of your system.

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt once
it is active.

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

This installs:

- **PySide6** — the desktop user interface
- **pandas** — data processing
- **openpyxl** — reading/writing `.xlsx` files
- **xlrd** — reading older `.xls` files

### 4. Run the application

```bash
python main.py
```

The main window should open with the sidebar on the left and the
workspace on the right.

## Everyday use

Once installed, running the app again only requires activating the
virtual environment and starting it:

**Windows:**

```powershell
cd CAT-SRNWU
venv\Scripts\activate
python main.py
```

**macOS / Linux:**

```bash
cd CAT-SRNWU
source venv/bin/activate
python main.py
```

## Project data

Everything you create in the app is stored locally under the `projects/`
folder, one subfolder per project:

```text
projects/
└── My Audit Project/
    ├── project.json     Project metadata, mappings, filters, results
    ├── data/             Copies of uploaded source files
    ├── mappings/
    ├── results/
    ├── reports/
    └── archive/
```

Nothing in this folder is ever sent anywhere — it only exists on this
computer.

## Changing the theme

The workspace header includes a **Theme** selector with several
professional colour themes (Black & White, NWU Professional, Corporate
Navy, Slate Graphite, Forest Audit). Changing it restyles the sidebar,
workspace and every page immediately — the choice is not saved between
runs yet.

## Troubleshooting

- **`python` / `pip` not recognised** — make sure Python is installed and
  added to your system `PATH`, or use `python3` / `pip3` on macOS/Linux.
- **`ModuleNotFoundError: No module named 'PySide6'`** — the virtual
  environment isn't active, or dependencies weren't installed; re-run
  steps 2 and 3.
- **Window doesn't appear on Linux** — make sure a desktop environment
  (X11 or Wayland) is running; this is a desktop app and cannot run on a
  headless server.
