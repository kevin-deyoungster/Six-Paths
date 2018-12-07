from pathlib import Path
import cv2
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


def getGrid(image_file):

    empty_world = grid_utils.generate_sparse_grid()
    original_image = cv2.imread(image_file)

    image = original_image.copy()

    # Perform Edge Detection (using Canny-Edge)
    edged_image = cv_utils.get_edges(image)

    # Get Largest Quadrilateral Contour (the field)
    # quadCnt, found = cv_utils.get_quadrilateral_contour(edged_image)

    quadCnt = cv_utils.get_quadrilateral_contour2(edged_image)

    if np.all(quadCnt):
        # Draw contour of the identified quadrilateral
        cv2.drawContours(image, [quadCnt], -1, (0, 255, 0), 2)
        # cv2.imshow(f"Boundary Identified - {image_file}", image)

        # Perform Perspective Transform to create top-down-view
        top_down_image = four_point_transform(original_image, quadCnt.reshape(4, 2))
        # cv2.imshow("Perspective Transform", top_down_image)

        # We'll be working with the top-down view henceforth, make that the main image
        image = top_down_image

        # Extract the colored objects (Start and Goal Positions)
        color_contoured_image = image.copy()
        red_contour = cv_utils.get_color_contour(image, RED_LOWER, RED_UPPER)
        blue_contour = cv_utils.get_color_contour(image, BLUE_LOWER, BLUE_UPPER)
        black_contour = cv_utils.get_color_contour(image, BLACK_LOWER, BLACK_UPPER)

        grid_cell_cnts = cv_utils.draw_grid(
            color_contoured_image, 3, (255, 255, 255), (255, 255, 255)
        )

        start_location = grid_utils.get_locations(image, blue_contour, grid_cell_cnts)
        goal_location = grid_utils.get_locations(image, red_contour, grid_cell_cnts)
        obstacles_locations = grid_utils.get_locations(
            image, black_contour, grid_cell_cnts
        )

        # grid_utils.set_grid_values(start_location, 100, empty_world)
        # grid_utils.set_grid_values(goal_location, 2, empty_world)
        grid_utils.set_grid_values(obstacles_locations, 1, empty_world)

        print(f"Goal is in location {goal_location}")
        print(f"Start is in location {start_location}")
        print(
            f"{len(obstacles_locations)} Obstacles are in locations {obstacles_locations}"
        )

        cv2.drawContours(color_contoured_image, red_contour, -1, (0, 0, 255), 2)
        cv2.drawContours(color_contoured_image, blue_contour, -1, (255, 0, 0), 2)
        cv2.drawContours(color_contoured_image, black_contour, -1, (0, 255, 0), 2)

        cv2.imshow("Recognized Colors", color_contoured_image)

        # cv2.imshow("Original Image", original_image)
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
