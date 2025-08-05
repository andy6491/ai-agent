import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir_path = os.path.abspath(working_directory)
    full_intented_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_intented_path)
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            max_check = f.read(1)
            if max_check != "":
                file_content_string = f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: error was found in "{e}" file'
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read"
            ),
        },
    ),
)