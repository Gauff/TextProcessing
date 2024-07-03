import os
import subprocess
import tempfile
from pathlib import Path


def create_text_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(text)


def write_string_array_to_text_file(input_string_array, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for string in input_string_array:
            file.writelines(string)


def generate_file_path_with_other_extension(input_epub_file_path, extension='.txt'):
    base_name, ext = os.path.splitext(input_epub_file_path)
    file_path = base_name + extension
    return file_path


def file_exists(file_path):
    """
    Check if a file exists given its path.

    Args:
    - file_path (str): The path to the file to check.

    Returns:
    - bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def check_file_path(file_path: str) -> tuple:
    """
    Check if a given text is a valid file path and if the file exists.

    Args:
    file_path (str): The path to the file.

    Returns:
    tuple: (is_valid_path, file_exists)
        is_valid_path (bool): True if the path is valid, False otherwise.
        file_exists (bool): True if the file exists, False otherwise.
    """
    try:
        # Check if the path is valid
        path = Path(file_path)
        is_valid_path = path.is_file() or path.is_dir() or not path.exists()

        # Check if the file exists
        file_exists = path.is_file()

        return is_valid_path, file_exists
    except Exception as e:
        # If any exception occurs, the path is not valid
        return False, False

def create_temp_text_file(content):
    temp_dir = tempfile.mkdtemp()

    file_path = os.path.normpath(os.path.join(temp_dir, "temp_file.txt"))

    with open(file_path, "w", encoding='utf-8') as file:
        file.write(content)

    return file_path


def delete_temp_file(file_path):
    try:
        os.remove(file_path)
        print(f"Temporary file '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting temporary file '{file_path}': {e}")


def extract_file_name(file_path):
    # Use os.path.basename() to extract the file name
    file_name = os.path.basename(file_path)

    # Split the file name by the dot to remove the extension
    file_name_without_extension = file_name.split('.')[0]

    return file_name_without_extension


def open_directory_in_explorer(directory_path):
    # Check if the directory path exists
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    # Use subprocess to open the directory in the default file explorer
    try:
        subprocess.Popen(f'explorer "{directory_path}"')
    except Exception as e:
        print(f"Error: {e}")


def delete_files_in_directory(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def is_audio_file(file_path_or_text):
    """
    Check if the given input is a path to an audio file that Whisper accepts or just a string containing text.
    
    Parameters:
    - file_path_or_text (str): Path to the file or text string to be checked.
    
    Returns:
    - bool: True if the input is a supported audio file, False if it is plain text.
    """
    if os.path.isfile(file_path_or_text):
        # List of supported audio file extensions
        supported_extensions = {'.wav', '.mp3', '.m4a', '.ogg', '.flac', '.webm'}
        
        # Get the file extension
        file_extension = os.path.splitext(file_path_or_text)[1].lower()
        
        # Check if the file extension is in the list of supported extensions
        return file_extension in supported_extensions
    else:
        # The input is not a file path but a text string
        return False