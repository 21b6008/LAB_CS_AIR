import socket
import websockets
import asyncio
import cv2
from pyniryo import *

## INSTRUCTIONS

# First run a python server by going to command prompt,
# Get to the RobotWebsite directory, and run "python -m http.server"
# Then run this program (remember to select the correct environment pyniryo_env)

# In VS Code:
# Select the correct interpreter in the bottom right corner (pyniryo_env)
# Click Run Python File in the top right corner

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8001
ADDR = HOST+":"+str(PORT)
ROBOT_ADDR = '192.168.1.102'    # robot ip address may change
FORMAT = 'utf-8'

# Initialize robot, happens at the start the program
print("Connecting to robot...")
robot = NiryoRobot(ROBOT_ADDR)
robot.calibrate_auto()

# Get image from robot and turn into byte array
def stream_image(robot): 
    # Getting image
    img_compressed = robot.get_img_compressed()
    # Uncompressing image
    img_raw = uncompress_image(img_compressed)

    # This code converts ndarray to jpg then to byte array
    _, jpg = cv2.imencode('.jpg', img_raw)
    return jpg.tobytes()

# Turns the message to a list of floating point numbers
def to_list(msg):
    """
    Turns the message to an array of strings 
    "0 0 0 0 0 0" --> ['0', '0', '0', '0', '0', '0']
    Then into a list of floats
    ['0', '0', '0', '0', '0', '0'] --> [0, 0, 0, 0, 0, 0]
    """
    string = msg.split()

    values = []
    for i in range(len(string)):
        values.append(float(string[i]))
    return values

def to_string(list): 
    """
    Turns the list to strings for sending
    [0, 0, 0, 0, 0, 0] --> "0 0 0 0 0 0 "
    """
    msg = ""
    for n in list:
        msg += str(round(n, 2))
        msg += " "
    return msg

async def handler(websocket):
    print(f"[NEW CONNECTION] New device connected.\n")
    robot.update_tool()
    robot.release_with_tool()   # Initialize the robot to open gripper
    gripper_open = True
    connected = True
    
    while connected:
        try:
            # Message sending
            await websocket.send(stream_image(robot))                       
            await websocket.send(to_string(robot.joints).encode(FORMAT))    

            # Message receiving
            msg = await websocket.recv()
            msg = msg.decode(FORMAT)

            if msg == None or msg == ".":
                # Skip the loop
                continue
            
            print(f"[{ADDR}]: {msg}")        

            # Logic to tell the robot what to do with the received message
            if msg == "DISCONNECT":
                print("[DISCONNECTING]\n")
                robot.go_to_sleep()
                connected = False
                print("Ready for new connection.")
                print(f"Server is listening on {ADDR}\n")

            elif msg == "GRIPPER":
                print("[USING GRIPPER]\n")
                if gripper_open:
                    robot.grasp_with_tool()
                    gripper_open = False
                else:
                    robot.release_with_tool()
                    gripper_open = True   

            elif msg == "LEARN_ON":
                if robot.get_learning_mode():
                    print("[MESSAGE] Learning mode is already on.\n")
                else:
                    print("[ENABLING LEARNING MODE]\n")
                    robot.set_learning_mode(True)
            elif msg == "LEARN_OFF":
                if robot.get_learning_mode():
                    print("[DISABLING LEARNING MODE]\n")
                    robot.set_learning_mode(False)
                else:
                    print("[MESSAGE] Learning mode is already off.\n")

            elif msg == "HOME":
                print("[HOME] Moving to Home configuration.\n")
                robot.move_to_home_pose()

            else:
                # Move joints
                print("[MOVING JOINTS]\n")
                robot.joints = to_list(msg)
        
        except KeyboardInterrupt:
            connected = False

async def start():
    async with websockets.serve(handler, HOST, PORT):
        print(f"[SERVER STARTING] Server is listening on {ADDR}\n")
        await asyncio.Future() # run forever

asyncio.run(start())