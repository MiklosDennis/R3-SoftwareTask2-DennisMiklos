How to run the code. Please view the README in raw format.

First run output.py to startup server.
Second run input.py to startup client.

The client has been designed to only read and send the joystick data
2 Joysticks are required for the client side. A PS4 or PS5 controller works the best! 

NOTE: Please have the controller plugged in prior to running the client side file.

The server side will prind the wheel PWM values in the following order:
If your rover looks like this from top view:
	0[	]0
	 [	]
	0[	]0
The server interprets this as the following and constructs this matrix:
	0[	]1
	 [	]	-->	[speed(0), speed(1);
	2[	]3		 speed(2), speed(3)]

The server than manipulates the movement matrix printing out the individual speeds in the following format:
	[f255][f255][f255][f255] - forward

f255 indicates maximum forward speed of wheels
r255 is maximum reverse speed
	
An example video has been provided to show the rover movements in action
	
