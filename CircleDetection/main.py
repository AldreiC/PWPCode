#Aldrei Chua 1/16/2025
import cv2
import numpy as np


def detect_circle(image):
    # Detect a circle in the given image and return an overlay of a green circle with a red center

    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Convert the picture into grayscale
    gray_img = cv2.GaussianBlur(gray_img, (3, 3), 0)  # Blur the image

    # Create and apply a mask to hide distracting elements
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[150:525, 300:700] = 255
    #gray_img = cv2.bitwise_and(gray_img, gray_img, mask=mask)

    # Use Canny edge detection to find strong borders and find contours based on the edges
    edges = cv2.Canny(gray_img, 50, 150)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circles = []  # Stores all circles found
    avg_circle = [[0, 0], 0]  # Stores the average of the most popular cluster of circles

    for contour in contours:
        # Make a circle around each contour and store its center and radius into the circles list
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = [int(x), int(y)]
        radius = int(radius)

        # Filters out dots and extremely large circles
        if radius >= 50:
            circles.append([center, radius, 0])  # Add the center, radius, and a measure of similarity to other circles

    # Increments the similarity measure when the circle finds another circle with a similar center
    for circle in circles:
        for other_circle in circles:
            if (abs(circle[0][0] - other_circle[0][0]) <= 10 or abs(circle[0][1] - other_circle[0][1]) <= 10) and circle != other_circle:
                circle[2] += 1

    circles.sort(key=lambda x: x[2], reverse=True)  # Sorts the circles list to put the most popular circles first
    circle_x = 0
    circle_y = 0
    circle_r = 0
    circle_count = 0

    for circle in circles:
        # Only use the circles with the highest similarity measure
        if circle[2] < circles[0][2]:
            break
        circle_count += 1  # Counts number of circles
        circle_x += circle[0][0]
        circle_y += circle[0][1]
        circle_r += circle[1]

    # Assign the average of the circles' measurements to avg_circle (accounts for duplication from for loop)
    avg_circle[0][0] += (circle_x / circle_count)
    avg_circle[0][1] += (circle_y / circle_count)
    avg_circle[1] += (circle_r / circle_count)

    # Draw the average circle and its center point
    cv2.circle(image, tuple([int(avg_circle[0][0]), int(avg_circle[0][1])]), int(avg_circle[1]), (0, 255, 0), 3)
    cv2.circle(image, tuple([int(avg_circle[0][0]), int(avg_circle[0][1])]), 2, (0, 0, 255), 3)

    return image


# Receive, process, and display an image of a can with image overlay
img = cv2.imread("Can_Image.png")
imgResult = detect_circle(img)
cv2.imshow("Circle Overlay", imgResult)
cv2.waitKey(0)  # Close the window when a key is pressed
