#!/usr/bin/env python3

import CoDrone
from threading import Thread
from camera.cam import *
from time import *

drone = CoDrone.CoDrone()
drone.pair(drone.Nearest)

in_flight = True
done_hovering = False
waiting_for_pick = True


def flight():
    global done_hovering
    drone.takeoff()
    if drone.is_flying():
        drone.hover(10)
        print("In the air")
        done_hovering = True
        drone.land()


def snap_me():
    global done_hovering
    global waiting_for_pick

    while True and waiting_for_pick == True:
        if done_hovering:
            cc = Capture()
            cc.capture_image()
            print("image is taken")
            waiting_for_pick = False
        else:
            print("Still Flying!")


def start():
    t1 = Thread(target=flight)
    t1.start()

    t2 = Thread(target=snap_me)
    t2.start()


start()
