"""
This file contains the software for completing the Snack Run Task
"""
from modes.tasks_enum import Task
import SFR

# Local values
# When the target buoy is no longer in range, we want the boat to continue moving for a 
# set amount of time
time=0 
# Find the target value Z position (+ room for error) and current Z position and subtract
# the two values
distance_to_moveX=0
distance_to_moveZ=0
moving_circle=False
moving_back=False
state=1

object_list = [] #will be given to us
important_objects = [] #the objects we care about


#find the target value X position (+- room for error)

#object states for blue, red, and green buoys
#these object states will have position vectors (x and z matter), and classes types
#they will be set in filter buoys
#all relative positions
blue_buoy = [0,0] 
red_buoy = [0,0]
green_buoy = [0, 0]

#farthest distance is the relative distance of the farthest buoy we care about
farthestDistance = 0

#constant for how big the task is (in ft)
TASK_SCOPE = 106 
RADIUS_OF_MOTION = 10



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
        #make the boat move forward firing one motor more than the other
        #if the x position of the blue buoy is to far left of us, make the buoy fire both motor equally
        
        # when the blue buoy is no longer in vision fire both motor equally for a set period of time
        # after it has finished the constant period of time change the state to 2
        pass
    pass
    
def state_move_in_circle():
    # we plan to have a predefined radius and distance that the boat should travel in 
    # so that it can make a loop around the blue buoy
    # when completed the half circle
    if (state==2):
        # determine the radius of the path 
        # make the boat move in a predetermined circular path
        # when the red and green buoys are in sight (without the blue) make the boat move in a straight line towards them
        # for a period of time
        pass
    # if completed predetermined path and moves straight line for a period of time, change state to 3
    pass
def state_move_back():
    if (state==3):
        # Make the boat move towards the red and green buoy. Aiming for the center between the two buoy
        # Try to make the x position to the red buoy and the -x position to the green buoy is the same 
        pass
    # when it has passed the red and green buoys again change the state to 4
    pass 

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
    if state < 2:
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
    
    #turning around
    elif state == 2: 
        #will check if we see a blue buoy (if we do --> special behavior)
        for obj in object_list:
            if (obj.z**2 + obj.y**2) < RADIUS_OF_MOTION**2 and obj.classType == "BLUE":
                #will call a function to correct the motion
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
        
        
def correct_motion():
    # THIS METHOD IS ONLY CALLED WHEN IT IS IN STATE 2 
    # Only happens if it evers sees the blue buoy and is too close to it
    # Makes the boat fire motor on the opposite side so it moves away from blue buoy
    # if it does fire motor on the opposite side, it will reverse fire the motor to the original direction 
    state=0
    # After it has corrected it's path state=2
    
    pass #PERHAPS WRITE ANOTHER METHOD FOR BEHAVIOR ON THE WAY BACK?
