from pathlib import Path
import sys

from PIL import Image
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def test_image() -> Image.Image:
    """
    Create a small in-memory RGB image for tests.
    """
    return Image.new("RGB", (2, 2), color=(255, 255, 255))
