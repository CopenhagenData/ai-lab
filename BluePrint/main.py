# The above command writes the programme to a file called main.py

# Import namespaces
from dotenv import load_dotenv
import os
import openai
from glob import glob

# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('AZURE_COG_KEY')
cog_region = os.getenv('AZURE_COG_REGION')
openai_key = os.getenv('OPENAI_API_KEY')

# Configure OpenAI
openai.api_key = openai_key

# Input folder to analyse
input_folder_path = input("Enter the path to the folder to analyse: ")
if input_folder_path == "":
    input_folder_path = "./"

# Save path
save_file_path = './documentation/'

# Get the list of files in the folder
def get_files_list(input_folder_path):
    return glob(input_folder_path + "/**/*.py", recursive=True)

# Get the content of a file
def get_file_content(file_path):
    with open(file_path, "r") as f:
        return f.read()

# Get the documentation for a file using OpenAI
def generate_file_documentation(file, style='description'):
    file_content = get_file_content(file)
    command = ''

    if style == 'table':
        command = f"""For the following code: \n {file_content} \n
                    Provide a table in markdown of each function in the code 
                    with four columns: the function name, input, 
                    output, and a description.\n"""
    else:
        command = f"Provide a short description of this code:\n {file_content} \n"
    
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= command,
        temperature=0.5,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response['choices'][0]['text']

# Get the documentation for each file
def create_file_documentation(files_list):
    files_docuemntation = ""
    for file in files_list:
        print("Analysing file: " + file)

        title = "# Documentation for " + file + "\n"
        subtitle1 = "\n## Description\n"
        body1 = generate_file_documentation(file, style='description')

        subtitle2 = "\n## Table\n"
        body2 = generate_file_documentation(file, style='table')
                
        files_docuemntation += title + subtitle1 + body1 + "\n" + subtitle2 + body2 + "\n\n"
    
    return files_docuemntation

# Write the documentation to a file
def save_file_documentation(files_docuemntation):
    with open(save_file_path + "documentation.md", "w", encoding="utf-8") as fs:
        fs.write(files_docuemntation)

# Main function
def main():
    files_list = get_files_list(input_folder_path)
    files_docuemntation = create_file_documentation(files_list)
    save_file_documentation(files_docuemntation)

# Run the main function
if __name__ == "__main__":
    main()
