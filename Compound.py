import time

from Object3D import *

class Compound:
    def __init__(self,models,colors,order,camera,trans = [0,0,0],rot = [0,0,0],scale = 1):
        self.models = []
        for i in order:
            self.models.append(Object(models[i],colors[i],camera,trans,rot,scale))

        # compound representative
        self.rep = self.models[0]

    def rotateAround(self,ax,ay,az,delta):
        for model in self.models:
            model.rotateAround(ax,ay,az,delta)

    def changeCamera(self, camera):
        for model in self.models:
            model.camera = camera

    def move(self,x,y,z,delta):
        for model in self.models:
            model.move(x,y,z,delta)

    def movement(self,trans = [0,0,0],rot = [0,0,0],delta = 1):
        for model in self.models:
            model.movement(trans,rot,delta)

    def update(self,delta = 1,keyOccur = False):
        if not keyOccur:
            return
        for model in self.models:
            model.update(True)

        self.maxx = self.rep.maxx
        self.minx = self.rep.minx
        self.maxy = self.rep.maxy
        self.miny = self.rep.miny
        self.maxz = self.rep.maxz
        self.minz = self.rep.minz

    def run(self):
        for model in self.models:
            model.run()
