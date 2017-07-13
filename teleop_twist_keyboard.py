#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist and MultiArray
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

g : up (+z)
b : down (-z)

For Robotic Arm 
--------------------------
   Joint Ang Jog(+)  1  2  3  4  5  6   
   Joint Ang Jog(-)  q  w  e  r  t  y

f/v : increase/decreas increament deg  by 10%

anything else : stop

a/z : increase/decrease max speeds by 10%
s/x : increase/decrease only linear speed by 10%
d/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

moveBindings = {
		'i':(1,0,0,0),
		'o':(1,0,0,-1),
		'j':(0,0,0,1),
		'l':(0,0,0,-1),
		'u':(1,0,0,1),
		',':(-1,0,0,0),
		'.':(-1,0,0,1),
		'm':(-1,0,0,-1),
		
		'O':(1,-1,0,0),
		'I':(1,0,0,0),
		'J':(0,1,0,0),
		'L':(0,-1,0,0),
		'U':(1,1,0,0),
		'<':(-1,0,0,0),
		'>':(-1,-1,0,0),
		'M':(-1,1,0,0),
		
		'g':(0,0,1,0),
		'b':(0,0,-1,0),
	    }

armMoveBindings = {
		'1':(0.2,0,0,0,0,0),
		'2':(0,0.2,0,0,0,0),
		'3':(0,0,0.2,0,0,0),
		'4':(0,0,0,0.2,0,0),
		'5':(0,0,0,0,0.2,0),
		'6':(0,0,0,0,0,0.2),

		'q':(-0.2,0,0,0,0,0),
		'w':(0,-0.2,0,0,0,0),
		'e':(0,0,-0.2,0,0,0),
		'r':(0,0,0,-0.2,0,0),
		't':(0,0,0,0,-0.2,0),
		'y':(0,0,0,0,0,-0.2),

		
	    }
		
		
speedBindings={
		'a':(1.1,1.1),
		'z':(0.9,0.9),
		's':(1.1,1),
		'x':(0.9,1),
		'd':(1,1.1),
		'c':(1,0.9),
            }
jointAngSpeedBindings={ 
        	'f':(1.1),
        	'v':(0.9), 
	    }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)
	

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub    = rospy.Publisher('wheelVel_cmd', Twist, queue_size = 1)
	armPub = rospy.Publisher('jointAng_cmd',Float32MultiArray,queue_size = 1)
	rospy.init_node('teleop_twist_keyboard')

	speed = rospy.get_param("~speed", 0.5)
	turn  = rospy.get_param("~turn",  1.0)
    	jointAngSpeed = rospy.get_param("~angSpeed", 1)
	x      = 0
	y      = 0
	z      = 0
	th     = 0
	status = 0

    	jointAng1 = 90.
    	jointAng2 = 90.
    	jointAng3 = 90.
    	jointAng4 = 90.
    	jointAng5 = 90.
    	jointAng6 = 90.
    	jointAng7 = 90. 

	try:
                
		print msg
		print vels(speed,turn)
				
		while(1):
			key = getKey()
			if key in moveBindings.keys():
				x  = moveBindings[key][0]
				y  = moveBindings[key][1]
				z  = moveBindings[key][2]
				th = moveBindings[key][3]
				twist = Twist()
				twist.linear.x = x*speed; 
				twist.linear.y = y*speed; 
				twist.linear.z = z*speed;
				twist.angular.x = 0; 
				twist.angular.y = 0; 
				twist.angular.z = th*turn
				pub.publish(twist)

				
			elif key in speedBindings.keys():
				speed = speed * speedBindings[key][0]
				turn  = turn  * speedBindings[key][1]
				print vels(speed,turn)
				if (status == 14):
					print msg
				status = (status + 1) % 15
				twist = Twist()
				twist.linear.x = x*speed; 
				twist.linear.y = y*speed; 
				twist.linear.z = z*speed;
				twist.angular.x = 0; 
				twist.angular.y = 0; 
				twist.angular.z = th*turn
				pub.publish(twist)
       
            		elif key in jointAngSpeedBindings.keys():
  	            		jointAngSpeed = jointAngSpeed * jointAngSpeedBindings[key]
                		print "curr joint Speed  %s  " % (jointAngSpeed)

			elif key in armMoveBindings.keys():
                		theta1 = armMoveBindings[key][0]
				theta2 = armMoveBindings[key][1]
				theta3 = armMoveBindings[key][2]
				theta4 = armMoveBindings[key][3]				
				theta5 = armMoveBindings[key][4]
				theta6 = armMoveBindings[key][5]				
	
				theta_1_6 = Float32MultiArray()
				theta_1_6.layout.dim.append(MultiArrayDimension())
				theta_1_6.layout.dim[0].label  = "armJoints"
				theta_1_6.layout.dim[0].size   = 6
				theta_1_6.layout.dim[0].stride = 6
				theta_1_6.layout.data_offset   = 0
				theta_1_6.data = [0]*6	
                                
				jointAng1 = jointAng1 + theta1 * jointAngSpeed
				jointAng2 = jointAng2 + theta2 * jointAngSpeed
				jointAng3 = jointAng3 + theta3 * jointAngSpeed
				jointAng4 = jointAng4 + theta4 * jointAngSpeed
				jointAng5 = jointAng5 + theta5 * jointAngSpeed
				jointAng6 = jointAng6 + theta6 * jointAngSpeed
				
                		if (jointAng2 < 0 ): jointAng2 = 0
                		if (jointAng3 < 0 ): jointAng3 = 0 
                		if (jointAng2 + jointAng3 > 209): jointAng2 = 209 - jointAng3
				if (jointAng4 < 0): jointAng4 = 0
                		if (jointAng4 >170): jointAng4 =170
                		if (jointAng5 >180): jointAng5 = 180
                		if (jointAng5 <0  ): jointAng5 = 0
                		if (jointAng6 >180): jointAng6 = 180
                		if (jointAng6 <0  ): jointAng6 = 0
 
                		theta_1_6.data[0] = jointAng1
				theta_1_6.data[1] = jointAng2
				theta_1_6.data[2] = jointAng3
				theta_1_6.data[3] = jointAng4
				theta_1_6.data[4] = jointAng5
				theta_1_6.data[5] = jointAng6
			        				
				print "currently:\tj1 %s\tj2 %s\tj3 %s\tj4 %s\tj5 %s\tj6 %s\tj7 %s  " % (jointAng1, jointAng2, jointAng3, jointAng4, jointAng5, jointAng6, jointAng7)
				if (status == 14):
					print msg
				status = (status + 1) % 15				
				armPub.publish(theta_1_6)
				
			else:
				x = 0
				y = 0
				z = 0
				th = 0
				twist = Twist()
				twist.linear.x = x*speed; 
				twist.linear.y = y*speed; 
				twist.linear.z = z*speed;
				twist.angular.x = 0; 
				twist.angular.y = 0; 
				twist.angular.z = th*turn
				pub.publish(twist)
				
				if (key == '\x03'):
					break

	except:
		print e

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


