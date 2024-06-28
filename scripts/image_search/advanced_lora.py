"""
This script performs the following tasks:
1. Searches for images on DuckDuckGo based on specified keywords.
2. Downloads the images and saves them locally.
3. Crops the images into square thumbnails of a specified size.
4. Utilizes multi-threading to download and process images concurrently.

Usage:
    Run the script with the necessary command-line arguments to specify search terms,
    safesearch level, image size, image type, maximum number of images to download,
    destination path, and crop size.

Example:
    python script.py "cat,dog,bird" --safesearch moderate --size Large --type_image photo --max_images 100 --dest_path ./images --crop_size 512
"""

import requests
import os
from PIL import Image
from pathlib import Path
from time import sleep
from typing import Optional
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        from duckduckgo_search import DDGS
        return list(
            DDGS().images(
                keywords,
                safesearch=safesearch,
                size=size,
                type_image=type_image
            )
        )[:max_results]
    except ImportError:
        logger.error("Failed to import the duckduckgo_search library.")
        raise

def save_image(dest, image_data):
    """
    Save image data to file.

    Parameters:
        dest (str): Destination path to save the image.
        image_data (bytes): Image data to save.
    """
    try:
        with open(dest, 'wb') as f:
            f.write(image_data)
    except IOError as e:
        logger.error(f"Failed to save image: {e}")
        raise

def download_and_save_image(url, dest):
    """
    Download image from URL and save it to file.

    Parameters:
        url (str): URL of the image to download.
        dest (str): Destination path to save the image.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if content_type == 'image/jpeg' or content_type == 'image/png':
                save_image(dest, response.content)
                logger.info(f"Downloaded image: {dest}")
            else:
                logger.warning(f"Unsupported image format: {content_type}")
        else:
            logger.warning(f"Failed to download image: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to download image: {e}")

def square_crop(image_path, dest, crop_size):
    """
    Perform square crop on image and resize it to the specified crop size.

    Parameters:
        image_path (str): Path to the image file.
        dest (str): Destination path to save the cropped image.
        crop_size (int): Size for square cropping in pixels.
    """
    try:
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
        logger.info(f"Cropped image: {dest}")
    except IOError as e:
        logger.error(f"Failed to crop image: {e}")
        raise

def download_and_crop_image(url, dest, crop_size):
    """
    Download image from URL, save it to file, and perform cropping.

    Parameters:
        url (str): URL of the image to download.
        dest (str): Destination path to save the image.
        crop_size (int): Size for square cropping in pixels.
    """
    download_and_save_image(url, dest)
    square_crop(dest, dest, crop_size)

def run_image_downloader():
    """
    Main function to run the image downloader program.
    Configures command-line argument parser and initiates image search, download, and cropping.
    """
    # Configure command-line argument parser
    parser = argparse.ArgumentParser(description='Image Downloader')
    parser.add_argument('search_terms', help='Search terms (separated by comma)')
    parser.add_argument('--safesearch', default='moderate', help='Safesearch level (on, moderate, off)')
    parser.add_argument('--size', help='Image size (Small, Medium, Large, Wallpaper)')
    parser.add_argument('--type_image', help='Image type (photo, clipart, gif, transparent, line)')
    parser.add_argument('--max_images', type=int, default=200, help='Maximum number of images to download per search term')
    parser.add_argument('--dest_path', default='', help='Destination path')
    parser.add_argument('--crop_size', type=int, default=1024, help='Size for square cropping (in pixels)')
    args = parser.parse_args()

    # Set destination path
    dest_path = args.dest_path.strip()
    if dest_path:
        path = Path(dest_path)
    else:
        path = Path.cwd()

    images_folder = path / "images"
    images_folder.mkdir(exist_ok=True)

    # Set up thread pool executor for parallel image downloads
    max_workers = min(args.max_images, os.cpu_count() or 1)
    executor = ThreadPoolExecutor(max_workers=max_workers)

    # Split search terms
    search_terms = args.search_terms.split(',')

    for search_term in search_terms:
        search_folder = images_folder / search_term.strip()
        search_folder.mkdir(exist_ok=True)

        # Search and download images
        photo_urls = search_images(
            f'{search_term} photo',
            safesearch=args.safesearch,
            size=args.size,
            type_image=args.type_image,
            max_results=args.max_images
        )

        # Download and crop images using thread pool executor
        download_tasks = []
        for i, image in enumerate(photo_urls):
            url = image['image']
            dest
