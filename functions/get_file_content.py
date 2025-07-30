import os
from google.genai import types
from config import CHAR_LIMIT


def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))   
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outsidethe permitted working directory'        
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: {file_path}"'
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read(CHAR_LIMIT)            
            if os.path.getsize(abs_file_path) > CHAR_LIMIT:
                content += (
                    f'[... File "{file_path}" truncated to {CHAR_LIMIT} characters]'
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
      
      
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
      