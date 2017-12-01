import PyDungeonGraphics as Graphics
import PyDungeonTurns as TurnController
import pygame
g_controllers = []
pygame.font.init()



class Controller():
    #Used for the ability menu; each Controller is one name and button
    def __init__(self, identity):
        g_screenSize = Graphics.GetScreenSize()
        self.position = [0+60*len(g_controllers),g_screenSize[1]-100 ]
        self.name = "---"
        self.id = identity+1
        self.target = print
        self.arguments = ["1"]

    def setName(self, string):
        self.name = string
        g_fontTiny = Graphics.GetFonts()[0]
        g_fontReg = Graphics.GetFonts()[1]
        Graphics.ClearRectInfo(self.position[0],self.position[1],60,60)
        #re-draw selection number
        if string != "":
            sizex, sizey = g_fontTiny.size(str(self.id))
            tempSurf = g_fontTiny.render(str(self.id), 0, (255,255,255))
            Graphics.BlitInfo(tempSurf, self.position[0]+5-sizex/2,self.position[1]+5)
        else:
            sizex, sizey = g_fontTiny.size("")
            tempSurf = g_fontTiny.render("", 0, (255,255,255))
            Graphics.BlitInfo(tempSurf, self.position[0]+5-sizex/2,self.position[1]+5)            

        #draw self.name (the ability name, usually)
        sizex, sizey = g_fontReg.size(string)
        tempSurf = g_fontReg.render(string, 0, (255,255,255))
        Graphics.BlitInfo(tempSurf, self.position[0]+30-sizex/2,self.position[1]+15)

for _ in range(6):
    g_controllers.append(Controller(_))

def ClearAllControls():
    for self in g_controllers:
        Graphics.ClearRectInfo(self.position[0],self.position[1],60,60)        
        self.target = None
        self.arguments = ["Attempted to use empty control!"]
def OpenInventory(obj, start):
    """Opens the mob's inventory, showing items"""
    counter = 0
    if start != None :
        counter = counter + start
    if len(dic) > 6:
        while counter < 4  :
            counter += 1
            g_controllers[counter].setName(dict.keys[counter])
            g_controllers[counter].target = dict[dict.keys[counter]]

def LoadMenuFromIndicator():
    pass

def InteractFunction(activeMob):
    ClearAllControls()
    g_controllers[1].target = LoadMenuFromIndicator
    g_controllers[1].arguments = []
    g_controllers[1].setName("Back")    


def ActivateController(number):
    """Activates the controllers' target with the controllers' arguments"""
    if g_controllers[number].target != None:
        returnFunc = g_controllers[number].target(*g_controllers[number].arguments)
        print(returnFunc, "returned from function",g_controllers[number].target)
        if returnFunc != None:
            ClearAllControls()
            g_controllers[0].setName("Back")
            g_controllers[0].target = returnFunc
            g_controllers[0].arguments = []

def OpenDictInteraction(iterable, start, activator):
    """Iterates through abilities in a list without an object"""
    ClearAllControls()
    abilityIndex = -1
    counter = -1
    if start != None :  
        abilityIndex = abilityIndex + start
    #If we're using multiple pages
    if len(iterable) > 6: 
        while counter < 4:
            counter += 1
            abilityIndex += 1
            #Assign 3 moves
            if dic.keys[counter] != None:
                g_controllers[counter].setName(iterable[abilityIndex].name)
                g_controllers[counter].target = iterable[abilityIndex].Activate 
                g_controllers[counter].arguments = [iterable[abilityIndex], activator]
        #and create the page-scrolling plus back function
        g_controllers[counter].target = OpenDictInteraction
        g_controllers[counter].setName("<")
        if start > 0:
            g_controllers[counter].arguments = [obj, start-4,activator]
        else:            
            g_controllers[counter].arguments = [obj, start,activator]
        counter +=1
        g_controllers[counter].target = OpenDictInteraction
        g_controllers[counter].arguments = [obj, start+4,activator]
        g_controllers[counter].setName(">")
        g_controllers[counter+1].target = LoadMenu
        g_controllers[counter+1].arguments = []
        g_controllers[counter+1].setName("Back")
    else:
        #If we only have one page of abilities, we don't need page functions.
        for ability in iterable:
            counter += 1
            abilityIndex += 1
            g_controllers[counter].setName(iterable[abilityIndex].name)
            g_controllers[counter].target = iterable[abilityIndex].Activate 
            g_controllers[counter].arguments = [iterable[abilityIndex], activator]
        g_controllers[counter+1].target = LoadMenu
        g_controllers[counter+1].arguments = []
        g_controllers[counter+1].setName("Back")
