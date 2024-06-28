"""
This script resizes and fits images to predefined target resolutions, then saves them in a specified directory.
It also checks for duplicate images using MD5 hash comparison and logs the processing details.

Functionality:
1. Defines a set of target resolutions.
2. Finds the closest target resolution for each image based on its aspect ratio.
3. Resizes and crops the image to fit the target resolution.
4. Saves the processed images with a specified JPEG quality.
5. Detects and logs duplicate images based on MD5 hash comparison.

Usage:
    Adjust the command-line arguments to specify the input directory, output directory, and JPEG quality.

Example:
    python script.py --input_dir /path/to/input --output_dir /path/to/output --jpeg_quality 90
"""

import argparse
import math
import logging
import os
import concurrent.futures
from pathlib import Path
from PIL import Image
from hashlib import md5

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_target_resolutions():
    """
    Return a list of target resolutions (width, height) tuples.
    """
    return [
        (640, 1632), (704, 1472), (768, 1360), (832, 1248), (896, 1152),
        (960, 1088), (992, 1056), (1024, 1024), (1056, 992), (1088, 960),
        (1152, 896), (1248, 832), (1360, 768), (1472, 704), (1632, 640)
    ]

def find_closest_resolution(width, height, resolutions):
    """
    Find the closest resolution based on aspect ratio.

    Parameters:
        width (int): Width of the original image.
        height (int): Height of the original image.
        resolutions (list): List of target resolutions.

    Returns:
        tuple: The closest resolution (width, height).
    """
    min_diff = float('inf')
    selected_res = None
    aspect_ratio = width / height
    for res in resolutions:
        res_aspect_ratio = res[0] / res[1]
        aspect_diff = abs(aspect_ratio - res_aspect_ratio)
        if aspect_diff < min_diff:
            min_diff = aspect_diff
            selected_res = res
    return selected_res

def resize_and_fit_to_bucket(image, target_resolution):
    """
    Resize and fit the image to the target resolution.

    Parameters:
        image (PIL.Image.Image): The original image.
        target_resolution (tuple): The target resolution (width, height).

    Returns:
        PIL.Image.Image: The resized and cropped image.
    """
    target_width, target_height = target_resolution
    image_ratio = image.width / image.height
    target_ratio = target_width / target_height
    if image_ratio > target_ratio:
        scale_height = int(image.height * target_width / image.width)
        resized_image = image.resize((target_width, scale_height), Image.LANCZOS)
    else:
        scale_width = int(image.width * target_height / image.height)
        resized_image = image.resize((scale_width, target_height), Image.LANCZOS)
    return resized_image.crop((0, 0, target_width, target_height))

def calculate_md5(image_path):
    """
    Calculate the MD5 hash of an image file.

    Parameters:
        image_path (str): Path to the image file.

    Returns:
        str: The MD5 hash of the image.
    """
    hash_md5 = md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def process_image(image_path, output_dir, resolutions, jpeg_quality):
    """
    Process an image: resize, crop, and save it.

    Parameters:
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the processed image.
        resolutions (list): List of target resolutions.
        jpeg_quality (int): JPEG quality for saving the image.

    Returns:
        Path: Path to the processed image or None if processing failed.
    """
    try:
        with Image.open(image_path) as image:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            closest_res = find_closest_resolution(image.width, image.height, resolutions)
            processed_image = resize_and_fit_to_bucket(image, closest_res)
            output_path = output_dir / f"{image_path.stem}_{closest_res[0]}x{closest_res[1]}.jpg"
            processed_image.save(output_path, 'JPEG', quality=jpeg_quality)
            return output_path
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")
        return None

def main(input_dir, output_dir, jpeg_quality):
    """
    Main function to process all images in the input directory.

    Parameters:
        input_dir (str): Directory containing input images.
        output_dir (str): Directory where output images will be saved.
        jpeg_quality (int): JPEG quality for saving images.
    """
    resolutions = get_target_resolutions()
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    checksums = {}
    duplicates = []
    image_paths = list(input_dir.glob('*.*'))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_image, path, output_dir, resolutions, jpeg_quality): path for path in image_paths}
        for future in concurrent.futures.as_completed(futures):
            image_path = futures[future]
            result_path = future.result()
            if result_path:
                md5_hash = calculate_md5(result_path)
                if md5_hash in checksums:
                    duplicates.append((result_path, checksums[md5_hash]))
                    logging.info(f"Duplicate found: {result_path} is a duplicate of {checksums[md5_hash]}")
                else:
                    checksums[md5_hash] = result_path

    logging.info(f"Processed images: {len(image_paths) - len(duplicates)}")
    logging.info(f"Duplicate images found: {len(duplicates)}")
    return image_paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and fit images to predefined resolutions.")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing input images.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory where output images will be saved.")
    parser.add_argument("--jpeg_quality", type=int, default=100, help="JPEG quality for saving images.")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir, args.jpeg_quality)
