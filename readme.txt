### TURNING ON/OFF THE ROBOT ###
1. Turn on the open switch (rocker switch) at the back of the robot. It is just next to where the power connector is.
2. Wait till the light turns blue.
3. To turn off the robot safely, press and hold the push button switch (silver color) on top of the until the light changes color. Wait for it to turn red. Turn off the rocker switch ON/OFF switch.

### RUNNING THE SERVER ###
1. First run a python web server. To do that:
	1. Open "Niryo NED - Shortcut" in Desktop.
	2. Open "Niryo Ned Server 2022".
	3. Open a terminal in this directory. One way to do it is to Shift+Right Click on the directory window
	   and click "Open PowerShell window here".
	4. In the terminal, run: "python -m http.server" .
	   It should serve a webserver on port 8000.

2. Run the server.py file.
	1. First, the robot needs to be connected before running the program. So turn on the robot and wait for
	   the light to turn from green to blue. 
	2. Open "Niryo NED - Shortcut" in Desktop.
	3. Open "Niryo Ned Server 2022".
	4. Open "server.py" file in VS Code. Make sure the file is not in restricted mode. Ensure that the interpreter chosen is "pyniryo_env'. This is a Conda environment.
	5. In the top right corner, click the drop-down beside the ▷ button. Then "Run Python File".
	   Afterwards, clicking the ▷ button will automatically choose the "Run Python File" option.
	   The robot should now be moving to calibrate.
	6. The robot arm will move and perform calibration and move to its home position.
	6. If robot IP has changed, connection will fail. Refer to CHANGING ROBOT IP section to change the robot IP.

### CHANGING ROBOT IP ###
The server.py has set the IP address of the robot.
The web server and the robot should be on the same network. At the moment, the robot is connected to the 
router through ethernet. The other devices (web and mobile) can connect to the wifi (G38B) or ethernet of the same router.
Robot IP may change. If this happened, you will receive an error when running the server.py.
You will need to find out the IP to connect to the robot.
You may get the robot IP from Niryo Studio, as below:
- Run the NiryoStudio.exe - Shortcut on the desktop, click the left arrow on the top right side (Connection menu). 
- Click the search icon and see the robot IP on the dropdown list.
- You will need to update this IP in the server.py; edit the ROBOT_ADDR constant (around line 20).

### CONNECTING VIA WEBSITE ###
1. Type "localhost:8000" into the URL of a web browser. You should see the website after entering.
2. In the "Host IP Address" bar, type "192.168.1.100" (IP of the server PC, i.e. where server.py is run). In the "Port Number", type "8001". Note the IP address 
   may change. You should see the IP address and the port number on the terminal or the running server.py.
3. Connect to Socket.
   You should now be connected to the robot. You should see the digital twin align its pose to the physical 
   robot, and the camera stream from the robot.
4. You can now control the robot from the web interface.
5. The current robot server only support one connect (client, either web or mobile) at a time. You will need 
   to disconnet from web if you want to control from the mobile app; and vice versa.

### CONNECTING VIA THE MOBILE APP ###
Note: You will need to disconnect the robot from the webserver (if it was connected).
1. Make sure the phone is connected to the same network as the robot/server.
2. On the mobile phone, run the "Ned Controller" app.
3. At the top, in the "IP Address" bar, type "192.168.1.100" (IP of the robot server PC, i.e. where server.py is run). In the "Port", type "8001".
4. Then tap the "Connect to" button, this can be found at the bottom.
   You should now be connected to the robot. You should see the digital twin align its pose to the physical robot, and the camera stream from the robot.
5. You can now control the robot from the app interface.

### OPERATING THE ROBOT ###
In both the website and mobile app, the available controls and buttons are similar.

# To move the robot arm, you need to set the different joint values. Use the slider to change the robot joint 
values and press "Move Joint".
# Press "Return Home" or "Home" to return to the home configuration of the robot.
# "Open/Close Gripper" will open or close the grippers depending on its current status.
# "Learning Mode" - toggling it on will make the robot not stiff and users are able to move the robot by hand and see the digital twin moves accordingly.
# When done, click the "Disconnect" button the disconnect from the server. The robot will move to the home 
configuration.
