"""
This file contains the software for completing the Mandatory Navigation Channel Task.
"""
from modes.tasks_enum import Task
import SFR
import numpy as np

objects = np.array([])  # array of buoy objects from object_detection


def filter(objects):
    threshold = 0  # distance of buoys to pay attention to, 120ft?
    buoys = objects[np.where(
        objects.string == "green buoy" or objects.string == "red buoy")]
    close_buoys = np.sort(buoys[np.where(objects.z < threshold)], order='oz')
    if (len(close_buoys) > 2):      # gets nearest 2 buoys, objects is sorted by z value
        return close_buoys[:2]
    return close_buoys


def execute():
    # Determine goal position
    # Outline path to take
    # Follow path using PID control

    # filter buoys by proximity and type (z coordinate)
    # move forward to keep x vectors of all buoys within threshold
    # move until no buoys in sight (+ x sec)

    while (not isComplete()):

        buoys = filter(objects)
        if (buoys[0].ox < 0):
            x1 = np.abs(buoys[0].ox)    # left buoy
            x2 = np.abs(buoys[1].ox)    # right buoy
        else:
            x1 = np.abs(buoys[1].ox)    # left buoy
            x2 = np.abs(buoys[0].ox)    # right buoy

        threshold = 0
        if (np.abs(x1 - x2) < threshold):
            # move forward (both motors at = force)
            pass
        elif (x1 > x2):
            # adjust by running right motor
            pass
        else:
            # adjust by running left motor
            pass

    # move forward for x seconds

    SFR.MNC = True
    SFR.task = Task.DETERMINE_TASK


def isComplete():
    # returns a boolean indicating whether the mandatory navigation channel task is complete
    # complete when less than 2 "valid" buoys in sight
    return len(filter(objects)) < 2
