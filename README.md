# teleop_twist_keyboard
Generic Keyboard Teleop for ROS
#Launch
To run: `rosrun teleop_twist_keyboard teleop_twist_keyboard.py`

#Usage
```
Reading from the keyboard  and Publishing to Twist!
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
===================================
For Robotic Arm 
--------------------------
Joint Ang Jog(+)  1  2  3  4  5  6   
Joint Ang jOG(-)  q  w  e  r  t  y
f/v : increase/decreas increament deg  by 10%
====================================
anything else : stop
a/z : increase/decrease max speeds by 10%
s/x : increase/decrease only linear speed by 10%
d/c : increase/decrease only angular speed by 10%

CTRL-C to quit
```

