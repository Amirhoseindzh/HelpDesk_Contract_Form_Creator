import os
import ctypes


# icons path settings
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Get the absolute path of the current script's directory

ICON_PATH = os.path.join(
    BASE_DIR, "icons/banana.ico"
)  # Assuming the icons folder is in your project directory
PNG_PATH = os.path.join(BASE_DIR, "icons/banana.png")
# Logo path for PDF (optional)
LOGO_PATH = None  # Set to image file path to add company logo to PDFs

# PDF Settings
PDF_TERMS_AND_CONDITIONS = """Terms & Conditions:
- Service provided as requested
- All terms agreed upon verbally or in writing
- Payment due upon completion
- 30-day warranty on parts"""

# Theme preference (light, dark, or system)
THEME_MODE = "system"

# Persian font to use for inputs and PDFs (adjust to installed font on the system)
PERSIAN_FONT = "Tahoma"

# database path settings
db_folder = os.path.join(BASE_DIR, "db")
PCFORM_DB_PATH = os.path.join(db_folder, "pcform_db.db")

if not os.path.exists(db_folder):
    os.makedirs(db_folder)


# Security
MIN_PASSWORD_LENGTH = 6
USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"


# Generate a unique AppID for your program
myappid = "amirdzh.pcform.config.v2.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
