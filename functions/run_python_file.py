import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        if os.path.commonpath([abs_working_directory, target_file]) != abs_working_directory:
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise Exception(f'"{file_path}" does not exist or is not a regular file')
        if target_file[-3:] != ".py":
            raise Exception(f'"{file_path}" is not a Python file')
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        completed_process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)
        output = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout == "" and completed_process.stderr == "":
            output.append("No output produced")
        if completed_process.stdout != "":
            output.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr != "":
            output.append(f"STDERR: {completed_process.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"
