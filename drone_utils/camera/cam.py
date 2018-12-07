#!/usr/bin/env python3

"""
@author nknab
@version 1.0
@date 26/06/2018
@description This class is to capture images or videos using the camera
"""

"""
Various imports needed by the class
"""
import numpy as np
import cv2
import datetime
import os
from time import sleep


class Capture:
    """
    Declaring and instantiating a global object of my camera
    """
    camera = cv2.VideoCapture('rtsp://192.168.100.1/cam1/mpeg4')
    #camera = cv2.VideoCapture(0)

    """
    This method is responsible for streaming a video from the drone
    """
    def stream(self):
        while self.camera.isOpened():
            ret, frame = self.camera.read()
            cv2.imshow('AIX 2018', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.stop()

    # camera = cv2.VideoCapture('rtsp://192.168.100.1/cam1/mpeg4')

    """
    This method is responsible for detecting a color from the camera.
    """
    def color(self):
        while self.camera.isOpened():
            ret, frame = self.camera.read()
            cv2.imshow('AIX 2018', frame)

            # ----------------------------------------------------------------------
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_values = np.array([160, 120, 120])
            upper_values = np.array([180, 255, 255])

            mask_frame = cv2.inRange(hsv_frame, lower_values, upper_values)

            color_cutout = cv2.bitwise_and(frame, frame, mask=mask_frame)

            cv2.imshow('Color Cutout', color_cutout)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.stop()

    """
    This method is responsible for recording a video from the drone.
    
    :arg
        departure (String): This gets the current location of the drone.
        arrival (String): This gets the final location of the drone.
    """
    def record(self, departure, arrival):
        height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        time = datetime.datetime.now().strftime('%I.%M.%S %p')
        date = datetime.datetime.now().strftime('%a, %d %b %Y')

        file_path = "videos/" + str(departure) + " To " + str(arrival) + "/" + date + "/" + time + ".avi"
        root_file = "videos/" + str(departure) + " To " + str(arrival) + "/" + date
        if not os.path.exists(root_file):
            os.makedirs(root_file)

        out = cv2.VideoWriter(file_path, fourcc, 12.0, (int(width), int(height)))

        while self.camera.isOpened():
            ret, frame = self.camera.read()
            out.write(frame)
            cv2.imshow('AIX 2018', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.stop()

    """
    This method is responsible for stopping the drone camera.
    """
    def stop(self):
        self.camera.release()
        cv2.destroyAllWindows()

    """
    This method is responsible for taking a picture from the drone.

    :arg
        position (String): This gets the current position of the camera
    """
    def capture_image(self):
        time = datetime.datetime.now().strftime('%I.%M.%S %p')
        date = datetime.datetime.now().strftime('%a, %d %b %Y')

        file_path = "images/" + time + ".jpg"
        root_file = "images/"

        if not os.path.exists(root_file):
            os.makedirs(root_file)

        a = 0
        while a != 2:
            ret, frame = self.camera.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            cv2.imshow('frame', rgb)
            sleep(1)
            cv2.imwrite(file_path, frame)
            a += 1
        self.camera.release()
        cv2.destroyAllWindows()
