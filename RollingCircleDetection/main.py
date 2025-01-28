# Aldrei Chua 1/24/2025
import cv2
import numpy as np


# Receive the video
video = cv2.VideoCapture("RollingCan.MOV")


def detect_circle(img):
    # Detects the can's circular shape in every frame and returns an overlay of the detected circle and center point

    # Format the image
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    gray_img = cv2.blur(gray_img, (3, 3))  # Blur the image

    _, mask = cv2.threshold(gray_img, 100, 200, cv2.THRESH_BINARY)  # Creates a mask that erases weak lines
    gray_img = cv2.bitwise_and(gray_img, gray_img, mask=mask)  # Apply the mask

    # Find circles with strong edges and with a similar radius to that of the top of the soda can
    edges = cv2.Canny(gray_img, 150, 200, apertureSize=5)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 100, param1=120, param2=50, minRadius=160, maxRadius=180)

    # Store all the circles into an array
    try:
        circles = np.uint16(np.around(circles))
    except TypeError:
        circles = []

    # For each detected circle in the array, overlay a blue circle with the same dimensions along with a red center
    try:
        for circle in circles[0][:]:
            cv2.circle(img, (circle[0], circle[1]), circle[2], (255, 0, 0), 2)
            cv2.circle(img, (circle[0], circle[1]), 1, (0, 0, 255), 3)

    except IndexError:
        pass

    return img


while video.isOpened():
    # Constantly reads the webcam feed and creates individual images for processing

    _, image = video.read()

    # If the video is over, stop the loop
    if not _:
        break

    imgResult = detect_circle(image)  # Stores the result of detect_circle as a variable

    cv2.imshow("Rolling Circle Detection", imgResult)  # Displays a window with the image overlay

    # Closes the window when the space bar is pressed
    if cv2.waitKey(1) == ord(' '):
        break

# Close the window after the video is finished
video.release()
cv2.destroyAllWindows()
