import random
import math
import os
import pygame
import numpy
import PyDungeonOptions as Options
particleList = []


level_dimensions = [150,50]
tile_size = 16
tiles_x = 31
tiles_y = 31
level_dimensionsPixel = [level_dimensions[0]*tile_size,level_dimensions[1]*tile_size]
viewport_dimensionsPixel = [tiles_y*tile_size,tiles_x*tile_size]

screen_width = tile_size*tiles_x
screen_height = tile_size*tiles_x + 100
screen = pygame.display.set_mode([screen_width, screen_height],pygame.SRCALPHA,32)
screenarray = pygame.surfarray.array3d(screen)
g_levelSurf = pygame.Surface([tile_size*level_dimensions[0],tile_size*level_dimensions[1]])
g_levelArray = pygame.surfarray.pixels3d(g_levelSurf)
g_levelTiles = numpy.array([[1]*level_dimensions[1]]*level_dimensions[0])
g_particleSurf = pygame.Surface([tile_size*tiles_x,tile_size*tiles_y], 24)
g_particleArray = pygame.surfarray.pixels3d(g_particleSurf)
g_floorSurf = pygame.Surface([tile_size*tiles_x,tile_size*tiles_y],32)
g_mobSurf = pygame.Surface([screen_width,screen_height],32)
g_mobSurf.fill((127,127,127))
g_infoSurf = pygame.Surface([screen_width,screen_height],32)
g_infoSurf.fill((255,0,0),pygame.Rect(0,0,screen_width,screen_height))
g_targetSurf = pygame.Surface([tile_size*tiles_x,tile_size*tiles_y],32)
g_targetArray = pygame.surfarray.pixels3d(g_targetSurf)
g_spriteSSurf = pygame.image.load("tiles.png") #spritesheet surface
g_spriteSSize = g_spriteSSurf.get_size()
g_spriteArray = pygame.surfarray.pixels3d(g_spriteSSurf)
g_cameraPos = [0,0]
g_targetColor = (0,255,0)

def SetupFromOptions():
#for later
    Options.GetTiles()

    
def GetTileSize():
    return tile_size
def GetFonts():
    g_fontReg = pygame.font.SysFont("Lucida Console", 10)
    g_fontTiny = pygame.font.SysFont("Lucida Console", 7)
    return (g_fontTiny, g_fontReg)
def GetResolution():
    return [screen_width, screen_height]
def LocalToWorld(pos):
    """Local tile to world tile"""
    return [g_cameraPos[0]-math.floor(tiles_x/2)+pos[0],pos[1]+g_cameraPos[1]-math.floor(tiles_y/2)]
def WorldToLocal(pos):
    """World tile to local tile"""
    return [pos[0]-(g_cameraPos[0]-math.floor(tiles_x/2)), pos[1]-(g_cameraPos[1]-math.floor(tiles_y/2)) ]

def LocalToWorldPixel(pos):
    """Local pixel to world pixel"""
    return [(g_cameraPos[0]-math.floor(tiles_x/2))*tile_size+pos[0],(g_cameraPos[1]-math.floor(tiles_y/2))*tile_size+pos[1]]
def WorldToLocalPixel(pos):
    """World pixel to local pixel"""
    return [int(pos[0]-(g_cameraPos[0]-math.floor(tiles_x/2))*tile_size), int(pos[1]-(g_cameraPos[1]-math.floor(tiles_y/2))*tile_size) ]

def PosPixels(pos):
    midway = math.floor(tile_size/2)
    return (pos[0]*tile_size+midway, pos[1]*tile_size+midway)
    
def BlitInfo(surface,x,y):
    surface.set_colorkey((0,0,0))
    g_infoSurf.blit(surface, (x,y), None)
def GetScreenSize():
    return [screen_width,screen_height]

def ClearTargetArray():
    global g_targetArray
    del g_targetArray
    g_targetSurf.fill((0,0,0))
    g_targetArray = pygame.surfarray.pixels3d(g_targetSurf)
    

def UpdateTargetIndicator(tileX,tileY,tiletype):
    g_targetColor = (0,255,0)
    wPos = WorldToLocal((tileX,tileY))
    if wPos[0] >= 0 and wPos[0] < tiles_x and wPos[1] >= 0 and wPos[1] < tiles_y:
        startX = wPos[0]*tile_size# Sort out positions in the world
        startY = wPos[1]*tile_size
        midX = int(startX+math.floor(tile_size/2)-1)
        midY = int(startY+math.floor(tile_size/2)-1)
        g_cameraPos = [0,0]
        if tiletype == 1:
            for x in range(tile_size-1): #if tile is selectable
                g_targetArray[startX+x][startY] = g_targetColor
                g_targetArray[startX+x][startY+tile_size-1] = g_targetColor
                g_targetArray[startX][startY+x] = g_targetColor
                g_targetArray[startX+tile_size-1][startY+x+1] = g_targetColor
                
        if tiletype > 1: #If tile is in AoE
            for x2 in range(6):
                g_targetArray[midX-2+x2][midY-2] = g_targetColor
                g_targetArray[midX+3][midY-2+x2] = g_targetColor
                g_targetArray[midX-2+x2][midY+3] = g_targetColor
                g_targetArray[midX-2][midY+3-x2] = g_targetColor
                
        if tiletype > 2: #If tile is selected
            g_targetArray[midX][midY] = g_targetColor
            g_targetArray[midX][midY+1] = g_targetColor
            g_targetArray[midX+1][midY] = g_targetColor
            g_targetArray[midX+1][midY+1] = g_targetColor
                

            
        
     

