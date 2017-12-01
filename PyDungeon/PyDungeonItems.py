import PyDungeonWorld as World
class Item():
    def __init__(self):
        self.name = "NULLITEM"
        self.id = World.AssignObjectID()
        self.itemid = World.AssignItemID()
        self.slot = ""
        self.owner = None
        self.position = [0,0]
        self.tokens = []
        self.spriteID = 255
    def NewID(self):
        self.id = World.AssignEntityID(self)
        self.objectid = World.AssignItemID(self)
    def Render(self):
        Graphics.renderSprite(self)
    def UnRender(self):
        Graphics.UnRenderMob(self)        
		
class HealthPotion(Item):
    def __init__(self):
        Item.__init__(self)

    def Activate(self):
        modStats = {"Health":self.owner["Health"]}
        if modStats["Health"] <= (modStats["MaxHealth"]-15):
            modStats["Health"] = modStats["Health"]+15
        elif modStats["Health"] <= modStats["MaxHealth"]:
            modStats["Health"] = modStats["MaxHealth"]
        self.owner.ModifyStats(modStats)
