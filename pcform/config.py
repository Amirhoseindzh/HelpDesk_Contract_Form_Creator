import os

# icons path settings
project_folder = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current script's directory
ICON_PATH = os.path.join(project_folder, "icons/banana.ico")   # Assuming the icons folder is in your project directory


#database path settings
db_folder = os.path.join(project_folder, 'db')
PCFORM_DB_PATH = os.path.join(db_folder, "pcform_db.db")

if not os.path.exists(db_folder):
    os.makedirs(db_folder)
   