def FillTile(array, localTileX, localTileY, color=[0,0,0]):
        x1 = (localTileX)*tile_size
        y1 = (localTileY)*tile_size
        for x in range(tile_size):
            for y in range(tile_size):
                array[x+x1][y+y1] = color
def TileFloor(array, localTileX, localTileY):
        #"""Renders the specified tile, uses world position"""
        #nextColor and outerColor are used to decide what color will be drawn to this tile
        nextColor = [0,0,0]
        outerColor = [0,0,0]
        worldPos = LocalToWorld([localTileX,localTileY])
        tilex = math.floor(worldPos[0])
        tiley = math.floor(worldPos[1])
        #Pick the tiles' color based upon the number assigned to it
        x1 = (localTileX)*tile_size
        y1 = (localTileY)*tile_size
        wx1 = (tilex)*tile_size
        wy1 = (tiley)*tile_size
        #print("Drawing tile",x1/tile_size,",",y1/tile_size,"with value from",[tilex,tiley],"after",[localTileX,localTileY])
        #Draw the tile
        """for x in range(tile_size):
            array[x1+x][y1] = outerColor
            array[x1+x][y1+tile_size-1] = outerColor
        for y in range(tile_size):
            array[x1][y1+y] = outerColor
            array[x1+tile_size-1][y1+y] = outerColor"""
        for x in range(tile_size):
            for y in range(tile_size):
                array[x+x1][y+y1] = g_levelArray[wx1+x][wy1+y]
                
def ReRenderCamera():
    """Renders the entire camera perspective (Slowly)"""
    g_floorArray = pygame.surfarray.pixels3d(g_floorSurf)
    for xpos in range(tiles_x):
        for ypos in range(tiles_y):
            TileFloor(g_floorArray,xpos,ypos)
    pygame.display.flip()

def MoveCamera(posref):
    """Renders the levelarray from the camera's perspective, based on positional input"""
    global g_cameraPos
    global g_floorSurf
    pos = posref[:]
    g_floorArray =  pygame.surfarray.array3d(g_floorSurf)
    g_particleArray =  pygame.surfarray.array3d(g_particleSurf)

    
    #pos is the new position of the camera, limited within bounds (so that it doesn't scroll off-screen)
    pos[0] = max(math.floor(tiles_x/2), min(math.floor(pos[0]), level_dimensions[0]-math.ceil(tiles_x/2)))
    pos[1] = max(math.floor(tiles_y/2), min(math.floor(pos[1]), level_dimensions[1]-math.ceil(tiles_y/2)))

    #Get the difference between the current camera position and the new one
    movementHorizontal = g_cameraPos[0]-pos[0]
    movementVertical = g_cameraPos[1]-pos[1]
    g_cameraPos[0] = max(tiles_x/2, min(math.floor(pos[0]), level_dimensions[0]-math.ceil(tiles_x/2)))
    g_cameraPos[1] = max(tiles_y/2, min(math.floor(pos[1]), level_dimensions[1]-math.ceil(tiles_y/2)))

    #Roll the viewport arrays based on the number of squares moved.
    g_floorArray=numpy.roll(g_floorArray,int(movementHorizontal*tile_size),axis=0)
    g_floorArray=numpy.roll(g_floorArray,int(movementVertical*tile_size),axis=1)
    g_particleArray=numpy.roll(g_particleArray,int(movementHorizontal*tile_size),axis=0)
    g_particleArray=numpy.roll(g_particleArray,int(movementVertical*tile_size),axis=1)
    #print(g_cameraPos, "is drawn")



    #Handle the camera movement horizontally 
    if movementHorizontal < 0:
        #To sum it up: Update each column of tiles that has been moved into
        for xDiff in range(min(tiles_x,abs(movementHorizontal))):
            for i in range(tiles_y):
                TileFloor(g_floorArray,math.floor(tiles_x)-1-xDiff, i)
                FillTile(g_particleArray,math.floor(tiles_x)-1-xDiff, i)
    elif movementHorizontal > 0:
        for xDiff in range(min(tiles_x,abs(movementHorizontal))):
            for i in range(tiles_y):
                TileFloor(g_floorArray,xDiff, i)
                FillTile(g_particleArray,xDiff, i)
    #Handle the camera movement vertically
    if movementVertical < 0:
        for yDiff in range(min(tiles_y,abs(movementVertical))):
            for i in range(tiles_y):
                TileFloor(g_floorArray,i,math.floor(tiles_y)-1-yDiff)
                FillTile(g_particleArray,i,math.floor(tiles_y)-1-yDiff)
    elif movementVertical > 0:
        for yDiff in range(min(tiles_y,abs(movementVertical))):
            for i in range(tiles_y):
                TileFloor(g_floorArray,i,yDiff)
                FillTile(g_particleArray,i,yDiff)
        
    
    #Now we write the new, updated floor to the appropriate array.
    pygame.surfarray.blit_array(g_floorSurf, g_floorArray)
    pygame.surfarray.blit_array(g_particleSurf, g_particleArray)
    #..and move the camera.
    g_cameraPos = pos[:]

