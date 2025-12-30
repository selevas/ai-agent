import os

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

