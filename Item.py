from Compound import *

class Item(Compound):
    def __init__(self,models,colors,order,camera,trans = [0,0,0],rot = [0,0,0],scale = 1,type = 0):
        super().__init__(models,colors,order,camera,trans,rot,scale)
        self.type = type
        self.vspeed = 15
        '''
        type 0 = gas
        type 1 = wrench
        type 2 = nitrus
        '''