def renderSprite(mob):
    """Renders a specific mob or object"""
    g_mobArray = pygame.surfarray.pixels3d(g_mobSurf)
    #print(g_cameraPos[0],",",g_cameraPos[1], "is camera pos")
    #print(mob.position[0],",",mob.position[1], "is mob pos")
    #Getting the position of the mob's sprite in the spritesheet
    xpos = tile_size*(math.floor(mob.spriteID/(g_spriteSSize[0]/tile_size)))
    ypos = tile_size*(mob.spriteID%(math.floor(g_spriteSSize[1]/tile_size)))

    #...and the position of the sprite in the world
    xtarget = tile_size*(math.floor(tiles_x/2)+(mob.position[0]-g_cameraPos[0]))
    ytarget = tile_size*(math.floor(tiles_y/2)+(mob.position[1]-g_cameraPos[1]))
    if (((mob.position[0] > g_cameraPos[0]-tiles_x/2)and (mob.position[0] < g_cameraPos[0]+tiles_x/2))):
        if (((mob.position[1] > g_cameraPos[1]-tiles_y/2)and (mob.position[1] < g_cameraPos[1]+tiles_y/2))):   
            for x in range(tile_size):
                for y in range(tile_size):
                    g_mobArray[x+xtarget][y+ytarget] = g_spriteArray[xpos+x][ypos+y]
        

        
def UnRenderMob(mob):
    g_mobArray = pygame.surfarray.pixels3d(g_mobSurf)
    xpos = tile_size*(math.floor(mob.spriteID/(g_spriteSSize[1]/tile_size)))
    ypos = tile_size*(mob.spriteID%(math.floor(g_spriteSSize[1]/tile_size)))
    xtarget = tile_size*max(0,min((mob.position[0]-g_cameraPos[0]+math.floor(tiles_x/2)), tiles_x-1))
    ytarget = tile_size*max(0,min((mob.position[1]-g_cameraPos[1]+math.floor(tiles_x/2)), tiles_y-1))
    for x in range(tile_size):
        for y in range(tile_size):
            g_mobArray[x+xtarget][y+ytarget] = (127,127,127)
def ColorParticlePixel(pixx,pixy,color):
    pos = WorldToLocalPixel((pixx,pixy))
    if pos[0] >= 0 and pos[0] < viewport_dimensionsPixel[0] and pos[1] >= 0 and pos[1] < viewport_dimensionsPixel[1]:
        g_particleArray[pos[0],pos[1]] = color
def ColorFloorPixel(pixx,pixy,color):
    modx = pixx%16
    mody = pixy%16
    wPos = [int(pixx),int(pixy)]
    lPos = WorldToLocalPixel([pixx,pixy])
    bounds = g_floorArray.shape
    boundsWorld = g_levelArray.shape
    if (modx != 0 and modx != 15 and mody != 0 and mody != 15) or (color ==(0,0,0)):
        if 0 <= lPos[0] and lPos[0] < bounds[0] and 0 <= lPos[1]  and lPos[1] < bounds[1]:
            g_floorArray[lPos[0],lPos[1]] = color
        if 0 <= wPos[0] and wPos[0] < boundsWorld[0] and 0 <= pixy  and pixy < boundsWorld[1]:
            g_levelArray[wPos[0],wPos[1]] = color 
    else:
        if type(color) == tuple:
            color = list(color)
        color[0] = color[0]*0.8
        color[1] = color[1]*0.8
        color[2] = color[2]*0.8
        pixx = int(pixx)
        pixy = int(pixy)
        if 0 <= lPos[0] and lPos[0] < bounds[0] and 0 <= lPos[1]  and lPos[1] < bounds[1]:
            g_floorArray[lPos[0],lPos[1]] = color
        if 0 <= wPos[0] and wPos[0] < boundsWorld[0] and 0 <= pixy  and pixy < boundsWorld[1]:
            g_levelArray[wPos[0],wPos[1]] = color 

