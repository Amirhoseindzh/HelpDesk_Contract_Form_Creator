from tkinter import filedialog
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from data_store import PcFormDatabase
from form_handler import form_docx_to_pdf_handler
from config import ICON_PATH


class App(ctk.CTk):
    ctk.set_appearance_mode("system")
    def __init__(self):
        super().__init__()
        self.title("Computer Services")
        self.maxsize(500, 570)
        self.minsize(500, 570)
        self.window_width = 570
        self.window_height = 570

        # add widgets to main window
        self.add_widgets()  # add widgets to main window
        self.setup_icon()  # change icon
        self.center_window()  # Center the main window

    # add methods to app
    def setup_icon(self):  # initialize icon
        if ICON_PATH:
            self.iconbitmap(ICON_PATH)

    def add_widgets(self):
        button_crform = ctk.CTkButton(self, text="Create Form",
                                      command=self.dialog_create_form,
                                      width=200, height=100)
        button_crform.grid(row=1, column=0, padx=35, pady=200)

        button_srforms = ctk.CTkButton(self, text="Search Forms",
                                       command=self.dialog_search,
                                       width=200, height=100)
        button_srforms.grid(row=1, column=1, padx=1, pady=200)

        author_label = ctk.CTkLabel(self,
                                    text="""Author Email: amirdej6@gmail.com .
                                    \nAuthor Social Acc: @amirhoseindzh.""")
        author_label.grid(row=2, column=0, padx=15, pady=0, sticky="w")
        author_label.configure(text_color="lightblue")

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
        self.center_dialog(dialog, 400, 300)
        dialog.grab_set()  # Grab focus, disable interactions with main window
        dialog.wait_window()  # Wait until the dialog is closed
        self.grab_release()  # Release focus, enable interactions with main window

    def dialog_search(self):
        main_frame = SearchMainFrame(self, title="Search Forms")
        App.center_dialog(main_frame, 600, 600)


class FormDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.maxsize(400, 420)
        self.minsize(400, 420)
        self.iconbitmap = self.setup_icon()
        self.entries = {}
        self.pcform_db = PcFormDatabase
        
        fields = [
            ("Full Name:", "fullname"),
            ("Device Model:", "device_model"),
            ("Device Serial Number:", "device_serial"),
            ("ServiceMan FullName:", "serviceman"),
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

        submit_button = ctk.CTkButton(
            self, text="Submit", command=self.submit_form)
        submit_button.grid(row=len(fields) + 2, columnspan=2, padx=6, pady=0)

    def setup_icon(self):
        # You can define ICON_PATH here if needed
        if ICON_PATH:
            self.iconbitmap(ICON_PATH)

    def submit_form(self):
        for entry_name, entry_widget in self.entries.items():
            if isinstance(entry_widget, ctk.CTkEntry) and not entry_widget.get():
                messagebox.showerror("Error", "Please fill out all fields.")
                return

            if isinstance(entry_widget, ctk.CTkTextbox) and not entry_widget.get("1.0", "end-1c"):
                messagebox.showerror("Error", "Please fill out all fields.")
                return

        self.form_data = [{
            entry_name: entry_widget.get()
            if isinstance(entry_widget, ctk.CTkEntry)
            else entry_widget.get("1.0", "end-1c")
            for entry_name, entry_widget in self.entries.items()
        }
        ]

        # Save form data to file
        file_path = filedialog.asksaveasfilename(defaultextension="",
                                                 filetypes=[
                                                     ("PDF (*.pdf)", ""),
                                                     # ("All Files", "*.*"),
                                                 ]
                                                 )
        if file_path:
            # create and insert data table in db
            self.pcform_db.insert_pcform(self.get_data())
            # create pdf from docx file
            form_docx_to_pdf_handler(self.get_data(), file_path)
            print("Form data saved successfully to:", file_path)
            # Display success message
            self.status_label.configure(text="Data saved successfully!",
                                        text_color="green")
            # Clear entry fields
            for entry_widget in self.entries.values():
                if isinstance(entry_widget, ctk.CTkEntry):
                    entry_widget.delete(0, 'end')
                elif isinstance(entry_widget, ctk.CTkTextbox):
                    entry_widget.delete('1.0', 'end')
        else:
            self.status_label.configure(text="cancled",
                                        text_color="red")

    def get_data(self):
        return self.form_data


class SearchMainFrame(ctk.CTkToplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.minsize(800, 800)
        #self.maxsize(800, 800)
        self.iconbitmap = self.setup_icon()
        self.search_frame = SearchForm(self)
        self.search_frame.pack(fill="x", padx=10, pady=10)

        self.detail_button = ctk.CTkButton(
            self, text="Show Detail", command=self.toggle_detail)
        self.detail_button.pack(pady=10)

        self.database_frame = DatabaseInfo(self)
        self.database_frame.pack(fill="both", padx=10, pady=10)
        self.hide_database_info()

    def setup_icon(self):
        # You can define ICON_PATH here if needed
        if ICON_PATH:
            self.iconbitmap(ICON_PATH)

    def toggle_detail(self):
        if self.database_frame.winfo_ismapped():
            self.hide_database_info()
            self.detail_button.configure(text="Show Detail")
        else:
            self.show_database_info()
            self.detail_button.configure(text="Hide Detail")

    def show_database_info(self):
        self.database_frame.pack(fill="both", padx=10, pady=10)

    def hide_database_info(self):
        self.database_frame.pack_forget()


class SearchForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.entry = ctk.CTkEntry(self, width=200)
        self.entry.pack(side="top", padx=1, pady=2)

        self.search_button = ctk.CTkButton(
            self, text="Search", command=self.search)
        self.search_button.pack(side="top", padx=2, pady=1)

        self.database_frame = DatabaseInfo(self)
        self.database_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def search(self):
        query = self.entry.get()

        # Implement search functionality here
        self.database_frame.search(query)
        print("Searching for:", query)


class DatabaseInfo(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title_list = PcFormDatabase.get_column_titles()
        # Adjust columns as needed
        self.tree = ttk.Treeview(self, columns=self.title_list)
        # self.tree.heading('#0', text='ID')
        for i, column in enumerate(self.title_list):
            self.tree.heading(f'#{i}', text=column)

        # Populate Treeview with data
        self.populate_treeview()
        self.tree.pack(fill='both', expand=True)

    def populate_treeview(self):
        # Fetch data from database
        rows = PcFormDatabase.treeview()
        # Insert fetched data into treeview
        for row in rows:
            # Assuming first column is ID
            self.tree.insert('', 'end', text=row[0], values=row[1:])

    def search(self, query):
        self.tree.delete(*self.tree.get_children())
        search_columns = ["fullname", "Device_Model", "Device_Serial",
            "ServiceMan", "Device_Problem", "Description"]
        search_result = PcFormDatabase._search(search_columns, query)

        if search_result:
            for row in self.tree.get_children(): # Clear existing rows in the tree
                self.tree.delete(row)
            for item in search_result:  # Insert new rows with the search results
                self.tree.insert('', 'end',text=item[0], values=item[1:])
        else:
            self.tree.insert('', 'end', values=("\t\tNo results found.",))


def main():
    app = App()
    app.mainloop()
    