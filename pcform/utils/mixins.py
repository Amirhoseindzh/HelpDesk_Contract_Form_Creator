from create_form.form import FormDialog
from search_form.search import SearchMainFrame
from utils.widget_utils import center_dialog


class FormDialogMixin:
    """Mixin class to add form dialog related methods to the main App class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open_search_windows = []

    def dialog_create_form(self):
        """Open the create form dialog"""
        dialog = FormDialog(
            self, title="Create Form", on_success_callback=self.refresh_search_windows
        )
        center_dialog(dialog, 700, 750)
        dialog.transient(self)  # Make it appear above parent
        dialog.lift()  # Bring to front
        dialog.attributes("-topmost", True)  # Force to top
        dialog.after_idle(
            lambda: dialog.attributes("-topmost", False)
        )  # Remove after shown
        dialog.focus_force()  # Force focus
        dialog.grab_set()  # Grab focus, disable interactions with main window
        dialog.wait_window()  # Wait until the dialog is closed
        self.grab_release()  # Release focus, enable interactions with main window

    def dialog_search(self):
        """Open the search forms main frame"""
        main_frame = SearchMainFrame(self, title="Search Forms", app_ref=self)
        center_dialog(main_frame, 1200, 850)
        # Make it a transient window (appears above parent)
        main_frame.transient(self)
        main_frame.lift()  # Bring to front
        main_frame.attributes("-topmost", True)  # Force to top
        main_frame.after_idle(
            lambda: main_frame.attributes("-topmost", False)
        )  # Remove after shown
        main_frame.focus_force()  # Force focus
        # Track this window
        self.open_search_windows.append(main_frame)
        # Remove from list when closed
        main_frame.protocol(
            "WM_DELETE_WINDOW", lambda: self._close_search_window(main_frame)
        )

    def _close_search_window(self, window):
        """Remove window from tracking when closed"""
        if window in self.open_search_windows:
            self.open_search_windows.remove(window)
        window.destroy()

    def refresh_search_windows(self):
        """Refresh any open search windows"""
        # This will be called after form creation to refresh search results
        for search_window in self.open_search_windows:
            if search_window.winfo_exists():
                search_window.database_frame.populate_treeview()
