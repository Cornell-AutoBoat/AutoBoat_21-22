"""
This file contains the software for completing the Skeeball Task
"""
from modes.tasks_enum import Task
import SFR
import numpy as np

in_position = False

"""
TODO IMPORTANT: this code assumes that the shooter is run by servos that can simply be written an angle to.
IF ANYONE FINDS OUT OTHERWISE LET CS TEAM KNOW. I will need to make this a control loop.
"""


def FetchObjects():
    objects = np.array([])  # TODO: SUBSTITUTE ARRAY FOR ZED
    return objects


def filter(objects):
    # filter buoys array to contain 2 objects: must be red or green and within a distance threshold

    threshold = 0  # distance of buoys to pay attention to, 120ft?
    # buoys contains only green + red buoys
    buoys = objects[np.where(
        objects.label == "skeeball_frame")]  # TODO: CHANGE FOR CORRECT NAME

    # sort buoys buy z value
    close_buoys = np.sort(buoys[np.where(buoys.oz < threshold)], order='oz')

    # gets nearest 2 buoys
    if (len(close_buoys) == 1):
        return close_buoys[0:1]
    else:
        filter(FetchObjects())


def execute():
    # The boat must deploy and shoot balls through the frame and onto the skeeball table, in any of the three holes

    shoot(getXYZ())  # shoots one ball
    if isComplete():
        SFR.SKEEBALL = True
        SFR.task = Task.DETERMINE_TASK


def getXYZ():
    bouy = filter(FetchObjects())[0]
    return [bouy.ox,bouy.oy,bouy.oz]


def shoot(lst):
    hieght = heightRad(lst[0], lst[1], lst[2])
    orien = orienRad(lst[0], lst[1], lst[2])
    # move hieght servo #TODO: add correct ECE api functions
    # move width servo
    # shoot


def orienRad(x, y, z):  # equations here
    return np.arctan(y/x)  # BASIC NONSENSE CODE


def heightRad(x, y, z):  # equatinos here
    return np.arctan(y/z)  # BASIC NONSENSE CODe


def isComplete():
    # returns a boolean indicating whether the skeeball task is complete
    return True