def LoadLevel(level):
    """Loads the level, tile by tile, writing the graphics to the level array"""
    global g_levelTiles
    global g_cameraPos
    g_levelTiles = level
    def tileLevel(tilex, tiley):
        g_levelArray = pygame.surfarray.pixels3d(g_levelSurf)
        nextColor = [0,0,0]
        outerColor = [0,0,0]
        
        #If the tile is a wall, set the color to be darker.
        if level[tilex][tiley] == 1:
            nextColor = [70,70,70]
            outerColor = [50,50,50]
        elif level[tilex][tiley] == 0:
            nextColor = [30,30,30]
            outerColor = [20,20,20]
        elif level[tilex][tiley] == 2:
            nextColor = [85,85,85]
            outerColor = [75,75,75]
        elif level[tilex][tiley] == 3:
            nextColor = [100,100,130]
            outerColor = [80,80,100]
        elif level[tilex][tiley] == 4:
            nextColor = [70,70,70]
            outerColor = [50,50,50]
        elif level[tilex][tiley] == 5:
            nextColor = [30,30,30]
            outerColor = [20,20,20]
        else:
            nextColor = [85,85,85]
            outerColor = [75,75,75]
        x1 = tilex*tile_size
        y1 = tiley*tile_size
        bounds = g_levelArray.shape
        #Draw the tile
        for x in range(tile_size):
                g_levelArray[x1+x][y1] = outerColor
                g_levelArray[x1+x][y1+tile_size-1] = outerColor
        for y in range(tile_size):
            if 0 <= x1 and x1 < bounds[0] and 0 <= y1+y  and y1+y < bounds[1]:
                g_levelArray[x1][y1+y] = outerColor
                g_levelArray[x1+tile_size-1][y1+y] = outerColor
        for x in range(tile_size-2):
            for y in range(tile_size-2):
                if 0 <= x1+x and x1+x < bounds[0] and 0 <= y1  and y1 < bounds[1]:
                    if 0 <= x1 and x1 < bounds[0] and 0 <= y1+y  and y1+y < bounds[1]:
                        g_levelArray[x+1+x1][y+1+y1] = nextColor

    for xpos in range(level_dimensions[0]):
        for ypos in range(level_dimensions[1]):
            tileLevel(xpos,ypos)
    g_cameraPos = [16,16]
    ReRenderCamera()
    pygame.display.flip()
    
    """
    #This code was used for testing and draws the entire level at 50% resolution.
    #The particle rendering should be disabled for this.
    pixPerTile = 8
    xScale = 150*pixPerTile
    yScale = 50*pixPerTile
    tempSurface = pygame.display.set_mode((xScale,yScale))
    for ypos in range(yScale):
        for xpos in range(xScale):
            xTile = math.floor(xpos*2)
            yTile = math.floor(ypos*2)
            color = g_levelArray[xTile][yTile]
            
            if g_levelArray[xTile][yTile] == 1:
                color = (127,127,127)
            elif g_levelArray[xTile][yTile] == 2:
                color = (147,147,147)
            elif g_levelArray[xTile][yTile] == 3:
                color = (255,0,0)
            elif g_levelArray[xTile][yTile] == 4:
                color = (100,100,0)
            elif g_levelArray[xTile][yTile] == 5:
                color = (255,0,255)
            elif g_levelArray[xTile][yTile] == 7:
                color = (0,255,0)
            elif g_levelArray[xTile][yTile] == 8:
                color = (255,255,255)
            else:
                color = (90,90,90)
            tempSurface.set_at((xpos,ypos),color)"""
    pygame.display.flip()
    
def RunParticleSystem():
    g_floorArray =  pygame.surfarray.pixels3d(g_floorSurf)
    global g_floorArray
    global g_particleArray
    global g_targetArray
    for particle in particleList:
        if particle != None:
            particle.Tick()

    #Blitting the arrays to their surfaces
    pygame.surfarray.blit_array(g_floorSurf,g_floorArray)
    pygame.surfarray.blit_array(g_particleSurf,g_particleArray)
    g_particleSurf.set_colorkey((0,0,0))
    g_targetSurf.set_colorkey((0,0,0))
    g_infoSurf.set_colorkey((255,0,0))
    g_mobSurf.set_colorkey((127,127,127))

    #Delete the reference arrays so that we can unlock the surfaces
    del g_floorArray
    del g_particleArray
    del g_targetArray
    screen.blit(g_floorSurf, (0,0), None)
    screen.blit(g_mobSurf, (0,0), None)
    screen.blit(g_targetSurf, (0,0), None)
    screen.blit(g_particleSurf, (0,0), None)
    screen.blit(g_infoSurf, (0,0), None)

    #Bring them back with the new values

    g_floorArray =  pygame.surfarray.pixels3d(g_floorSurf)
    g_particleArray = pygame.surfarray.pixels3d(g_particleSurf)
    g_targetArray = pygame.surfarray.pixels3d(g_targetSurf)

    pygame.display.update()

    g_infoSurf.fill((255,0,0),pygame.Rect(0,0,screen_width,screen_height))
    
def ClearRectInfo(x=None, y=None, w=None, h=None):
    """Clears a rectangle of the screen in the InfoSurface"""
    #used by the controllers to clear them
    if x == None or y == None or w == None or h == None:
        x = 0
        y = 0
        w = g_infoSurf.get_width()
        h = g_infoSurf.get_height()
    
    tempSurf =  pygame.Surface((w,h))
    tempSurf.fill([0,0,0])
    g_infoSurf.set_colorkey(None)
    g_infoSurf.blit(tempSurf, pygame.Rect(x,y,0,0))
    g_infoSurf.set_colorkey((255,0,0))
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

