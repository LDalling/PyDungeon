import random
import math
import numpy
import PyDungeonGraphics as Graphics
import PyDungeonControls as Controls
import PyDungeonWorld as World
from PyDungeonTurns import *
g_abilityRunning = 0
abilities = {}
g_targetingOffset = [0,0]
g_targetingReference = None

def Normalize(toNormal):
    """Returns a vector with the same direction as input, but with a magnitude of one"""
    distance = 0
    for value in toNormal:
        if value <= 0:
            distance -= value
        else:
            distance += value
    if distance > 0:
        for index in range(len(toNormal)):
            toNormal[index] = toNormal[index]/distance
    return toNormal

def SumVelocity(toNormal):
    """Returns the magnitude of a vector"""
    distance = 0
    for value in toNormal:
        if value <= 0:
            distance -= value
        else:
            distance += value
    return distance
def Distance(vector):
    """Returns the triangulated distance of a vector"""
    return math.sqrt(vector[0]**2 + vector[1]**2)
class AbilityEffect():
    def Activate(self,caster):
        """Rewritable function for the ability affect"""
        print("Active!")
    def Cast(self,caster, targetinfo):
        """Rewritable function, for when targeting is done"""
        
    def Finish(self,caster):
        """handles player/AI mob turn finishing"""
        activeMob.turnTimer -= 1000
        if activeMob.turnTimer < 1000:
            if activeMob.playerInput:
                print("Player is now tired!")

class TargetingRules(): #Used to store how spells may be cast
    def __init__(self,pattern,patternDir,maxRange,mob,ability):
        self.pattern = pattern
        self.patternDirectional = patternDir
        self.maxRange = maxRange
        self.mobOwner = mob
        self.ability = ability
        print(mob.GetPos(),"stored as targetingrules")

    def Cast(self, offset):
        self.ability.Cast(self,offset)

def ReDrawTargetting():
    global g_targetingReference
    if g_targetingReference.patternDirectional: #if we have diagonal pattern differences
        pass
    else:
        mobPos = GetActiveMob().position
        print(GetActiveMob())
        Graphics.ClearTargetArray()
        maxRange = g_targetingReference.maxRange
        #starting position of the iteration (to save repeatedly re-calculating it)
        startX = (mobPos[0]-maxRange)
        startY = (mobPos[1]-maxRange)
        shape = g_targetingReference.pattern.shape
        pattern = g_targetingReference.pattern
        shapeOffset = -(shape[0]-1)/2
        if shape[0] == shape[1] and shape[0] % 2 == 1:
            for x in range(maxRange*2+1):
                for y in range(maxRange*2+1):
                    Graphics.UpdateTargetIndicator(startX+x,startY+y, 1)
            for x in range(shape[0]):
                for y in range(shape[1]):
                    Graphics.UpdateTargetIndicator(mobPos[0]+shapeOffset+g_targetingOffset[0]+x,mobPos[1]+shapeOffset+g_targetingOffset[1]+y, pattern[x][y])
        elif shape[0] == shape[1]:
            print("ABILITY PATTERN MUST HAVE A CENTRE!")
        else:
            print("ABILITY PATTERN MUST BE SQUARE!")
        
def EscapeAreaSelect():
    global g_abilityRunning
    g_abilityRunning = 0
    g_targetingReference = None
    Graphics.ClearTargetArray()
    Controls.LoadMenu()
def HandleMoveKey(dirX, dirY):
    global playerActive
    global g_targetingReference
    global g_abilityRunning
    if PlayerActive() == True:
        if g_abilityRunning == 1: #Single-target spell (range needed)
            pass
        elif g_abilityRunning == 2: #Ground-target spell (AoE indicators needed)
            maxRange = g_targetingReference.maxRange
            g_targetingOffset[0] = max(-maxRange,min(g_targetingOffset[0]+dirX,maxRange))
            g_targetingOffset[1] = max(-maxRange,min(g_targetingOffset[1]+dirY,maxRange))
            ReDrawTargetting()
        else:
            print("walking!")
            GetActiveMob().Walk(dirX, dirY)

