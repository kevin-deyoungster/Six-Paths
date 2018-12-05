# title           :follow_path.py
# description     :This will create a header for a python script.
# author          :Nii Quateboye Quartey & Kwamina Essandoh Amoako
# date            :20/10/18

#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import *
from Library import *
from math import *
from time import *

rightMotor = ev3.LargeMotor("outB")
leftMotor = ev3.LargeMotor("outA")
# button = ev3.Button()
lcd = ev3.Screen()
lcd.update()

# Names of cardinal directions corresponding to the integers 0, 1, 2, and 3
directions = [
    "east",
    "south-east",
    "south",
    "south-west",
    "west",
    "north-west",
    "north",
    "north-east",
]

# Computes the direction of pos2 relative to pos1, if pos2 is adjacent to pos1
# pos1 and pos2 are assumed to be tuples in the form (x,y)
# Direction is represented as an integer between 0 (corresponding to east) and
# 3 (corresponding to north)
# Throws an exception if pos2 is not adjacent to pos1

# Empthy wavefront plan
world_map = [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0]]

# Determine the neighbors of a given cell
def DetermineNeighbors(cell):
    X = (len(world_map)) - 1
    Y = (len(world_map[0])) - 1
    (x, y) = cell
    neighbor1 = (x, (y - 1))
    neighbor2 = ((x + 1), y)
    neighbor3 = (x, (y + 1))
    neighbor4 = ((x - 1), y)
    neighbor5 = ((x + 1), (y + 1))
    neighbor6 = ((x + 1), (y - 1))
    neighbor7 = ((x - 1), (y - 1))
    neighbor8 = ((x - 1), (y + 1))
    neighbors = [
        neighbor1,
        neighbor2,
        neighbor3,
        neighbor4,
        neighbor5,
        neighbor6,
        neighbor7,
        neighbor8,
    ]
    Fneighbors = []
    for i in range(len(neighbors)):
        x1 = neighbors[i][0]
        y1 = neighbors[i][1]
        if (
            0 <= x1 <= X
            and 0 <= y1 <= Y
            and world_map[neighbors[i][0]][neighbors[i][1]] != 1
        ):
            Fneighbors.append(neighbors[i])
    return Fneighbors


# Given a completed Wavefront plan, develops a plan from the start cell to the goal cell
def Plan(start, Wavefront, goal):
    curr = start
    value = Wavefront[curr[0]][curr[1]]
    Path = []
    while goal not in Path:
        value = Wavefront[curr[0]][curr[1]]
        nextSet = DetermineNeighbors(curr)
        for i in range(len(nextSet)):
            if Wavefront[nextSet[i][0]][nextSet[i][1]] < value:
                Path.append((nextSet[i][0], nextSet[i][1]))
                curr = (nextSet[i][0], nextSet[i][1])
    return Path


# Developes a completed wavefront plan
def DevWavefront(start, goal, world_map):
    X = (len(world_map)) - 1
    Y = (len(world_map[0])) - 1
    wave = []
    world_map[goal[0]][goal[1]] = 2
    wave.append(goal)
    while len(wave) != 0:
        cell = wave.pop(0)
        neighbors = DetermineNeighbors(cell)
        for item in neighbors:
            x1 = item[0]
            y1 = item[1]
            if 0 <= x1 <= X and 0 <= y1 <= Y:
                if world_map[x1][y1] == 0:
                    val = world_map[cell[0]][cell[1]]
                    world_map[x1][y1] = val + 1
                    wave.append(item)

    return world_map


def relDirection(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    if x2 == x1 and y2 == y1 + 1:
        dir = 0
    elif x2 == x1 + 1 and y2 == y1 + 1:
        dir = 1
    elif x2 == x1 + 1 and y2 == y1:
        dir = 2
    elif x2 == x1 + 1 and y2 == y1 - 1:
        dir = 3
    elif x2 == x1 and y2 == y1 - 1:
        dir = 4
    elif x2 == x1 - 1 and y2 == y1 - 1:
        dir = 5
    elif x2 == x1 - 1 and y2 == y1:
        dir = 6
    elif x2 == x1 - 1 and y2 == y1 + 1:
        dir = 7
    else:
        raise ValueError(
            str(pos1)
            + " and "
            + str(pos2)
            + " are not neighbors,"
            + "so cannot compute relative direction between them."
        )
    return dir


# Assuming the robot starts at startPosition, facing the direction startOrientation,
# This function enables the robot to follow the path (a list of tuples representing
# positions) stored in the parameter path.
def followPath(startPosition, startOrientation, path):
    curPos = startPosition
    curDir = startOrientation

    for i in range(len(path)):
        nextPos = path[i]
        relDir = relDirection(curPos, nextPos)
        print(
            "At pos "
            + str(curPos)
            + " facing direction "
            + str(curDir)
            + " ("
            + directions[curDir]
            + ")"
        )
        print(
            "Next pos is "
            + str(nextPos)
            + ", whose direction relative to the current pos is "
            + str(relDir)
            + " ("
            + directions[relDir]
            + ")"
        )
        print()

        # TO DO: IF NECESSARY, TURN TO FACE IN THE CORRECT DIRECTION
        if curDir != relDir:
            Sangle = 40
            by = curDir - relDir
            # if (by == 3):
            # by = 1
            # if (by == -3):
            # by = -1
            Tangle = abs(Sangle * by)
            if by < 0:
                spinRight(Tangle, 200)
                sleep(2.5)
            else:
                spinLeft(Tangle, 200)
                sleep(2.5)
            curDir = relDir

        # TO DO: MOVE ONE CELL FORWARD INTO THE NEXT POSITION
        if curDir == relDir and curPos != nextPos:
            DriveStraight(51, 230)
            sleep(5)

        # Update the current position and orientation
        curPos = nextPos
        curDir = relDir


# Test the code
if __name__ == "__main__":
    goal = (2, 1)
    startPos = (0, 0)
    StartOrientation = 0
    Wavefront = DevWavefront(startPos, goal, world_map)
    print(Wavefront)
    path1 = Plan(startPos, Wavefront, goal)

    Path = [(0, 1), (1, 1), (2, 2), (2, 3), (3, 4), (3, 3), (3, 2)]

    followPath(startPos, StartOrientation, Path)

