
import time

import cv2

from camera.stream import CameraStream
from utils.metrics import PerformanceMetrics


STREAM_URL = "http://192.168.1.36:8080/video"


def main():
    camera = CameraStream(STREAM_URL)
    metrics = PerformanceMetrics()

    try:
        camera.start()
        print("Press Q to quit.")

        while True:
            frame = camera.read()

            if frame is None:
                continue

            start_time = time.perf_counter()

            # Placeholder for future YOLO inference.
            display_frame = frame

            elapsed = time.perf_counter() - start_time

            metrics.record_frame()
            metrics.record_processing_time(elapsed)

            cv2.putText(
                display_frame,
                f"FPS: {metrics.fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                display_frame,
                f"Processing: {metrics.average_processing_ms:.2f} ms",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.imshow("BlindNav - Performance Test", display_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
