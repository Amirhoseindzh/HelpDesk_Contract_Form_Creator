import tkinter as tk
import customtkinter as ctk


class App(ctk.CTk):
    ctk.set_appearance_mode("system")

    def __init__(self):
        super().__init__()
        self.title("cumputer services")
        self.maxsize(500, 500)
        self.minsize(500, 500)
        self.window_width = 500
        self.window_height = 500
        self.center_window()

        # add widgets to app

        button_crform = ctk.CTkButton(self, text="Create Form",
                                      command=self.dialog_create_form,
                                      width=200, height=100)
        button_crform.grid(row=1, column=0, padx=35, pady=200)

        button_srforms = ctk.CTkButton(self, text="Search Forms",
                                       command=self.dialog_search,
                                       width=200, height=100)
        button_srforms.grid(row=1, column=1, padx=1, pady=200)

    # add methods to app
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width - self.window_width) / 2)
        y_coordinate = int((screen_height - self.window_height) / 2)

        self.geometry(
            f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

    @classmethod
    def dialog_geometry(cls, dialog, dialog_width, dialog_height):
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()

        x_coordinate = int((screen_width - dialog_width) / 2)
        y_coordinate = int((screen_height - dialog_height) / 2)

        dialog.geometry(
            f"{dialog_width}x{dialog_height}+{x_coordinate}+{y_coordinate}")

    @classmethod
    def dialog_create_form(cls):
        dialog_width = 300  # Adjust as needed
        dialog_height = 200  # Adjust as needed
        dialog = ctk.CTkInputDialog(text="Fill The Form:", title="Create Form")
        cls.dialog_geometry(dialog, dialog_width, dialog_height)
        print("Fullname:", dialog.get_input())

    @classmethod
    def dialog_search(cls):
        dialog_width = 300  # Adjust as needed
        dialog_height = 200  # Adjust as needed
        dialog = ctk.CTkInputDialog(text="Search Forms:", title="serach")
        cls.dialog_geometry(dialog, dialog_width, dialog_height)
        print("Search:", dialog.get_input())


app = App()
app.mainloop()
