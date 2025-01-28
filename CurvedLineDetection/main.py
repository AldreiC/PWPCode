# Aldrei Chua 1/23/2025
import cv2
import numpy as np


# Get the video feed from the web camera
video = cv2.VideoCapture(0)


def curve_detect(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_img = cv2.blur(gray_img, (3, 3))

    _, mask = cv2.threshold(gray_img, 100, 150, cv2.THRESH_BINARY)
    gray_img = cv2.bitwise_and(gray_img, gray_img, mask=mask)

    edges = cv2.Canny(gray_img, 100, 200, apertureSize=5)

    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi/180, threshold=200, minLineLength=10, maxLineGap=10)
    for line in lines:
        x3, y3, x4, y4 = line[0]
        cv2.line(img, (x3, y3), (x4, y4), (0, 255, 0), 3)

    """try:
        x1, y1, x2, y2 = lines[0][0]
        if x1 != x2:
            m1 = (y2 - y1) / (x2 - x1)
        else:
            m1 = 10000
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        for line in lines:
            x3, y3, x4, y4 = line[0]
            if x3 != x4:
                m2 = (y4 - y3) / (x4 - x3)
            else:
                m2 = 10000

            if (int(m1 * m2) == -1) or (m1 == 0 and abs(m2) >= 1000) or (abs(m1) >= 1000 and m2 == 0):
                cv2.line(img, (x3, y3), (x4, y4), (0, 255, 0), 3)
    except:
        pass"""

    return img


while True:
    # Constantly reads the webcam feed and creates individual images for processing

    _, image = video.read()
    imgResult = curve_detect(image)

    cv2.imshow("Curved Line Detection", imgResult)  # Displays a window with the image overlay

    # Closes the window when the space bar is pressed
    if cv2.waitKey(1) == ord(' '):
        break
