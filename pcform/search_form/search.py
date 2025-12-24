import customtkinter as ctk
from search_form.database_info import DatabaseInfo

from settings.config import PERSIAN_FONT
from utils.widget_utils import set_icon


class SearchMainFrame(ctk.CTkToplevel):
    """Main search window frame"""

    def __init__(self, parent, title, app_ref=None):
        super().__init__(parent)
        self.title(title)
        self.minsize(1200, 850)
        self.maxsize(1600, 1000)
        set_icon(self)
        self.app_ref = app_ref

        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Logo and title frame
        header_frame = ctk.CTkFrame(self.main_container)
        header_frame.pack(fill="x", padx=5, pady=(5, 10))

        logo_label = ctk.CTkLabel(
            header_frame,
            text="🍌 Search Forms",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        logo_label.pack(side="left", padx=10, pady=5)

        # Search frame at top
        self.search_frame = SearchForm(self.main_container)
        self.search_frame.pack(fill="x", padx=5, pady=5)

        # Database frame with results
        self.database_frame = DatabaseInfo(self.main_container, self)
        self.database_frame.pack(fill="both", expand=True, padx=5, pady=5)


class SearchForm(ctk.CTkFrame):
    """Search form with advanced filtering options

    Args:
        ctk (frame): CustomTkinter frame
    """

    def __init__(self, master):
        super().__init__(master)
        self.parent_window = master
        # Main search section
        self.search_label = ctk.CTkLabel(
            self, text="Search:", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.search_label.pack(side="left", padx=(15, 10), pady=15)

        self.entry = ctk.CTkEntry(
            self,
            width=450,
            placeholder_text="Enter search term...",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=14),
        )
        self.entry.pack(side="left", padx=10, pady=15)
        self.entry.bind("<Return>", lambda e: self.search())  # Search on Enter key

        self.search_button = ctk.CTkButton(
            self,
            text="🔍 Search",
            command=self.search,
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
        )
        self.search_button.pack(side="left", padx=10, pady=15)

        self.clear_button = ctk.CTkButton(
            self,
            text="Clear",
            command=self.clear_search,
            width=100,
            font=ctk.CTkFont(size=13),
            fg_color="gray",
            height=40,
        )
        self.clear_button.pack(side="left", padx=10, pady=15)

        self.filter_button = ctk.CTkButton(
            self,
            text="⚙️ Advanced Filters",
            command=self.open_advanced_filters,
            width=150,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            fg_color="blue",
        )
        self.filter_button.pack(side="left", padx=10, pady=15)

        self.filters = {}

    def open_advanced_filters(self):
        """Open the advanced filters dialog"""
        dialog = OpenFiltersDialog(self.parent_window)
        dialog.open_filters()

    def search(self):
        """Perform search based on entry text and advanced filters"""
        query = self.entry.get()
        # Find ancestor that has database_frame (the SearchMainFrame)
        host = self.parent_window
        while host is not None and not hasattr(host, "database_frame"):
            host = getattr(host, "master", None)

        # If advanced filters are set, prefer them (filters override simple query)
        if hasattr(self, "filters") and any(self.filters.values()):
            if host is not None and hasattr(host, "database_frame"):
                host.database_frame.apply_advanced_filters(self.filters)
        else:
            if host is not None and hasattr(host, "database_frame"):
                host.database_frame.search(query)
        print("Searching for:", query)

    def clear_search(self):
        """Clear search entry and reset filters"""
        self.entry.delete(0, "end")
        self.filters = {}
        # Find ancestor that has database_frame and reset it
        host = self.parent_window
        while host is not None and not hasattr(host, "database_frame"):
            host = getattr(host, "master", None)

        if host is not None and hasattr(host, "database_frame"):
            host.database_frame.populate_treeview()


class OpenFiltersDialog(ctk.CTkToplevel):
    """Advanced filter dialog window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_window = args[0]
        self.title("Advanced Filters")
        self.geometry("400x650")
        self.resizable(False, False)
        set_icon(self)

    def apply_filters(
        self,
        fullname_entry,
        model_entry,
        provider_entry,
        problem_entry,
        date_from_entry,
        date_to_entry,
        favorites_var,
    ):
        filters = {
            "fullname": fullname_entry.get().strip(),
            "device_model": model_entry.get().strip(),
            "service_provider": provider_entry.get().strip(),
            "problem_type": problem_entry.get().strip(),
            "date_from": date_from_entry.get().strip(),
            "date_to": date_to_entry.get().strip(),
            "favorites_only": favorites_var.get(),
        }
        # Find ancestor that has database_frame/search_frame (the SearchMainFrame)
        host = self.parent_window
        while host is not None and not (hasattr(host, "database_frame") or hasattr(host, "search_frame")):
            host = getattr(host, "master", None)

        if host is not None and hasattr(host, "database_frame"):
            host.database_frame.apply_advanced_filters(filters)

        # Store filters on the search frame so subsequent searches respect them
        if host is not None and hasattr(host, "search_frame"):
            try:
                host.search_frame.filters = filters
            except Exception:
                pass
        self.destroy()

    def reset_filters(self):
        """Reset all filters and refresh main view"""
        self.filters = {}
        # Find ancestor host
        host = self.parent_window
        while host is not None and not (hasattr(host, "database_frame") or hasattr(host, "search_frame")):
            host = getattr(host, "master", None)

        if host is not None and hasattr(host, "database_frame"):
            host.database_frame.populate_treeview()
        if host is not None and hasattr(host, "search_frame"):
            try:
                host.search_frame.filters = {}
            except Exception:
                pass
        self.destroy()

    def open_filters(self):
        # Frame for filters
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="both", expand=True, padx=25, pady=15)

        # Full Name filter
        ctk.CTkLabel(
            filter_frame, text="Full Name:", font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        fullname_entry = ctk.CTkEntry(
            filter_frame,
            width=450,
            placeholder_text="Filter by name",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=16),
        )
        fullname_entry.pack(anchor="w", pady=5)

        # Device Model filter
        ctk.CTkLabel(
            filter_frame, text="Device Model:", font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        model_entry = ctk.CTkEntry(
            filter_frame,
            width=450,
            placeholder_text="Filter by model",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=16),
        )
        model_entry.pack(anchor="w", pady=5)

        # Service Provider filter
        ctk.CTkLabel(
            filter_frame,
            text="Service Provider:",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(10, 5))
        provider_entry = ctk.CTkEntry(
            filter_frame,
            width=450,
            placeholder_text="Filter by provider",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=16),
        )
        provider_entry.pack(anchor="w", pady=5)

        # Problem Type filter
        ctk.CTkLabel(
            filter_frame, text="Problem Type:", font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        problem_entry = ctk.CTkEntry(
            filter_frame,
            width=450,
            placeholder_text="Filter by problem",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=16),
        )
        problem_entry.pack(anchor="w", pady=5)

        # Date range filters
        ctk.CTkLabel(
            filter_frame,
            text="Date From (YYYY-MM-DD):",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(10, 5))
        date_from_entry = ctk.CTkEntry(
            filter_frame,
            width=450,
            placeholder_text="e.g., 2024-01-01",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=16),
        )
        date_from_entry.pack(anchor="w", pady=5)

        ctk.CTkLabel(
            filter_frame,
            text="Date To (YYYY-MM-DD):",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(10, 5))
        date_to_entry = ctk.CTkEntry(
            filter_frame,
            width=450,
            placeholder_text="e.g., 2024-12-31",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=16),
        )
        date_to_entry.pack(anchor="w", pady=5)

        # Favorites only checkbox
        favorites_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            filter_frame,
            text="Show Favorites Only",
            variable=favorites_var,
            font=ctk.CTkFont(size=16),
        ).pack(anchor="w", pady=(15, 10))

        # Button frame
        button_frame = ctk.CTkFrame(filter_frame)
        button_frame.pack(fill="x", pady=15)

        apply_btn = ctk.CTkButton(
            button_frame,
            text="Apply Filters",
            command=lambda: self.apply_filters(
                fullname_entry,
                model_entry,
                provider_entry,
                problem_entry,
                date_from_entry,
                date_to_entry,
                favorites_var,
            ),
            width=160,
            height=40,
            fg_color="green",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=12),
        )
        apply_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.reset_filters,
            width=160,
            height=40,
            fg_color="red",
            font=ctk.CTkFont(family=PERSIAN_FONT, size=12),
        )
        reset_btn.pack(side="left", padx=5)
