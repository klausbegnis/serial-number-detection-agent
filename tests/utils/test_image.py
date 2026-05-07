import base64
import io

from PIL import Image

from app.utils.image import image_to_data_url


def test_image_to_data_url_encodes_png(test_image: Image.Image) -> None:
    """
    Encode a PNG data URL that can be decoded back to PNG bytes.
    """
    data_url = image_to_data_url(test_image)

    assert data_url.startswith("data:image/png;base64,")
    encoded = data_url.split(",", 1)[1]
    raw = base64.b64decode(encoded)
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"

    decoded = Image.open(io.BytesIO(raw))
    assert decoded.size == test_image.size
