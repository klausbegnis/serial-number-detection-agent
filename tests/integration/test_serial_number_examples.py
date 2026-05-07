import json
from pathlib import Path

from PIL import Image
import pytest

from app.services.serial_number_detector import SerialNumberDetector

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
EXAMPLES_PATH = PROJECT_ROOT / "tests" / "data" / "examples.json"


def _load_examples() -> list[dict[str, str]]:
    """
    Load labeled serial number examples from JSON.
    """
    with EXAMPLES_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.mark.ci
@pytest.mark.parametrize("example", _load_examples())
def test_detects_serial_numbers_from_examples(example: dict[str, str]) -> None:
    """
    Validate serial number detection against labeled examples.
    """
    image_path = DATA_DIR / example["filename"]
    expected = example["serial_number"]

    detector = SerialNumberDetector()
    image = Image.open(image_path)
    result = detector.detect(image)

    assert result.serial_number == expected
