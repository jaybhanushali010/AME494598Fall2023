import cv2
import pickle
import cvzone
import numpy as np
import requests

# Video feed
cap = cv2.VideoCapture('car_park_test_server.mp4')

with open('Car_park_pos_server', 'rb') as f:
    posList = pickle.load(f)

width, height = 180, 300
window_size = (550, 310)  # Adjust this based on your screen resolution

# URL of your EC2 server
ec2_server_url = "http://18.205.239.215:8080/update_space_counter"

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 4000:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                            thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                        thickness=5, offset=20, colorR=(0, 200, 0))

    # Send spaceCounter to EC2 server
    send_data_to_ec2(spaceCounter)

# Function to send data to EC2 server
def send_data_to_ec2(spaceCounter):
    try:
        # Define the data payload
        payload = {'space_counter': spaceCounter}

        # Make a POST request to the EC2 server
        response = requests.post(ec2_server_url, data=payload)

        # Check the response status
        if response.status_code == 200:
            print("Space counter sent successfully.")
            print(spaceCounter)
        else:
            print(f"Failed to send space counter. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error sending space counter to EC2 server: {e}")

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    resized_img = cv2.resize(img, window_size)  # Resize the image
    cv2.imshow("Image", resized_img)
    cv2.waitKey(10)
