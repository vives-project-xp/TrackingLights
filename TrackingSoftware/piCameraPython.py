import picamera
import time

def test_picamera():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)  # Set the resolution as needed
        camera.start_preview()

        # Allow some time for the camera to warm up
        time.sleep(2)

        try:
            while True:
                # Capture a frame and display it for 5 seconds
                camera.capture('test_image.jpg')  # Captures an image and saves it
                time.sleep(5)  # Display the captured image for 5 seconds

        except KeyboardInterrupt:
            pass

        camera.stop_preview()

if __name__ == "__main__":
    test_picamera()
