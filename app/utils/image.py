import base64
import io

from PIL import Image


def image_to_data_url(image: Image.Image) -> str:
    """
    Convert a PIL image to a PNG data URL.
    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
