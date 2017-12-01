import pygame
import random
import numpy
import math
import PyDungeonGraphics as Graphics
import PyDungeonWorld as World
import PyDungeonMaps as Maps
import PyDungeonAbilities as AbilityLib
import PyDungeonMobs
import PyDungeonItems
import PyDungeonTurns as TurnController
import PyDungeonControls as Controls

g_tiles = [["_"]*500]*500
g_player = PyDungeonMobs.Player()
g_clock = pygame.time.Clock()
g_gameRunning = False
g_volumeLevel = float(0)
print("Loaded modules.")
def QuitGame():
    pygame.mixer.music.stop()
    g_gameRunning = False
    pygame.display.quit()


#Main game
def StartGame():
    World.LoadWorldFromFile(0)
    World.MovePlayerToLevel(0,g_player)
    g_gameRunning = True
    while g_gameRunning == True:
        eventList = pygame.event.get()
        Graphics.RunParticleSystem()
        TurnController.TickTurnDelay()
        TurnController.NextTurn()
        for event in eventList:
            if event.type == pygame.QUIT:
                g_gameRunning = False
                pygame.display.quit()
                break
                
            elif event.type == pygame.KEYDOWN and TurnController.playerActive:
                #Control mapping here
                print(event.key)
                if event.key == 257: #DL
                    AbilityLib.HandleMoveKey(-1,1)                
                elif event.key == 258: #down
                    AbilityLib.HandleMoveKey(0,1)   
                elif event.key == 259: #DR
                    AbilityLib.HandleMoveKey(1,1)   
                elif event.key == 260: #L
                    AbilityLib.HandleMoveKey(-1,0)   
                elif event.key == 261: #STAY
                    AbilityLib.HandleMoveKey(0,0)   
                elif event.key == 262: #R
                    AbilityLib.HandleMoveKey(1,0)   
                elif event.key == 263: #UL
                    AbilityLib.HandleMoveKey(-1,-1)   
                elif event.key == 264: #U
                    AbilityLib.HandleMoveKey(0,-1)   
                elif event.key == 265: #UR
                    AbilityLib.HandleMoveKey(1,-1)   
                elif event.key == 273: #up
                    AbilityLib.HandleMoveKey(0,-1)   
                elif event.key == 274: #down
                    AbilityLib.HandleMoveKey(0,1)                
                elif  event.key == 275: #right
                    AbilityLib.HandleMoveKey(1,0)                
                elif  event.key == 276: #left
                    AbilityLib.HandleMoveKey(-1,0)
                elif  event.key == 13 or event.key == 271: #enter
                    AbilityLib.HandleConfirmation() 
                elif  event.key == 49: #1
                    Controls.ActivateController(0)
                elif  event.key == 50: #2
                    Controls.ActivateController(1)
                elif  event.key == 51: #3
                    Controls.ActivateController(2)
                elif  event.key == 52: #4
                    Controls.ActivateController(3)
                elif  event.key == 53: #5
                    Controls.ActivateController(4)
                elif  event.key == 54: #6
                    Controls.ActivateController(5)
                elif  event.key == 55: #7
                    print("Cleared!!!")
                    World.ClearAllObjects()
                if event.key == 53: #8
                    pass               
                if event.key == 53: #9
                    pass       
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Create some random blood splatters
                angle = random.randint(1,360)
                for i in range(1):
                    angleRad = (angle+i*random.randint(3, 8))/180*math.pi
                    spark = Graphics.ParticleBlood()
                    x,y = pygame.mouse.get_pos()
                    spark.velocity = [math.sin(angleRad)*random.randint(4,12),math.cos(angleRad)*random.randint(4,12)]
                    spark.SetPos([x,y],[0,0],[2,2])
                for i in range(2):
                    angleRad = (angle+i*random.randint(-8, 8))/180*math.pi
                    spark = Graphics.ParticleBloodSmall()
                    x,y = pygame.mouse.get_pos()
                    spark.velocity = [math.sin(angleRad)*random.randint(4,12),math.cos(angleRad)*random.randint(4,12)]
                    spark.SetPos([x,y],[0,0],[2,2])  
        g_clock.tick(60)


print("starting main")
def main():
    logo = pygame.sprite.Sprite()
    pygame.mixer.init()
    pygame.mixer.music.load("Title.ogg")
    pygame.mixer.music.set_volume(g_volumeLevel)
    pygame.mixer.music.play()
    global g_gameRunning
    menuFont = Graphics.GetFonts()[1]
    resolution = Graphics.GetResolution()
    menuRunning = True
    def RunGame():
        pygame.mixer.music.stop()
        g_gameRunning = True
        for option in range(len(menuOptions)):
            sizex, sizey = menuFont.size(str(menuOptions[option][0]))
            Graphics.ClearRectInfo(math.floor((resolution[0]-sizex)/2), math.floor((resolution[1]/2)-100+(option*20)), sizex,sizey )
        StartGame()
    print("main started")
    menuOptions = [["Start game!", RunGame], ["Exit",QuitGame]]

    print("main")
    
    Graphics.RunParticleSystem()
    def DrawMainMenu(menuRunning):
        global g_volumeLevel    
        colorChoice = [255,255,255]
        tempSurf = menuFont.render("Music by Dan George", 0, colorChoice)
        Graphics.BlitInfo(tempSurf, math.floor((resolution[0])/2)-63, resolution[1]-100)     

        selectedOption = 0
        while menuRunning:
            eventList = pygame.event.get()
            colorChoice = [255,255,255]
            for option in range(len(menuOptions)):
                sizex, sizey = menuFont.size(str(menuOptions[option][0]))
                Graphics.ClearRectInfo(math.floor((resolution[0]-sizex)/2), math.floor((resolution[1]/2)-100+(option*20)), sizex,sizey )
                colorChoice = [255,255,255]
                if option == selectedOption:
                    colorChoice = [255,0,0]
                tempSurf = menuFont.render(str(menuOptions[option][0]), 0, colorChoice)
                Graphics.BlitInfo(tempSurf, math.floor((resolution[0]-sizex)/2), math.floor((resolution[1]/2)-100+(option*20)))     
            Graphics.RunParticleSystem()
            for event in eventList:
                if event.type == pygame.QUIT:
                    menuRunning = False
                    pygame.mixer.music.stop()
                    pygame.display.quit()
                    break
                    
                elif event.type == pygame.KEYDOWN:
                    #Control mapping here
                    print(event.key)
                    if event.key == 273: #up
                        selectedOption -= 1
                        selectedOption = selectedOption%len(menuOptions)
                    elif event.key == 274: #down         
                        selectedOption += 1
                        selectedOption = selectedOption%len(menuOptions)
                    elif  event.key == 275: #right
                        pass
                    elif  event.key == 276: #left
                        pass
                    elif  event.key == 13 or event.key == 271: #enter
                        menuRunning = False
                        menuOptions[selectedOption][1]()

            if g_volumeLevel < 1:
                g_volumeLevel += .002
                pygame.mixer.music.set_volume(g_volumeLevel)
            
            g_clock.tick(40)
    DrawMainMenu(menuRunning)
main()


