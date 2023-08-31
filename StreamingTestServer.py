import socket
import websockets
import asyncio
import cv2
from pyniryo import *

HEADER = 4
HOST = socket.gethostbyname(socket.gethostname())
PUBLIC = '202.160.0.5'
PORT = 8002
ADDR = HOST+":"+str(PORT)
ROBOT_ADDR = '192.168.1.148'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
STREAM_MESSAGE = "!STREAM"

# Initialize robot
print("Connecting to Niryo Ned...")
robot = NiryoRobot(ROBOT_ADDR)
print("Robot connected.\n")
robot.calibrate_auto()
robot.update_tool()
# Initialize the robot to open gripper
robot.release_with_tool()
gripper_open = True


# Get image from robot and turn into byte array
def stream_image(robot): 
    # Getting image
    img_compressed = robot.get_img_compressed()
    # Uncompressing image
    img_raw = uncompress_image(img_compressed)

    # This code converts ndarray to jpg then to byte array
    _, jpg = cv2.imencode('.jpg', img_raw)
    # print(f"jpg {jpg}")
    byte_encode = jpg.tobytes()

    # data_encode = np.array(jpg)
    # print(f"data encode {data_encode}")
    # byte_encode = data_encode.tobytes()

    # print(f"byte_encode {byte_encode}")
    return byte_encode

# Turns the message to a list of floating point numbers
def to_list(msg):
    # Turns the string message to an array of strings
    # (0 0 0 0 0 0) --> ['0', '0', '0', '0', '0', '0']
    string_list = msg.split()

    # Turns the strings into floating point numbers and put in a list
    # ['0', '0', '0', '0', '0', '0'] --> [0, 0, 0, 0, 0, 0]
    values = []
    for i in range(len(string_list)):
        values.append(float(string_list[i]))

    return values

def recv_nowait(websocket):
    try:
        return websocket.messages.get_nowait()
    except asyncio.queues.QueueEmpty:
        pass

async def robot_controller(websocket):
    print(f"[NEW CONNECTION] {ADDR} connected.\n")
    connected = True

    while connected:
        try:
            await websocket.send(stream_image(robot))

            #msg = recv_nowait(websocket)\
            msg = await websocket.recv()
            #msg = msg.decode(FORMAT)  
            #print(f"msg: {msg}")   

            if msg == None:
                # Skip the loop
                continue

            elif msg == DISCONNECT_MESSAGE:
                print(f"[{ADDR}]: {msg}\n")
                print("[DISCONNECTING]")
                robot.go_to_sleep()
                robot.close_connection()
                connected = False

            elif msg == "gripper":
                print(f"[{ADDR}]: {msg}\n")
                print("[USING GRIPPER]")
                if gripper_open:
                    robot.grasp_with_tool()
                    gripper_open = False
                else:
                    robot.release_with_tool()   
                    gripper_open = True

            else:
                print(f"[{ADDR}]: {msg}\n")                
                print("[MOVING JOINTS]")
                robot.joints = to_list(msg)

            await task

        except KeyboardInterrupt:
            robot.close_connection()
            pass

        except:
            connected = False

        
        # except websockets.exceptions.ConnectionClosedOK:
        #     print("websockets.exceptions.ConnectionClosedOK")

async def video_streaming(websocket, connected):
    i = 0
    while connected:
        while i < 50:
            await websocket.send(stream_image(robot))
        await asyncio.sleep(1)

    

async def start():
    async with websockets.serve(robot_controller, "", PORT):
        await asyncio.Future() # run forever

print(f"[SERVER STARTING] Server is listening on {ADDR}\n")
asyncio.run(start())