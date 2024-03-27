import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox


class App(ctk.CTk):
    ctk.set_appearance_mode("system")

    def __init__(self):
        super().__init__()
        self.title("cumputer services")
        self.maxsize(500, 500)
        self.minsize(500, 500)
        self.window_width = 500
        self.window_height = 500

        # add widgets to main window
        self.add_widgets()

        # Center the main window
        self.center_window()

    # add methods to app

    def add_widgets(self):
        button_crform = ctk.CTkButton(self, text="Create Form",
                                      command=self.dialog_create_form,
                                      width=200, height=100)
        button_crform.grid(row=1, column=0, padx=35, pady=200)

        button_srforms = ctk.CTkButton(self, text="Search Forms",
                                       command=self.dialog_search,
                                       width=200, height=100)
        button_srforms.grid(row=1, column=1, padx=1, pady=200)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width - self.window_width) / 2)
        y_coordinate = int((screen_height - self.window_height) / 2)
        self.geometry(
            f"{screen_width}x{screen_height}+{x_coordinate}+{y_coordinate}"
        )

    @staticmethod
    def center_dialog(dialog, width, height):
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x_coordinate = (screen_width - width) // 2
        y_coordinate = (screen_height - height) // 2
        dialog.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def dialog_create_form(self):
        dialog = FormDialog(self, title="Create Form")
        self.center_dialog(dialog, 300, 400)
        dialog.grab_set()  # Grab focus, disable interactions with main window
        dialog.wait_window()  # Wait until the dialog is closed
        self.grab_release()  # Release focus, enable interactions with main window

    @staticmethod
    def dialog_search():
        dialog = ctk.CTkInputDialog(text="Search Forms:", title="Search")
        App.center_dialog(dialog, 300, 200)
        print("Search:", dialog.get_input())


class FormDialog(ctk.CTkToplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.maxsize(400, 420)
        self.minsize(400, 420)
        self.entries = {}

        fields = [
            ("Full Name:", "fullname"),
            ("Device Model:", "device_model"),
            ("Device Serial Number:", "device_serial"),
            ("Service Man Full Name:", "serviceman"),
            ("Device Problem:", "device_problem")
        ]

        for i, (label_text, entry_name) in enumerate(fields):
            label = ctk.CTkLabel(self, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(self, width=220)
            entry.grid(row=i, column=1, padx=5, pady=7, sticky="we")
            self.entries[entry_name] = entry

        description_label = ctk.CTkLabel(self, text="Description:")
        description_label.grid(row=len(fields), column=0,
                               padx=5, pady=5, sticky="w")

        self.description_entry = ctk.CTkTextbox(
            self, height=100, width=40)

        self.description_entry.grid(
            row=len(fields), column=1, padx=5, pady=7, sticky="we")

        self.entries["description"] = self.description_entry

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=len(fields) + 1,
                               columnspan=2, padx=6, pady=10)

        submit_button = ctk.CTkButton(self, text="Submit",
                                      command=self.submit_form)

        submit_button.grid(row=len(fields) + 2, columnspan=2, padx=6, pady=0)

    def submit_form(self):
        for entry_name, entry_widget in self.entries.items():
            if isinstance(entry_widget, ctk.CTkEntry) and not entry_widget.get():
                messagebox.showerror("Error", "Please fill out all fields.")
                return

            if isinstance(entry_widget, ctk.CTkTextbox) and not entry_widget.get("1.0", "end-1c"):
                messagebox.showerror("Error", "Please fill out all fields.")
                return

        form_data = {
            entry_name: entry_widget.get()
            if isinstance(entry_widget, ctk.CTkEntry)
            else entry_widget.get("1.0", "end-1c")
            for entry_name, entry_widget in self.entries.items()
        }
        print("Form submitted successfully!")
        print("Form Data:", form_data)

        # Clear entry fields
        for entry_widget in self.entries.values():
            if isinstance(entry_widget, ctk.CTkEntry):
                entry_widget.delete(0, 'end')
            elif isinstance(entry_widget, ctk.CTkTextbox):
                entry_widget.delete('1.0', 'end')

        # Display success message
        self.status_label.configure(text="Data saved successfully!",
                                    text_color="green")


app = App()
app.mainloop()
