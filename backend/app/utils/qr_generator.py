"""
utils/qr_generator.py — Generates a QR code, uploads it to Cloudinary, and returns the hosted badge URL.
"""

import qrcode
import io
from cloudinary.uploader import upload
from app.logger_config import setup_logger

logger = setup_logger()

def generate_qr_and_upload(data: str, filename: str = "visitor_badge") -> str | None:
    """
    Generates a QR code from the given data, uploads it to Cloudinary,
    and returns the secure URL.

    Args:
        data (str): The content to encode in the QR code.
        filename (str): The public ID to use when uploading (default: "visitor_badge").

    Returns:
        str | None: Secure Cloudinary URL of the uploaded QR image or None if failed.
    """
    try:
        qr = qrcode.make(data)
        buffered = io.BytesIO()
        qr.save(buffered, format="PNG")
        buffered.seek(0)

        result = upload(
            buffered,
            folder="visitor_badges",
            public_id=filename,
            resource_type="image",
            overwrite=True
        )

        url = result.get("secure_url")
        if url:
            logger.info(f"✅ QR badge uploaded successfully — {url}")
        else:
            logger.warning("⚠️ QR uploaded but no secure_url returned.")

        return url

    except Exception as e:
        logger.error(f"❌ Failed to generate/upload QR code: {e}", exc_info=True)
        return None
