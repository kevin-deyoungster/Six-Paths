"""
Project Six-Paths
Robotics 2018 / 2019
Kevin de Youngster + Kofi Anamoa + Kwamina Amoako + David Duamekpor
"""

from pathlib import Path
import cv2
import numpy as np
from libs import grid_utils
from libs import cv_utils
from libs.p_transform import four_point_transform

BLUE_LOWER = [102, 120, -15]
BLUE_UPPER = [128, 204, 121]

RED_LOWER = [145, 25, -5]
RED_UPPER = [177, 233, 170]

BLACK_LOWER = [-10, -10, -21]
BLACK_UPPER = [100, 255, 63]

COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)


def get_grid(image_file):
    """
    Takes image and returns 2d array representing grid, start and goal positions
    """

    empty_world = grid_utils.create_new_grid(3, 3)

    original_image = cv2.imread(image_file)
    image = original_image.copy()

    # Perform Edge Detection (using Canny-Edge)
    edged_image = cv_utils.get_edges(image)
    # cv2.imshow("Identified Edges", edged_image)

    # Get Largest Quadrilateral Contour (the field)
    quad_contour = cv_utils.get_quadrilateral_contour(edged_image)

    if not np.all(quad_contour):
        print("No Quadrilateral Contour Found")
        return None, None, None

    # Draw contour of the identified quadrilateral
    cv2.drawContours(image, [quad_contour], -1, COLOR_GREEN, 2)
    # cv2.imshow("Identified Field", image)

    # Perform Perspective Transform to create top-down-view
    top_down_image = four_point_transform(image, quad_contour.reshape(4, 2))
    # cv2.imshow("Top-Down View", top_down_image)

    # Top Down Image is now the current working image
    image = top_down_image

    # Extract the colored objects (Start & Goal Positions, Obstacles)
    red_contour = cv_utils.get_contours_of_color(image, RED_LOWER, RED_UPPER)
    blue_contour = cv_utils.get_contours_of_color(image, BLUE_LOWER, BLUE_UPPER)
    black_contour = cv_utils.get_contours_of_color(image, BLACK_LOWER, BLACK_UPPER)

    # Get contours of grid cells
    v_lines, h_lines = grid_utils.get_lines(3, 3, image)
    grid_cells_cnts, grid_cell_coords = grid_utils.get_cell_contours_and_coords(
        3, 3, image
    )
    grid_utils.draw_grid(image, h_lines, v_lines)

    start_location = (
        grid_utils.get_locations(
            image, blue_contour, grid_cells_cnts, grid_cell_coords
        )[0]
        if blue_contour
        else None
    )
    goal_location = (
        grid_utils.get_locations(image, red_contour, grid_cells_cnts, grid_cell_coords)[
            0
        ]
        if red_contour
        else None
    )
    obstacles = (
        grid_utils.get_locations(
            image, black_contour, grid_cells_cnts, grid_cell_coords
        )
        if black_contour
        else None
    )

    print(f"Goal is in {goal_location}")
    print(f"Start is in {start_location}")
    if obstacles:
        print(f"{len(obstacles)} Obstacles are in {obstacles}")
        grid_utils.set_grid_values(obstacles, 1, empty_world)

    cv2.drawContours(image, red_contour, -1, COLOR_RED, 2)
    cv2.drawContours(image, blue_contour, -1, COLOR_BLUE, 2)
    cv2.drawContours(image, black_contour, -1, COLOR_GREEN, 2)

    cv2.imshow("Grid with Recognized Colors", image)
    cv2.imshow(f"Original Image - {image_file}", original_image)
    print(empty_world)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return empty_world, start_location, goal_location


IMAGES = Path("images").glob("**/*.JPG")
# IMAGES = ["images/IMG_3957.JPG"]
for test_image in IMAGES:

    world_map, start, goal = get_grid(str(test_image))

    if all([start, goal]):
        grid_utils.write_world_map_to_file(
            tuple(np.flip(start)), tuple(np.flip(goal)), world_map
        )
    else:
        print(f"Could not find start position {start} or end position {goal}")
