"""
This file contains the software for completing the Avoid The Crowd Task
"""
from modes.tasks_enum import Task
import SFR

def execute():
    # The boat will find/outline a path through the obstacle red, yellow, and green buoy
    # The boat will alway stay in between the green and red buoy
    # The yellow buoy will always be between a red and green buoy
    # The boat will choose the closest, easiest path to pass through two different colored buoy
    # Follow path using PID control

    if isComplete():
        SFR.AVOID_THE_CROWD = True
        SFR.task = Task.DETERMINE_TASK

def configurationOne():
    # The only buoy directly infront of it is a green and red
    # choose the midpoint between the two buoy 
    # make the boat go throug hthat midpoint 
    pass
def configurationTwo(): 
    # There is a yellow buoy, green buoy, and red buoy directly in front of it 
    # The yellow buoy must be relatively close to the green and red in terms of z distances
    # find the midpt between the green and yellow and red and yellow
    # prioritize based on how easy it will be to pass and then the distance to each
    pass
def configurationThree():
    # there is yellow buoy, green buoy, and red buoy directly in front of it 
    # the yellow buoy is beyond the threshold of the z distance allocated for configuration 2
    # therefore, the boat will fix the midpoint distance between the red and green buoy
    # if it sees the yellow buoy in front of it such that it will crash into it
    # the room for error for the buoy being in front is another buoy (at the very least) to ensure no collisions occur
    # the boat will make a fixed semicircle (pick side with the most leeway) around the yellow buoy
     pass




def isComplete():
    #returns a boolean indicating whether the avoid the crowds task is complete
    pass
