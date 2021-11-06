from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
import sys, json
import pygame

with open("../config.json", "r") as f: config = json.load(f);f.close()



class PieEngine(object):

    def __init__(self, mapNum):
        self.initCollision()
        self.loadLevel(mapNum)
        self.initPlayer()
        base.accept("escape", sys.exit)
        base.disableMouse()
        text_tooltip = OnscreenText(text=config["screenSettings"]["tooltip"], style=1, fg=(1,1,1,1),
            pos=(-1.3, 0.95), align=TextNode.ALeft, scale = .05)

        
    def initCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        
    def loadLevel(self, mapNum):
        self.level = loader.loadModel(config["gameSettings"]["level"+str(mapNum)])
        self.level.reparentTo(render)
        self.level.setTwoSided(True)
                
    def initPlayer(self):
        self.node = Player()
        
class Player(object):
    speed = config["playerSettings"]["walkSpeed"]
    FORWARD = Vec3(0,2,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-1,0,0)
    RIGHT = Vec3(1,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    readyToJump = False
    jump = 0
    
    def __init__(self):
        print("Welcome to Pie3D V1.0 Alpha!")
        self.loadModel()
        self.setUpCamera()
        self.createCollisions()
        self.attachControls()
        print("Loaded PlayerModule")
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        taskMgr.add(self.jumpUpdate, 'jump-task')
        
    def loadModel(self):
        self.node = NodePath('player')
        self.node.reparentTo(render)
        self.node.setPos(0,0,2)
        self.node.setScale(.05)
    
    def setUpCamera(self):
        pl =  base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.node)
        
    def createCollisions(self):
        cn = CollisionNode('player')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.node, base.drive.node())

        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('playerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
        
    def attachControls(self):
        # attach key events
        base.accept( "space" , self.__setattr__,["readyToJump",True])
        base.accept( "space-up" , self.__setattr__,["readyToJump",False])
        base.accept( "s" , self.__setattr__,["walk",self.STOP] )
        base.accept( "w" , self.__setattr__,["walk",self.FORWARD])
        base.accept( "s" , self.__setattr__,["walk",self.BACK] )
        base.accept( "s-up" , self.__setattr__,["walk",self.STOP] )
        base.accept( "w-up" , self.__setattr__,["walk",self.STOP] )
        base.accept( "a" , self.__setattr__,["strafe",self.LEFT])
        base.accept( "d" , self.__setattr__,["strafe",self.RIGHT] )
        base.accept( "a-up" , self.__setattr__,["strafe",self.STOP] )
        base.accept( "d-up" , self.__setattr__,["strafe",self.STOP] )
        
    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, int(base.win.getXSize()/2), int(base.win.getYSize()/2)):
            self.node.setH(self.node.getH() -  (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
        return task.cont
    
    def moveUpdate(self,task): 


        self.node.setPos(self.node,self.walk*globalClock.getDt()*self.speed)
        self.node.setPos(self.node,self.strafe*globalClock.getDt()*self.speed)
        return task.cont
        
    def jumpUpdate(self,task):


        highestZ = -100
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Cube":
                highestZ = z

        self.node.setZ(self.node.getZ()+self.jump*globalClock.getDt())
        self.jump -= 1*globalClock.getDt()
        if highestZ > self.node.getZ()-config["playerSettings"]["PlayerHeight"]:
            self.jump = 0
            self.node.setZ(highestZ+config["playerSettings"]["PlayerHeight"])
            if self.readyToJump:
                self.jump = 1
        return task.cont

def menuPlayMap(mapNum = 1):
    PieEngine(mapNum)
    base.run()

