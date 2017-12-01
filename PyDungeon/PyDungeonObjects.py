import PyDungeonWorld as World
import PyDungeonGraphics as Graphics
import PyDungeonAbilities as AbilityLib
def Ability(name):
    return AbilityLib.GetAbility(name)
objTable = {}
def CreateObject(name):
    return objTable[name]

class Object():
    classType = "object"
    def __init__(self):
        self.name = "NULLOBJ"
        self.id = World.AssignEntityID(self)
        self.objectid = World.AssignObjectID(self)
        self.position = [0,0]
        self.isSolid = False
        self.perpetual = False
        self.classname = "unidentified"
        self.interactions = []
        self.spriteID = 255
    def NewID(self):
        self.id = World.AssignEntityID(self)
        self.objectid = World.AssignObjectID(self)
    def Render(self):
        Graphics.renderSprite(self)
    def UnRender(self):
        Graphics.UnRenderMob(self)
    def Delete(self):
        World.DeleteObject(self)
        del self

class StairCase(Object):
    def __init__(self,identity, direction):
        Object.__init__(self)
        self.isSolid = False
        self.stairid = identity
        self.name = "Staircase"
        self.classname = "staircase"
        self.levelModifier = direction
        self.abilities = [Ability("takestairs")]
        if direction > 0:
            self.spriteID = 82
        else:
            self.spriteID = 83
    def Activate(controllerused, self, activator):
        self.abilities[0].ability.Activate(activator,self)
        
objTable["staircase"] = StairCase
class TopStairCase(Object):
    def __init__(self):
        Object.__init__(self)
        self.name = "Exit"
        self.isSolid = False
        self.classname = "startstair"
        self.interactions = [Ability("leavestairs")]
        self.spriteID = 83
        
    def Activate(controllerused, self, activator):
        self.abilities[0].ability.Activate(activator,self)
objTable["topstaircase"] = TopStairCase

class OpenDoor(Object):
    def __init__(self):
        Object.__init__(self)
        self.isSolid = False
        self.classname = "dooropen"
        self.name = "Door"
        self.spriteID = 81
    def Activate(controllerused, self, activator):
        newdoor = ClosedDoor()
        newdoor.position = self.position        
        self.UnRender()
        newdoor.Render()
        self.Delete()
objTable["dooropen"] = OpenDoor

class LockedDoor(Object):
    def __init__(self):
        Object.__init__(self)
        self.isSolid = True
        self.classname = "doorlocked"
        self.name = "Door"
        self.spriteID = 80
    def Activate(controllerused, self, activator):
        pass
objTable["doorlocked"] = LockedDoor

class ClosedDoor(Object):
    def __init__(self):
        Object.__init__(self)
        self.isSolid = True
        self.classname = "door"
        self.name = "Door"
        self.abilities = []
        self.spriteID = 80
    def Activate(controllerused, self, activator):
        newdoor = OpenDoor()
        newdoor.position = self.position        
        self.UnRender()
        newdoor.Render()
        self.Delete()
        
objTable["door"] = ClosedDoor

