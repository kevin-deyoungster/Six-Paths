#!/usr/bin/env python3
# Names of cardinal directions corresponding to the integers 0, 1, 2, and 3
directions = ['east','south','west','north']

# Computes the direction of pos2 relative to pos1, if pos2 is adjacent to pos1
# pos1 and pos2 are assumed to be tuples in the form (x,y)
# Direction is represented as an integer between 0 (corresponding to east) and
# 3 (corresponding to north)
# Throws an exception if pos2 is not adjacent to pos1

from ev3dev.ev3 import *
from math import *
from planning_map import *

cellLength = 50

rightMotor = LargeMotor('outB')
leftMotor = LargeMotor('outA')
button = Button()

def Straight ():
    raw_distance = cellLength
    motor_speed = 300
    offset = 3.3
    distance = (raw_distance / (2 * pi * offset)) * 360
    rightMotor.run_to_rel_pos(position_sp=distance, speed_sp=motor_speed) 
    leftMotor.run_to_rel_pos(position_sp=distance, speed_sp=motor_speed)
    rightMotor.wait_while('running')
    leftMotor.wait_while('running')
    leftMotor.stop(stop_action="brake") 
    rightMotor.stop(stop_action="brake")

def SpinRight (multiplier):
    angle_deg = 360 * multiplier
    speed = 300
    distance = angle_deg/2 + 11
    rightMotor.run_to_rel_pos(position_sp=-distance, speed_sp=speed)
    leftMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    rightMotor.wait_while('running')
    leftMotor.wait_while('running')
    leftMotor.stop(stop_action="brake") 
    rightMotor.stop(stop_action="brake")

def SpinLeft (multiplier):
    angle_deg = 360 * multiplier
    speed = 300
    distance = angle_deg/2 + 11
    rightMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    leftMotor.run_to_rel_pos(position_sp=-distance, speed_sp=speed)
    rightMotor.wait_while('running')
    leftMotor.wait_while('running')
    leftMotor.stop(stop_action="brake") 
    rightMotor.stop(stop_action="brake")    

# Names of cardinal directions corresponding to the integers 0, 1, 2, and 3
directions = ['east','south','west','north']

