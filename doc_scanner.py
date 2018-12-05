from utils.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import imutils
import cv2

RED_LOWER = [140, 150, 0]
RED_UPPER = [170, 255, 255]
BLUE_LOWER = [100, 150, 0]
BLUE_UPPER = [140, 255, 255]


def highlight_color(image, lower_color, upper_color):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    edged = cv2.Canny(mask, 75, 200)
    # cv2.imshow('masked', edged)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cv2.drawContours(image, [cnts[0]], -1, (0, 255, 0), 2)
    # cv2.imshow("Final", image)


def get_quadrilateral_contour(edged_image):
    cnts = cv2.findContours(edged_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    if len(cnts) < 0:
        print("No Contours Found in Image")
        return None, False
    else:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # Get Approximate estimate of contour
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                print("Found contour with 4 sides")
                return approx, True
        return None, False


def getGrid(file_path):

    image = cv2.imread(file_path)
    original_image = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    cv2.imshow("Edged", edged)

    quadCnt, found = get_quadrilateral_contour(edged)

    if found:
        cv2.drawContours(image, [quadCnt], -1, (0, 255, 0), 2)

        top_down_image = four_point_transform(original_image, quadCnt.reshape(4, 2))
        image = top_down_image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)
        cv2.imshow("Edged", edged)
        # highlight_color(image, RED_LOWER, RED_UPPER)
        # highlight_color(image, BLUE_LOWER, BLUE_UPPER)

        # T = threshold_local(warped, 31, offset=10, method="gaussian")
        # warped = (warped > T).astype("uint8") * 255
        cv2.imshow("Traced Image", image)
        cv2.imshow("Original Image", original_image)
        cv2.imshow("Warped", top_down_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Did not find any 4 sided contour")


getGrid("file-3.jpeg")
getGrid("image2.JPG")
