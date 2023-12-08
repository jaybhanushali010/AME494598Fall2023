from picamera import PiCamera
from time import sleep
import datetime

# Initialize the camera
camera = PiCamera()

# Set up the video filename with a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"video_{timestamp}.h264"

# Start recording
camera.start_recording(filename)

# Change Time according to requirement
sleep(60)

# Stop recording
camera.stop_recording()

print(f"Video saved as {filename}")
