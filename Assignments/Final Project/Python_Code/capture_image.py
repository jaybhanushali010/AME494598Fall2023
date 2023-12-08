from picamera import PiCamera
from time import sleep
import datetime

# Initialize the camera
camera = PiCamera()

# Function to capture images
def capture_image():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.jpg"
    camera.capture(filename)
    print(f"Captured {filename}")

# Main loop
try:
    while True:
        capture_image()
        sleep(15)  # Wait for 15 seconds before next capture
except KeyboardInterrupt:
    print("Program stopped")
