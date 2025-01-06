#Aldrei Chua
"""
Title: Alternate simpler method for directly extracting points
Author: GeeksForGeeks
Date: 07/25/2024
Type: Source Code
Availability: https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
"""

"""
Title: Live Webcam Drawing using OpenCV
Author: GeeksForGeeks
Date: 01/03/2023
Type: Source Code
Availability: https://www.geeksforgeeks.org/live-webcam-drawing-using-opencv/
"""


import cv2
import numpy as np

# Set the dimensions of window
frameWidth = 640
frameHeight = 480

# Get the video feed from the web camera
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def canny_edge(image):
    # Detect lines in the input image and output the image with two blue parallel lines and a red centerline

    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Convert the video into grayscale
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)  # Blur the image
    edges = cv2.Canny(gray_img, 50, 200, 5, L2gradient=True)  # Detect edges that are very dark
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi/180,  # Angle resolution in radians
        threshold=5,  # Min number of votes for valid line
        minLineLength=20,  # Min allowed length of line
        maxLineGap=10  # Max allowed gap between line for joining them
    )

    # Create arrays to separate the lines into two main parallel lines
    first_line = []
    second_line = []
    try:
        # Take the first line in the whole array
        x1, y1, x2, y2 = lines[0][0]
        if x1 != x2:
            m = (y1 - y2) / (x1 - x2)
            b = y1 - x1 * m
        else:
            m = 1000
            b = y1 - x1 * 1000
        first_line.append([m, b])  # Put the slope and y-intercept in the first_line array

        for points in lines[1:]:
            # Use the other lines in the list
            x1, y1, x2, y2 = points[0]
            if x1 != x2:
                m1 = (y1 - y2) / (x1 - x2)
                b1 = y1 - x1 * m1
            else:
                m1 = 1000
                b1 = y1 - x1 * 1000

            # Checks the line has a similar slope and y-intercept to the reference line
            if ((b <= 0 and b1 <= 0 and b*1.5 <= b1 <= b*0.5) or (b >= 0 and b1 >= 0 and b*0.5 <= b1 <= b*1.5) or b-20 <= b1 <= b+20) and ((m <= 0 and m1 <= 0 and m*1.1 <= m1 <= m*0.9) or ((m >= 0 and m1 >= 0 and m*0.9 <= m1 <= m*1.1) or m-0.25 <= m1 <= m+0.25)):
                first_line.append([m1, b1])  # Puts slope and intercept in first array if both are similar
            elif (m <= 0 and m1 <= 0 and m*1.1 <= m1 <= m*0.9) or ((m >= 0 and m1 >= 0 and m*0.9 <= m1 <= m*1.1) or m-0.25 <= m1 <= m+0.25):
                second_line.append([m1, b1])  # Puts slope and intercept in second array if only slope is similar

        # Create arrays that hold the slope and intercept for the two parallel lines
        line1 = [0, 0]
        line2 = [0, 0]

        # Find the average slope and intercept of the lines in the first array
        for line in first_line:
            line1[0] += line[0]/len(first_line)
            line1[1] += line[1]/len(first_line)

        # Find the average slope and intercept of the lines in the second array
        for other_line in second_line:
            line2[0] += other_line[0]/len(second_line)
            line2[1] += other_line[1]/len(second_line)

        # Draw the two parallel lines based on the average slopes and intercepts calculated
        cv2.line(image, (0, int(line1[1])), (640, int(640 * line1[0] + line1[1])), (255, 0, 0), 2)
        cv2.line(image, (0, int(line2[1])), (640, int(640 * line2[0] + line2[1])), (255, 0, 0), 2)

        # Draw the centerline based on the average slopes and intercepts of the two parallel lines
        cv2.line(image, (0, int((line1[1]+line2[1])/2)), (640, int(((640 * line1[0] + line1[1])+(640 * line2[0] + line2[1]))/2)), (0, 0, 255), 2)

    except TypeError:
        pass

    return image


while True:
    # Constantly reads the webcam feed and creates individual images for processing

    success, img = cap.read()
    imgResult = canny_edge(img)

    cv2.imshow("Line Detection", imgResult)  # Displays a window with the image overlay

    # Closes the window when the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break
