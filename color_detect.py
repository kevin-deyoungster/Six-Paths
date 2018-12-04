import cv2
import numpy as np

image = cv2.imread("image2.JPG")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([22,25,68])
upper_red = np.array([12,17,55])

mask = cv2.inRange(hsv, lower_red, upper_red)

res = cv2.bitwise_and(image,image,mask=mask)
cv2.imshow('frame', image)
cv2.imshow('mask', mask)
cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()