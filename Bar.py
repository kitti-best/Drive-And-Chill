from Setting import *

class ShearBar:
    def __init__(self,screen,rect,max,color):
        self.screen = screen
        self.rect = rect

        self.x = self.rect[0]
        self.y = self.rect[1]
        self.w = self.rect[2]
        self.h = self.rect[3]
        self.shear = 15

        self.max = max
        self.current = max
        self.beadsLength = self.rect[2]//self.max
        self.color = color

    def drawBeads(self):
        for offset in range(self.current):
            poly = ((self.x + self.shear + offset * self.beadsLength, self.y)
                   ,(self.x + self.beadsLength + self.shear + offset * self.beadsLength, self.y)
                   ,(self.x + self.beadsLength + offset * self.beadsLength, self.y + self.h)
                   ,(self.x + offset * self.beadsLength, self.y + self.h))

            pygame.draw.polygon(self.screen, self.color, poly) # bar color
            pygame.draw.polygon(self.screen, FFFWHITE, poly, 2) # line color

    def update(self,val):
        self.current = int(val)

    def run(self):
        self.drawBeads()
        poly = ((self.x,self.y),(self.x + self.w + self.shear ,self.y),(self.x + self.w,self.y + self.h),(self.x,self.y+self.h))
        # pygame.draw.polygon(self.screen,(255,255,255),poly,2)


class BarHorizon:
    def __init__(self,screen,rect,max,color):
        self.screen = screen
        self.rect = rect

        self.x = self.rect[0]
        self.y = self.rect[1]
        self.w = self.rect[2]
        self.h = self.rect[3]

        self.max = max
        self.current = max
        self.beadsLength = self.rect[2]//self.max
        self.color = color

    def drawBeads(self):
        rect = (self.x, self.y, self.beadsLength * self.max, self.h)
        pygame.draw.rect(self.screen,PALEGRAY,rect)

        rect = (self.x,self.y,self.beadsLength * self.current,self.h)
        pygame.draw.rect(self.screen,self.color,rect)

    def update(self,val):
        self.current = int(val)

    def run(self):
        self.drawBeads()

