import os
from docx import Document
import inputs_checking as inp
import courses as nc

def search_in_word_files(directory, search_text):
    """
    Search for the given text in all Word files within the specified directory.

    Args:
        directory (str): Path to the directory containing Word files.
        search_text (str): The text to search for.

    Returns:
        list: List of filenames that contain the search text.
    """
    matching_files = []

    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.docx'):
            filepath = os.path.join(directory, filename)
            doc = Document(filepath)
            
            # Search for the text in each table cell of the document
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if search_text.lower() in cell.text.lower():
                            matching_files.append(filename)
                            break
                    if filename in matching_files:
                        break
                if filename in matching_files:
                    break

    return matching_files
# Example usage
directory_path = ''  # Replace with the path to your Word files directory
k = []
def empty():
    global k
    k = []
def sent():
    global k
    return {'recommendations': k, "scores": [1 for i in range(len(k))]}
def get(cd):
    global directory_path
    directory_path = cd
def matching_files(directory_path,search_text):
    matching_files = search_in_word_files(directory_path, search_text)
    global k
    k = matching_files
    # if matching_files:
    #     print("Files containing the text '{}':".format(search_text))
    #     for file in matching_files:
    #         # print(file)
    #         continue
    # else:
    #     print("No files contain the text '{}'".format(search_text))
# search_text = inp.main()co
       
def taking_input(user_input):
    search_text1, search_text2, ch,ck = inp.main(user_input)


    if search_text2 == " ":
        # if the input is inverted commas
        if ch == 1:
            k = []
            k.append(search_text1)
            search_text1 = k
            str1 = " "
            search_text1 = str1.join(search_text1)
            matching_files(directory_path,search_text1)
                
        # if the input is not in inverted commas
        if ch == 0:
            nc.take_prompt(search_text1)
            
    if search_text2 != " ":
        if ch == 1:
            k = []
            k.append(search_text1)
            search_text1 = k
            str1 = " "
            search_text1 = str1.join(search_text1)
            matching_files(directory_path,search_text1)
        
        if ch == 0:
            nc.take_prompt(search_text1) 
        if ck == 1:
            k = []
            k.append(search_text2)
            search_text2 = k
            str1 = " "
            search_text2 = str1.join(search_text2)
            matching_files(directory_path,search_text2)   
        
        if ck == 0:
            nc.take_prompt(search_text2)
        
            
            
