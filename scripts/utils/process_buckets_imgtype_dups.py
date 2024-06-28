"""
This script resizes and crops images based on generated bucket resolutions, converts them to sRGB color space if necessary,
saves them in a specified format, and finds duplicate images based on their MD5 hash.

Functionality:
1. Generates bucket resolutions based on specified constraints.
2. Converts images to sRGB color space if they contain an ICC profile.
3. Resizes and crops images to fit into the closest bucket resolution.
4. Saves the processed images in the specified output format.
5. Uses concurrent processing to speed up image processing.
6. Finds and logs duplicate images based on their MD5 hash.

Usage:
    Run the script with the necessary command-line arguments to specify input and output directories,
    bucket resolution constraints, and output format.

Example:
    python script.py --input_dir ./input --output_dir ./output --output_format png
"""

import argparse
import math
import logging
import os
import io
import concurrent.futures
from pathlib import Path
from PIL import Image, ImageCms
from hashlib import md5

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def make_bucket_resolutions(max_sqrt_area=1024, min_size=512, max_size=2048, divisible_by=64):
    """
    Generate bucket resolutions based on specified constraints.
    """
    resolutions = set()
    max_sqrt_area //= divisible_by
    max_area = max_sqrt_area ** 2
    size = max_sqrt_area * divisible_by
    resolutions.add((1.0, size, size))

    size = min_size
    while size <= max_size:
        width = size
        height = min(max_size, (max_area // (width // divisible_by)) * divisible_by)
        resolutions.add((width / height, width, height))
        resolutions.add((height / width, height, width))
        size += divisible_by

    resolutions = list(resolutions)
    resolutions.sort()
    return resolutions

def load_profile(profile_name):
    """
    Attempt to load an ICC profile by name.
    """
    try:
        return ImageCms.createProfile(profile_name)
    except IOError:
        logging.error(f"Failed to load the {profile_name} profile.")
        return None

def convert_to_srgb(image):
    """
    Convert the given image to sRGB color space if necessary.
    """
    if 'icc_profile' in image.info:
        try:
            input_profile = ImageCms.ImageCmsProfile(io.BytesIO(image.info['icc_profile']))
            srgb_profile = load_profile("sRGB")
            if srgb_profile:
                return ImageCms.profileToProfile(image, input_profile, srgb_profile, outputMode='RGB')
        except ImageCms.PyCMSError as e:
            logging.error("Failed to build transform, using fallback method: " + str(e))
            # Fallback method: Convert to a basic RGB profile first
            image = image.convert('RGB')
            return image
    return image

def resize_and_crop_image(image_path, output_dir, bucket_resolutions, output_format):
    """
    Resize and crop a single image based on the resolution buckets, convert it to sRGB, and save it in the specified format.
    """
    try:
        with Image.open(image_path) as image:
            # Convert to RGB if not already (necessary for profile conversion)
            if image.mode not in ['RGB', 'RGBA']:
                image = image.convert('RGB')

            # Convert to sRGB
            image = convert_to_srgb(image)

            width, height = image.size
            aspect_ratio = width / height
            closest_aspect_ratio = None
            target_width = None
            target_height = None
            closest_aspect_ratio_diff = float("inf")

            for bucket_aspect_ratio, bucket_width, bucket_height in bucket_resolutions:
                if width >= bucket_width and height >= bucket_height:
                    aspect_ratio_diff = abs(bucket_aspect_ratio - aspect_ratio)
                    if aspect_ratio_diff < closest_aspect_ratio_diff:
                        closest_aspect_ratio_diff = aspect_ratio_diff
                        closest_aspect_ratio = bucket_aspect_ratio
                        target_width = bucket_width
                        target_height = bucket_height

            if closest_aspect_ratio is not None:
                new_width, new_height = adjust_image_size(image, closest_aspect_ratio, target_width, target_height, width, height)
                image = image.resize((new_width, new_height), Image.LANCZOS)
                image = crop_image(image, new_width, new_height, target_width, target_height)
                output_path = output_dir / f"{image_path.stem}.{output_format.lower()}"
                image.save(output_path, format=output_format.upper() if output_format.lower() != 'jpg' else 'JPEG')
                return output_path, None
            else:
                return None, f"No suitable bucket for {image_path.name}"
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")
        return None, str(e)

def adjust_image_size(image, aspect_ratio, target_width, target_height, width, height):
    """
    Adjust the size of the image to maintain the aspect ratio closest to the target.
    """
    if aspect_ratio > width / height:
        new_width = target_width
        new_height = math.ceil(height * new_width / width)
    else:
        new_height = target_height
        new_width = math.ceil(width * new_height / height)
    return new_width, new_height

def crop_image(image, new_width, new_height, target_width, target_height):
    """
    Crop the image to fit into the target dimensions.
    """
    if new_height > target_height:
        top = (new_height - target_height) // 2
        bottom = top + target_height
        image = image.crop((0, top, new_width, bottom))
    elif new_width > target_width:
        left = (new_width - target_width) // 2
        right = left + target_width
        image = image.crop((left, 0, right, new_height))
    return image

def find_duplicates(image_directory):
    """
    Find duplicate images based on MD5 hash.
    """
    hashes = {}
    duplicates = []
    for image_path in Path(image_directory).rglob('*.*'):
        with open(image_path, 'rb') as file:
            hash_md5 = md5(file.read()).hexdigest()
            if hash_md5 in hashes:
                duplicates.append((image_path, hashes[hash_md5]))
            else:
                hashes[hash_md5] = image_path
    return duplicates

def process_images(input_dir, output_dir, bucket_resolutions, output_format):
    """
    Process all images using concurrent processing.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = [p for ext in ["*.png", "*.jpg", "*.jpeg"] for p in input_dir.glob(ext)]
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(resize_and_crop_image, path, output_dir, bucket_resolutions, output_format) for path in image_paths]
        for future in concurrent.futures.as_completed(futures):
            result, error = future.result()
            if error:
                logging.error(error)
            else:
                results.append(result)
    return results

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Resize and crop images based on generated bucket resolutions.")
    parser.add_argument("--max_sqrt_area", type=int, default=1024, help="Maximum square root value of each resolution area.")
    parser.add_argument("--min_size", type=int, default=512, help="Minimum size for the bucket resolutions.")
    parser.add_argument("--max_size", type=int, default=2048, help="Maximum size for the bucket resolutions.")
    parser.add_argument("--divisible_by", type=int, default=64, help="Factor by which the bucket widths and heights should be divisible.")
    parser.add_argument("--input_dir", type=str, help="Directory containing input images.")
    parser.add_argument("--output_dir", type=str, help="Directory where output images will be saved.")
    parser.add_argument("--output_format", type=str, default='jpg', help="Output image format.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    bucket_resolutions = make_bucket_resolutions(args.max_sqrt_area, args.min_size, args.max_size, args.divisible_by)
    processed_images = process_images(args.input_dir, args.output_dir, bucket_resolutions, args.output_format)
    duplicates = find_duplicates(args.output_dir)
    logging.info(f"Processed images: {len(processed_images)}")
    logging.info(f"Duplicate images found: {len(duplicates)}")
