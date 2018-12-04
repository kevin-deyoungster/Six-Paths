from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

def getGrid(file):
        image = cv2.imread(file)
        orig = image.copy()

        # Convert to Grayscale for Processing, and blur it (Gaussian)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        # Find all contours 
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # Get the largest 5 contours
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None
        foundBoundary = False

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            screenCnt = approx

            if len(approx) == 4:
                print("Found contour with 4 sides")
                screenCnt = approx
                foundBoundary = True
                break

        if foundBoundary:
                cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
                warped = four_point_transform(orig, screenCnt.reshape(4, 2))

                warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                T = threshold_local(warped, 31, offset=10, method="gaussian")
                warped = (warped > T).astype("uint8") * 255

                # cv2.imshow("Original", orig)
                # cv2.imshow(file, image)
                # cv2.imshow("Scanned", warped)
                showContours(warped)

                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
                print("Did not find any 4 sided contour")

def showContours(image):
        
        # Find all contours 
        cnts = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # Get the largest 5 contours
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            screenCnt = approx

        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        cv2.imshow(file, image)


getGrid("image.jpeg")