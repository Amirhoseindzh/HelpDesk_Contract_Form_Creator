# 🧾 HelpDesk Contract Form Creator
  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-Apache--2.0-green)

A lightweight **desktop application** for creating, managing, and exporting **computer repair service contracts**.  
Designed for small help-desks and startups that need fast paperwork without heavy systems.

This project is a lightweight desktop application for creating and managing help‑desk repair contracts. It provides a simple form for entering contract details, saves records to an SQLite database, and supports exporting contracts to PDF, Excel, and CSV.


## 🖼️ Preview

<p align="center">
  <a href="assets/search_form.png">
    <img src="assets/search_form.png" width="670">
  </a> 
</p>

<p align="center"><i>Search records and generate exportable contracts</i></p>

## Features

- User authentication (login / register)
- Create service contract forms with automatic timestamps
- Store and retrieve records from SQLite
- Export to PDF, Excel (.xlsx) and CSV
- Persian font support and RTL-friendly display where configured
- View full contract details in a dedicated window

## Prerequisites

- Python 3.8+
- pip or pipenv
- Windows is required for COM-based DOCX→PDF conversion (pywin32)

## Quick Start

Clone the repository and run the app:

````bash
git clone https://github.com/Amirhoseindzh/Computer_Services_Repair_Form.git
﻿# HelpDesk Contract Form Creator

This project is a lightweight desktop application for creating and managing help‑desk repair contracts. It provides a simple form for entering contract details, saves records to an SQLite database, and supports exporting contracts to PDF, Excel, and CSV.

## Features

- User authentication (login / register)
- Create service contract forms with automatic timestamps
- Store and retrieve records from SQLite
- Export to PDF, Excel (.xlsx) and CSV
- Persian font support and RTL-friendly display where configured
- View full contract details in a dedicated window

## Prerequisites

- Python 3.8+
- pip or pipenv
- Windows is required for COM-based DOCX→PDF conversion (pywin32)

## Quick Start

Clone the repository and run the app:

```bash
git clone https://github.com/Amirhoseindzh/Computer_Services_Repair_Form.git
cd Computer_Services_Repair_Form

# Install dependencies
pip install -r requirements.txt

# Run the application
python pcform/main.py
````

Or with pipenv:

```bash
pipenv install
pipenv shell
pipenv run python pcform/main.py
```

## Configuration

Edit `pcform/settings/config.py` to customize:

- `PERSIAN_FONT` — font family used for Persian text
- `LOGO_PATH` — path to logo used in exports
- `PDF_TERMS_AND_CONDITIONS` — path to the terms document included in PDFs
- `PCFORM_DB_PATH` — path to the SQLite database file

## Usage

1. Login or register an account
2. Create a new contract using the Create Form
3. Use the Search window to find existing records
4. Select a record to view details or export to PDF/Excel/CSV

## Notes on PDF export

- DOCX → PDF conversion uses Windows automation (pywin32). On non‑Windows systems export to DOCX is supported, but automatic PDF conversion may not work.

## Optional Dependencies

- `openpyxl` — Excel export support (recommended)
- `pywin32` — required for DOCX→PDF conversion on Windows

Install optional packages with:

```bash
pip install openpyxl pywin32
```


## 📦 Project Structure

```text
pcform/
├── create_form/
│   └── form.py
│
├── exports/
│   ├── sections/
│   │   ├── base_section.py
│   │   ├── device_section.py
│   │   ├── parties_section.py
│   │   ├── problem_section.py
│   │   ├── signature_section.py
│   │   └── terms_section.py
│   │
│   ├── document_generator.py
│   ├── pdf_converter.py
│   └── styles.py
│
├── repositories/
│   ├── base_repo.py
│   ├── pcform_repo.py
│   └── user_repo.py
│
├── search_form/
│   ├── database_info.py
│   └── search.py
│
├── services/
│   ├── auth_service.py
│   └── database.py
│
├── settings/
│   ├── db/
│   │   └── pcform_db.db
│   │
│   ├── icons/
│   │   ├── banana.ico
│   │   └── banana.png
│   │
│   └── config.py
│
├── utils/
│   ├── mixins.py
│   ├── security.py
│   └── widget_utils.py
│
├── app.py
├── authentications.py
└── main.py
```

## Contributing

Bug reports, feature requests and pull requests are welcome. Please open issues or PRs on the project GitHub.

## License

This project is licensed under the Apache‑2.0 license. See `LICENSE` for details.
