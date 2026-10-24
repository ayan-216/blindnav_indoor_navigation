
import time
from collections import deque


class PerformanceMetrics:
    def __init__(self, window_size: int = 30):
        self._frame_times = deque(maxlen=window_size)
        self._processing_times = deque(maxlen=window_size)
        self._last_frame_time = None

    def record_frame(self):
        """Record when a frame is processed."""
        now = time.perf_counter()

        if self._last_frame_time is not None:
            self._frame_times.append(now - self._last_frame_time)

        self._last_frame_time = now

    def record_processing_time(self, elapsed_seconds: float):
        """Record the duration of a processing operation."""
        self._processing_times.append(elapsed_seconds)

    @property
    def fps(self) -> float:
        """Estimate processing FPS from recent frame intervals."""
        if not self._frame_times:
            return 0.0

        average_interval = sum(self._frame_times) / len(self._frame_times)

        return 1.0 / average_interval if average_interval > 0 else 0.0

    @property
    def average_processing_ms(self) -> float:
        """Average recorded processing duration in milliseconds."""
        if not self._processing_times:
            return 0.0

        average_seconds = (
            sum(self._processing_times) / len(self._processing_times)
        )

        return average_seconds * 1000.0
