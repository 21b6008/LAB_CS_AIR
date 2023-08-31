import asyncio
import websockets
import cv2
import numpy as np

HOST = "192.168.1.100"
PORT = 8001
ADDR = HOST+":"+str(PORT)
VIDEOADDR = HOST+":"+str(PORT+1)
HEADER = 4
VIDEOHEADER = 15
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

async def image(img):
    #img = np.array(img) 
    # img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    # cv2.imshow("Stream", img)
    print(img)

async def start():
    async with websockets.connect("ws://"+ADDR) as websocket:
        #await websocket.send("0 0 0 0 0 0")
        await websocket.send(DISCONNECT_MESSAGE)    

async def video():
    async with websockets.connect("ws://"+ADDR) as websocket:
        task = asyncio.create_task(control_robot(websocket))
        i = 0
        while i < 100:
            #await asyncio.sleep(0.1)
            img = await websocket.recv()
            i += 1
            await websocket.send(f"frames: {i}")
        
        await asyncio.sleep(2)

        while i < 200:
            img = await websocket.recv()
            i += 1
            await websocket.send(f"frames: {i}") 

        await task      


async def control_robot(websocket):
    await websocket.send("0 0 0 0 0 0") 
    await websocket.send("gripper")
    await websocket.send("gripper")  
    await websocket.send(DISCONNECT_MESSAGE)       


#asyncio.run(video())    
asyncio.run(start())

