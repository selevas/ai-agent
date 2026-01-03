import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))
    if os.path.commonpath([abs_working_directory, target_dir]) != abs_working_directory:
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir):
        raise Exception(f'Error: "{directory}" is not a directory (absolute directory {target_dir})')
    try:
        with os.scandir(target_dir) as entries:
            contents = []
            for entry in entries:
                contents.append(f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}")
            return "\n".join(contents)
    except Exception as e:
        print(f"Target dir: {target_dir}")
        raise Exception(f"Error: {e}")

