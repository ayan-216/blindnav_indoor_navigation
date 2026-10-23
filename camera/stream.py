
import threading
import time

import cv2


class CameraStream:
    def __init__(self, stream_url: str):
        self.stream_url = stream_url
        self.cap = None

        self._latest_frame = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = None

        self.frames_received = 0
        self.last_frame_time = None

    def start(self):
        """Open the stream and start reading frames in the background."""
        self.cap = cv2.VideoCapture(self.stream_url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            raise RuntimeError(
                f"Could not connect to camera: {self.stream_url}"
            )

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._read_frames,
            daemon=True,
        )
        self._thread.start()

        return self

    def _read_frames(self):
        """Continuously replace the stored frame with the newest frame."""
        while not self._stop_event.is_set():
            success, frame = self.cap.read()

            if not success:
                time.sleep(0.01)
                continue

            with self._lock:
                self._latest_frame = frame
                self.frames_received += 1
                self.last_frame_time = time.monotonic()

    def read(self):
        """Return the latest frame, or None if no frame has arrived yet."""
        with self._lock:
            if self._latest_frame is None:
                return None

            return self._latest_frame.copy()

    def stop(self):
        """Stop reading frames and release the camera connection."""
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=2.0)

        if self.cap is not None:
            self.cap.release()
            self.cap = None
