
import os
from pathlib import Path

from ultralytics import YOLO


class ObjectDetector:
    def __init__(
        self,
        model_path: str | None = None,
        confidence: float = 0.35,
    ):
        if model_path is None:
            model_path = os.getenv("VISION_MODAL", "yolo26n.pt")

        model_file = Path(model_path)

        if not model_file.is_file():
            raise FileNotFoundError(
                f"YOLO model not found: {model_file.resolve()}"
            )

        self.model = YOLO(str(model_file))
        self.confidence = confidence

    def detect(self, frame):
        """Run YOLO inference on one OpenCV frame."""
        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False,
        )

        return results[0]
