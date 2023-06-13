import cv2
import numpy as np


# Read the image and convert i     t to grayscale
image = cv2.imread('objects.jpg')
image = cv2.resize(image, None, fx=0.9, fy=0.9)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Now convert the grayscale image to binary image
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Now detect the contours
contours, hierarchy = cv2.findContours(binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

#  Visualizing the data structures
print("Length of contours {}".format(len(contours)))
print(contours)

# draw contours on the original image
image_copy = image.copy()
image_copy = cv2.drawContours(image_copy, contours, -1, (0, 255, 0), thickness=2, lineType=cv2.LINE_AA)


# Visualizing the results
cv2.imshow("Original image", image)
cv2.imshow("Grayscale image", gray)
cv2.imshow("Drawn contours", image_copy)
cv2.imshow("Binary image", binary)


cv2.imwrite("gray_object.jpg", gray)
cv2.imwrite("contoured_object.jpg", image_copy)
cv2.imwrite("binary_object.jpg", binary)

cv2.waitKey(0)
cv2.destroyAllWindows()
