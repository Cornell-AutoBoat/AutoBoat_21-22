"""
This file contains the software for completing the Mandatory Navigation Channel Task.
"""
from modes.tasks_enum import Task
import SFR
import numpy as np

objects = np.array([])  # array of buoy objects from object_detection


def pivot():
    # if less than 2 valid buoys in sight at beginning of task, pivot until 2 are seen

    # stop motors
    while(len(filter(objects) < 2)):
        # pivot in 1 circle
        pass
    if (len(filter(objects) < 2)):
        return 0
    return 1


def filter(objects):
    # filter buoys array to contain 2 objects: must be red or green and within a distance threshold

    threshold = 0  # distance of buoys to pay attention to, 120ft?
    buoys = objects[np.where(
        objects.label == "green buoy" or objects.label == "red buoy")]
    close_buoys = np.sort(buoys[np.where(objects.oz < threshold)], order='oz')
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

    if (pivot(objects) == 0):
        finish()

    while (not isComplete()):

        buoys = filter(objects)
        if (buoys[0].ox < 0):
            x1 = np.abs(buoys[0].ox)    # left (red) buoy
            x2 = np.abs(buoys[1].ox)    # right (green) buoy
        else:
            x1 = np.abs(buoys[1].ox)    # left (red) buoy
            x2 = np.abs(buoys[0].ox)    # right (green) buoy

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
    finish()


def finish():
    # mark task as complete

    # move forward for x seconds
    SFR.MNC = True
    SFR.task = Task.DETERMINE_TASK


def isComplete():
    # returns a boolean indicating whether the mandatory navigation channel task is complete
    # complete when less than 2 "valid" buoys in sight

    return len(filter(objects)) < 2
