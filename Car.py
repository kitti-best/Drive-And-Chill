from Object3D import *

class Car:
    def __init__(self,body,trunk,wheels,colors,camera,trans = [0,0,0],rot = [0,0,0],scale = 1,controlable = False,reverse = False):
        self.controlable = controlable

        # set cars component
        self.body = Object(body,colors[0],camera,trans,rot,scale)
        self.trunk = Object(trunk,colors[0],camera,trans,rot,scale)
        self.wheelFL = Object(wheels[0],colors[1],camera,trans,rot,scale) # front left
        self.wheelFR = Object(wheels[1],colors[1],camera,trans,rot,scale) # front right
        self.wheelRL = Object(wheels[2],colors[1],camera,trans,rot,scale) # rear left
        self.wheelRR = Object(wheels[3],colors[1],camera,trans,rot,scale) # rear right

        # right side and left side have specific drawing order
        # for specific position so we separate it
        self.rightSide = [self.wheelFR,self.wheelRR]
        self.leftSide = [self.wheelFL,self.wheelRL]
        self.mid = [self.trunk,self.body]

        # list of all models
        self.models = [self.body,self.trunk,self.wheelFL,self.wheelFR,self.wheelRL,self.wheelRR]

        # set speed
        self.vspeed = 6
        self.hspeed = 6

        # set a value to determine if the cars is on right side or left side of the road
        self.sideRate = 0.17

        # if the car in revers
        self.reverse = reverse

        # set min and max value
        self.maxx = self.body.maxx
        self.minx = self.body.minx
        self.maxy = self.body.maxy
        self.miny = self.body.miny
        if self.reverse:
            self.maxz = self.body.maxz
            self.minz = self.trunk.minz
        else:
            self.maxz = self.trunk.maxz
            self.minz = self.body.minz

    def checkCollision(self,obj):
        return self.body.checkCollision(obj)

    def resetPosition(self):
        for model in self.models:
            model.resetPosition()

    def changeCamera(self, camera):
        for model in self.models:
            model.camera = camera

    def movement(self,trans = [0,0,0],rot = [0,0,0],delta = 1):
        for model in self.models:
            model.movement(trans,rot,delta)

    def drawRight(self):
        for model in self.rightSide:
            model.run()

    def drawLeft(self):
        for model in self.leftSide:
            model.run()

    def drawMid(self):
        for model in self.mid:
            model.run()

    def update(self,delta = 1,keyOccur = False):
        # do nothing if no key occur
        if not keyOccur:
            return

        # update all model
        for model in self.models:
            model.update(True)

        # find new body min-max
        self.maxx = self.body.maxx
        self.minx = self.body.minx
        self.maxy = self.body.maxy
        self.miny = self.body.miny
        if self.reverse:
            self.maxz = self.body.maxz
            self.minz = self.trunk.minz
        else:
            self.maxz = self.trunk.maxz
            self.minz = self.body.minz

        # if this is not controllable do nothing
        if not self.controlable:
            return

        # move car left or right
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.movement([-self.hspeed, 0, 0],delta = delta)
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.movement([self.hspeed, 0, 0],delta = delta)

    def run(self):
        # if on right side
        onRight = self.minx > self.sideRate
        onLeft = self.maxx < -self.sideRate

        if self.reverse and onRight or onLeft and not self.reverse:
            self.drawLeft()
            self.drawMid()
            self.drawRight()
        elif onRight and not self.reverse or onLeft and self.reverse:
            self.drawRight()
            self.drawMid()
            self.drawLeft()
        # in middle
        else:
            self.drawRight()
            self.drawLeft()
            self.drawMid()