def OpenAbilityDict(obj, start, listName, func="Cast"):
    """Iterates through the object's abilities, assigning controllers"""
    #This is ver similar to the previous function,
    #but making this function modular enough to do what
    #the other does would make this function awkward to
    #use effectively (as most of the repetition is just
    #UI related)
    ClearAllControls()
    abilityList = getattr(obj, listName)
    abilityIndex = -1
    counter = -1
    if start != None :  
        abilityIndex = abilityIndex + start
    #If we're using multiple pages
    if len(abilityList) > 6:
        while counter < 4:
            counter += 1
            abilityIndex += 1
            #Assign 3 moves
            if dic.keys[counter] != None:
                g_controllers[counter].setName(abilityList[abilityIndex].name)
                g_controllers[counter].target = getattr(abilityList[abilityIndex],func)   
                g_controllers[counter].arguments = [obj]
        #and create the page-scrolling plus back function
        g_controllers[counter].target = OpenAbilityDict
        if start <= 0:
            g_controllers[counter].arguments = [obj, start,listName]
        else:
            g_controllers[counter].arguments = [obj, start+4,listName]            
        g_controllers[counter].setName("<")
        g_controllers[counter+1].target = OpenAbilityDict
        g_controllers[counter+1].arguments = [obj, start+4,listName]
        g_controllers[counter+1].setName(">")
        g_controllers[counter+2].target = LoadMenu
        g_controllers[counter+2].arguments = []
        g_controllers[counter+2].setName("Back")
    else:
        #If we only have one page of abilities, we don't need page functions.
        for ability in abilityList:
            counter += 1
            abilityIndex += 1
            g_controllers[counter].setName(abilityList[abilityIndex].name)
            g_controllers[counter].target = getattr(abilityList[abilityIndex],func)  
            g_controllers[counter].arguments = [obj]
        g_controllers[counter+1].target = LoadMenu
        g_controllers[counter+1].arguments = []
        g_controllers[counter+1].setName("Back")


def SetController(key, name, func, args):
    g_controllers[key].target = func
    g_controllers[key].arguments = args
    g_controllers[key].setName(name)
    

def ActivateMenu(key):

    g_controllers[key].target(g_tiles[key].argument)
          
def LoadMenu():
    """Sets up the menu from the start position for the player"""

    activeMob = TurnController.GetActiveMob()
    g_controllers[0].setName("Attack")
    #Do checks to see if the mob actually has something equipped
    if activeMob.equipment["weapon"] != None:
        print(activeMob.equipment["weapon"])
        g_controllers[0].target = OpenAbilityDict
        g_controllers[0].arguments = [TurnController.GetActiveMob().equipment["weapon"],0,"abilities"]
    else:
        g_controllers[0].target = None
        g_controllers[0].arguments = ["Attempted to use nonexistent weapon!"]
        
    g_controllers[1].setName("Offhand")
    if activeMob.equipment["offhand"] != None:
        g_controllers[1].target = OpenAbilityDict
        g_controllers[1].arguments = [TurnController.GetActiveMob().equipment["offhand"],0,"abilities"]
    else:
        g_controllers[1].target = None
        g_controllers[1].arguments = ["Attempted to use nonexistent weapon!"]
    g_controllers[2].setName("Cast")
    g_controllers[2].target = OpenAbilityDict 
    g_controllers[2].arguments = [TurnController.GetActiveMob(),0,"abilities"]
    g_controllers[3].setName("Interact")
    g_controllers[3].target = OpenAbilityDict
    g_controllers[3].arguments = [TurnController.GetActiveMob(),0,"interactions"]
    g_controllers[4].setName("Inventory")
    if activeMob.equipment["weapon"] != None:
        g_controllers[4].target = OpenInventory 
        g_controllers[4].arguments = [TurnController.GetActiveMob().equipment["weapon"],0,"abilities"]
    else:
        g_controllers[4].target = None
        g_controllers[4].arguments = ["Attempted to use nonexistent weapon!"]

def UnLoadMenu():
    """Disables the controllers and removes their name."""
    g_controllers[0].setName("")
    g_controllers[0].target = None 
    g_controllers[1].setName("")
    g_controllers[1].target = None 
    g_controllers[2].setName("")
    g_controllers[2].target = None 
    g_controllers[3].setName("")
    g_controllers[3].target = None 
    g_controllers[4].setName("")
    g_controllers[4].target = None 
    g_controllers[5].setName("")
    g_controllers[5].target = None 

