import os
from docx import Document

def convert_txt_to_docx(txt_file, output_dir):
    # Open the text file and read its content
    with open(txt_file, 'r', encoding='utf-8') as txt:
        content = txt.read()

    # Create a new Document
    doc = Document()
    # Add the content of the text file to the Document
    doc.add_paragraph(content)

    # Get the file name (without extension) from the txt file
    filename = os.path.splitext(os.path.basename(txt_file))[0]

    # Save the Document as a .docx file
    docx_file = os.path.join(output_dir, f"{filename}.docx")
    doc.save(docx_file)
    #print(f"Converted {txt_file} to {docx_file}")

def convert_all_txt_to_docx(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through each file in the input directory
    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            txt_file = os.path.join(input_dir, file)
            convert_txt_to_docx(txt_file, output_dir)

# Replace these paths with your input and output directories
input_directory = "data\jobs_txt"
output_directory = "data\jobs_docs"

convert_all_txt_to_docx(input_directory, output_directory)
