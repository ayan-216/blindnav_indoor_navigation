import cv2
import os

stream_url = os.getenv(
    "CAMERA_STREAM_URL",
    "http://127.0.0.1:8080/video"
)
cap = cv2.VideoCapture(stream_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
if not cap.isOpened():
    print("Could not connect to the camera.")
    exit()

print("Camera connected! Press Q to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to receive a frame.")
        break

    cv2.imshow("BlindNav - Live Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()