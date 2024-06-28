"""
This script recursively searches through a specified directory for .txt files to check for specific error messages. 
If any of the predefined error messages are found within a .txt file, the script moves both the .txt file and its 
corresponding .jpg file (assumed to have the same name, differing only in file extension) to a 'redo_error' directory. 
This 'redo_error' directory is created within the starting directory if it does not already exist. The script provides 
updates on its progress, including the number of files processed, the number of files moved due to errors, and a list of 
files that were checked but did not contain any of the specified errors. This is useful for managing and correcting files 
that failed automated processing due to these specific errors.
"""

import os
import shutil

def check_and_move_files(start_path):
    """
    Check .txt files for specific error messages and move them, along with their corresponding .jpg files, to a 'redo_error' directory if errors are found.

    Parameters:
    - start_path (str): The directory path to start searching for .txt files.

    Returns:
    None
    """
    # Define the error messages to search for
    error_messages = [
        "Error Connecting: HTTPSConnectionPool",
        "OOps: Something Else: HTTPSConnectionPool",
        "I'm sorry, I can't provide assistance with that request.",
        "HTTP Error: 400 Client Error: Bad Request for url: https://api.openai.com/v1/chat/completions"
    ]
    
    # Setup 'redo_error' directory within 'start_path'
    redo_error_path = os.path.join(start_path, 'redo_error')
    if not os.path.exists(redo_error_path):
        os.makedirs(redo_error_path)
    
    # Counters for files processed and moved
    files_processed = 0
    files_moved = 0
    files_with_no_error = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".txt"):
                files_processed += 1
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    contents = f.read()
                    if any(error_message in contents for error_message in error_messages):
                        jpg_file_path = os.path.splitext(file_path)[0] + '.jpg'
                        new_txt_path = os.path.join(redo_error_path, os.path.basename(file_path))
                        new_jpg_path = os.path.join(redo_error_path, os.path.basename(jpg_file_path))
                        
                        # Move the .txt file
                        shutil.move(file_path, new_txt_path)
                        
                        # Move the corresponding .jpg file if it exists
                        if os.path.exists(jpg_file_path):
                            shutil.move(jpg_file_path, new_jpg_path)
                        files_moved += 1
                        print(f"Error found and moved: {file} and corresponding .jpg")
                    else:
                        files_with_no_error.append(file)

    # Summary of actions
    print(f"Total files processed: {files_processed}")
    print(f"Total files moved due to errors: {files_moved}")
    if files_with_no_error:
        print("Files with no specified errors:")
        for file in files_with_no_error:
            print(f"- {file}")
    else:
        print("No files without specified errors.")

# Replace 'your_start_directory_path_here' with the path to the directory where you want to start processing
check_and_move_files('/PATH/fix')
