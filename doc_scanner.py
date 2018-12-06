from utils.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import imutils
import cv2

BLUE_LOWER = [102, 135, 11]
BLUE_UPPER = [128, 183, 108]

RED_LOWER = [154, 72, 35]
RED_UPPER = [177, 233, 142]


def get_color_contour(image, lower_color, upper_color):
    """
    Returns contours of [color]
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    edged = cv2.Canny(mask, 75, 200)
    cv2.imshow(f"masked-{lower_color}", mask)
    # height, width = mask.shape
    # print(f"Height - {height}, Width - {width}")
    # print(mask.shape)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts


def get_edges(image, optimal=False):
    """
    Returns a canny edged render of [image]
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    v = np.median(gray)
    sigma = 0.33
    # ---- apply optimal Canny edge detection using the computed median----
    lower_thresh = int(max(0, (1.0 - sigma) * v)) if optimal else 75
    upper_thresh = int(min(255, (1.0 + sigma) * v)) if optimal else 200

    edged = cv2.Canny(gray, lower_thresh, upper_thresh)
    return edged


def get_quadrilateral_contour(edged_image):
    """
    Finds contour of the largest quadrilateral in image
    """
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
    edged = get_edges(image)
    quadCnt, found = get_quadrilateral_contour(edged)

    if found:
        # Draw contour of the identified quadrilateral
        cv2.drawContours(image, [quadCnt], -1, (0, 255, 0), 2)
        cv2.imshow(f"Boundary Identified - {file_path}", image)

        # Perform Perspective Transform to create top-down-view
        top_down_image = four_point_transform(original_image, quadCnt.reshape(4, 2))
        cv2.imshow("Perspective Transform", top_down_image)

        # We'll be working with the top-down view henceforth, make that the main image
        image = top_down_image

        # Extract the colored objects (Start and Goal Positions)
        color_contoured_image = image.copy()
        red_contour = get_color_contour(image, RED_LOWER, RED_UPPER)
        blue_contour = get_color_contour(image, BLUE_LOWER, BLUE_UPPER)

        cv2.drawContours(color_contoured_image, red_contour, -1, (0, 255, 0), 2)
        cv2.drawContours(color_contoured_image, blue_contour, -1, (0, 255, 0), 2)

        cv2.imshow("Recognized Colors", color_contoured_image)

        cv2.imshow("Original Image", original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Did not find any 4 sided contour")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


from pathlib import Path

getGrid("image2.JPG")
pathlist = Path("im-5").glob("**/*.JPG")
for path in pathlist:
    getGrid(str(path))

# getGrid("file12-2.jpeg")
# getGrid("file5-1.jpeg")
