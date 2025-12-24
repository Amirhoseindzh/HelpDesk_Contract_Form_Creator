import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from settings.config import THEME_MODE
from utils.widget_utils import center_dialog, center_window, open_link, set_icon

from utils.mixins import FormDialogMixin

# Constants
PLACEHOLDER_DESCRIPTION = "Enter detailed service description..."


class App(FormDialogMixin, ctk.CTk):
    ctk.set_appearance_mode(THEME_MODE)

    def __init__(self):
        super().__init__()
        self.title("Computer Services")
        self.maxsize(500, 570)
        self.minsize(500, 570)
        self.window_width = 580
        self.window_height = 580
        # Disable resizing to hide the maximize icon
        self.resizable(False, False)
        # Track open search windows
        self.open_search_windows = []

        # add widgets to main window
        self.add_widgets()
        set_icon(self)  # change icon
        center_window(self)  # Center the main window
        # Create Menu
        self.create_menu()

    # Define Menu theme settings
    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="About", command=lambda: about(self))
        file_menu.add_separator()
        file_menu.add_command(
            label="Logout", command=lambda: logout(self), foreground="red"
        )

    # add methods to app
    def add_widgets(self):
        title_label = ctk.CTkLabel(
            self, text="Computer Services", font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=40, padx=10)
        button_crform = ctk.CTkButton(
            self,
            text="Create Form",
            command=self.dialog_create_form,
            width=200,
            height=100,
        )
        button_crform.grid(row=1, column=0, padx=35, pady=200)

        button_srforms = ctk.CTkButton(
            self, text="Search Forms", command=self.dialog_search, width=200, height=100
        )
        button_srforms.grid(row=1, column=1, padx=1, pady=200)


def logout(app_instance):
    """Logout the user and close the app"""
    messagebox.showinfo("Logout", "Logged out successfully!")
    app_instance.destroy()


def about(app_instance):
    """About user information window"""
    about_window = ctk.CTkToplevel(app_instance)
    about_window.title("About - Computer Services")
    about_window.geometry("450x350")
    about_window.transient(app_instance)
    about_window.lift()
    about_window.attributes("-topmost", True)
    about_window.after_idle(lambda: about_window.attributes("-topmost", False))
    about_window.resizable(False, False)
    set_icon(about_window)

    # Center the window
    center_dialog(about_window, 450, 350)

    # Main container
    main_container = ctk.CTkFrame(about_window)
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    title_label = ctk.CTkLabel(
        main_container,
        text="Computer Services",
        font=ctk.CTkFont(size=20, weight="bold"),
    )
    title_label.pack(pady=(0, 5))

    subtitle_label = ctk.CTkLabel(
        main_container,
        text="Service Contract Management System",
        font=ctk.CTkFont(size=12, slant="italic"),
    )
    subtitle_label.pack(pady=(0, 20))

    # Separator
    separator = ctk.CTkFrame(main_container, height=2, fg_color="gray")
    separator.pack(fill="x", pady=10)

    # Developer info
    dev_label = ctk.CTkLabel(
        main_container,
        text="Developer Information",
        font=ctk.CTkFont(size=14, weight="bold"),
    )
    dev_label.pack(pady=(10, 10))

    # Email section
    email_frame = ctk.CTkFrame(main_container, fg_color="transparent")
    email_frame.pack(fill="x", pady=5)

    email_label = ctk.CTkLabel(email_frame, text="📧 Email:", font=ctk.CTkFont(size=11))
    email_label.pack(side="left", padx=5)

    email_link = ctk.CTkLabel(
        email_frame,
        text="amirhosein.de78@gmail.com",
        font=ctk.CTkFont(size=18, underline=True),
        text_color="blue",
        cursor="hand2",
    )
    email_link.pack(side="left", padx=5)
    email_link.bind(
        "<Button-1>", lambda e: open_link("mailto:amirhosein.de78@gmail.com")
    )

    # GitHub section
    github_frame = ctk.CTkFrame(main_container, fg_color="transparent")
    github_frame.pack(fill="x", pady=5)

    github_label = ctk.CTkLabel(
        github_frame, text="🔗 GitHub:", font=ctk.CTkFont(size=11)
    )
    github_label.pack(side="left", padx=5)

    github_link = ctk.CTkLabel(
        github_frame,
        text="@Amirhoseindzh",
        font=ctk.CTkFont(size=18, underline=True),
        text_color="blue",
        cursor="hand2",
    )
    github_link.pack(side="left", padx=5)
    github_link.bind(
        "<Button-1>", lambda e: open_link("https://github.com/Amirhoseindzh")
    )

    # Separator
    separator2 = ctk.CTkFrame(main_container, height=2, fg_color="gray")
    separator2.pack(fill="x", pady=15)

    # Close button
    close_button = ctk.CTkButton(
        main_container,
        text="Close",
        command=about_window.destroy,
        width=120,
        height=35,
    )
    close_button.pack(pady=10)


def main():
    app = App()
    app.mainloop()
