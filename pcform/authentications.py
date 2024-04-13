from config import ICON_PATH
from data_store import PcFormDatabase
from tkinter import messagebox
import customtkinter as ctk
import re


class LoginForm(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = ctk.CTkButton(
            self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=3, column=0, columnspan=2)

        # Load saved username if available
        self.load_saved_username()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Perform validation
        if not username or not password:
            self.error_label.configure(
                text="Username and password are required.")
            return

        # Here you would implement your actual authentication logic
        data_filter = PcFormDatabase.auth_data_retrieve(username, password)
        if data_filter== True:
            self.error_label.configure(text="")
            messagebox.showinfo("Success", "Login successful!")
            self.on_login_success()
        else:
            self.error_label.configure(text="Invalid username or password.")

    def load_saved_username(self):
        # Load saved username if available
        # Here you would implement loading saved username from a file or database
        # For demonstration purposes, let's assume there is a saved username
        saved_username = PcFormDatabase.load_last_username()
        self.username_entry.insert(0, saved_username)


class RegisterForm(ctk.CTkFrame):
    def __init__(self, parent, on_register_success):
        super().__init__(parent)
        self.parent = parent
        self.on_register_success = on_register_success
        self.create_widgets()

    def create_widgets(self):
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.confirm_password_label = ctk.CTkLabel(
            self, text="Confirm Password:")
        self.confirm_password_label.grid(
            row=2, column=0, padx=10, pady=5, sticky="e")
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.register_button = ctk.CTkButton(
            self, text="Register", fg_color="green",
            hover_color="darkgreen", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0, columnspan=2)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        entries_list = [{"username": username, "password": password}]
        # Perform validation
        if not username or not password or not confirm_password:
            self.error_label.configure(text="All fields are required.")
            return

        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match.")
            return

        if len(password) < 6:
            self.error_label.configure(
                text="Password must be at least 6 characters long.")
            return

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            self.error_label.configure(
                text="Username can only contain letters and numbers.")
            return

        # Here you would implement your actual registration logic
        user_exists = PcFormDatabase.check_user_exists(username)
        if user_exists == False:
            self.error_label.configure(
                text=f"Username '{username}' is already exist.")
            return
        else:
            PcFormDatabase.insert_pcform_auth(entries_list)

        # For demonstration purposes, let's just print the entered username and password
        print("Registered username:", username)
        print("Registered password:", password)

        messagebox.showinfo("Success", "Registration successful!")
        self.on_register_success()


# import icon path


class AuthApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Computer Services")
        self.maxsize(325, 260)
        self.minsize(325, 260)
        self.window_width = 570
        self.window_height = 570

        self.current_form = None
        # Add widgets to main window
        self.center_window()
        self.add_auth_widgets()
        self.setup_icon()

    def setup_icon(self):
        # You can define ICON_PATH here if needed
        if ICON_PATH:
            self.iconbitmap(ICON_PATH)

    def add_auth_widgets(self):
        self.show_login_form()
        self.show_register_form()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width - self.window_width) / 2)
        y_coordinate = int((screen_height - self.window_height) / 2)
        self.geometry(
            f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

    def show_login_form(self):
        if not isinstance(self.current_form, LoginForm):
            if self.current_form:
                self.current_form.grid_forget()
            self.current_form = self.show_register_button()
            self.current_form = LoginForm(self, self.switch_to_app)
            self.current_form.grid(
                row=1, column=0, columnspan=2, padx=10, pady=10)

    def show_register_form(self):
        if self.current_form:
            self.current_form.grid_forget()
        self.current_form = self.show_login_button()
        self.current_form = RegisterForm(self, self.switch_to_app)
        self.current_form.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def show_login_button(self):
        if self.current_form:
            self.current_form.grid_forget()
            self.current_form = None
        self.login_button = ctk.CTkButton(
            self, text="Sign in", command=self.show_login_form)
        self.login_button.grid(row=0, column=0, padx=10, pady=10)

    def show_register_button(self):
        if self.current_form:
            self.current_form.grid_forget()
            self.current_form = None
        self.register_button = ctk.CTkButton(
            self, text="Register", fg_color="green", hover_color="darkgreen",
            command=self.show_register_form)
        self.register_button.grid(row=0, column=1, padx=10, pady=10)

    def switch_to_app(self):
        from form import App
        self.destroy()  # Close the AuthApp window
        # Run your app class after successful login or registration
        app = App()
        app.add_widgets()
        app.mainloop()


auth_app = AuthApp()
auth_app.mainloop()

# its developed by @amirhoseindzh
