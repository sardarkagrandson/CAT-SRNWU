from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """
    Central theme manager for the application.

    All application colours are maintained here so that themes
    can be changed without modifying every individual page.
    """

    theme_changed = Signal(str)

    # =========================================================
    # THEME DEFINITIONS
    # =========================================================

    THEMES = {

        "Black & White": {

            "window_background": "#f4f5f6",
            "workspace_background": "#f4f5f6",

            "sidebar_background": "#252a2f",

            "card_background": "#ffffff",

            "primary_text": "#20242a",
            "secondary_text": "#4d555e",
            "muted_text": "#737c86",

            "sidebar_text": "#c7ccd1",
            "sidebar_muted": "#9da5ad",

            "border": "#dfe3e7",

            "menu_hover": "#30363c",
            "menu_selected": "#3a4148",

            "accent": "#343a40",
            "accent_hover": "#24282c",

            "button_text": "#ffffff",

            "input_background": "#ffffff",
            "input_text": "#30363d",
            "input_border": "#cfd5da",

            "danger_text": "#9a3f3f",
            "danger_border": "#d7c2c2",

            "table_header": "#f0f2f4",
            "table_selected": "#e4e7ea",
        },

        "NWU Professional": {

            "window_background": "#f4f5f6",
            "workspace_background": "#f4f5f6",

            "sidebar_background": "#181512",

            "card_background": "#ffffff",

            "primary_text": "#181512",
            "secondary_text": "#4d555e",
            "muted_text": "#78848e",

            "sidebar_text": "#d5d9dc",
            "sidebar_muted": "#aeb7bd",

            "border": "#d9dde0",

            "menu_hover": "#30383d",
            "menu_selected": "#00889c",

            "accent": "#00889c",
            "accent_hover": "#006f7e",

            "button_text": "#ffffff",

            "input_background": "#ffffff",
            "input_text": "#181512",
            "input_border": "#b8c0c5",

            "danger_text": "#9a3f3f",
            "danger_border": "#d7c2c2",

            "table_header": "#eef1f2",
            "table_selected": "#d9eef1",
        },

        "Corporate Navy": {

            "window_background": "#f4f6f8",
            "workspace_background": "#f4f6f8",

            "sidebar_background": "#0f1c2e",

            "card_background": "#ffffff",

            "primary_text": "#14213d",
            "secondary_text": "#46536b",
            "muted_text": "#7c8aa0",

            "sidebar_text": "#cdd6e4",
            "sidebar_muted": "#93a1b8",

            "border": "#dde3ea",

            "menu_hover": "#17263c",
            "menu_selected": "#1f4287",

            "accent": "#1f4287",
            "accent_hover": "#163264",

            "button_text": "#ffffff",

            "input_background": "#ffffff",
            "input_text": "#14213d",
            "input_border": "#c3cbd8",

            "danger_text": "#9a3f3f",
            "danger_border": "#d7c2c2",

            "table_header": "#eef1f5",
            "table_selected": "#dbe6f5",
        },

        "Slate Graphite": {

            "window_background": "#f5f5f6",
            "workspace_background": "#f5f5f6",

            "sidebar_background": "#23272b",

            "card_background": "#ffffff",

            "primary_text": "#212429",
            "secondary_text": "#4c525a",
            "muted_text": "#767d86",

            "sidebar_text": "#cbd0d5",
            "sidebar_muted": "#98a0a8",

            "border": "#dfe2e5",

            "menu_hover": "#2f343a",
            "menu_selected": "#46708c",

            "accent": "#46708c",
            "accent_hover": "#375a70",

            "button_text": "#ffffff",

            "input_background": "#ffffff",
            "input_text": "#292d33",
            "input_border": "#ccd2d8",

            "danger_text": "#9a3f3f",
            "danger_border": "#d7c2c2",

            "table_header": "#eef0f2",
            "table_selected": "#dce6ec",
        },

        "Forest Audit": {

            "window_background": "#f4f6f4",
            "workspace_background": "#f4f6f4",

            "sidebar_background": "#16211a",

            "card_background": "#ffffff",

            "primary_text": "#1a231d",
            "secondary_text": "#46524a",
            "muted_text": "#77857d",

            "sidebar_text": "#cdd8d0",
            "sidebar_muted": "#96a89d",

            "border": "#dbe3dd",

            "menu_hover": "#1f2e24",
            "menu_selected": "#2f6b47",

            "accent": "#2f6b47",
            "accent_hover": "#235437",

            "button_text": "#ffffff",

            "input_background": "#ffffff",
            "input_text": "#1a231d",
            "input_border": "#c3d0c8",

            "danger_text": "#9a3f3f",
            "danger_border": "#d7c2c2",

            "table_header": "#eef2ef",
            "table_selected": "#d9ecdf",
        },
    }

    def __init__(
        self,
        initial_theme="Black & White"
    ):

        super().__init__()

        if initial_theme not in self.THEMES:
            initial_theme = "Black & White"

        self.current_theme = initial_theme

    # =========================================================
    # SET THEME
    # =========================================================

    def set_theme(
        self,
        theme_name
    ):

        if theme_name not in self.THEMES:
            return

        if theme_name == self.current_theme:
            return

        self.current_theme = theme_name

        self.theme_changed.emit(
            theme_name
        )

    # =========================================================
    # GET CURRENT THEME
    # =========================================================

    def get_theme(
        self
    ):

        return self.THEMES[
            self.current_theme
        ]

    # =========================================================
    # GET COLOUR
    # =========================================================

    def color(
        self,
        name
    ):

        theme = self.get_theme()

        return theme.get(
            name,
            "#000000"
        )

    # =========================================================
    # GET CURRENT THEME NAME
    # =========================================================

    def name(
        self
    ):

        return self.current_theme

    # =========================================================
    # AVAILABLE THEMES
    # =========================================================

    def available_themes(
        self
    ):

        return list(
            self.THEMES.keys()
        )