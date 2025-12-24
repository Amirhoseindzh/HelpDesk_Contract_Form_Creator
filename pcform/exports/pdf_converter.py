import os
from contextlib import contextmanager
from typing import Optional

from .document_generator import form_saveto_docx_handler


class PDFConverter:
    """Converts DOCX files to PDF."""

    PDF_FORMAT = 17

    @contextmanager
    def _get_word_app(self):
        """Context manager for Word application."""
        import win32com.client

        word = None
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
            yield word
        finally:
            if word:
                try:
                    word.Quit(SaveChanges=False)
                except Exception:
                    pass

    def convert(self, docx_path: str, pdf_path: Optional[str] = None) -> str:
        """Convert DOCX to PDF."""
        docx_path = os.path.abspath(docx_path)
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"DOCX file not found: {docx_path}")

        if pdf_path is None:
            pdf_path = docx_path.replace(".docx", ".pdf")
        pdf_path = os.path.abspath(pdf_path)

        doc = None
        with self._get_word_app() as word:
            try:
                doc = word.Documents.Open(docx_path, ReadOnly=True)
                doc.SaveAs(pdf_path, FileFormat=self.PDF_FORMAT)
            except Exception as e:
                raise RuntimeError(f"PDF conversion failed: {e}")
            finally:
                if doc:
                    try:
                        doc.Close(SaveChanges=False)
                    except Exception:
                        pass

        if not os.path.exists(pdf_path):
            raise RuntimeError("PDF file was not created")

        return pdf_path


def convert_docx_to_pdf(docx_path: str, pdf_path: str) -> bool:
    """Convenience function - drop-in replacement."""
    converter = PDFConverter()
    converter.convert(docx_path, pdf_path)
    return True


def form_docx_to_pdf_handler(data_list: list, destination_folder: str) -> str:
    """Generate DOCX and convert to PDF."""

    docx_path = form_saveto_docx_handler(data_list, destination_folder)

    pdf_path = destination_folder + ".pdf"
    converter = PDFConverter()
    converter.convert(docx_path, pdf_path)

    try:
        os.remove(docx_path)
    except OSError:
        pass

    print(f"✅ PDF created: {pdf_path}")
    return pdf_path
