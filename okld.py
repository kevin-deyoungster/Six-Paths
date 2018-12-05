import cv2
import numpy as np


def detect_color(image):
    image = cv2.imread(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    res = cv2.bitwise_and(image,image,mask=mask)
    cv2.imshow('frame', image)
    # cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


detect_color("image2.JPG")