import PyDungeonWorld as World

activeMobID = 0
activeMob = None 
playerActive = False
turnDelay = 0
turnWaiting = False
def GetActiveMob():
    """Returns the active Mob"""
    return activeMob

def PlayerActive():
    """Returns if player is active"""
    return playerActive
def EndTurn():
    """Chooses the next mob to take a turn"""
    global turnWaiting
    turnWaiting = False
def EndTurnPlayer():
    """Chooses the next mob to take a turn"""
    global turnWaiting
    global playerActive
    turnWaiting = False
    playerActive = False
def NextTurn():
    """If we're not waiting on a mob, starts the next turn."""
    global playerActive
    global turnWaiting
    global activeMob
    global turnDelay
    if turnDelay == 0:
        if not playerActive and not turnWaiting:
            turnWaiting = True
            turnReady = False
            while not turnReady:
                for mob in World.mobs:
                    activeMobID = mob.mobID
                    activeMob = mob
                    playerActive = activeMob.playerInput
                    mob.turnTimer += mob.attributes["Speed"]
                    if mob.turnTimer >= 1000:
                        mob.turnTimer -= 1000
                        turnReady = True
                        turnWaiting = False
                        if mob.playerInput:
                            playerActive = True
                        print(mob,"Selected")
                        mob.TakeTurn()
def TickTurnDelay(times=1):
    global turnDelay
    if turnDelay > 0:
        turnDelay -= times
def AddTurnDelay(number=10):
    global turnDelay
    turnDelay += number
