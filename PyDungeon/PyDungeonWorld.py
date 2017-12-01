import PyDungeonMaps as Maps
import PyDungeonGraphics as Graphics
import numpy as np
import pickle
import math
import os.path
entities = [] 
mobs = [] 
objects = [] 
items = [] 
g_levelNumber = 0
g_worldSize = [150,50]
g_worldFile = open("worlds/levels.dat","wb+")
g_activeLevelArray = np.empty(g_worldSize)
g_stairsList = []
def ActiveLevel():
    return g_levelNumber


def DeleteCompletely(obj):
    if obj.classType == "object":
        global objects
        objects[obj.objectid] = False
    elif obj.classType == "mob":
        global mobs
        mobs[mob.mobid] = False
    elif obj.classType == "item":
        global items
        items[item.itemid] = False
    global entities
    entities[obj.id] = False
    del obj
        
def ClearAllObjects():
    print("World purged.")
    global entities
    for thing in entities:
        if thing != False and thing.perpetual != True :
            thing.UnRender()
            if not thing.perpetual:
                DeleteCompletely(thing)
    print(entities)
def LoadObjectsFromTable(table):
    global entities
    global mobs
    global objects
    global items
    for ent in table:
        if ent != False and ent.perpetual != True:
            ent.NewID()
def AssignWorldArray(world):
    pass

def DeleteObject(obj):
    global objects
    objects[obj.objectid] = False
    DeleteCompletely(obj)
def AssignEntityID(obj):
    """Assigns an ID for an entity in the world."""
    intRange = range(len(entities))
    for index in intRange:
        if entities[index] == False:
            entities[index]=obj
            return index
            break
    entities.append(obj)
    return len(entities)-1

def GetEntitiesFromPosition(pos):
    resultTable = []
    global entities
    for ent in entities:
        if ent != False and ent.position == pos:
            result.append(ent)
    return resultTable

def GetInteractablesFromPosition(pos):
    resultTable = []
    global entities
    for ent in entities:
        if ent != False and ent.position[0] == pos[0] and ent.position[1] == pos[1] and (ent.classType == "object" or ent.classType == "item"):
            resultTable.append(ent)
    return resultTable

def AssignObjectID(obj):
    """Assigns an ID for an object in the world."""
    intRange = range(len(objects))
    for index in intRange:
        if objects[index] == False:
            objects[index]=obj
            return index
            break
    objects.append(obj)
    return len(objects)-1
def AssignItemID(obj):
    """Assigns an ID for an item in the world."""
    intRange = range(len(items))
    for index in intRange:
        if items[index] == False:
            items[index]=obj
            return index
            break
    items.append(obj)
    return len(items)-1

def AssignMobID(mob):
    """Assigns an ID for a mob in the world."""
    intRange = range(len(mobs))
    for index in intRange:
        if mobs[index] == False:
            mobs[index]=mob
            return index
            break
    mobs.append(mob)
    return len(mobs)-1
def GiveMobTable():
    global mobs
    return mobs
def GiveObjectTable():
    global objects
    return objects

def UnrenderAll():
	#This repetition allows us to define the 'layers' - So we can see mobs on top of items.
    global entities
    for obj in entities:
        if obj != False:
            obj.UnRender()
    for obj in objects:
        if obj != False:
            obj.UnRender()
    for obj in items:	
        if obj != False:
            obj.UnRender()
    for obj in mobs:
        if obj != False:
            obj.UnRender()
def RenderAll():
	#This repetition allows us to define the 'layers' - So we can see mobs on top of items.
    global entities
    for obj in objects:
        if obj != False:
            obj.Render()
    for obj in items:	
        if obj != False:
            obj.Render()
    for obj in mobs:
        if obj != False:
            obj.Render()
def StairFromID(identity, sign):
    global objects
    for obj in objects:
        if identity >= 0 and obj.classname == "staircase" and math.copysign(1,obj.levelModifier) != math.copysign(1,sign):
            print(obj.stairid, "and",identity)
            if obj.stairid == identity:
                return obj
        elif identity == -1 and obj.classname == "startstair":
            return obj
    print("FAILED TO FIND STAIR!")
def SaveObjectsToFile(level, objects):
    file = open("worlds/level"+str(level)+".dat","rb+")
    array = pickle.load(file)
    stairnum = pickle.load(file)
    file = open("worlds/level"+str(level)+".dat","wb+")
    pickle.dump(array,file)
    pickle.dump(stairnum,file)
    pickle.dump(objects,file)
def SaveWorldToFile(level, array,numberstairs,objects):     
    file = open("worlds/level"+str(level)+".dat","wb+")
    pickle.dump(array,file)
    pickle.dump(numberstairs,file)
    pickle.dump(objects,file)
def Walkable(posx, posy):
    if posx >= 0 and posx < g_worldSize[0] and posy >= 0 and posy < g_worldSize[1]:
        print(posx,posy)
        return (not Maps.TileSolid(g_activeLevelArray[posx][posy]))
    else:
        return False
def LoadWorldFromFile(level):
    global g_activeLevelArray
    global g_levelNumber
    global g_stairsList
    for x in range(level+1- len(g_stairsList)):
        g_stairsList.append(0)
    if not os.path.isfile("worlds/level"+str(level)+".dat"):
        g_stairsList[level] = CreateLevel(level, g_stairsList[level])
    file = open("worlds/level"+str(level)+".dat", "rb")
    array = pickle.load(file)
    stairnum = pickle.load(file)
    objects = pickle.load(file)
    ClearAllObjects()
    LoadObjectsFromTable(objects)
    g_levelNumber = level
    g_activeLevelArray = array
    Graphics.LoadLevel(array)
    print(objects,"after loading")
    
def ForceNewLevel(level):
    global g_stairsList
    for _ in range(level+1-len(g_stairsList)):
        g_stairsList.append(0)
    g_stairsList[level] = CreateLevel(level, g_stairsList[level])
    
def CreateLevel(level,stairarray):
    global entities
    global g_stairsList
    tupleinfo = None
    print(g_stairsList, "stairs")
    if level == 0:
        tupleInfo = Maps.GenerateLevel(level, 0)
    else:
        tupleInfo = Maps.GenerateLevel(level, g_stairsList[level-1])
    array = tupleInfo[0]
    numberstairs = tupleInfo[1]
    SaveWorldToFile(level, array, numberstairs, entities)
    return numberstairs
    
def MovePlayerToLevel(level, player, stair=None):
    global g_levelNumber
    global entities
    player.UnRender()
    SaveObjectsToFile(g_levelNumber, entities)
    LoadWorldFromFile(level)
    g_levelNumber = level
    if stair == None:
        player.SetPos(*StairFromID(-1, -1).position)
    else:
        player.SetPos(*StairFromID(stair.stairid, stair.levelModifier).position)
