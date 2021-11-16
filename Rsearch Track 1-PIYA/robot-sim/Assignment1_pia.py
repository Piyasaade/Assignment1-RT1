from __future__ import print_function

import time
from sr.robot import *

"""
the main idea of this code is to control a robot in a way that will always grab the silver token and not the golden one, 
while it will turn under specific conditions and angles that we're set in this code once it detects a golden token. 
1) the robot will check if a golden token is near
2) if yes, it will check for silver token 
3) if silver token is detected, the robot will drive toward the token, grab it, and then put it behind him and continue its path
4) else if silver is not detected then it will rotate through specific conditions by taking the path where there is more space
5) else if golden token is not detected neither so the robot has to drive until it finds a token  
"""

golden_dist=0.75
""" float: a fixed distance that the robot can't pass it once golden token is detected"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""


silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""


def Direction_Golden():
	right_dist=100
	left_dist=100
	for token in R.see():
		if (token.info.marker_type is MARKER_TOKEN_GOLD): #if golden token is detected from R.see function
			if token.rot_y<105 and token.rot_y>75: # the gold token is on its right
				if token.dist < right_dist:
					right_dist=token.dist # store the nearest golden token on my right
			elif -105<token.rot_y<-75: # the gold token is on its left
				if token.dist<left_dist:
					left_dist=token.dist# store the nearest silver token
	return  right_dist,left_dist				
						
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=50
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

while 1:
	dist_g, rot_g = find_golden_token()
	dist_s, rot_s = find_silver_token()

	if dist_g < golden_dist and abs(rot_g)<75: # stay far from the boxes on its left and right with 75 degrees and just drive forward
		print("golden token is near")
		print(dist_s, abs(rot_s))
		if dist_s < 1 and abs(rot_s)<85: # if silver token is just infront of the robot
			print("silver is HERE!! go grab it!") 
					
			if -a_th<= rot_s <= a_th: # if the robot is well aligned with the token, we go forward
				print("Ah, that'll do.")
				if dist_s< d_th: 
					R.grab() # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
					print("Gotcha!")
					turn(20, 3)
					R.release() # release the silver token that you just grabed
					drive(-10,0.5)
					turn(-20,3)	
				else :
					drive(25,0.5)
			elif rot_s < -a_th: # if the robot is not well aligned with the token, we move it on the left 
				print("Left a bit...")
				turn(-2, 0.5)
			elif rot_s > a_th: #if the robot is not well aligned with the token, we move it on the right
				print("Right a bit...")
				turn(+2, 0.5)
		else:
			right_dist,left_dist = Direction_Golden() # calling the function Direction_Golden() to get the right and left distance
			print("OHH!! Pay Attention, Golden token detected! TURN!!")
			if (right_dist>left_dist):
				print("turn right robot")
				while abs(rot_g)<80: # keep rotating until the absolute angle and the nearest token is larger than 80 degrees
					dist_g, rot_g = find_golden_token() #get the distance and the angle between the golden token and the robot by calling the function find_golden_tocken()
					turn(5,0.25)
				drive(25,0.25)
			elif(right_dist<left_dist):
				print("turn left robot")
				while abs(rot_g)<80:
					dist_g, rot_g = find_golden_token()
					turn(-5,0.25)
				drive(25,0.25)
					
	else:
		print("golden token is far, you're safe")
		print(dist_s, abs(rot_s))
		if dist_s < 1 and abs(rot_s)<85:
			print("silver is HERE!! go grab it!") 
			
			if -a_th<= rot_s <= a_th: # if the robot is well aligned with the token, we go forward
				print("Ah, that'll do.")
				if dist_s< d_th:
					R.grab() # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
					print("Gotcha!")
					turn(20, 3)
					R.release()
					turn(-20,3)	
				else :
					drive(25,0.5)
			elif rot_s < -a_th: # if the robot is not well aligned with the token, we move it on the left 
				print("Left a bit...")
				turn(-2,0.5)
			elif rot_s > a_th: # if the robot is not well aligned with the token, we move it on the left
				print("Right a bit...")
				turn(+2,0.5)
		else:
			print("Drive safely! no token detected!")
			drive(25,0.5)