def HandleConfirmation():
    global playerActive
    global g_targetingReference
    global g_targetingOffset
    if PlayerActive() == True:
        if g_targetingReference != None:
            EscapeAreaSelect()
            g_targetingReference.Cast(g_targetingOffset)
            g_targetingReference = None
            
                        
def TargetSelect(distance, caster,ability):
    """Do selection for mob-specific targeting"""
    print("Selecting one target!")
    #I'll want to check if the AI is casting this or not
def AreaSelect(distance,patterns,patternsDir, caster,ability):
    """Do selection for ground-based targeting"""
    global g_targetingReference
    global g_targetingOffset
    if PlayerActive():
        Controls.ClearAllControls()
        Controls.SetController(0,"Cancel",EscapeAreaSelect,[])
        global g_abilityRunning
        g_abilityRunning = 2
        g_targetingOffset = [0,0]
        g_targetingReference = TargetingRules(patterns,patternsDir, distance, caster, ability)
        print(GetActiveMob().GetPos())
        # I use the global references so that the game can start asynchronous
        # directional input while still processing graphics
        #(it'd be hard passing values otherwise)
        print("Selecting AOE target!")
        ReDrawTargetting()
    else:
        pass
    #AI area selection goes here

class Suicide(AbilityEffect):
    def __init__(self):
        self.name = "Suicide"
    def Activate(ability,self):
        for i in range(60):
            angleRad = (random.randint(0,360))/180*math.pi
            spark = Graphics.ParticleBlood()
            spark.velocity = [math.sin(angleRad)*random.randint(4,20),math.cos(angleRad)*random.randint(4,20)]
            spark.SetPos(Graphics.PosPixels(self.position),[0,0],[2,2])
        for i in range(80):
            angleRad = (random.randint(0,360))/180*math.pi
            spark = Graphics.ParticleBloodSmall()
            spark.velocity = [math.sin(angleRad)*random.randint(4,20),math.cos(angleRad)*random.randint(4,20)]
            spark.SetPos(Graphics.PosPixels(self.position),[0,0],[2,2])
        self.UnRender()
        print(self,"Suicided.")
abilities["suicide"] = Suicide()

class PoisonBolt(AbilityEffect):
    def __init__(self):
        self.name = "Poison Bolt"
    def Activate(ability,caster):
        for i in range(80):
            angleRad = (random.randint(0,360))/180*math.pi
            spark = Graphics.ParticleBloodSmall()
            spark.velocity = [math.sin(angleRad)*random.randint(4,20),math.cos(angleRad)*random.randint(4,20)]
            spark.SetPos(Graphics.PosPixels(self.position),[0,0],[2,2])
abilities["poisonbolt"] = PoisonBolt()

class Fireball(AbilityEffect):
    def __init__(self):
        self.name = "Fireball"
    def Activate(ability,caster):
        splash = numpy.array([[3]])
        Controls.ClearAllControls()
        print(caster.GetPos(),"fired")
        Controls.SetController(0,"Cancel",EscapeAreaSelect,[])
        pos = AreaSelect(10, splash,False, caster,ability)
        
    def Cast(self, targettinginfo, offset):
        castFrom = targettinginfo.mobOwner.position
        castTo = offset
        print("castTo is ",castTo)
        tile_size = Graphics.GetTileSize()
        distance = [castTo[0]*tile_size,castTo[1]*tile_size]
        velo = Normalize(offset)
        print(velo, "is prior velo")
        velo[0] = (distance[0]/15)
        velo[1] = (distance[1]/15)
        print(velo, "is post velo")
        lifeTime = 15
        ball = Graphics.ParticleFireball(lifeTime)
        ball.velocity = velo
        ball.SetPos(Graphics.PosPixels(castFrom),[0,0],[0,0])
        AddTurnDelay(lifeTime)
        targettinginfo.mobOwner.EndTurn()
        
