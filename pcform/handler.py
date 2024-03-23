import win32com.client
from docx import Document
import os

# docx handlers


def add_user_input_to_docx(filename, data_list):
    file_name = f"{filename}.docx"
    document = Document()
    document.add_heading('Computer service', 0)
    for data in data_list:
        document.add_paragraph(data, style='List Number')
    document.save(file_name)


# pdf handlers

def docx_to_pdf(input_docx_file, output_pdf_file):
    # Create a new instance of the Word application
    word = win32com.client.Dispatch("Word.Application")

    try:
        # Open the Word document
        file_path = os.path.abspath(input_docx_file)
        if os.path.exists(file_path):
            doc = word.Documents.Open(file_path)

        # Save the document as PDF
        # 17 corresponds to PDF format
        doc.SaveAs(output_pdf_file, FileFormat=17)

        # Close the document
        doc.Close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Quit Word application
        word.Quit()
        os.remove(file_path)
        print(f"User input added to '{input_docx_file}' successfully.")
