from Button import *
from Compound import *
from Text import *

class Menu:
    def __init__(self):
        # create camera
        self.camera = Camera([0,5,8],angle=[10,0,0])

        # create list of all necessary object
        self.roadNum = 5
        self.roads = []
        self.lines = []
        self.mountR = []
        self.mountL = []

        for i in range(self.roadNum + 1):
            self.roads.append(Compound([ROADPLAIN, ROADEDGE], [(100, 100, 100), (220, 220, 220)], [0, 1], self.camera,[0, 0, -20 * i]))
            self.lines.append(Object(ROADLINE, (233, 200, 40), self.camera, [0, 0, -20 * i]))
            self.mountR.append(Object(MNTR2, JADE, self.camera, [0, 0, -20 * i]))
            self.mountL.append(Object(MNTL2, JADE, self.camera, [0, 0, -20 * i]))

        self.lines.append(Object(ROADLINE, (233, 200, 40), self.camera, [0, 0, -20 * (self.roadNum + 1)]))
        self.mountR.append(Object(MNTR2, JADE, self.camera, [0, 0, -20 * (self.roadNum + 1)]))
        self.mountL.append(Object(MNTL2, JADE, self.camera, [0, 0, -20 * (self.roadNum + 1)]))

        # create UI and also apply ratio for responsive design
        self.creatorName = Text((50 * WIDTHRATE,8 * HEIGHTRATE,200 * WIDTHRATE,60 * HEIGHTRATE),int(42 * WIDTHRATE),SEASHELL)
        self.gameButton = Button((50 * WIDTHRATE,58 * HEIGHTRATE,200 * WIDTHRATE,60 * HEIGHTRATE),SLATEGRAY,"START",int(38 * WIDTHRATE),(255,255,255),5,(255,255,255))
        self.scoreButton = Button((50 * WIDTHRATE,148 * HEIGHTRATE,200 * WIDTHRATE,60 * HEIGHTRATE),SLATEGRAY,"SCORE",int(38 * WIDTHRATE),(255,255,255),5,(255,255,255))
        self.exitButton = Button((50 * WIDTHRATE,238 * HEIGHTRATE,200 * WIDTHRATE,60 * HEIGHTRATE),SLATEGRAY,"EXIT",int(38 * WIDTHRATE),(255,255,255),5,(255,255,255))

        self.allButton = [self.gameButton,self.scoreButton,self.exitButton]

        self.id = "menu"
        self.nextState = 0

    def drawBackground(self):
        grad1H = HH - HH / 3
        drawGradient(15, DIGITALNAY, SUNGLOW, (0, 0, SCREENWIDTH, grad1H))
        pygame.draw.circle(SCREEN, SUNGLOW, (HW, grad1H), 75)
        pygame.draw.rect(SCREEN, JADE,(0, grad1H + 50 * HEIGHTRATE, SCREENWIDTH, SCREENHEIGHT - grad1H - 50 * HEIGHTRATE))

    def update(self,delta):
        self.creatorName.update("กิตติพันธ์ อ้นเล่ห์ 65010081")

    def run(self,delta):
        self.update(delta)
        self.drawBackground()

        # run(draw) mountain
        for mntr, mntl in zip(self.mountR[::-1], self.mountL[::-1]):
            mntr.run()
            mntl.run()

        # run(draw) road
        for road in self.roads:
            road.run()

        # run(draw) lines
        for line in self.lines:
            line.run()

        # run(draw) name
        self.creatorName.run()

        # check if this page is finish
        self.nextState = 0
        for index,button in enumerate(self.allButton):
            button.run()
            if button.is_clicked():
                self.nextState = index + 1