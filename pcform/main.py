from handler import add_user_input_to_docx
from handler import docx_to_pdf
from handler import destination_folder
import os


def main_menu():
    print(
        """
    1. Create a New Form
    2. Serach Forms

    """
    )


def create_form():
    print("Creating Form...\n")
    customer_fullname = input("Customer Fullname:")
    device_model = input("Dvice Model Name:")
    device_serial = input("Device Serial Number:")
    device_problems = input("Dvice Problems:")
    serviceman = input("Serviceman Fullname:")
    description = input("Descriptions:")
    data = {
        "Customer Fullname": customer_fullname,
        "Device Model": device_model,
        "Device Serial": device_serial,
        "Device Problems": device_problems,
        "ServiceMan": serviceman,
        "Description": description,
        "_":'_'
    }
    print("_"*60)
    # print('its Done. Lets See Your Form Details.\n')
    return data

def run():
    data_list = list()
    main_menu()
    user_input = int(input("Select And Enter a Number Of Menu:"))
    if user_input == 1:
        count = int(input("Enter Device Count: "))
        while count:
            data_list.append(create_form())
            count -= 1

    file_name = input("Enter The Name For -PDF- File: ")
    add_user_input_to_docx(file_name, data_list)
    input_docx_file = f"{file_name}.docx"
    input_docx_path = destination_folder
    input_docx_file = os.path.join(input_docx_path, input_docx_file)
    # ----------------------------------------------------------------
    output_pdf_file = f"{file_name}.pdf"
    output_pdf_path = destination_folder
    output_pdf_file = os.path.join(output_pdf_path, output_pdf_file)
    # ----------------------------------------------------------------
    docx_to_pdf(input_docx_file, output_pdf_file)


if __name__ == "__main__":
    run()
