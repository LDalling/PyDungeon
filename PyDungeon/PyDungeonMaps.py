import numpy as np
import random as random
import pygame as pg
import PyDungeonMobs as Mobs
import PyDungeonObjects as Objects
import queue
import time
import math
tileArray = np.array([[0]*50]*150)
maxRoomHeight = 20
maxRoomWidth = 20
minRoomHeight = 7
minRoomWidth = 7
"""
Level generator
0: ungenerated
1: walls
2: floors
3: caves
4: doors
5: ungenerated (but would cause long straight)
"""
tileWeight = [5,1023,1023, 1, 1023, 12]
tileSolid = [True,True,False,False,False,True]


def Object(name):
    return Objects.CreateObject(name)
def Mob(name):
    return Mobs.CreateObject(name)

def TileSolid(tiletype):
    return tileSolid[tiletype]
        
def Neighbors(pos):
    ourList = []
    posX = pos[0]
    posY = pos[1]
    for xPos in range(3):
        for yPos in range(3):
            if yPos != 1 or xPos != 1:
                    if posX -1 + xPos <150 and posY-1+yPos<50 and posX-1+xPos>= 0 and posY-1+yPos >= 0 and tileArray[posX-1+xPos][posY-1+yPos] != 2 and tileArray[posX-1+xPos][posY-1+yPos] != 1:
                        ourList.append((posX+xPos-1,posY-1+yPos))
    return ourList
"""
A* Pathfinding learned from Red Blob Games
http://www.redblobgames.com/pathfinding/a-star/introduction.html
"""
def Heuristic(node, goal):
    dx = abs(node[0] - goal[0])
    dy = abs(node[0] - goal[1]) 
    return 5 * (dx + dy) + (1 - 2 * 1) * min(dx, dy)

def FindPath(startPos,endPos):
    queuePriority = queue.PriorityQueue()
    queuePriority.put((0,startPos))
    nodeParents = {}
    nodeDistances = {}
    nodeParents[tuple(startPos)] = None
    nodeDistances[tuple(startPos)] = 0
    current = 0
    while not queuePriority.empty():
        current = queuePriority.get()[1]
        if current == endPos:
            break
           
        for nextNode in Neighbors(current):
            new_cost = nodeDistances[current] + tileWeight[tileArray[nextNode[0]][nextNode[1]]]
            currentIterator = current
            cavestraightlen = -random.randint(4,9)
            difference = [nextNode[0]-current[0], nextNode[1]-current[1]]
            
            while nodeParents[currentIterator] != None and current[1]-nextNode[1] == nodeParents[currentIterator][1]-currentIterator[1] and current[0]-nextNode[0] == nodeParents[currentIterator][0]-currentIterator[0] :
                currentIterator = nodeParents[currentIterator]
                cavestraightlen += 1
                if cavestraightlen >= 0:
                    for i in range(random.randint(4,8)):
                        pos = [max(0,min(149,current[0]+difference[0]*i)),max(0,min(49,current[1]+difference[1]*i))]
                        if tileArray[pos[0]][pos[1]] == 0:
                            tileArray[pos[0]][pos[1]] = 5
            if nextNode not in nodeDistances or new_cost < nodeDistances[nextNode]:
                nodeDistances[nextNode] = new_cost
#                print(5*math.sqrt(math.pow(endPos[0]-nextNode[0],2)+math.pow(endPos[1]-nextNode[1],2)))
                priority = new_cost +  Heuristic(nextNode,endPos)
                queuePriority.put((priority,nextNode))
                nodeParents[nextNode] = current
                

    while nodeParents[current] != None:
        tileArray[current[0]][current[1]] = 3
        current = nodeParents[current]

class Room():
    def __init__(self):
        self.placed = False
        self.position = [0,0]
        self.size = [0,0]
