# Aldrei Chua 1/23/2025
"""
Title: Image Thresholding
Author: OpenCV
Type: Source Code
Availability: https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
"""

"""
Title: Contour Features
Author: OpenCV
Type: Source Code
Availability: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
"""


import cv2
import numpy as np


# Get the video feed from the web camera
video = cv2.VideoCapture(0)


def curve_detect(img):
    """Returns an image with an overlay of curved parallel lines and their centerline

    Detects curved parallel lines, calculates their centerline, and returns an image with the image overlay

    Parameters
    ------------
        img: numpy.ndarray
            An individual frame of the video obtained by the camera
    Return
    ------------
        img: numpy.ndarray
            The original image modified with image overlay detecting two curved parallel lines and their centerline
    """

    # Preprocess the raw image for detection
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_img = cv2.blur(gray_img, (11, 11))

    kernel = np.ones((7, 7), np.uint8)
    gray_img = cv2.dilate(gray_img, kernel, iterations=1)

    mask = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 11)
    gray_img = cv2.bitwise_and(gray_img, gray_img, mask=mask)

    edges = cv2.Canny(gray_img, 150, 200, apertureSize=5, L2gradient=True)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_list = []

    try:
        # Detect all long, curved contours around the middle of the screen
        for contour in contours:
            epsilon = 0.001 * cv2.arcLength(contour, False)
            approximate_contour = cv2.approxPolyDP(contour, epsilon, False)

            length = cv2.arcLength(approximate_contour, False)
            coordinate_total = approximate_contour[0][0][0] + approximate_contour[0][0][1]
            if length <= 500 or coordinate_total <= (width+height) * 0.2 or coordinate_total >= (width+height) * 0.8:
                continue

            contour_list.append(approximate_contour)
            cv2.drawContours(img, [approximate_contour], -1, (0, 0, 255), 2)

        # Find and display the midline between two contours
        c_line1 = contour_list[0]
        c_line2 = contour_list[1]

        midline = []
        for point1, point2 in zip(c_line1, c_line2):
            m_pointx = (point1[0][0] + point2[0][0]) // 2
            m_pointy = (point1[0][1] + point2[0][1]) // 2
            midline.append([m_pointx, m_pointy])

        midline = np.array(midline, dtype=np.int32)
        cv2.polylines(img, [midline], isClosed=False, color=(0, 255, 0), thickness=2)

    except:
        pass

    return img


while True:
    # Constantly reads the webcam feed and creates individual images for processing

    _, image = video.read()
    height, width = image.shape[:2]
    imgResult = curve_detect(image)

    # Display a window with the image overlay
    cv2.imshow("Curved Line Detection", imgResult)

    # Close the window when the space bar is pressed
    if cv2.waitKey(1) == ord(' '):
        break
