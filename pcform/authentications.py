import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional

from services.auth_service import AuthService
from utils.widget_utils import set_icon


class LoginForm(ctk.CTkFrame):
    """Login form widget."""

    def __init__(
        self, parent: ctk.CTk, auth_service: AuthService, on_success: Callable[[], None]
    ):
        super().__init__(parent)
        self.auth_service = auth_service
        self.on_success = on_success
        self._create_widgets()
        self._load_saved_username()

    def _create_widgets(self):
        # Username
        ctk.CTkLabel(self, text="Username:").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password
        ctk.CTkLabel(self, text="Password:").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry.bind("<Return>", lambda e: self._handle_login())

        # Button
        ctk.CTkButton(self, text="Login", command=self._handle_login).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=3, column=0, columnspan=2)

    def _handle_login(self):
        result = self.auth_service.login(
            self.username_entry.get(), self.password_entry.get()
        )

        if result.success:
            self.error_label.configure(text="")
            messagebox.showinfo("Success", result.message)
            self.on_success()
        else:
            self.error_label.configure(text=result.message)

    def _load_saved_username(self):
        saved = self.auth_service.get_last_username()
        if saved:
            self.username_entry.insert(0, saved)


class RegisterForm(ctk.CTkFrame):
    """Register form widget."""

    def __init__(
        self, parent: ctk.CTk, auth_service: AuthService, on_success: Callable[[], None]
    ):
        super().__init__(parent)
        self.auth_service = auth_service
        self.on_success = on_success
        self._create_widgets()

    def _create_widgets(self):
        # Username
        ctk.CTkLabel(self, text="Username:").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password
        ctk.CTkLabel(self, text="Password:").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Confirm
        ctk.CTkLabel(self, text="Confirm:").grid(
            row=2, column=0, padx=10, pady=5, sticky="e"
        )
        self.confirm_entry = ctk.CTkEntry(self, show="*", width=200)
        self.confirm_entry.grid(row=2, column=1, padx=10, pady=5)

        # Button
        ctk.CTkButton(
            self,
            text="Register",
            fg_color="green",
            hover_color="darkgreen",
            command=self._handle_register,
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # Error
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0, columnspan=2)

    def _handle_register(self):
        result = self.auth_service.register(
            self.username_entry.get(),
            self.password_entry.get(),
            self.confirm_entry.get(),
        )

        if result.success:
            messagebox.showinfo("Success", result.message)
            self.on_success()
        else:
            self.error_label.configure(text=result.message)


class AuthWindow(ctk.CTk):
    """Main authentication window."""

    def __init__(self):
        super().__init__()

        self.title("Computer Services - Login")
        self.resizable(False, False)
        self.minsize(350, 280)
        self.maxsize(350, 280)

        # Create service (Dependency Injection)
        self.auth_service = AuthService()

        self.current_form: Optional[ctk.CTkFrame] = None

        self._center_window()
        self._create_navigation()
        self._show_login_form()

        set_icon(self)

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 350) // 2
        y = (self.winfo_screenheight() - 280) // 2
        self.geometry(f"+{x}+{y}")

    def _create_navigation(self):
        nav = ctk.CTkFrame(self)
        nav.grid(row=0, column=0, pady=10, sticky="ew")

        self.login_btn = ctk.CTkButton(
            nav, text="Sign In", command=self._show_login_form
        )
        self.login_btn.pack(side="left", padx=10)

        self.register_btn = ctk.CTkButton(
            nav,
            text="Register",
            fg_color="green",
            hover_color="darkgreen",
            command=self._show_register_form,
        )
        self.register_btn.pack(side="left", padx=10)

    def _clear_form(self):
        if self.current_form:
            self.current_form.destroy()
            self.current_form = None

    def _show_login_form(self):
        self._clear_form()
        self.current_form = LoginForm(self, self.auth_service, self._on_auth_success)
        self.current_form.grid(row=1, column=0, padx=20, pady=10)
        self.login_btn.configure(state="disabled")
        self.register_btn.configure(state="normal")

    def _show_register_form(self):
        self._clear_form()
        self.current_form = RegisterForm(
            self, self.auth_service, self._show_login_form  # Go to login after register
        )
        self.current_form.grid(row=1, column=0, padx=20, pady=10)
        self.login_btn.configure(state="normal")
        self.register_btn.configure(state="disabled")

    def _on_auth_success(self):
        """Called when login succeeds - transition to main app."""
        # Use after() to schedule the transition safely
        self.after(100, self._open_main_app)

    def _open_main_app(self):
        """Safely open main app and close auth window."""
        from app import App

        self.destroy()

        app = App()
        app.mainloop()