def FirstEmptyParticle():
    """Gets the first free index in the particleList"""
    #Stops the game leaking from blank particle entries
    for index in range(len(particleList)):
        if particleList[index] == None:
            return index
            break
    particleList.append(False)
    return (len(particleList)-1)

class Particle():
    def __init__(self):
        self.ID = FirstEmptyParticle()
        particleList[self.ID] = self
        self.position = [0,0]
        self.velocity = [0.0,0.0]
        self.variance = [0,0]
        self.color = [255,0,255]
        self.prevcolor = [0,0,0]
        self.lifeTime = 5
    def Tick(self):
        """Lowers the lifeTime of the particle by 1, decaying if ready"""
        self.lifeTime = self.lifeTime-1
        if self.lifeTime == 0:
            self.Decay()
    def Decay(self):
        """Clears the particle from memory"""
        particleList[self.ID] = None
        
    def SetPos(self,pos,offset,rand):
        """Sets the position of this particle"""
        xRand =random.randint(-rand[1],rand[1])
        yRand = random.randint(-rand[1],rand[1])
        xPos = pos[0]+(offset[0]*(tile_size/4))+xRand
        yPos = pos[1]+(offset[1]*(tile_size/4))+yRand
        self.position = [xPos, yPos]
        return self.position
    
class ParticleSpark(Particle):

    def __init__(self, parent):
        Particle.__init__(self)
        self.lifeTime = random.randint(3,8)
        self.color = [255,0,0]
        self.width = random.randint(3,5)
        self.velocity = parent.velocity
        
    def Tick(self):
        ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        self.position[0] = self.position[0]+math.floor(self.velocity[0])
        self.position[1] = self.position[1]+math.floor(self.velocity[1])
        self.velocity[0] = self.velocity[0] * 0.8
        self.velocity[1] = self.velocity[1] * 0.8
        ColorParticlePixel(self.position[0],self.position[1],self.color)
        Particle.Tick(self)
    def Decay(self):
        g_particleArray[self.position[0]][self.position[1]] = (0,0,0)
        Particle.Decay(self)



class ParticleBloodSplatter(Particle):

    def __init__(self, parent):
        Particle.__init__(self)
        self.width = random.randint(1,3)
        self.lifeTime = random.randint(self.width*2,self.width*3)
        self.maxLife = self.lifeTime
        self.velocity = Normalize(parent.velocity)
        self.right = [-self.velocity[1], self.velocity[0]]
        self.splatterList = [0,0,0,0,0,1,0,0,0,0,0]
        self.splatterLR = [4,6]
        self.color = [255,0,0]
        self.position = parent.position

    def Tick(self):
        for _ in range(3):
            if self.lifeTime > 0:
                if self.maxLife-self.lifeTime < self.width-1:
                    sideExtend = random.randint(1,2)
                    if sideExtend == 1 and self.splatterLR[0] < 10:
                        self.splatterList[self.splatterLR[0]] = 1
                        self.splatterLR[0] -= 1
                    elif self.splatterLR[1] > 0:
                        self.splatterList[self.splatterLR[1]] = 1
                        self.splatterLR[1] += 1
                elif self.lifeTime <= self.width:
                    splatterRemove = random.randint(1,self.width)
                    self.width -= 1
                    for index in range(len(self.splatterList)):
                        if self.splatterList[index] == 1:
                            splatterRemove-= 1
                        if splatterRemove == 0:
                            self.splatterList[index] = 0
                            break
                self.position[0] = self.position[0]+self.velocity[0]
                self.position[1] = self.position[1]+self.velocity[1]
                for index in range(len(self.splatterList)):
                    if self.splatterList[index] == 1:
                        posx = round(self.position[0] - self.right[0]*(index-4))
                        posy = round(self.position[1] - self.right[1]*(index-4))
                        ColorFloorPixel(posx,posy,(150, 8, 39))
            
            Particle.Tick(self)
    def Decay(self):
        Particle.Decay(self)





