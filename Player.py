from Car import *

class Player(Car):
    def __init__(self,body,trunk,wheels,colors,camera,trans = [0,0,0],rot = [0,0,0],scale = 1):

        super().__init__(body,trunk,wheels,colors,camera,trans,rot,scale,True)

        self.hitAble = True
        self.maxhp = 8
        self.hp = 8
        self.maxgas = 40
        self.gas = 40
        self.maxnitro = 20
        self.nitro = 20

    def hit(self,obj,type):
        if type == "car":
            self.hp = max(self.hp - 1,0)
        if type == "item":
            if obj.type == 1: # gas
                self.gas = self.maxgas
            elif obj.type == 2: # wrench
                self.hp = min(self.hp + 1,self.maxhp)
            elif obj.type == 3: # nitrus
                self.nitro = min(self.nitro + self.maxnitro/2,self.maxnitro)
