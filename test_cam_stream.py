
import cv2

from camera.stream import CameraStream


STREAM_URL = "http://192.168.1.36:8080/video"


def main():
    camera = CameraStream(STREAM_URL)

    try:
        camera.start()
        print("Camera stream started. Press Q to quit.")

        while True:
            frame = camera.read()

            if frame is None:
                continue

            cv2.imshow("BlindNav - Camera Module Test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
