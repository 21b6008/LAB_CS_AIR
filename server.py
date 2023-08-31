import socket
import websockets
import asyncio
import cv2
from pyniryo import *

HOST = socket.gethostbyname(socket.gethostname())
PUBLIC = '202.160.0.5'
PORT = 8001
ADDR = HOST+":"+str(PORT)
ROBOT_ADDR = '192.168.1.148'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


# Initialize robot
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
    # Turns the message to an array of strings
    # (0 0 0 0 0 0) --> ['0', '0', '0', '0', '0', '0']
    string = msg.split()

    # Turns the strings into floating point numbers and put in a list
    # ['0', '0', '0', '0', '0', '0'] --> [0, 0, 0, 0, 0, 0]
    values = []
    for i in range(len(string)):
        values.append(float(string[i]))

    return values

async def handler(websocket):
    print(f"[NEW CONNECTION] {ADDR} connected.\n")

    robot.update_tool()
    # Initialize the robot to open gripper
    robot.release_with_tool()
    gripper_open = True

    connected = True

    while connected:
        try:
            await websocket.send(stream_image(robot))

            msg = await websocket.recv()
            msg = msg.decode(FORMAT)
            
            if msg == None or msg == ".":
                # Skip the loop
                continue
            
            print(f"[{ADDR}]: {msg}")           
            if msg == DISCONNECT_MESSAGE:
                print("[DISCONNECTING]\n")
                robot.go_to_sleep()
                connected = False
                print("Ready for new connection.")
                print(f"Server is listening on {ADDR}\n")

            elif msg == "gripper":
                print("[USING GRIPPER]\n")
                if gripper_open:
                    robot.grasp_with_tool()
                    gripper_open = False
                else:
                    robot.release_with_tool()
                    gripper_open = True   

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