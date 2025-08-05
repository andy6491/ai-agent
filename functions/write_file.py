import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir_path = os.path.abspath(working_directory)
    full_intended_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_intended_path)
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path))
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be written to"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file"
            ),
        },
    ),
)