from handler import add_user_input_to_docx
from handler import docx_to_pdf
import os


def main_menu():
    print(
        """
    1. Create a New Form
    2. Serach Forms

    """
    )


def create_form():
    data_list = list()
    print("Creating Form...\n")
    customer_fullname = input("Customer Fullname:")
    device_model = input("Dvice Model Name:")
    device_serial = input("Device Serial Number:")
    device_problems = input("Dvice Problems:")
    serviceman = input("Serviceman Fullname:")
    description = input("Descriptions:")
    data_list += [customer_fullname, device_model, device_serial,
                  device_problems, serviceman, description]
    print("_"*60)
    # print('its Done. Lets See Your Form Details.\n')
    return data_list


if __name__ == "__main__":
    main_menu()
    user_input = int(input("Select And Enter a Number Of Menu:"))
    if user_input == 1:
        data_list = create_form()

    file_name = input(
        "Enter the filename for the file: ")
    add_user_input_to_docx(file_name, data_list)
    input_docx_file = f"{file_name}.docx"
    output_pdf_file = f"{file_name}.pdf"
    output_pdf_path = 'A:/MyProject/py'
    output_pdf_file = os.path.join(output_pdf_path, output_pdf_file)
    docx_to_pdf(input_docx_file, output_pdf_file)
