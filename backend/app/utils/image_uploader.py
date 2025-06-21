"""
utils/image_uploader.py — Uploads base64 image data to Cloudinary and returns the secure image URL.
"""

import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from app.logger_config import setup_logger

# Load environment variables
load_dotenv()
logger = setup_logger()

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image_base64(image_base64: str, folder: str = "visitors") -> str | None:
    """
    Uploads a base64-encoded image string to Cloudinary and returns the secure URL.

    Args:
        image_base64 (str): The base64-encoded image string.
        folder (str): Target Cloudinary folder (default: "visitors").

    Returns:
        str | None: Secure URL of the uploaded image or None if failed.
    """
    try:
        result = cloudinary.uploader.upload(
            image_base64,
            folder=folder,
            resource_type="image"
        )
        url = result.get("secure_url")
        if not url:
            logger.warning("⚠️ Image uploaded but no secure_url returned.")
        else:
            logger.info(f"🖼️ Image uploaded to Cloudinary — {url}")
        return url
    except Exception as e:
        logger.error(f"❌ Failed to upload image to Cloudinary: {e}", exc_info=True)
        return None
