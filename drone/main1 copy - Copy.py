#!/usr/bin/env python3

from threading import Thread
import CoDrone
from time import *
from camera.cam import *

drone = CoDrone.CoDrone()
drone.pair(drone.Nearest)

def flight_test(height):
    drone.takeoff()
    print("i am in the air")
    drone.go_to_height(height)
    watch()
    drone.land()

def watch():
    cc = Capture()
    cc.capture_image()
    print("Image is taken")

flight_test(700)

