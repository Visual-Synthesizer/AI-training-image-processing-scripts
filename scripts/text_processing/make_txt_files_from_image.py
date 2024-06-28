"""
This script searches for all image files with '.png', '.jpg', and '.jpeg' extensions in a specified folder,
and creates a corresponding text file for each image file. The text file will contain a placeholder text
indicating it is associated with the image file.

Functionality:
1. Prompts the user to input the path to the folder containing the image files.
2. Retrieves all image files with the specified extensions in the specified folder.
3. For each image file, creates a text file with the same name (but with a .txt extension) containing a placeholder text.

Usage:
    Run the script and provide the folder path when prompted.

Example:
    python script.py
"""

import os

def create_text_files_for_images(folder_path):
    """
    Creates text files for each image file in the given folder path.

    Parameters:
    - folder_path (str): The path to the folder containing the image files.

    Returns:
    None
    """
    # Get all PNG and JPG files
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Create a text file for each image
    for image_file in image_files:
        text_file_name = os.path.splitext(image_file)[0] + '.txt'
        text_file_path = os.path.join(folder_path, text_file_name)

        # Create and write the text file
        with open(text_file_path, 'w') as file:
            file.write(f'This is a text file for {image_file}\n')

    print(f"Created {len(image_files)} text files for images in '{folder_path}'.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    create_text_files_for_images(folder_path)
