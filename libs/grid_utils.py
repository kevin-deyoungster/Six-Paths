import os
import stat
import numpy as np
import cv2
from libs import cv_utils


def create_new_grid(row,col):
    return np.zeros([row,col])
       
def set_grid_values(locations, value, grid):
    for location in locations:
        grid[location[0]][location[1]] = value

def write_world_map_to_file(startPos, endPos, worldMap):
    text = f"#!/usr/bin/env python3\ntestStartPos={startPos}\ntestStartOrientation=3\ntestEnd={endPos}\nraw_world_map={worldMap.astype(int).tolist()}"
    with open("planning_map.py", "w") as f:
        f.write(text)
    st = os.stat("planning_map.py")
    os.chmod("planning_map.py", st.st_mode | stat.S_IEXEC)

def get_lines(row_size, column_size, image):
    return _get_lines(row_size, column_size, image.shape[1], image.shape[0])


def _get_lines(row_size, column_size, width, height):
    step_w = int(width / row_size)
    step_h = int(height / column_size)
    vertical_lines = []
    horizontal_lines = []

    vertical_marker = (0, 0)
    horizontal_marker = (0, 0)

    for i in range(row_size - 1):
        top_marker = (vertical_marker[0], vertical_marker[1] + step_w)
        bottom_marker = (height, top_marker[1])
        # print(f"Vertical Line from {top_marker} to {bottom_marker}")
        vertical_marker = top_marker
        vertical_lines.append((top_marker, bottom_marker))

    for i in range(column_size - 1):
        left_marker = (horizontal_marker[0] + step_h, horizontal_marker[1])
        right_marker = (left_marker[0], width)
        # print(f"Horizontal Line from {left_marker} to {right_marker}")
        horizontal_marker = left_marker
        horizontal_lines.append((left_marker, right_marker))

    return vertical_lines, horizontal_lines


def draw_lines(image, lines):
    for line in lines:
        line_coordinates = np.flip(line)
        cv2.line(
            image,
            tuple(line_coordinates[0]),
            tuple(line_coordinates[1]),
            (0, 255, 0),
            1,
            1,
        )


def draw_grid(image, horizontal, vertical):
    draw_lines(image, horizontal)
    draw_lines(image, vertical)


def get_cell_contours_and_coords(row_size, column_size, image):
    return _get_cells(row_size, column_size, image.shape[1], image.shape[0])


def _get_cells(row_size, column_size, width, height):
    step_w = int(width / row_size)
    step_h = int(height / column_size)

    cells_corner_points = []
    cell_coordinates = []

    marker = (0, 0)
    for i in range(row_size):
        botttom_left = None
        for j in range(column_size):
            # print(i, j)
            cell_top_left = marker
            cell_top_right = (cell_top_left[0], cell_top_left[1] + step_w)
            cell_bottom_right = (cell_top_left[0] + step_h, cell_top_left[1] + step_w)
            cell_bottom_left = (cell_top_left[0] + step_h, cell_top_left[1])

            # Set bottom left to bottom left of the first cell
            botttom_left = cell_bottom_left if botttom_left is None else botttom_left
            # print(
            #     f"Cell {i}-{j}: {[cell_top_left, cell_top_right, cell_bottom_right, cell_bottom_left]}"
            # )
            if j == column_size - 1:
                # At the end of the row, move top left marker down far left
                marker = botttom_left
            else:
                # Move the marker to the right
                marker = cell_top_right

            cells_corner_points.append(
                np.array(
                    [cell_top_left, cell_top_right, cell_bottom_right, cell_bottom_left]
                )
            )
            cell_coordinates.append((i, j))
    return cells_corner_points, cell_coordinates


def get_locations(image, object_contours, grid_cells, grid_cell_coords):
    grid_cells = grid_cells.copy()
    grid_cell_coords = grid_cell_coords.copy()
    coords = []
    already_seen_center_points = []
    for contour in object_contours:
        found_grid_cell_index = None
        center_point = cv_utils.get_center_point_of_contour(contour)
        if center_point not in already_seen_center_points:
            for index, grid_cell in enumerate(grid_cells):
                if cv_utils.is_point_in_contour(center_point, grid_cell):
                    coords.append(grid_cell_coords[index])
                    found_grid_cell_index = index
                    break
        if found_grid_cell_index:
            del grid_cells[found_grid_cell_index]
            del grid_cell_coords[found_grid_cell_index]
        already_seen_center_points.append(center_point)
    return coords if coords else None


# image = cv2.imread("IMG-8897.JPG")
# v_lines, h_lines = get_lines(3, 3, image.shape[1], image.shape[0])

# grid_cells, coords = get_cells(3, 3, image.shape[1], image.shape[0])
# print(coords)

# draw_grid(image, h_lines, v_lines)

# cv2.imshow("Something", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