class ParticleBloodSplatterBig(Particle):

    def __init__(self, parent):
        Particle.__init__(self)
        self.width = random.randint(3,5)
        self.lifeTime = random.randint(self.width*2,self.width*3)
        self.maxLife = self.lifeTime
        self.velocity = Normalize(parent.velocity)
        self.right = [-self.velocity[1], self.velocity[0]]
        self.splatterList = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
        self.splatterLR = [9,11]
        self.color = (200, 8, 39)
        self.position = parent.position

    def Tick(self):
        for _ in range(7):
            if self.lifeTime > 0:
                if self.maxLife-self.lifeTime < self.width-1:
                    sideExtend = random.randint(1,2)
                    if sideExtend == 1 :
                        self.splatterList[self.splatterLR[0]] = 1
                        self.splatterLR[0] -= 1
                    elif self.splatterLR[1] > 0:
                        self.splatterList[self.splatterLR[1]] = 1
                        self.splatterLR[1] += 1
                elif self.lifeTime <= self.width:
                    sideExtend = random.randint(1,2)
                    if sideExtend == 1 :
                        self.splatterList[self.splatterLR[0]] = 0
                        self.splatterLR[0] += 1
                    elif self.splatterLR[1] > 0:
                        self.splatterList[self.splatterLR[1]] = 0
                        self.splatterLR[1] -= 1
                self.position[0] = self.position[0]+self.velocity[0]
                self.position[1] = self.position[1]+self.velocity[1]
                for index in range(len(self.splatterList)):
                    if self.splatterList[index] == 1:
                        posx = round(self.position[0] - self.right[0]*(index-4))
                        posy = round(self.position[1] - self.right[1]*(index-4))
                        ColorFloorPixel(posx,posy,(150, 8, 39))
            
            Particle.Tick(self)
    def Decay(self):
        Particle.Decay(self)



    
                  
class ParticleBloodSmall(Particle):

    def __init__(self):
        Particle.__init__(self)
        self.lifeTime = random.randint(2,4)
        self.color = (200, 8, 39)


    def Tick(self):
        bounds = g_particleArray.shape
        if 0 <= self.position[0] and self.position[0] < bounds[0] and 0 <= self.position[1]  and self.position[1] < bounds[1]:
            ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        self.position[0] = self.position[0]+math.floor(self.velocity[0])
        self.position[1] = self.position[1]+math.floor(self.velocity[1])
        self.velocity[0] = self.velocity[0] * 0.8
        self.velocity[1] = self.velocity[1] * 0.8
        if random.randint(1,5) == 2:
            ColorFloorPixel(self.position[0],self.position[1],(150, 8, 39))
        if 0 <= self.position[0] and self.position[0] < bounds[0] and 0 <= self.position[1]  and self.position[1] < bounds[1]:
            ColorParticlePixel(self.position[0],self.position[1],self.color)
        Particle.Tick(self)
    def Decay(self):
        bounds = g_particleArray.shape
        splatter = ParticleBloodSplatter(self)
        if 0 <= self.position[0] and self.position[0] < bounds[0] and 0 <= self.position[1]  and self.position[1] < bounds[1]:
            ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        Particle.Decay(self)
                 
                  
class ParticleBlood(Particle):

    def __init__(self):
        Particle.__init__(self)
        self.lifeTime = random.randint(2,5)
        self.color = (200, 8, 39)

        
    def Tick(self):
        bounds = g_particleArray.shape
        if 0 <= self.position[0] and self.position[0] < bounds[0] and 0 <= self.position[1]  and self.position[1] < bounds[1]:
            ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        self.position[0] = self.position[0]+math.floor(self.velocity[0])
        self.position[1] = self.position[1]+math.floor(self.velocity[1])
        self.velocity[0] = self.velocity[0] * 0.8
        self.velocity[1] = self.velocity[1] * 0.8
        if random.randint(1,5) == 2:
            ColorFloorPixel(self.position[0],self.position[1],(150, 8, 39))
        if 0 <= self.position[0] and self.position[0] < bounds[0] and 0 <= self.position[1]  and self.position[1] < bounds[1]:
            ColorParticlePixel(self.position[0],self.position[1],self.color)
        Particle.Tick(self)
    def Decay(self):
        bounds = g_particleArray.shape
        splatter = ParticleBloodSplatterBig(self)
        if 0 <= self.position[0] and self.position[0] < bounds[0] and 0 <= self.position[1]  and self.position[1] < bounds[1]:
            ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        Particle.Decay(self)

                  
class MagicParticle(Particle):
    def __init__(self, lifetime, color):
        Particle.__init__(self)
        lifemul = (1/lifetime+2)
        self.lifeTime = lifetime
        self.colorLoss = [0,0,0]
        self.colorLoss[0] = math.floor(color[0]*lifemul)
        self.colorLoss[1] = math.floor(color[1]*lifemul)
        self.colorLoss[2] = math.floor(color[2]*lifemul)
        self.width = random.randint(3,5)
        
    def Tick(self):
        for key in range(3):
            self.color[key] = self.color[key] - self.colorLoss[key]
        self.position[0] = self.position[0]+math.floor(self.velocity[0])
        self.position[1] = self.position[1]+math.floor(self.velocity[1])
        self.velocity[0] = self.velocity[0] * 0.8
        self.velocity[1] = self.velocity[1] * 0.8
        ColorParticlePixel(self.position[0],self.position[1],self.color)
        Particle.Tick(self)
    def Decay(self):
        map(int,self.position)
        ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        Particle.Decay(self)

         
                  
