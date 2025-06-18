import qrcode
import io
from cloudinary.uploader import upload

def generate_qr_and_upload(data: str, filename: str = "visitor_badge") -> str:
    qr = qrcode.make(data)

    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    buffered.seek(0)

    result = upload(buffered, folder="visitor_badges", public_id=filename)
    return result["secure_url"]