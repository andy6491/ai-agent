import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir_path = os.path.abspath(working_directory)
    full_intended_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_intended_path)
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python", abs_file_path] + args, timeout=30, capture_output=True, text=True)
        output_lines = []
        if completed_process.stdout:
            output_lines.append("STDOUT: " + completed_process.stdout)
        if completed_process.stderr:
            output_lines.append("STDERR: " + completed_process.stderr)
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")
        if not output_lines:
            return "No output produced."
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"