class FadingFlame(Particle):
    def __init__(self, lifetime, color, position = None):
        Particle.__init__(self)
        lifemul = (1/lifetime)
        self.lifeTime = lifetime-2
        self.colorLoss = [0,0,0]
        self.color = list(color)
        if position != None:
            self.position = position
        self.colorLoss[0] = math.floor(color[0]*lifemul-0.1)
        self.colorLoss[1] = math.floor(color[1]*lifemul-0.1)
        self.colorLoss[2] = math.floor(color[2]*lifemul-0.1)
        self.width = random.randint(3,5)
        
    def Tick(self):  
        for key in range(3):
            self.color[key] = self.color[key] - self.colorLoss[key]
        ColorParticlePixel(self.position[0],self.position[1],self.color)
        Particle.Tick(self)
    def Decay(self):
        map(int,self.position)
        ColorParticlePixel(self.position[0],self.position[1],(0,0,0))
        Particle.Decay(self)

colorScheme = ((255,242,83),(243,197,37),(237,87,44),(250,146,31))

class ParticleSmokeSplosion(Particle):
    def __init__(self,lifetime):
        Particle.__init__(self)
        self.width = 0
        color = list(random.choice(colorScheme))
        self.widthincr = 1
        self.multiplier = 1
        if lifetime < 10:
            self.lifeTime = lifetime*2
            self.widthincr = 0.5
        if lifetime >= 10:
            self.lifeTime = lifetime/2
            self.multiplier = 2
        self.maxwidth = self.lifeTime*self.multiplier
        
        particle = FadingFlame(16,color)
        particle.position[0] = self.position[0]
        particle.position[1] = self.position[1]
        colorfloor = list(g_levelArray[self.position[0]][self.position[1]])
        colorfloor[0] = max(0,colorfloor[0]-(self.maxwidth))
        colorfloor[1] = max(0,colorfloor[1]-(self.maxwidth))
        colorfloor[2] = max(0,colorfloor[2]-(self.maxwidth))
        ColorFloorPixel(self.position[0],self.position[1],(colorfloor))
    def Tick(self):
        for _ in range(self.multiplier):
            self.width += self.widthincr
            if self.width%1 == 0:
                self.placePos = [self.position[0],self.position[1]+self.width]
                for state in range(4): #we build 4 sides to the diamond/sphere
                    for _ in range(int(self.width)):
                        if state == 0 or state == 3: # if we're going to the right
                            self.placePos[0] = self.placePos[0]+ 1
                        else:
                            self.placePos[0] = self.placePos[0]- 1
                        if state < 2: #if we're going down
                            self.placePos[1] = self.placePos[1]- 1
                        else:
                            self.placePos[1] = self.placePos[1]+1
                        color = colorScheme[random.randint(0,len(colorScheme)-1)]
                        particle = FadingFlame(16,color)
                        particle.position[0] = self.placePos[0]
                        particle.position[1] = self.placePos[1]
                        colorfloor = list(g_levelArray[self.placePos[0]][self.placePos[1]])
                        colorfloor[0] = max(0,colorfloor[0]-(self.maxwidth-self.width))
                        colorfloor[1] = max(0,colorfloor[1]-(self.maxwidth-self.width))
                        colorfloor[2] = max(0,colorfloor[2]-(self.maxwidth-self.width))
                        ColorFloorPixel(self.placePos[0],self.placePos[1],(colorfloor))
        Particle.Tick(self)
    def Decay(self):
        Particle.Decay(self)

class ParticleFireball(Particle):
    def __init__(self,lifetime):
        Particle.__init__(self)
        self.color = (200, 8, 39)
        self.lifeTime = lifetime
        for x in range(5):
            for y in range(5):
                color = list(random.choice(colorScheme))
                particle = FadingFlame(12,color)
                particle.color = color
                particle.position[0] = self.position[0]-2+x
                particle.position[1] = self.position[1]-2+y
                
        
    def Tick(self):
        print(self.position)
        bounds = g_particleArray.shape
        xdiff = self.velocity[0]
        ydiff = self.velocity[1]
        divisions = math.floor(max(abs(xdiff),abs(ydiff)))
        xper = 0
        yper = 0
        if divisions != 0:
            yper = ydiff/divisions
            xper = xdiff/divisions
        oldpos = self.position[:]

        for move in range(divisions):
            self.position[0] = oldpos[0]+xper
            self.position[1] = oldpos[1]+yper
            xchange = math.floor(self.position[0])-math.floor(oldpos[0])
            ychange = math.floor(self.position[1])-math.floor(oldpos[1])
            oldpos[0] = self.position[0]
            oldpos[1] = self.position[1]
            for y in range(abs(ychange)):
                for x in range(3):
                    color = list(colorScheme[random.randint(0,len(colorScheme)-1)])
                    particle = FadingFlame(12,color)
                    particle.color = color
                    if yper < 0:
                        particle.position[0] = self.position[0]-1+x
                        particle.position[1] = self.position[1]-1+y
                    else:
                        particle.position[0] = self.position[0]-1+x                    
                        particle.position[1] = self.position[1]+1+y
            for x in range(abs(xchange)):
                for y in range(3):
                    color = list(random.choice(colorScheme))
                    particle = FadingFlame(12,color)
                    particle.color = color
                    if xper < 0:
                        particle.position[0] = self.position[0]-1+x
                        particle.position[1] = self.position[1]-1+y
                    else:
                        particle.position[0] = self.position[0]+1-x                    
                        particle.position[1] = self.position[1]-1+y
            
        
        #self.position[0] = self.position[0]+(self.velocity[0])
        #self.position[1] = self.position[1]+(self.velocity[1])
        Particle.Tick(self)
    def Decay(self):
        particle = ParticleSmokeSplosion(12)
        self.position[0] = round(self.position[0])
        self.position[1] = round(self.position[1])
        particle.position = self.position
        Particle.Decay(self)


