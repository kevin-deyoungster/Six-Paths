import numpy as np
import imutils
import cv2


def get_edges(image):
    """
    Returns image of edges
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    lower_thresh = 75
    upper_thresh = 200
    edged = cv2.Canny(gray, lower_thresh, upper_thresh)
    return edged


def _get_contours(edged_image):
    """
    Returns contours in edged_image
    """
    cnts = cv2.findContours(edged_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    if len(cnts) < 0:
        return None
    return cnts


def get_quadrilateral_contour(edged_image):
    """
    Returns contour of largest quadrilateral in [edged_image]
    """
    contours = _get_contours(edged_image)

    # Get 5 largest contours
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contours = sorted_contours[:5]

    for contour in largest_contours:

        # Trace contour and check if number of 'corners' is 4
        perimeter = cv2.arcLength(contour, True)
        approximage_contour = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approximage_contour) == 4:
            return approximage_contour
    return None


def get_center_point_of_contour(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cY, cX)

def is_point_in_contour(point, contour):
    return cv2.pointPolygonTest(contour, point, False) == 1.0

def get_contours_of_color(image, lower_color, upper_color):
    """
    Returns contours of [color]
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    edged = cv2.Canny(mask, 75, 200)
    # cv2.imshow(f"masked-{lower_color}", mask)
    return _get_contours(edged)