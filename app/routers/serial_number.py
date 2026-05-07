import io
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image

from app.schemas.serial_number import (
    SerialNumberPathRequest,
    SerialNumberResult,
)
from app.services.serial_number_detector import (
    SerialNumberDetector,
    get_serial_number_detector,
)

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
UPLOAD_FILE = File(...)
DETECTOR_DEP = Depends(get_serial_number_detector)


def _resolve_image_path(filename: str) -> Path:
    candidate = (DATA_DIR / filename).resolve()
    if DATA_DIR not in candidate.parents and candidate != DATA_DIR:
        raise HTTPException(status_code=400, detail="Invalid image path.")
    if not candidate.exists():
        raise HTTPException(status_code=404, detail="Image not found.")
    return candidate


@router.post("/serial-number/upload", response_model=SerialNumberResult)
async def detect_serial_number_upload(
    file: UploadFile = UPLOAD_FILE,
    detector: SerialNumberDetector = DETECTOR_DEP,
) -> SerialNumberResult:
    """
    Detect serial number from an uploaded image.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image uploads allowed.",
        )

    payload = await file.read()
    try:
        image = Image.open(io.BytesIO(payload))
        image.load()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file.",
        ) from exc

    return detector.detect(image)


@router.post("/serial-number/path", response_model=SerialNumberResult)
async def detect_serial_number_path(
    request: SerialNumberPathRequest,
    detector: SerialNumberDetector = DETECTOR_DEP,
) -> SerialNumberResult:
    """
    Detect serial number from an image stored under /data.
    """
    image_path = _resolve_image_path(request.filename)
    try:
        image = Image.open(image_path)
        image.load()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file.",
        ) from exc

    return detector.detect(image)
