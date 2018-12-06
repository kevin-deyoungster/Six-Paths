import numpy as np
import imutils
import cv2

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


g = generate_sparse_grid()
set_grid_values([(1, 1), (0, 0), (2, 2)], 2, g)
print(g)

