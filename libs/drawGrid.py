import cv2
import imutils
import numpy as np


def _get_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts


def _get_grid_cell_contours(image, parts=3):
    height = img.shape[0]
    width = img.shape[1]
    return [
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


def get_location_of_point_in_grid(point, grid_cells_contours):
    location = None
    for index, cell in enumerate(grid_cells_contours):
        inside = cv2.pointPolygonTest(cell, point, False) == 1.0
        if inside:
            location = index + 1
            break
        # else:
        #     print(f"Object is NOT in cell {index+1}")
    return location


def get_locations(obj_label,img, object_cnts, grid_cell_cnts):
    already_done = []
    locations = []
    for cnt in object_cnts:
        # Get center point of contour
        M = cv2.moments(cnt)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        center_point = (cx, cy)

        if center_point not in already_done:
            cell_location = get_location_of_point_in_grid(center_point, grid_cell_cnts)
            if cell_location:
                already_done.append(center_point)
                locations.append(location_dict[cell_location])
    
    return locations

location_dict = {
    1: (0, 0),
    2: (1, 0),
    3: (2, 0),
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    7: (0, 2),
    8: (1, 2),
    9: (2, 2),
}

# Main Entry of Code
images = [f"grid_images/blob_cell{i+1}.png" for i in range(10)]

for img in images:
    img = cv2.imread(img)
    object_contours = _get_contours(img)
    grid_cell_contours = _get_grid_cell_contours(img)
    locations = get_locations("blob",img, object_contours, grid_cell_contours)
    print(f"blob is in cell locations {locations}")

# seen_boundings = []
# for img in images:

#     # Get contours of Objects in the Image
#     img = cv2.imread(img)
#     object_contours = _get_contours(img)
#     cv2.drawContours(img, object_contours, -1, (0, 0, 255), 2)

#     center_point = None
#     for contour in object_contours:
#         bounding_box = cv2.boundingRect(contour)
#         x, y, w, h = bounding_box
#         if bounding_box not in seen_boundings:
#             seen_boundings.append(bounding_box)
#             M = cv2.moments(contour)
#             cx = int(M["m10"] / M["m00"])
#             cy = int(M["m01"] / M["m00"])
#             center_point = (cx, cy)
#             cv2.circle(img, center_point, 10, (0, 0, 255), -1)

#             cv2.drawContours(img, contour, -1, (0, 0, 255), 2)
#             cell_contours = draw_grid(img)

#             for index, cell in enumerate(cell_contours):

#                 inside = cv2.pointPolygonTest(cell, center_point, False) == 1.0
#                 if inside:
#                     print(f"Object is in cell {index+1}")
#                     # cv2.imshow("Before", img)
#                     # cv2.fillPoly(img, pts=[cell], color=(255, 255, 255))
#                     # print(center_point)
#                     # print(cell)
#                     cv2.imshow("lined", img)

#                     break
#                 # else:
#                 #     print(f"Object is NOT in cell {index+1}")

#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
