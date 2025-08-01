import os

def get_files_info(working_directory, directory="."):
    abs_working_dir_path = os.path.abspath(working_directory)
    full_intended_path = os.path.join(working_directory, directory)
    abs_target_path = os.path.abspath(full_intended_path)
    if not abs_target_path.startswith(abs_working_dir_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target_path):
        return f'Error: "{directory}" is not a directory'
    contents = []
    try:
        for i in os.listdir(abs_target_path):
            t = os.path.join(abs_target_path, i)
            contents.append(f"- {i}: file_size={os.path.getsize(t)} bytes, is_dir={os.path.isdir(t)}")
        return "\n".join(contents)
    except Exception as e:
        return f"Error: an error was found in {e}"
    
