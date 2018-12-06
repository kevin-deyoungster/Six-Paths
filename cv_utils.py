import numpy as np
import imutils
import cv2


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
    # cv2.imshow(f"masked-{lower_color}", mask)
    # height, width = mask.shape
    # print(f"Height - {height}, Width - {width}")
    # print(mask.shape)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts


def draw_grid(img, parts=3, color=(0, 255, 0), sub_color=(255, 0, 0)):
    """
    Draws grid lines on image and returns contours of the grid cells
    """
    height = img.shape[0]
    width = img.shape[1]

    # Draw Vertical Lines
    cv2.line(img, (int(0.33 * width), 0), (int(0.33 * width), height), color, 2, 1)
    cv2.line(img, (int(0.67 * width), 0), (int(0.67 * width), height), color, 2, 1)

    # Draw Horizontal Lines
    cv2.line(img, (0, int(0.33 * height)), (width, int(0.33 * height)), color, 2, 1)
    cv2.line(img, (0, int(0.67 * height)), (width, int(0.67 * height)), color, 2, 1)

    # Draw the 9 cells
    contours = [
        np.array(
            [
                [0, 0],
                [int(0.33 * width), 0],
                [int(0.33 * width), int(0.33 * height)],
                [0, int(0.33 * height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [int(0.33 * width), 0],
                [int(0.67 * width), 0],
                [int(0.67 * width), int(0.33 * height)],
                [int(0.33 * width), int(0.33 * height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [int(0.67 * width), 0],
                [width, 0],
                [width, int(0.33 * height)],
                [int(0.67 * width), int(0.33 * height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [0, int(0.33 * height)],
                [int(0.33 * width), int(0.33 * height)],
                [int(0.33 * width), int(0.67 * height)],
                [0, int(0.67 * height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [int(0.33 * width), int(0.33 * height)],
                [int(0.67 * width), int(0.33 * height)],
                [int(0.67 * width), int(0.67 * height)],
                [int(0.33 * width), int(0.67 * height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [int(0.67 * width), int(0.33 * height)],
                [int(width), int(0.33 * height)],
                [int(width), int(0.67 * height)],
                [int(0.67 * width), int(0.67 * height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [0, int(0.67 * height)],
                [int(0.33 * width), int(0.67 * height)],
                [int(0.33 * width), int(height)],
                [0, int(height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [int(0.33 * width), int(0.67 * height)],
                [int(0.67 * width), int(0.67 * height)],
                [int(0.67 * width), int(height)],
                [int(0.33 * width), int(height)],
            ],
            dtype=np.int32,
        ),
        np.array(
            [
                [int(0.67 * width), int(0.67 * height)],
                [int(width), int(0.67 * height)],
                [int(width), int(height)],
                [int(0.67 * width), int(height)],
            ],
            dtype=np.int32,
        ),
    ]

    cv2.drawContours(img, contours, -1, sub_color, 2)
    # cv2.imshow("lined", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return contours