def CreateDoor(roomStart):
    def CreateDoorObj(posx, posy):
        door = None
        randint = random.randint(0,10)
        if randint > 9:
            door = Object("door")()
        elif randint > 6:
            door = Object("dooropen")()
        else:
            door = Object("door")()
        door.position = [posx,posy]

    startSide = random.randint(0,3)
    startPos = [0,0]
    if roomStart.position[0] == 0 and startSide == 2:
        startSide = 0
    elif roomStart.position[1] == 0 and startSide == 3:
        startSide = 1
    elif roomStart.position[0]+roomStart.size[0] == 150 and startSide == 0:
        startSide = 2
    elif roomStart.position[1]+roomStart.size[1] == 50 and startSide == 1:
        startSide = 3
    if startSide == 0: #if right
        randomVar = random.randint(roomStart.position[1],roomStart.position[1]+roomStart.size[1]-1)
        startPos = [roomStart.position[0]+roomStart.size[0], randomVar]
        tileArray[startPos[0]-1][startPos[1]] = 4
        CreateDoorObj(startPos[0]-1,startPos[1])
        tileArray[startPos[0]][startPos[1]] = 3
    elif startSide == 1: #if bottom
        randomVar = random.randint(roomStart.position[0],roomStart.position[0]+roomStart.size[0]-1)
        startPos = [randomVar, roomStart.position[1]+roomStart.size[1]]
        tileArray[startPos[0]][startPos[1]-1] = 4
        CreateDoorObj(startPos[0],startPos[1]-1)
        tileArray[startPos[0]][startPos[1]] = 3
    elif startSide == 2: #if left
        randomVar = random.randint(roomStart.position[1],roomStart.position[1]+roomStart.size[1]-1)
        startPos = [roomStart.position[0]-1, randomVar]
        tileArray[startPos[0]+1][startPos[1]] = 4
        CreateDoorObj(startPos[0]+1,startPos[1])
        tileArray[startPos[0]][startPos[1]] = 3
    else: #if top
        randomVar = random.randint(roomStart.position[0],roomStart.position[0]+roomStart.size[0]-1)
        startPos = [randomVar,roomStart.position[1]-1]
        tileArray[startPos[0]][startPos[1]+1] = 4
        CreateDoorObj(startPos[0],startPos[1]+1)
        tileArray[startPos[0]][startPos[1]] = 3
    return tuple(startPos)  

def CreateStaircases(roomsPlaced, level, numstairsup):
    print(numstairsup, "handed")
    if level == 0:
        room = roomsPlaced[random.randint(0,len(roomsPlaced)-1)]
        stairs = Object("topstaircase")()
        stairs.position = [room.position[0] + random.randint(1,room.size[0]-2),room.position[1] + random.randint(1,room.size[1]-2)]

        
    numstairs = random.randint(1,3)
    for i in range(numstairs):
        room = roomsPlaced[random.randint(0,len(roomsPlaced)-1)]
        stairs = Object("staircase")(i,1)
        print(stairs," is created????")
        stairs.position = [room.position[0] + random.randint(1,room.size[0]-2),room.position[1] + random.randint(1,room.size[1]-2) ]
        
    for j in range(numstairsup):
        room = roomsPlaced[random.randint(0,len(roomsPlaced)-1)]
        stairs = Object("staircase")(j,-1)
        stairs.position = [room.position[0] + random.randint(1,room.size[0]-2),room.position[1] + random.randint(1,room.size[1]-2) ]
    return numstairs

def GeneratePath(roomStart,roomEnd):
    FindPath(CreateDoor(roomStart),CreateDoor(roomEnd))
        

def CreateRoom(sizex, sizey ):
    """Creates a room and stores it in roomsChosen"""
    #Used to choose rooms to build in the level.
    genRoom = Room()
    genRoom.size = [sizex,sizey]
    return genRoom
def BuildRoom(room,posx, posy):
    pos = [posx, posy]

    #Check if the room's bounds are valid
    for xPos in range(room.size[0]):
        for yPos in range(room.size[1]):
            if xPos+posx >= 150 or posx < 0:
                #print(xPos+room.position[0])
                return None
            if yPos+posy >= 50 or posy < 0:
                #print("Failed Y")
                return None
            
    #Check each tile to see if it's on top of or too close to another room
    for xPos in range(room.size[0]+8):
        for yPos in range(room.size[1]+8):
            if xPos+posx < 150 and xPos+posy >= 0 and yPos+posy < 50 and yPos+posy >= 0:
                if tileArray[xPos+posx-4,yPos+posy-4] != 0:
                    #print("Otherwise, failed at ",xPos+posx,yPos+posy)
                    return None
            elif xPos+posx-8 < 150 and yPos + posy-8 < 50:
                if tileArray[xPos+posx-8,yPos+posy-8] != 0:
                    #print("Otherwise, failed at ",xPos+posx,yPos+posy)
                    return None

    #If the function hasn't failed this far, the room is safe to build.
    #(so we build it)
    for xPos in range(room.size[0]-2):
        for yPos in range(room.size[1]-2):
            tileArray[xPos+posx+1][yPos+posy+1] = 2
    for pos in range(room.size[0]):
        tileArray[posx+pos][posy] = 1
        tileArray[posx+pos][posy-1+room.size[1]] = 1
    for pos in range(room.size[1]):
        tileArray[posx][posy+pos] = 1
        tileArray[posx+room.size[0]-1][posy+pos] = 1
    room.position = [posx,posy]
    return room

def GenerateRooms():
    table = []
    start = time.clock()
    room = None
    roomPointsLeft = 80 #'Currency' used to buy rooms
    #Complex or dangerous rooms can be assigned greater 'costs'
    while roomPointsLeft > 0:
        roomType = random.randint(1,30)
        if roomType < 5:
            roomPointsLeft -= 4
            room = CreateRoom(random.randint(18,27),random.randint(18,27))
        else:
            roomPointsLeft -= 2
            room = CreateRoom(random.randint(8,13),random.randint(8,13))
        if room != None:
            table.append(room)
    print(time.clock() - start,"choosing rooms")
    return table

