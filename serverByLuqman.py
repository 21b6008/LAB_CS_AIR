import socket
import threading
import asyncio
import websockets

from pyniryo import *

HEADER = 4
HOST = socket.gethostbyname(socket.gethostname())
PUBLIC = '202.160.0.5'
PORT = 8001
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

"""
def video_streaming(robot):
    # Getting image
    img_compressed = robot.get_img_compressed()
    # Uncompressing image
    img_raw = uncompress_image(img_compressed)
"""

# function that turns a string into a list of float
def to_list(msg):
    # Turns the message to an array of strings
    string = msg.split()

    # Turns the strings into floating point numbers
    values = []
    for i in range(len(string)):
        values.append(float(string[i]))
        #print(f"joint[{i}]: {float(string[i])}")

    return values


# coroutine that handles all the messages sent to the server
async def listener(websocket):
    addr = "192.168.1.116:8001"
    connected = True
    gripper_open = True
    print("Connecting to Niryo Ned...")
    robot = NiryoRobot("192.168.1.148")
    print("Robot connected.")
    robot.calibrate_auto()
    robot.update_tool()
    # Initialize the robot to open gripper
    robot.release_with_tool()
    print(f"[NEW CONNECTION] {addr} connected.")
    async for message in websocket:
        message = message.decode(FORMAT)
        if message is None:
                # Skip the loop
            continue
        elif message == DISCONNECT_MESSAGE:
            robot.go_to_sleep()
            connected = False
        elif message == "gripper":
            print("[USING GRIPPER]")
            if gripper_open:
                robot.grasp_with_tool()
                gripper_open = False
            else:
                robot.release_with_tool()   
                gripper_open = True
        else:
            # Move joints
            print("[MOVING JOINTS]")
            robot.joints = to_list(message)

        print(f"[{addr}]: {message}")
        

# starts the server websocket
async def main():
    async with websockets.serve(listener, "", 8001):
        await asyncio.Future()  # run forever

print("Server starting...")
print(f"Server is listening on {ADDR}")
asyncio.run(main())