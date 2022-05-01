"""
This file contains the software for completing the Skeeball Task
"""
from modes.tasks_enum import Task
import SFR
import numpy as np

in_position = False

"""
IMPORTANT: this code assumes that the shooter is run by servos that can simply be written an angle to.
IF ANYONE FINDS OUT OTHERWISE LET CS TEAM KNOW. I will need to make this a control loop.
"""


def execute():
    # The boat must deploy and shoot balls through the frame and onto the skeeball table, in any of the three holes
    
    shoot(getXYZ()) #shoots one ball
    if isComplete():
        SFR.SKEEBALL = True
        SFR.task = Task.DETERMINE_TASK

def getXYZ():
    return[0,0,0]


def shoot(lst):
    hieght = heightRad(lst[0],lst[1],lst[2])
    orien = orienRad(lst[0],lst[1],lst[2])
    #move hieght servo
    #move width servo
    #shoot


def orienRad(x,y,z): #equations here
    return np.arctan(y/x) #BASIC NONSENSE CODE

def heightRad(x,y,z): #equatinos here
    return np.arctan(y/z) #BASIC NONSENSE CODe


def isComplete():
    # returns a boolean indicating whether the skeeball task is complete
    return True
