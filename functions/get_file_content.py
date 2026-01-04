import os

from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Outputs content of a file up to the maximum length of {MAX_CHARS} characters. Any file output that exceeds {MAX_CHARS} characters will be suffixed with a notice that the file contents have been truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file from which to output content, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        if os.path.commonpath([abs_working_directory, target_file]) != abs_working_directory:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        with open(target_file, 'r') as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception as e:
        return f"Error: {e}"
