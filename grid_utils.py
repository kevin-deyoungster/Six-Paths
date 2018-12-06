import imutils
import cv2
import os
import stat
import numpy as np

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


def get_locations(img, object_cnts, grid_cell_cnts):
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


def generate_sparse_grid():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def set_grid_values(locations, value, grid):
    for location in locations:
        grid[location[1]][location[0]] = value


def write_world_map_to_file(startPos, endPos, worldMap):
    text = f"#!/usr/bin/env python3\ntestStartPos={startPos}\ntestStartOrientation=3\ntestEnd={endPos}\nrow_world_map={worldMap}"
    with open("planning_map.py", "w") as f:
        f.write(text)
    st = os.stat("planning_map.py")
    os.chmod("planning_map.py", st.st_mode | stat.S_IEXEC)


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


def drawPath(points, img, block_size):
    grid_cell_cnts = draw_grid(img, 3, (255, 255, 255), (255, 255, 255))
    width_block = img.shape[1]
    height_block = img.shape[0]

    w_unit = int(width_block / block_size)
    h_unit = int(height_block / block_size)

    first = points[0]
    start = (int((first[0] + 1) * w_unit / 2), int(((first[1] + 1) * h_unit) / 2))
    end = None

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for index, point in enumerate(points[1:]):
        end = (int((point[0] + 1) * w_unit / 2), int((point[1] + 1) * h_unit / 2) * 2)
        print(start, "to", end)
        # end = point
        cv2.line(img, start, end, colors[index], 2, 1)

        start = end
    # cv2.line(img, (0, 0), (160, 106), (255, 0, 0), 2, 1)
    # cv2.line(img, (160, 106), (320, 107), (0, 255, 0), 2, 1)
    # cv2.line(img, (320, 107), (480, 108), (0, 0, 255), 2, 1)

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


drawPath([(0, 0), (0, 1), (2, 2)], cv2.imread("image2.JPG"), 3)
# g = generate_sparse_grid()
# set_grid_values([(1, 1), (0, 0), (2, 2)], 2, g)
# print(g)