def GenerateLevel(levelID,lastStairs):
    global tileArray     
    tileArray = np.array([[0]*50]*150)
    roomsChosen = GenerateRooms()
    roomsPlaced = []
    print(len(roomsChosen), "rooms to build")
    roomsPlaced.append(BuildRoom(roomsChosen[0],random.randint(1,3),random.randint(1,3)))
    startTimer = time.clock()
    while len(roomsChosen) > 0:
        roomPlaced = None
        xPos = -5
        yPos = random.randint(3,5)
        placeIndex = -1
        #First, try to place a new room below the last one
        while placeIndex < len(roomsPlaced)-1:
            placeIndex += 1
            while roomPlaced == None and yPos < random.randint(7,10):
                placepos = roomsPlaced[placeIndex].position
                xPos += random.randint(1,5)
                if xPos > 20:
                    yPos +=random.randint(1,5)
                    xPos = -5
                roomPlaced = BuildRoom(roomsChosen[-1], placepos[0]+xPos+ random.randint(5,9), placepos[1] + roomsPlaced[placeIndex].size[1] + random.randint(8,16) +yPos)
        iterIndex = -1
        #If that fails, we attempt place a room to the right of every existing room.
        while roomPlaced == None and iterIndex < len(roomsPlaced)-2:
            iterIndex +=1
            xPos = 5
            yPos = random.randint(-5, 0)
            
            while roomPlaced  == None and xPos < random.randint(12,17):
                yPos += random.randint(1, 4)
                if yPos > 20:
                    xPos +=random.randint(1,5)
                    yPos = random.randint(-10, 0)
                placepos = roomsPlaced[iterIndex].position

                roomPlaced = BuildRoom(roomsChosen[-1], placepos[0]+ random.randint(5,8) + xPos +roomsPlaced[iterIndex].size[0],placepos[1] + roomsPlaced[iterIndex].size[1] +yPos)
        iterIndex = -1
        #Ideally, the last two functions would be fine, but the generated levels tended to droop, resulting in left-heavy levels.
        #So, we attempt place a room to the top of every existing room.
        while roomPlaced == None and iterIndex < len(roomsPlaced)-2:
            iterIndex +=1
            xPos = 3
            yPos = random.randint(0, 5)
            while roomPlaced == None and xPos < random.randint(9,14):
                yPos += random.randint(1, 4)
                if yPos > 20:
                    xPos +=random.randint(1,5)
                    yPos = random.randint(-10, 0)
                placepos = roomsPlaced[iterIndex].position

                roomPlaced = BuildRoom(roomsChosen[-1], placepos[0]- random.randint(5,8) - xPos ,placepos[1]- random.randint(5,8) +yPos)
        if roomPlaced == None:
            roomsChosen.pop(-1)
        else:
            roomsChosen.pop(-1)
            roomsPlaced.append(roomPlaced)

    
    print(time.clock() - startTimer,"building rooms")
    roomsUnassigned = roomsPlaced
    startTimer = time.clock()
    roomsAssigned = []
    roomsAssigned.append(roomsPlaced[random.randint(0,len(roomsPlaced)-1)])
    
    while len(roomsUnassigned) > 0:
        key1 = random.randint(0,len(roomsUnassigned)-1)
        room1 = roomsUnassigned[key1]
        roomsUnassigned.pop(key1)
        
        key2 = random.randint(0,len(roomsAssigned)-1)
        room2 = roomsAssigned[key2]
        roomsAssigned.append(room1)
        GeneratePath(room1,room2)                
    print(time.clock() - startTimer,"building paths")
    numstairs = CreateStaircases(roomsAssigned, levelID,lastStairs)
    return (tileArray, numstairs)
            
"""
#This code can be used for testing and draws the room.
GenerateLevel()
pixPerTile = 5
xScale = 150*pixPerTile
yScale = 50*pixPerTile
tempSurface = pg.display.set_mode((xScale,yScale))
for ypos in range(yScale):
    for xpos in range(xScale):
        xTile = math.floor(xpos/pixPerTile)
        yTile = math.floor(ypos/pixPerTile)
        color = (0,0,0)
        if tileArray[xTile][yTile] == 1:
            color = (127,127,127)
        elif tileArray[xTile][yTile] == 2:
            color = (147,147,147)
        elif tileArray[xTile][yTile] == 3:
            color = (255,0,0)
        elif tileArray[xTile][yTile] == 4:
            color = (100,100,0)
        elif tileArray[xTile][yTile] == 5:
            color = (255,0,255)
        elif tileArray[xTile][yTile] == 7:
            color = (0,255,0)
        elif tileArray[xTile][yTile] == 8:
            color = (255,255,255)
        else:
            color = (90,90,90)
        tempSurface.set_at((xpos,ypos),color)
pg.display.flip()
"""
