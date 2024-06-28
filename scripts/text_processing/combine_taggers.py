"""
This script processes text files in a specified folder by grouping them based on common prefixes, 
merging the content of grouped files into a single file, and then deleting the original files.

Functionality:
1. Prompts the user to input the path to the folder containing the text files.
2. Retrieves all text files in the specified folder and its subfolders.
3. Groups the files by common prefixes.
4. Merges the content of files in each group into a single text file, separated by two newlines.
5. Deletes the original files after merging.

Usage:
    Run the script and provide the path to the folder when prompted.

Example:
    python script.py
"""

import os
import glob
import concurrent.futures

def process_files(filenames):
    """
    Merge content of files in filenames list into a single file and delete original files.

    Parameters:
        filenames (list): List of file paths to be processed.
    """
    common_name = os.path.commonprefix(filenames)
    with open(common_name + '.txt', 'w') as outfile:
        for i, fname in enumerate(filenames):
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
                if i != len(filenames) - 1:  # If it's not the last file, add two newlines
                    outfile.write('\n\n')
            os.remove(fname)  # Remove the original file

def main(folder_path):
    """
    Main function to process all text files in the specified folder.

    Parameters:
        folder_path (str): Path to the folder containing text files.
    """
    # Get all the txt files in the folder and its subfolders
    txt_files = glob.glob(f"{folder_path}/**/*.txt", recursive=True)

    # Group files by common prefix
    groups = {}
    for txt_file in txt_files:
        prefix = txt_file.rsplit("GIT", 1)[0].rsplit("blip", 1)[0].rsplit("WD", 1)[0]
        groups.setdefault(prefix, []).append(txt_file)

    # Process each group of files concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_files, groups.values())

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    main(folder_path)