# Computes the direction of pos2 relative to pos1, if pos2 is adjacent to pos1
# pos1 and pos2 are assumed to be tuples in the form (x,y)
# Direction is represented as an integer between 0 (corresponding to east) and
# 3 (corresponding to north)
# Throws an exception if pos2 is not adjacent to pos1
def relDirection(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    if x2==x1 and y2==y1+1:
        dir = 0
    elif x2==x1+1 and y2==y1:
        dir = 1
    elif x2==x1 and y2==y1-1:
        dir = 2
    elif x2==x1-1 and y2==y1:
        dir = 3
    else:
        raise ValueError(str(pos1)+" and " + str(pos2) + " are not neighbors,"
                         +"so cannot compute relative direction between them.")
    return dir

# Assuming the robot starts at startPosition, facing the direction startOrientation,
# This function enables the robot to follow the path (a list of tuples representing
# positions) stored in the parameter path.

##The function below is responsible for identifying the neighbors of a particular cell, called CurrentCell
##The function uses the world_map to identify what neighbors are in and out of bounds.
##Additionally, the function deletes neighbor cells which have a 'weight' of 1. i.e obstacle cells.
##

def Neighbor (CurrentCell,world_map):
    Xbound = [ ] #a list for all possible range of x values 
    Ybound = [ ] # a list for all possible range of y values 
    for i in range(len(world_map)):
        Xbound.append(i) 
    for i in range(len(world_map[0])):
        Ybound.append(i)
    N = [0,0,0,0] # a list containing neighbor cells 
    RemovedA = [ ]
    RemovedB = [ ]
    skipA = 0
    skipB = 0
    (x1, y1) = CurrentCell
    N[0] = (x1, y1+1)
    N[1] = (x1+1, y1)
    N[2] = (x1, y1-1)
    N[3] = (x1-1, y1) #the four neighbor cells are populated
    # the following parts remove any neigbor cell that is either out of bounds or that is an obstacle. 
    for i in range(len(N)):
        if N[i][0] not in Xbound or N[i][1] not in Ybound: 
            RemovedA.append(i) #to prevent index error the items to be removed are first identified 
    for i in RemovedA:
        N.pop(i - skipA) # the items can then be popped from the neighor list - N
        skipA = skipA + 1
    for i in range(len(N)):
        if raw_world_map[N[i][0]][N[i][1]] == 1:
            RemovedB.append(i)
    for i in RemovedB:
        N.pop(i - skipB)
        skipB = skipB + 1
    return (N)

## function that implements the wavefront algorithm, given a map with obstacles and a goal state. 
def WaveFrontAlgo (raw_world_map, start, goal):
    high = 2
    (x1, y1) = goal
    raw_world_map[x1][y1] = high # goal state is assigned a value of 2
    Queue = [ ]
    Queue.append(goal) 
    while Queue != [ ]:
        current = Queue.pop(0) 
        Nextset = Neighbor(current, raw_world_map) 
        for i in Nextset:
            if i not in Queue: #for each cell in the map if the value is 0, replace the 0 with 1 plus the current value which is being processed.
                if raw_world_map[i[0]][i[1]] == 0:
                    raw_world_map[i[0]][i[1]] = raw_world_map[current[0]][current[1]] + 1
                    Queue.append(i) 
                    
    for i in range(len(raw_world_map)):
        print(raw_world_map[i])
    print()          
    return raw_world_map 
                         

def WaveExec (world_map, start, goal):
    Alist = [ ]
    current = start
    appended = 0
    while goal not in Alist:
        (v,w) = current
        Curweight = world_map[v][w] #the weight of the current cell is found here. 
        minilist = Neighbor(current, world_map) #a list of the neighbors of the current cell
        for i in minilist: # for any of the neighbor cells, if its weight is one less than the current, we pick that path 
            if world_map[i[0]][i[1]]  ==  Curweight - 1 and appended == 0: #there may be more than one next cell (at least two cells with a value that is one less than the current cell. The appended variable checks that even if there are, only one cell is selected
                current = (i[0],i[1])
                Alist.append(current)
                appended = 1
            else:
                appended = 0
         
    print ("The list of approved coordinates are ", Alist)
    print()
    return (Alist)



def followPath(startPosition, startOrientation, raw_world_map):
    curPos = startPosition
    curDir = startOrientation

    for i in range(len(path)):
        nextPos = path[i]
        relDir = relDirection(curPos, nextPos)
        print("At pos " + str(curPos) + " facing direction " + str(curDir)
              + " (" + directions[curDir] + ")")
        print("Next pos is " + str(nextPos)
              + ", whose direction relative to the current pos is "
              + str(relDir) + " (" + directions[relDir] + ")")
        print()

        diff = relDir - curDir
        if diff < 0:
            if diff == -3:
                diff = 1 #optimization technique that tells the robot to spin 90 degrees in a particular direction instead of 270 in the opposite direction
                SpinRight(abs(diff))
            else:
                SpinLeft(abs(diff))
                
        elif diff > 0:
            if diff == 3:
                diff = 1  #optimization technique that tells the robot to spin 90 degrees in a particular direction instead of 270 in the opposite direction
                SpinLeft(abs(diff))
            else:
                SpinRight(abs(diff))
        else:
            print("Direction is correct As is")
        Straight()
        if curPos == path[-1]:
            break
        # Update the current position and orientation
        curPos = nextPos
        curDir = relDir

         
# Test the code
if __name__ == "__main__":
    # from the planning.py file, four paramters are expected.These are
    
    # testStartPos = (tuple)
    # testStartOrientation  = int
    # testEnd = (tuple)
    # raw_world_map = nested list
    
    world_map = WaveFrontAlgo (raw_world_map, testStartPos, testEnd)
    path = WaveExec(world_map, testStartPos, testEnd)
    followPath(testStartPos, testStartOrientation, path)
  
          
