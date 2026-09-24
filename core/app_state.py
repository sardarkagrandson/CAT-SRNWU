class AppState:
    """
    Central application state.

    All modules will use this object so that data can move between
    Upload → Preview → Mapping → Filters → Analysis → Results → Reports.
    """

    def __init__(self):
        self.uploaded_files = []
        self.selected_file = None
        self.selected_sheet = None
        self.selected_data = None

        self.column_types = {}
        self.filter_conditions = []

        self.analysis_results = []

        self.selected_analysis_files = []

    def clear(self):
        self.uploaded_files.clear()
        self.selected_file = None
        self.selected_sheet = None
        self.selected_data = None
        self.column_types.clear()
        self.filter_conditions.clear()
        self.analysis_results.clear()
        self.selected_analysis_files.clear()

    @property
    def file_count(self):
        return len(self.uploaded_files)

    @property
    def table_count(self):
        count = 0

        for uploaded_file in self.uploaded_files:
            count += len(uploaded_file.get("tables", []))

        return count