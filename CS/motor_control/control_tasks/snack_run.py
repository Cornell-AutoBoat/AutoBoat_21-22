"""
This file contains the software for completing the Snack Run Task
"""
from modes.tasks_enum import Task
import SFR
import numpy as np

# Local values
# When the target buoy is no longer in range, we want the boat to continue moving for a 
# set amount of time
time=0 

# Expected distance when buoy disappears
ExpectedDistance=0

# The state that the boat is at 
state=1

object_list = [] #will be given to us
important_objects = [] #the objects we care about

# how long to fire motors for when it passes state 1 
expectedTime=0

#find the target value X position (+- room for error)

#object states for blue, red, and green buoys
#these object states will have position vectors (x and z matter), and classes types
#they will be set in filter buoys
#all relative positions
blue_buoy = [0,0] 
red_buoy = [0,0]
green_buoy = [0, 0]

#farthest distance is the relative distance of the farthest buoy we care about (this should be the target Z value)
farthestDistance = 0

#constant for how big the task is (in ft)
TASK_SCOPE = 106 
RADIUS_OF_MOTION = 10

# Expect X position of the blue buoy relative to boat (should be negative since boat is traveling to the right)
Expected_BLUEX_position=0
# amount of error for blue buoy
Bbuoy_error=0
# amount of error for red and green buoy
buoy_error=0
# amount of time we should travel in a circle
circleTime=0


def execute():
    # Locates the blue buoy 
    # Outline path to take to the blue buoy circle around it and the return back to it's starting position
    # Follow path using PID control

    # Filter buoys with a z coordinate greater than 
    #  find the farthest buoy at start of task and then use relative distances
    #we're given a list of the objects

    #use extract buoys method
    filter_buoys()
    state_move_in_circle()
    state_move_back()
    state_move_back()
    state_isComplete()


def state_move_towards():
    # Will be considered state 1
    #we want to keep blue buoy to the left of us 
    #decrement the distance by how much the boat has moved 
    #basic idea: if a straight path, call both motors equally
    #if not take ratio of x/z
    #take in position of blue buoy
    if (state==1):
        # checks if the boat is lost or has finished the task
        if (blue_buoy[0]=0):
            buoy_disappear()

        elif (blue_buoy[0]<Expected_BLUEX_position+Bbuoy_error or blue_buoy[0]>Expected_BLUEX_position-Bbuoy_error):
            # fire both motors equally 
        elif (blue_buoy[0]>Expected_BLUEX_position-Bbuoy_error):
            # too far to the left of the Expected buoy X; fire boat to move to the right
        elif (blue_buoy[0]<Expected_BLUEX_position+Bbuoy_error):
            # too far to the right of the Expected buoy X;fire boat to move to the left 


def state_move_in_circle():
    # we plan to have a predefined radius and distance that the boat should travel in 
    # so that it can make a loop around the blue buoy
    # when completed the half circle
    if (state==2):
        # determine the radius of the path 
        # make the boat move in a predetermined circular path
        # when the red and green buoys are in sight (without the blue) make the boat move in a straight line towards them
        # for a period of time  
        while(time<circleTime):
            time=time+1
            # fire motors to turn left 
            # right motor > left motor 
        time=0
        state=state+1
        # check if it is at the expected distance from the buoys such that it should disappear
        # if the distance is not accpetable then execute that it is lost
        # if completed predetermined path and moves straight line for a period of time, change state to 3

    
def state_move_back():
        # Make the boat move towards the red and green buoy. Aiming for the center between the two buoy
        # Try to make the |x| position to the red buoy and the |x| position to the green buoy is the same 
    if (state==3):
        # checks if the boat is lost or has finished the task
        if (green_buoy[0]=0 and red_buoy[0]=0):
            buoy_disappear()
        elif (np.abs(green_buoy[0])+buoy_error>=np.abs(red_buoy[0]) or np.abs(green_buoy[0])-buoy_error<=np.abs(red_buoy[0])):
            # fire both motors equally, boat is moving towards the center
        elif (np.abs(green_buoy[0])-np.abs(red_buoy[0])>buoy_error):
            # too far to the left of the center fire boat to move to the right
        elif (np.abs(green_buoy[0])-np.abs(red_buoy[0])<buoy_error):
            # too far to the right of the center fire boat to move to the left 


def state_isComplete():
    if (state==4):
        SFR.SNACK_RUN = True
        SFR.task = Task.DETERMINE_TASK
    pass


#filters out all the buoys seen and updates the ones we care about
#different behavior for different states
def filter_buoys():
    #note: will adapt based on the object list that is passed in 

    nib = 0 #Number of Important Buoys
    #initial states -- navigating towards the buoy
    if state = 1 :
        #first pass through, if greater than TASK_SCOPE, filter out unneeded buoys
        if(farthestDistance == 0):
            for obj in object_list:
                if(obj.z <= TASK_SCOPE) and (obj.z > farthestDistance):
                    farthestDistance = obj.z #this final object update should be the blue buoy
                    
        #more general behavior after second pass through (seeing the blue buoy)
        for obj in object_list:
            if obj.z < farthestDistance: # we should only ever see max three buoys within
                if obj.classType == "GREEN":
                    green_buoy[0] = obj.x
                    green_buoy[1] = obj.z
                    nib += 1
                elif obj.classType == "RED":
                    red_buoy[0] = obj.x
                    red_buoy[1] = obj.z
                    nib += 1
                elif obj.classType == "BLUE":
                    blue_buoy[0] = obj.x
                    blue_buoy[1] = obj.z
                    farthestDistance = obj.z #updating every time
                    nib += 1
        if nib > 3: #sanity checking
            print("WARNING: UNEXPECTED NUMBER OF BUOYS SEEN")
    
    elif state == 2: 
        #will check if we see a blue buoy (if we do --> special behavior)
        for obj in object_list:
            if (obj.z**2 + obj.y**2) < RADIUS_OF_MOTION**2 and obj.classType == "BLUE":
                # will call a function to correct the motion 
                pass 
        farthestDistance = TASK_SCOPE #should happen before state 3
    
    #heading back
    elif state == 3:
        for obj in object_list:
            if obj.z < farthestDistance: # we should only ever see max three buoys within
                if obj.classType == "GREEN":
                    green_buoy[0] = obj.x
                    green_buoy[1] = obj.z
                    nib += 1
                elif obj.classType == "RED":
                    red_buoy[0] = obj.x
                    red_buoy[1] = obj.z
                    nib += 1
        if nib > 2: #sanity checking
            print("WARNING: UNEXPECTED NUMBER OF BUOYS SEEN")
        farthestDistance = (green_buoy[1]+red_buoy[1])*0.5

    #(finishing) should need nothing
    else: #state 4
        #probably don't need anything h
        pass
        
  
def buoy_disappear():
    # this method executes if the buoy is not in sight 
    # checks that the boat is at the expected distance where the buoy should disappear 
    # if it is in the expected distance state+=1
    # otherwise set state to state+=0.5
    if (farthestDistance-ExpectedDistance<0):
        while(time<expectedTime):
            #fire both motors equall 
            time+1
        time=0
        state=state+1
    else:
        state=state+0.5
     
         
def boat_lost():
    # This method executes if the boat does not see anything 
    if (state==1.5):
        while (blue_buoy[0]==0):
            # turn until it sees the blue buoy
        # if it sees the blue buoy state = 1
        state=1
    if (state==3.5):
        while (red_buoy[0]==0 and green_buoy[0]):
            # turn until it sees both the red and green buoy
        # if it sees the red and green buoy state = 3
        state=3
