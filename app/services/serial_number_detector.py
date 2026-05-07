from __future__ import annotations

from functools import lru_cache

from deepagents._models import resolve_model
from langchain_core.messages import HumanMessage
from PIL import Image

from app.schemas.serial_number import SerialNumberResult
from app.utils.image import image_to_data_url

DEFAULT_MODEL_SPEC = "google_genai:gemini-2.5-flash-lite"
SERIAL_NUMBER_PROMPT = (
    "Extract the product serial number from the image. "
    "Return JSON with key serial_number (string or null)."
)


class SerialNumberDetector:
    """
    Detects serial numbers from images using a Gemini model.
    """

    def __init__(
        self,
        model_spec: str = DEFAULT_MODEL_SPEC,
        raise_on_error: bool = False,
    ) -> None:
        """
        Initialize the detector with a model spec.
        """
        self._raise_on_error = raise_on_error
        self._model = resolve_model(model_spec)
        self._structured_model = self._model.with_structured_output(
            SerialNumberResult,
        )

    def detect(self, image: Image.Image) -> SerialNumberResult:
        """
        Detect the serial number from a PIL image.
        """
        data_url = image_to_data_url(image)
        message = HumanMessage(
            content=[
                {"type": "text", "text": SERIAL_NUMBER_PROMPT},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        )

        try:
            result = self._structured_model.invoke([message])
        except Exception:
            if self._raise_on_error:
                raise
            return SerialNumberResult(serial_number=None)

        return SerialNumberResult.model_validate(result)


@lru_cache
def get_serial_number_detector() -> SerialNumberDetector:
    """
    Build and cache the serial number detector.
    """
    return SerialNumberDetector()
