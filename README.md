# BlindNav — Real-Time Vision for Indoor Accessibility

BlindNav is an assistive-technology project focused on helping visually impaired users understand indoor environments through computer vision and real-time visual analysis.

The project uses a smartphone camera as a live video source and a YOLO object-detection model to identify objects in the environment. The long-term goal is to build an indoor navigation assistant that interprets its surroundings and provides useful audio guidance.

> **Current status:** Working real-time camera streaming and object detection prototype. Custom model integration, scene understanding, and navigation guidance are under development.

## Features

### Implemented
- Live video streaming from a smartphone over Wi-Fi.
- Background camera-frame acquisition using a reusable Python class.
- Real-time object detection using Ultralytics YOLO.
- Bounding-box visualization and object labels.
- Performance monitoring for FPS and inference time.
- Modular separation of camera, detection, and metrics components.

### Planned
- Integration of a custom-trained model for indoor environments.
- Detection of relevant objects such as doors, stairs, elevators, and obstacles, depending on the final model's classes.
- Standardized detection output for downstream processing.
- Scene understanding and spatial reasoning.
- Context-aware audio guidance.
- Robustness, latency, and detection-accuracy evaluation.

## Technology Stack

- **Python** — application logic
- **OpenCV** — camera streaming and image processing
- **Ultralytics YOLO** — object detection
- **PyTorch** — model inference backend
- **Threading** — background frame acquisition
- **deque and time utilities** — performance measurement

## Project Structure

```text
blindNav/
├── camera/
│   └── stream.py
├── vision/
│   └── detector.py
├── utils/
│   └── metrics.py
├── models/                     # Optional location for custom models
├── camera_test.py              # Basic camera test
├── test_camera_stream.py       # CameraStream test
├── test_camera_metrics.py      # Metrics test
├── test_live_detection.py      # Live end-to-end detection test
├── yolo26n.pt                  # Current pretrained model
├── requirements.txt
└── README.md
```

The `models/` directory is intended for custom model files when available. The structure above describes the intended layout; optional directories and test files may be added as development continues.

## Getting Started

### 1. Prerequisites

- Python 3.12
- A Windows, Linux, or macOS development environment
- A smartphone running a camera-streaming application
- A computer and phone connected to the same Wi-Fi network
- A compatible YOLO model file

### 2. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd blindNav
```

Replace `<YOUR_REPOSITORY_URL>` with the actual repository URL.

### 3. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

Install the project's dependencies:

```bash
python -m pip install --upgrade pip
pip install ultralytics opencv-python
```

If the project uses a maintained `requirements.txt`, install from that file instead:

```bash
pip install -r requirements.txt
```

Ensure the dependencies used by the current implementation are included in `requirements.txt` before relying on the file for a clean installation.

### 5. Configure the camera stream

Start the camera-streaming application on your smartphone and obtain its video-stream URL.

The current development setup uses an IP Webcam-style endpoint:

```text
http://<PHONE_IP>:8080/video
```

Replace `<PHONE_IP>` with the phone's current local network IP address.

Make sure the phone and computer can communicate over the local network. The URL, port, and endpoint may vary depending on the streaming application.

### 6. Run the camera test

```bash
python camera_test.py
```

Use this script to troubleshoot the camera connection independently of the detection pipeline.

### 7. Run live object detection

```bash
python test_live_detection.py
```

This is the main integration test for the current prototype. It combines the camera stream, YOLO detector, and performance metrics to display live object detections.

Press **Q** in the video window to exit.

## Core Components

### `camera/stream.py`

Implements the `CameraStream` class.

Responsibilities:
- Open the smartphone video stream.
- Continuously read frames in a background thread.
- Keep the latest available frame for processing.
- Provide thread-safe frame access.
- Stop frame acquisition and release the capture resource.

The latest-frame approach helps avoid building an application-level queue of stale frames.

### `vision/detector.py`

Implements the `ObjectDetector` class.

Responsibilities:
- Load a YOLO model.
- Run inference on OpenCV frames.
- Apply a configurable confidence threshold.
- Return the model's detection results.

The model path can be changed when the custom-trained BlindNav model is ready.

### `utils/metrics.py`

Implements the `PerformanceMetrics` class.

Responsibilities:
- Estimate processing FPS from recent frame intervals.
- Record processing durations.
- Calculate average processing time over a rolling window.

These measurements help evaluate responsiveness during development. Processing FPS is not necessarily the same as the camera's capture FPS.

### `test_live_detection.py`

Combines the current components into a real-time testing pipeline:

1. Connect to the smartphone camera.
2. Retrieve the latest frame.
3. Run object detection.
4. Measure inference duration and processing FPS.
5. Visualize the detections.
6. Clean up resources when the test exits.

## Model Configuration

The current `yolo26n.pt` model is a pretrained general-purpose object detector. Its supported classes depend on the model's training dataset and do not automatically include every indoor-navigation category.

The `ObjectDetector` class accepts a configurable model path:

```python
from vision.detector import ObjectDetector

detector = ObjectDetector(
    model_path="yolo26n.pt",
    confidence=0.35,
)
```

When a custom-trained model becomes available, configure the detector to use its file:

```python
detector = ObjectDetector(
    model_path="models/blindnav_best.pt",
    confidence=0.35,
)
```

The example custom model filename is illustrative. Use the actual filename and path supplied by the training team.

The custom model's class names and label mapping must be verified before interpreting its predictions.

## Performance

During initial development, the live detection prototype achieved approximately:

| Metric | Observed result |
|---|---:|
| Processing FPS | 20–25 FPS |
| Inference time | 30–35 ms |

These are preliminary measurements from the development setup, not guaranteed performance figures. Results may vary with hardware, model size, input resolution, camera buffering, and workload.

## Development Roadmap

- [x] Establish smartphone camera streaming.
- [x] Implement reusable camera-frame acquisition.
- [x] Integrate a pretrained YOLO model.
- [x] Display live detections and performance metrics.
- [ ] Normalize model output into a model-independent detection format.
- [ ] Integrate the custom-trained indoor object-detection model.
- [ ] Develop scene understanding and spatial reasoning.
- [ ] Implement context-aware audio guidance.
- [ ] Evaluate detection accuracy on held-out data.
- [ ] Test latency, failure cases, and real-world robustness.

## Safety and Limitations

BlindNav is an experimental prototype and is not yet a validated mobility or navigation aid.

Object detection alone cannot establish that a path is safe, determine reliable object distance, or guarantee that stairs and other hazards have been detected. Such capabilities require additional reasoning, suitable sensing or estimation methods, and extensive real-world testing.

Do not rely on the current prototype as the sole means of navigating hazardous or unfamiliar environments.

## Contributing

Development is organized into modular components so camera streaming, vision, metrics, and future navigation logic can be developed and tested independently.

When contributing:
- Keep components modular and reusable.
- Test changes against the live pipeline where appropriate.
- Document model requirements and class mappings.
- Avoid committing virtual environments, credentials, or unnecessary large model and dataset files.

## License

A license has not yet been specified. Add a `LICENSE` file before distributing the project under an open-source license.
