from pydantic import BaseModel, Field


class SerialNumberResult(BaseModel):
    """
    Structured result for serial number detection.
    """

    serial_number: str | None = Field(
        default=None,
        description="Detected serial number, or null when not found.",
    )


class SerialNumberPathRequest(BaseModel):
    """
    Request payload for detecting a serial number from a stored image.
    """

    filename: str = Field(
        ...,
        description="Image filename under the data directory.",
    )