abilities["fireball"] = Fireball()


class MagicMissile(AbilityEffect):
    def __init__(self):
        self.name = "Magic Mis."
    def Activate(ability,caster):
        splash = numpy.array([[3]])
        pos = AreaSelect(10, splash,False, caster,ability)
        
    def Cast(self, targettinginfo, offset):
        castFrom = targettinginfo.mobOwner.position
        castTo = offset
        print("castTo is ",castTo)
        tile_size = Graphics.GetTileSize()
        distance = [castTo[0]*tile_size,castTo[1]*tile_size]
        velo = Normalize(offset)
        print(velo, "is prior velo")
        velo[0] = (distance[0]/15)
        velo[1] = (distance[1]/15)
        print(velo, "is post velo")
        lifeTime = 15
        ball = Graphics.ParticleMagicMissile(lifeTime)
        ball.velocity = velo
        ball.SetPos(Graphics.PosPixels(castFrom),[0,0],[0,0])
        AddTurnDelay(lifeTime)
        targettinginfo.mobOwner.EndTurn()
        
abilities["magicmissile"] = MagicMissile()

class Firebomb(AbilityEffect):
    def __init__(self):
        self.name = "Firebomb"
    def Activate(ability,caster):
        splash = numpy.array([[0,2,0],[2,3,2],[0,2,0]])
        pos = AreaSelect(10, splash,False, caster,ability)
        
    def Cast(self, targettinginfo, offset):
        castFrom = targettinginfo.mobOwner.position
        castTo = offset
        tile_size = Graphics.GetTileSize()
        distance = [castTo[0]*tile_size,castTo[1]*tile_size]
        velo = Normalize(offset)
        velo[0] = (distance[0]/15)
        velo[1] = (distance[1]/15)
        lifeTime = 15
        ball = Graphics.ParticleFirebomb(lifeTime)
        ball.velocity = velo
        ball.SetPos(Graphics.PosPixels(castFrom),[0,0],[0,0])
        targettinginfo.mobOwner.EndTurn()
        
abilities["firebomb"] = Firebomb()

def GetAbility(name):
    newability = Ability(abilities[name])
    return newability

class Ability():
    def __init__(self,Ability):
        self.cooldown = 0
        self.name = Ability.name
        self.ability = Ability
    def Cast(self,caster):
        self.ability.Activate(caster)
        
class Interact(AbilityEffect):
    def __init__(self):
        self.name = "Interact"
    def Activate(ability,self):
        splash = numpy.array([[3]])
        pos = AreaSelect(1, splash,False, self,ability)
        print(self,"is interacting.")
    def Cast(self,targettinginfo,offset):
        castFrom = targettinginfo.mobOwner.position
        chosenTile = numpy.add(castFrom,offset)
        if PlayerActive():
            objList = World.GetInteractablesFromPosition(chosenTile)
            if len(objList) > 0:
                Controls.OpenDictInteraction(objList,0, targettinginfo.mobOwner)
            else:
                Controls.LoadMenu()
        
abilities["interact"] = Interact()
        
class TakeStairs(AbilityEffect):
    def __init__(self):
        self.name = "Travel"
    def Activate(ability,player,self):
        World.MovePlayerToLevel(World.ActiveLevel()+self.levelModifier,player,self)
        print("activated")
        ##
        #
        #
        #
        ## REMEMBER: STAIRCASES MAY BE GENERATED WITHIN EACH OTHEr
        #
        #
        #
        ##
abilities["takestairs"] = TakeStairs()

class LeaveStairs(AbilityEffect):
    def __init__(self):
        self.name = "Travel"
    def Activate(ability,player,self):
        World.MovePlayerToLevel(World.ActiveLevel()+self.levelModifier,player,self)
abilities["leavestairs"] = LeaveStairs()
