import PyDungeonWorld as World
import PyDungeonAbilities as AbilityLib
import PyDungeonControls as Controls
import PyDungeonGraphics as Graphics
import PyDungeonTurns as Turns
mobTable = {}
def CreateObject(name):
    return mobTable[name]()   
def RenderAll():
    for obj in World.GiveObjectTable():
        if obj != False:
            obj.Render()
    for mob in World.GiveMobTable():
        if mob != False:
            mob.Render()
    for item in World.GiveItemTable():
        if item != False:
            item.Render()
def Ability(name):
    return AbilityLib.GetAbility(name)
class Mob:
    
    def __init__(self):
        print("init called")
        #IDs for explicit calls and multi-turn effects
        self.ID = World.AssignEntityID(self)
        self.mobID = World.AssignMobID(self)

        #Game-related variables
        self.position = [0,0]
        
        self.turnTimer = 0
        self.spriteID = 0

        self.attributes = {"Health":5, "MaxHP":5, "Speed":500, "Strength":0,"Agility":0,"Intelligence":0,"Constitution":0}
        self.powers = {}
        self.equipment = {"weapon": None,"offhand": None,"weapon": None }
        self.abilities = []
        self.interactions = []
        self.inventory = []
        self.playerInput = False
        self.perpetual = False

        self.team = "Unassigned"
        self.name = "Unknown Stranger"
    def Render(self):
        Graphics.renderSprite(self)
    def UnRender(self):
        Graphics.UnRenderMob(self)
    def SetPos(self, newX, newY = None):
        """Sets the mob's position in the world without triggering stuff"""
        self.UnRender()
        if newY == None:
            self.position = newX
        else:
            self.position = [newX, newY]
        self.Render()
        return True

    def NewID(self):
        self.ID = World.AssignEntityID(self)
        self.mobID = World.AssignMobID(self)
    def Walk(self, dirX, dirY):
        """Makes the mob attempt to step this way"""
        if World.Walkable(self.position[0]+dirX, self.position[1]+dirY):
            self.UnRender()
            self.position = [self.position[0]+dirX, self.position[1]+dirY]
            self.Render()
            self.EndTurn()
            return True
        else:
            return False
    def EndTurn(self):
        print("end turn")
        if self.playerInput:
            print("player over")
            Turns.EndTurnPlayer()
        else:
            Turns.EndTurn()

    def WalkTo(self, newX, newY):
        """Makes the mob attempt to walk to this position, step by step."""
        self.UnRender()
        self.Render()
        self.EndTurn()

        
    def TeleportTo(self, newX, newY):
        """Makes the mob move to the specified position in one move."""
        self.UnRender()
        self.Render()
    def UseItem(self, itemID):
        """Activates the 'Activate()' function of the specified item."""
        Objects[itemID].Activate()

    def EquipItem(self, itemID):
        """Attempts to equip the item into its' assigned slot."""
    #equip

    def PerformAbility(self, ability):
        """Makes the mob perform the selected ability."""
    #perform relevant ability

    def HandleDamage(self, damageinfo):
        """Mobs may rewrite this function to change damage handling."""

    def TakeDamage(self, damageinfo):
        """Performs damage calculations."""

    def AssignStats(self, stats):
        """Modifies stats of mob, applying relevant bonuses and refreshing them to full."""
        self.attributes = stats
        self.attributes["MaxHealth"] = 5+stats["Constitution"]*2
        self.attributes["Health"] = self.attributes["MaxHealth"]
        
    def ModifyStats(self, modstats):
        """Changes stats of existing mob without recalculating variables."""
        for index in modstats.keys():
            self.attributes[index] = modstats[index]
    def TakeTurn(self):
        """Modifiable function to deal with AI turn-taking"""
    def Kill(self):
        """How the mob dies"""
        self.UnRender()
        del self 
        


class Player(Mob):
    classType = "mob"
    def __init__(self): 
        Mob.__init__(self)
        self.spriteID = 16
        self.position = [16,16]
        self.abilities = [Ability("suicide"),Ability("fireball"),Ability("firebomb")]
        self.interactions = [Ability("interact")]
        self.perpetual = True
        print("Created with",self.abilities)
        self.playerInput = True
    def TakeTurn(self):
        print("Player turn")
        Controls.LoadMenu()
    def EndTurn(self):
        Controls.UnLoadMenu()
        Mob.EndTurn(self)
    def SetPos(self,newX,newY):
        print(newX, " for you")
        World.UnrenderAll()
        Mob.SetPos(self,newX,newY)
        Graphics.MoveCamera(self.position)
        World.RenderAll()
    def GetPos(self):
        print(self.position,"is our pos")
        return self.position
    def Kill(self):
        del self        
        
    def Walk(self, dirX, dirY):
        if World.Walkable(self.position[0]+dirX, self.position[1]+dirY):
            World.UnrenderAll()
            self.position = [self.position[0]+dirX, self.position[1]+dirY]
            self.EndTurn()
            Graphics.MoveCamera(self.position)
            World.RenderAll()
            return True
        else:
            return False
        
class Goblin(Mob):

    def __init__(self):
        Mob.__init__(self)
        
        self.maxHealth = 5
        self.health = 5
        self.speed = 500
        self.turnTimer = 0        
        
        self.team = "Goblin"
        self.name = "Goblin"
        Mob.Render(self)
mobTable["goblin"]= Goblin
