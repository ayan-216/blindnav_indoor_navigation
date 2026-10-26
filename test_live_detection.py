
import time
import os
import cv2
from dotenv import load_dotenv

from camera.stream import CameraStream
from vision.detector import ObjectDetector
from utils.metrics import PerformanceMetrics

load_dotenv()

STREAM_URL = os.getenv(
    "CAMERA_STREAM_URL",
    "http://127.0.0.1:8080/video"
)

def main():
    camera = CameraStream(STREAM_URL)
    detector = ObjectDetector()
    metrics = PerformanceMetrics()

    try:
        camera.start()
        print("BlindNav live detection started. Press Q to quit.")
        while True:
            frame = camera.read()

            if frame is None:
                continue

            start_time = time.perf_counter()

            result = detector.detect(frame)

            inference_time = time.perf_counter() - start_time
            metrics.record_frame()
            metrics.record_processing_time(inference_time)

            annotated_frame = result.plot()

            cv2.putText(
                annotated_frame,
                f"Detection FPS: {metrics.fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                annotated_frame,
                f"Inference: {inference_time * 1000:.1f} ms",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.imshow("BlindNav - Live Object Detection", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
