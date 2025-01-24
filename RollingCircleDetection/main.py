#Aldrei Chua 1/24/2025
import cv2
import numpy as np


# Receive the video
cap = cv2.VideoCapture("RollingCan.MOV")


def detect_circle(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_img = cv2.blur(gray_img, (3, 3), 0)

    _, mask = cv2.threshold(gray_img, 50, 150, cv2.THRESH_BINARY)
    gray_img = cv2.bitwise_and(gray_img, gray_img, mask=mask)

    edges = cv2.Canny(gray_img, 50, 200)

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=50, minRadius=100, maxRadius=200)

    try:
        circles = np.uint16(np.around(circles))
    except TypeError:
        circles = []

    try:
        for circle in circles[0][:]:
            cv2.circle(image, (circle[0], circle[1]), circle[2], (255, 0, 0), 2)
            cv2.circle(image, (circle[0], circle[1]), 1, (0, 0, 255), 3)
    except IndexError:
        pass

    return image


while cap.isOpened():
    # Constantly reads the webcam feed and creates individual images for processing

    success, img = cap.read()

    if not success:
        break

    imgResult = detect_circle(img)

    cv2.imshow("Rolling Circle Detection", imgResult)  # Displays a window with the image overlay

    # Closes the window when the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
