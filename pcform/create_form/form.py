from tkinter import filedialog, messagebox

import customtkinter as ctk
from exports.pdf_converter import convert_docx_to_pdf, form_docx_to_pdf_handler
from repositories.pcform_repo import PCFormRepository
from settings.config import PERSIAN_FONT
from utils.widget_utils import set_icon

# Constants
PLACEHOLDER_DESCRIPTION = "Enter detailed service description..."


class FormDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, on_success_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.maxsize(700, 750)
        self.minsize(700, 750)
        self.resizable(False, False)
        set_icon(self)
        self.entries = {}
        self.form_data = []
        self.pcform_db = PCFormRepository()
        self.on_success_callback = on_success_callback
        self.is_saved = False

        # Main container with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Logo
        logo_label = ctk.CTkLabel(
            main_frame,
            text="🍌",
            font=ctk.CTkFont(size=48),
        )
        logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Create Service Form",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

        fields = [
            ("Full Name *", "fullname"),
            ("Device Model *", "Device_Model"),
            ("Device Serial *", "Device_Serial"),
            ("Service Provider *", "ServiceMan"),
            ("Device Problem *", "Device_Problem"),
        ]

        # Configure grid weights
        main_frame.grid_columnconfigure(1, weight=1)

        for i, (label_text, entry_name) in enumerate(fields, start=2):
            label = ctk.CTkLabel(
                main_frame, text=label_text, font=ctk.CTkFont(size=14, weight="bold")
            )
            label.grid(row=i, column=0, padx=(0, 15), pady=12, sticky="w")

            entry = ctk.CTkEntry(
                main_frame,
                width=380,
                placeholder_text=f"Enter {label_text.replace(' *', '')}",
                font=ctk.CTkFont(family=PERSIAN_FONT, size=13),
            )
            entry.grid(row=i, column=1, padx=5, pady=12, sticky="ew")
            self.entries[entry_name] = entry

        # Description field
        description_label = ctk.CTkLabel(
            main_frame,
            text="Service Description *",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        description_label.grid(
            row=len(fields) + 2, column=0, padx=(0, 15), pady=(12, 8), sticky="nw"
        )

        self.description_entry = ctk.CTkTextbox(
            main_frame,
            height=150,
            width=380,
            font=ctk.CTkFont(family=PERSIAN_FONT, size=13),
        )
        self.description_entry.grid(
            row=len(fields) + 2, column=1, padx=5, pady=12, sticky="ew"
        )
        self.description_entry.insert("1.0", PLACEHOLDER_DESCRIPTION)
        self.description_entry.bind(
            "<FocusIn>",
            lambda e: (
                self.clear_placeholder()
                if self.description_entry.get("1.0", "end-1c")
                == PLACEHOLDER_DESCRIPTION
                else None
            ),
        )

        self.entries["description"] = self.description_entry

        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=len(fields) + 3, columnspan=2, pady=12)

        # Button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=len(fields) + 4, columnspan=2, pady=15, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        submit_button = ctk.CTkButton(
            button_frame,
            text="💾 Save & Export",
            command=self.submit_form,
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen",
        )
        submit_button.grid(row=0, column=0, padx=8, pady=8)

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="gray",
            hover_color="darkgray",
        )
        cancel_button.grid(row=0, column=1, padx=8, pady=8)

    def clear_placeholder(self):
        """Clear placeholder text when user focuses on description field"""
        if self.description_entry.get("1.0", "end-1c") == PLACEHOLDER_DESCRIPTION:
            self.description_entry.delete("1.0", "end")

    def submit_form(self):
        """Main form submission handler"""
        if not self._validate_fields():
            return

        form_data_dict = self._collect_form_data()
        self.form_data = [form_data_dict]

        self.status_label.configure(text="Saving...", text_color="blue")

        file_path = self._get_save_file_path(form_data_dict)

        if file_path:
            self._save_form_to_database_and_pdf(file_path)
        else:
            self.status_label.configure(text="Save cancelled", text_color="orange")

    def _validate_fields(self):
        """Validate all form fields"""
        validation_errors = []
        for entry_name, entry_widget in self.entries.items():
            if isinstance(entry_widget, ctk.CTkEntry):
                value = entry_widget.get().strip()
                if not value:
                    field_label = entry_name.replace("_", " ").title()
                    validation_errors.append(f"{field_label} is required")
            elif isinstance(entry_widget, ctk.CTkTextbox):
                value = entry_widget.get("1.0", "end-1c").strip()
                if not value or value == PLACEHOLDER_DESCRIPTION:
                    validation_errors.append("Service Description is required")

        if validation_errors:
            error_msg = "Please fill out all required fields:\n" + "\n".join(
                f"• {err}" for err in validation_errors
            )
            messagebox.showerror("Validation Error", error_msg)
            self.status_label.configure(
                text="Please fill all required fields", text_color="red"
            )
            return False
        return True

    def _collect_form_data(self):
        """Collect form data from all entry fields"""
        form_data_dict = {}
        for entry_name, entry_widget in self.entries.items():
            if isinstance(entry_widget, ctk.CTkEntry):
                value = entry_widget.get().strip()
            else:
                value = entry_widget.get("1.0", "end-1c").strip()
            form_data_dict[entry_name] = value
        return form_data_dict

    def _get_save_file_path(self, form_data_dict):
        """Get the file path from user"""
        default_filename = f"Contract_{form_data_dict.get('fullname', 'Service')}_{form_data_dict.get('Device_Model', '')}"
        return filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=default_filename,
        )

    def _save_form_to_database_and_pdf(self, file_path):
        """Save form data to database and export to PDF"""
        try:
            # Prepare data for database (map 'description' to 'Description')
            db_data = self._prepare_database_data()

            # Insert into database first and get inserted ID
            # `db_data` is a list of dicts; repository.create expects a single dict
            if not db_data:
                raise ValueError("No data to save to database.")

            inserted_id = self.pcform_db.create(db_data[0])
            if not inserted_id:
                raise ValueError("Failed to save record to database.")

            # Fetch freshly saved record to obtain created_at timestamp
            record = self.pcform_db.get_by_id(inserted_id)
            created_at = record.get("created_at") if record else None

            # Build export payload from current form data and include created_at
            export_payload = []
            for item in self.get_data():
                item_copy = item.copy()
                if created_at:
                    item_copy["created_at"] = created_at
                export_payload.append(item_copy)

            # Try to create PDF using payload that includes saved timestamp
            try:
                form_docx_to_pdf_handler(export_payload, file_path)
            except (IOError, OSError, ValueError) as pdf_error:
                # PDF failed but DB save succeeded
                self.status_label.configure(
                    text=f"⚠ Form saved to database, but PDF export failed: {str(pdf_error)}",
                    text_color="orange",
                )
                messagebox.showwarning(
                    "Partial Success",
                    f"Form data saved to database successfully.\n\nHowever, PDF export failed:\n{str(pdf_error)}\n\nPlease try exporting again from the Search window.",
                )
            else:
                # Success
                self.status_label.configure(
                    text="✓ Form saved and contract exported successfully!",
                    text_color="green",
                )
                messagebox.showinfo(
                    "Success",
                    f"Form saved successfully!\n\nContract exported to:\n{file_path}\n\nRecord added to database.",
                )

            # Mark as saved and cleanup
            self.is_saved = True
            self._callback_and_cleanup()

        except (IOError, OSError, ValueError, AttributeError) as e:
            error_msg = f"Error saving form: {str(e)}"
            self.status_label.configure(text=error_msg, text_color="red")
            messagebox.showerror("Error", error_msg)

    def _prepare_database_data(self):
        """Prepare form data for database insertion"""
        db_data = []
        for item in self.get_data():
            db_item = item.copy()
            if "description" in db_item:
                db_item["Description"] = db_item.pop("description")
            db_data.append(db_item)
        return db_data

    def _export_to_pdf(self, file_path):
        """Export form data to PDF"""
        try:
            form_docx_to_pdf_handler(self.get_data(), file_path)
            # Success
            self.status_label.configure(
                text="✓ Form saved and contract exported successfully!",
                text_color="green",
            )
            messagebox.showinfo(
                "Success",
                f"""Form saved successfully!\n\n
                Contract exported to:\n{file_path}\n\n
                Record added to database.""",
            )
        except (IOError, OSError, ValueError) as pdf_error:
            # Database save succeeded, but PDF failed
            self.status_label.configure(
                text=f"⚠ Form saved to database, but PDF export failed: {str(pdf_error)}",
                text_color="orange",
            )
            messagebox.showwarning(
                "Partial Success",
                f"""Form data saved to database successfully.\n\n
                However, PDF export failed:\n{str(pdf_error)}\n\n
                Please try exporting again from the Search window.""",
            )

    def _callback_and_cleanup(self):
        """Callback and cleanup after successful save"""
        # Callback to refresh search windows
        if self.on_success_callback:
            self.on_success_callback()

        # Clear entry fields
        for entry_widget in self.entries.values():
            if isinstance(entry_widget, ctk.CTkEntry):
                entry_widget.delete(0, "end")
            elif isinstance(entry_widget, ctk.CTkTextbox):
                entry_widget.delete("1.0", "end")
                entry_widget.insert("1.0", PLACEHOLDER_DESCRIPTION)

        # Option to close after successful save
        if messagebox.askyesno(
            "Close Form", "Form saved successfully. Close this window?"
        ):
            self.destroy()

    def get_data(self) -> list:
        return self.form_data
