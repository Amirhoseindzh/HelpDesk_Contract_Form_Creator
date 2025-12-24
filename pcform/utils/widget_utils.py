import webbrowser

from settings.config import ICON_PATH, PNG_PATH


def set_icon(parent):
    """set window icon"""
    if ICON_PATH:
        parent.after(200, lambda: parent.iconbitmap(ICON_PATH))
    else:
        parent.after(200, lambda: parent.iconbitmap(PNG_PATH))


def open_link(url: str):
    webbrowser.open(url)


def center_window(parent):
    """window center on the screen"""
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    x_coordinate = int((screen_width - parent.window_width) / 2)
    y_coordinate = int((screen_height - parent.window_height) / 2)
    parent.geometry(
        f"{parent.window_width}x{parent.window_height}+{x_coordinate}+{y_coordinate}"
    )


def center_dialog(dialog, width, height):
    """Center a dialog window on the screen"""
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2
    dialog.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")
