import os
import stat
import numpy as np
from math import floor
import cv2
from lib import cv_utils


def create_new_grid(row, col):
    return np.zeros([row, col])


def set_grid_values(locations, value, grid):
    for location in locations:
        grid[location[0]][location[1]] = value


def get_lines(row_size, column_size, image):
    """
    Returns coordinates of vertical and horizontal grid lines for [image] using row_size
    """
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
    """
    Draws [lines] over image
    """
    for line in lines:
        line_coordinates = np.flip(line)
        cv2.line(
            image,
            tuple(line_coordinates[0]),
            tuple(line_coordinates[1]),
            (255, 255, 255),
            2,
            2,
        )


def draw_grid(image, horizontal, vertical):
    draw_lines(image, horizontal)
    draw_lines(image, vertical)


def get_position(coords, row_size, column_size, grid_height, grid_width):
    height_step = grid_height / row_size
    width_step = grid_width / column_size
    max_x = (grid_height / height_step) - 1
    max_y = (grid_width / width_step) - 1
    return (
        int(min(floor(coords[0] / height_step), max_x)),
        int(min(floor(coords[1] / width_step), max_y)),
    )


def get_locations(image, object_contours):
    """
    Returns list of coordinates of all objects in [object_contours]
    """
    coords = []
    seen = []
    for contour in object_contours:
        center_point = cv_utils.get_center_point_of_contour(contour)
        if center_point not in seen:
            position = get_position(center_point, 3, 3, image.shape[0], image.shape[1])
            coords.append(position)
            seen.append(center_point)
    return coords


def write_world_map_to_file(startPos, endPos, worldMap):
    text = f"#!/usr/bin/env python3\ntestStartPos={startPos}\ntestStartOrientation=3\ntestEnd={endPos}\nraw_world_map={worldMap.astype(int).tolist()}"
    with open("planning_map.py", "w") as f:
        f.write(text)
    st = os.stat("planning_map.py")
    os.chmod("planning_map.py", st.st_mode | stat.S_IEXEC)


###  Deprecated (Location Method 1)


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
            cell_top_left = marker
            cell_top_right = (cell_top_left[0], cell_top_left[1] + step_w)
            cell_bottom_right = (cell_top_left[0] + step_h, cell_top_left[1] + step_w)
            cell_bottom_left = (cell_top_left[0] + step_h, cell_top_left[1])

            # Set bottom left to bottom left of the first cell
            botttom_left = cell_bottom_left if botttom_left is None else botttom_left

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


def get_locations_old(image, object_contours, grid_cells, grid_cell_coords):
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
