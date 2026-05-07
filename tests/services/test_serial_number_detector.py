from unittest.mock import Mock, patch

from PIL import Image

from app.services.serial_number_detector import SerialNumberDetector


def test_detect_invokes_model_and_returns_structured_result(
    test_image: Image.Image,
) -> None:
    """
    Invoke the model once and map the structured response.
    """
    structured = Mock()
    structured.invoke.return_value = {"serial_number": "ABC123"}

    model = Mock()
    model.with_structured_output.return_value = structured

    with patch(
        "app.services.serial_number_detector.resolve_model",
        return_value=model,
    ):
        detector = SerialNumberDetector()
        result = detector.detect(test_image)

    model.with_structured_output.assert_called_once()
    structured.invoke.assert_called_once()
    assert result.serial_number == "ABC123"


def test_detect_returns_none_when_model_raises(
    test_image: Image.Image,
) -> None:
    """
    Return null when the model invocation fails.
    """
    structured = Mock()
    structured.invoke.side_effect = RuntimeError("model failure")

    model = Mock()
    model.with_structured_output.return_value = structured

    with patch(
        "app.services.serial_number_detector.resolve_model",
        return_value=model,
    ):
        detector = SerialNumberDetector()
        result = detector.detect(test_image)

    structured.invoke.assert_called_once()
    assert result.serial_number is None
