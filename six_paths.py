from pathlib import Path
import cv2
import imutils

import numpy as np

from libs import cv_utils
from libs import grid_utils
from libs.p_transform import four_point_transform

BLUE_LOWER = [102, 120, -15]
BLUE_UPPER = [128, 204, 121]

RED_LOWER = [145, 25, -5]
RED_UPPER = [177, 233, 170]

BLACK_LOWER = [-10, -10, -30]
BLACK_UPPER = [100, 255, 63]

COLOR_GREEN = (0, 255, 0)
COLOR_BLUE =  (255, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255,255,255)

def getGrid(image_file):

    empty_world = grid_utils.generate_sparse_grid()
    
    original_image = cv2.imread(image_file)
    image = original_image.copy()

    # Perform Edge Detection (using Canny-Edge)
    edged_image = cv_utils.get_edges(image)
    cv2.imshow("Identified Edges", edged_image)

    # Get Largest Quadrilateral Contour (the field)
    quad_contour = cv_utils.get_quadrilateral_contour(edged_image)

    if np.all(quad_contour):

        # Draw contour of the identified quadrilateral
        cv2.drawContours(image, [quad_contour], -1, COLOR_GREEN, 2)
        cv2.imshow("Identified Field", image)

        # Perform Perspective Transform to create top-down-view
        top_down_image = four_point_transform(image, quad_contour.reshape(4, 2))
        top_down_image = imutils.resize(top_down_image, width=image.shape[1], height=image.shape[0])
        cv2.imshow("Top-Down View", top_down_image)

        # Top Down Image is now the current working image
        image = top_down_image

        # Extract the colored objects (Start & Goal Positions, Obstacles)
        red_contour = cv_utils.get_contours_of_color(image, RED_LOWER, RED_UPPER)
        blue_contour = cv_utils.get_contours_of_color(image, BLUE_LOWER, BLUE_UPPER)
        black_contour = cv_utils.get_contours_of_color(image, BLACK_LOWER, BLACK_UPPER)

        # Get contours of grid cells
        grid_cell_cnts = cv_utils.draw_grid(image, 3, COLOR_WHITE, COLOR_WHITE)

        start = grid_utils.get_locations(image, blue_contour, grid_cell_cnts)[0] if len(blue_contour) > 0 else None
        goal = grid_utils.get_locations(image, red_contour, grid_cell_cnts)[0] if len(red_contour) > 0 else None
        obstacles = grid_utils.get_locations(
            image, black_contour, grid_cell_cnts
        ) if len(black_contour) > 0 else None

        grid_utils.set_grid_values(obstacles, 1, empty_world)

        print(f"Goal is in {goal}")
        print(f"Start is in {start}")
        print(
            f"{len(obstacles)} Obstacles are in {obstacles}"
        )

        cv2.drawContours(image, red_contour, -1, COLOR_RED, 2)
        cv2.drawContours(image, blue_contour, -1,  COLOR_BLUE, 2)
        cv2.drawContours(image, black_contour, -1, COLOR_GREEN, 2)

        cv2.imshow("Recognized Colors", image)

        cv2.imshow(f"Original Image - {image_file}", original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return empty_world, start_location, goal_location
    else:
        print("Did not find any 4 sided contour")
        return None

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# pathlist = ["images/file1-3.jpeg"]
pathlist = Path("images").glob("**/*.JPG")
for path in pathlist:
    # try:
    stuff = getGrid(str(path))

    if stuff != None:
        world_map, start, goal = stuff
        if len(start) > 0:
            print(world_map, f"Start: {start}", f"Goal: {goal}")

            grid_utils.write_world_map_to_file(
                tuple(np.flip(start[0])), tuple(np.flip(goal[0])), world_map
            )
    # except:
    # print("Oops something bad happened")
