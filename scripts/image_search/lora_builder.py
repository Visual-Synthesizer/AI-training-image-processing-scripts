"""
This script performs the following tasks:
1. Searches for images on DuckDuckGo based on specified keywords.
2. Downloads the images and saves them locally.
3. Crops the images into square thumbnails of a specified size.

Functionality:
- Prompts the user for search terms, safesearch level, image size, image type, maximum number of images, and destination path.
- Searches for images using DuckDuckGo's Search API.
- Downloads the images and saves them in the specified directory.
- Crops the downloaded images to a specified size.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

from duckduckgo_search import DDGS
import requests
import os
from PIL import Image
from pathlib import Path
from time import sleep
from typing import Optional

def search_images(
    keywords: str,
    safesearch: str = "moderate",
    size: Optional[str] = None,
    type_image: Optional[str] = None,
    max_results: int = 200
):
    """
    Perform image search using DuckDuckGo Search API.

    Parameters:
        keywords (str): Search keywords.
        safesearch (str): Safesearch level.
        size (Optional[str]): Size of the images.
        type_image (Optional[str]): Type of the images.
        max_results (int): Maximum number of images to return.

    Returns:
        list: List of image search results.
    """
    return list(
        DDGS().images(
            keywords,
            safesearch=safesearch,
            size=size,
            type_image=type_image
        )
    )[:max_results]

def save_image(dest, image_data):
    """
    Save image data to file.

    Parameters:
        dest (str): Destination path to save the image.
        image_data (bytes): Image data to save.
    """
    with open(dest, 'wb') as f:
        f.write(image_data)

def download_and_save_image(url, dest):
    """
    Download image from URL and save it to file.

    Parameters:
        url (str): URL of the image to download.
        dest (str): Destination path to save the image.
    """
    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if content_type == 'image/jpeg' or content_type == 'image/png':
            save_image(dest, response.content)
        else:
            print(f"Unsupported image format: {content_type}")
    else:
        print(f"Failed to download image: {response.status_code}")

def square_crop(image_path, dest, crop_size):
    """
    Perform square crop on image and resize it to the specified crop size.

    Parameters:
        image_path (str): Path to the image file.
        dest (str): Destination path to save the cropped image.
        crop_size (int): Size for square cropping in pixels.
    """
    img = Image.open(image_path)
    width, height = img.size
    if width != height:
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = (width + min_dim) // 2
        bottom = (height + min_dim) // 2
        img = img.crop((left, top, right, bottom))
    img.thumbnail((crop_size, crop_size))
    img.save(dest)

def run_image_downloader():
    """
    Main function to run the image downloader program.
    Prompts user for inputs and performs image search, download, and cropping.
    """
    # Get user inputs
    search_terms = input("Enter search terms (separated by comma): ").split(",")
    safesearch = input("Enter safesearch level (on, moderate, off): ")
    size = input("Enter image size (Small, Medium, Large, Wallpaper): ")
    type_image = input("Enter image type (photo, clipart, gif, transparent, line): ")
    max_images = int(input("Enter the maximum number of images to download per search term: "))

    dest_path = input("Enter the destination path (leave blank for current working directory): ").strip()
    if dest_path:
        path = Path(dest_path)
    else:
        path = Path.cwd()

    images_folder = path / "images"
    images_folder.mkdir(exist_ok=True)

    crop_size = int(input("Enter the size for square cropping (in pixels): "))

    for search_term in search_terms:
        search_folder = images_folder / search_term.strip()
        search_folder.mkdir(exist_ok=True)

        # Search and download images
        photo_urls = search_images(
            f'{search_term} photo',
            safesearch=safesearch,
            size=size,
            type_image=type_image,
            max_results=max_images
        )

        for i, image in enumerate(photo_urls):
            url = image['image']
            download_and_save_image(url, search_folder / f'photo_{i}.jpg')
            sleep(1)  # Pause between downloads

        # Crop images
        for image_path in search_folder.glob('*.jpg'):
            square_crop(image_path, image_path, crop_size)

    print("Image download and cropping completed.")

# Run the image downloader program
run_image_downloader()