class ParticleMagicMissile(Particle):
    def __init__(self,lifetime):
        Particle.__init__(self)
        self.color = (200, 8, 39)
        self.lifeTime = lifetime
        for x in range(5):
            for y in range(5):
                color = list(random.choice(colorScheme))
                particle = FadingFlame(12,color)
                particle.color = color
                particle.position[0] = self.position[0]-2+x
                particle.position[1] = self.position[1]-2+y
                
        
    def Tick(self):
        bounds = g_particleArray.shape
        xdiff = self.velocity[0]
        ydiff = self.velocity[1]
        divisions = math.floor(max(abs(xdiff),abs(ydiff)))
        xper = 0
        yper = 0
        if divisions != 0:
            yper = ydiff/divisions
            xper = xdiff/divisions
        oldpos = self.position[:]

        for move in range(divisions):
            self.position[0] = oldpos[0]+xper
            self.position[1] = oldpos[1]+yper
            xchange = math.floor(self.position[0])-math.floor(oldpos[0])
            ychange = math.floor(self.position[1])-math.floor(oldpos[1])
            oldpos[0] = self.position[0]
            oldpos[1] = self.position[1]
            for y in range(abs(ychange)):
                for x in range(3):
                    color = list(colorScheme[random.randint(0,len(colorScheme)-1)])
                    particle = FadingFlame(12,color)
                    particle.color = color
                    if yper < 0:
                        particle.position[0] = self.position[0]-1+x
                        particle.position[1] = self.position[1]-1+y
                    else:
                        particle.position[0] = self.position[0]-1+x                    
                        particle.position[1] = self.position[1]+1+y
            for x in range(abs(xchange)):
                for y in range(3):
                    color = list(random.choice(colorScheme))
                    particle = FadingFlame(12,color)
                    particle.color = color
                    if xper < 0:
                        particle.position[0] = self.position[0]-1+x
                        particle.position[1] = self.position[1]-1+y
                    else:
                        particle.position[0] = self.position[0]+1-x                    
                        particle.position[1] = self.position[1]-1+y
            
        
        #self.position[0] = self.position[0]+(self.velocity[0])
        #self.position[1] = self.position[1]+(self.velocity[1])
        Particle.Tick(self)
    def Decay(self):
        particle = ParticleSmokeSplosion(12)
        self.position[0] = round(self.position[0])
        self.position[1] = round(self.position[1])
        particle.position = self.position
        Particle.Decay(self)


class ParticleFirebomb(ParticleFireball):
    def Tick(self):
        bounds = g_particleArray.shape
        xdiff = self.velocity[0]
        ydiff = self.velocity[1]
        divisions = math.floor(max(abs(xdiff),abs(ydiff)))
        xper = 0
        yper = 0
        if divisions != 0:
            yper = ydiff/divisions
            xper = xdiff/divisions
        oldpos = self.position[:]

        for move in range(divisions):
            self.position[0] = oldpos[0]+xper
            self.position[1] = oldpos[1]+yper
            xchange = math.floor(self.position[0])-math.floor(oldpos[0])
            ychange = math.floor(self.position[1])-math.floor(oldpos[1])
            oldpos[0] = self.position[0]
            oldpos[1] = self.position[1]
            for y in range(abs(ychange)):
                for x in range(5):
                    color = list(colorScheme[random.randint(0,len(colorScheme)-1)])
                    particle = FadingFlame(12,color)
                    particle.color = color
                    if yper < 0:
                        particle.position[0] = self.position[0]-2+x
                        particle.position[1] = self.position[1]-2+y
                    else:
                        particle.position[0] = self.position[0]-2+x                    
                        particle.position[1] = self.position[1]+2+y
            for x in range(abs(xchange)):
                for y in range(5):
                    color = list(random.choice(colorScheme))
                    particle = FadingFlame(12,color)
                    particle.color = color
                    if xper < 0:
                        particle.position[0] = self.position[0]-2+x
                        particle.position[1] = self.position[1]-2+y
                    else:
                        particle.position[0] = self.position[0]+2-x                    
                        particle.position[1] = self.position[1]-2+y
            
        
        #self.position[0] = self.position[0]+(self.velocity[0])
        #self.position[1] = self.position[1]+(self.velocity[1])
        Particle.Tick(self)

    def Decay(self):
        particle = ParticleSmokeSplosion(24)
        self.position[0] = round(self.position[0])
        self.position[1] = round(self.position[1])
        particle.position = self.position
        Particle.Decay(self)
