import random
import pygame.transform
from Player import *
from Text import *
from Bar import *
from Button import *
from Compound import *
from Item import *

class Game:
    def __init__(self):
        # camera setting
        self.camera = Camera([0,5,8],angle=[10,0,0])

        # create all object
        self.roadNum = 5
        self.cars = []
        self.items = []
        self.roads = []
        self.lines = []
        self.mountR = []
        self.mountL = []

        for i in range(self.roadNum + 1):
            self.roads.append(Compound([ROADPLAIN, ROADEDGE], [(100,100,100), (220, 220, 220)], [0, 1],self.camera,[0,0,-20*i]))
            self.lines.append(Object(ROADLINE,(233,200,40),self.camera,[0,0,-20*i]))
            self.mountR.append(Object(MNTR2,JADE,self.camera,[0,0,-20*i]))
            self.mountL.append(Object(MNTL2,JADE,self.camera,[0,0,-20*i]))

        self.lines.append(Object(ROADLINE,(233,200,40),self.camera,[0,0,-20*(self.roadNum + 1)]))
        self.mountR.append(Object(MNTR2,JADE,self.camera,[0,0,-20*(self.roadNum + 1)]))
        self.mountL.append(Object(MNTL2,JADE,self.camera,[0,0,-20*(self.roadNum + 1)]))

        self.player = Player(SEDBODY,SEDTRUNK,[SEDWFL,SEDWFR,SEDWRL,SEDWRR],CARCOLOR4,self.camera,[0,0,-10],[0,180,0])

        # create UI
        self.gasBar = BarHorizon(SCREEN,(20 * WIDTHRATE,680 * HEIGHTRATE,400 * WIDTHRATE,20 * HEIGHTRATE),self.player.maxgas,CRIMSON)
        self.nitroBar = BarHorizon(SCREEN, (430 * WIDTHRATE,680 * HEIGHTRATE,400 * WIDTHRATE,20 * HEIGHTRATE),self.player.maxnitro,AZURE)
        self.damagedBar = BarHorizon(SCREEN,(840 * WIDTHRATE,680 * HEIGHTRATE,400 * WIDTHRATE,20 * HEIGHTRATE),self.player.maxhp,SLATEGRAY)
        self.backButton = Button((SCREENWIDTH-170 * WIDTHRATE, 20 * HEIGHTRATE, 120 * WIDTHRATE, 60 * HEIGHTRATE),None,"BACK",int(34 * WIDTHRATE),(255,255,255),5,(255,255,255))

        self.timeText = Text((HW,17),36,FFFWHITE,True)
        self.travelText = Text((HW,45),42,FFFWHITE,True)

        self.gasText = Text((20 * WIDTHRATE,650 * HEIGHTRATE),int(32 * WIDTHRATE),COVERTBLACK)
        self.nitroText = Text((430 * WIDTHRATE,650 * HEIGHTRATE),int(32 * WIDTHRATE),COVERTBLACK)
        self.damagedText = Text((840 * WIDTHRATE,650 * HEIGHTRATE),int(32 * WIDTHRATE),COVERTBLACK)

        self.pauseText = Text((HW,HH + 90 * HEIGHTRATE),int(42 * WIDTHRATE),FFFWHITE,True)

        # state properties
        self.id = "game"
        self.nextState = 0

        # game properties
        self.gameSpeedStart = 20
        self.gameSpeed = 20
        self.playTime = 0
        self.travel = 0

        # cooldown of item
        self.itemStartCD = 0

        # cooldown of generation
        self.acc = False
        self.justHit = True
        self.playerHitMnt = False
        self.startAccSpeed = self.gameSpeedStart
        self.objWaitTime = 1500
        self.objStartCD = pygame.time.get_ticks()

        # block mapper for items and cars
        self.blockMapper = [-3,-1,1,3]
        self.objectInEachBlock = [[],[],[],[]]
        self.occupiedIn = [0,0,0,0]
        self.occupiedOut = [0,0,0,0]

        # car generate info
        self.maxItemNum = 1
        self.maxCarNum = 6
        self.gasDroprate = 1

        # move mountain adn line
        self.envMoveTime = 50
        self.startMove = pygame.time.get_ticks()

        self.pause = False

    def generateItem(self):
        # random model type and block(lane) that item will be on
        modelType = random.randint(1, 3)
        block = random.randint(0, 3)

        # the block is facing out, so I check if every block have something that facing in
        # if so get out of this function
        if sum(self.occupiedIn) == 4:
            return

        # while that lanes have car in opposite direction
        while self.occupiedIn[block]:
            block = (block + 1) % 4

        # make that block occupy
        self.occupiedOut[block] = 1

        # move object to the right block
        transX = self.blockMapper[block] * 2.5
        # generate model from type we have random
        if modelType <= 1 * self.gasDroprate: # gas
            item = Item([GASTANK,GASPIPE],[LUST,MATTECHARCOAL],[1,0], self.camera, [transX, 0, -120],[0,0,0],1.2,1)
        elif modelType == 2: # wrench
            item = Item([WRENCH],[SLATEGRAY],[0], self.camera, [transX, 0, -120],[0,0,45],1.2,2)
        elif modelType == 3: # nitrus
            item = Item([NITRUSTANK,NITRUSHEAD],[AZURE,GOLD],[1,0], self.camera, [transX, 0, -120],[0,0,45],0.8,3)

        # set item speed
        item.vspeed = self.gameSpeed

        # add item in
        self.objectInEachBlock[block].append(item)
        self.items.append([item, block])

    def generateCar(self):
        # random car type
        modelType = random.randint(0,2)
        # random if this car wil face out or face in
        transZ = random.choice([0,-120])
        block = random.randint(0,3)
        colorSet = CARCOLORSET[random.randint(0,2)]

        # if head out
        if transZ < 0:
            # reverse true because the car model is now in reverse
            reverse = True
            rot = 0

            # check every block is occupied with car in other direction
            if sum(self.occupiedIn) == 4:
                self.objStartCD = pygame.time.get_ticks()
                return

            # while that lanes have car in opposite direction
            while self.occupiedIn[block]:
                block = (block + 1)%4

            # make that block occupy with car in this direction
            self.occupiedOut[block] = 1

        # if head in
        else:
            reverse = False
            rot = 180
            if sum(self.occupiedOut) == 4:
                self.objStartCD = pygame.time.get_ticks()
                return
            while self.occupiedOut[block]:
                block = (block + 1)%4
            self.occupiedIn[block] = 1

        # random placing car
        transX = self.blockMapper[block] * 2.5 + random.choice([-1,1])*random.randint(8,11)/10
        if modelType == 0:
            car = Car(SEDBODY,SEDTRUNK,[SEDWFL,SEDWFR,SEDWRL,SEDWRR],colorSet,self.camera,[transX,0,transZ],[0,rot,0],reverse = reverse)
        elif modelType == 1:
            car = Car(PICKBODY,PICKTRUNK,[SEDWFL,SEDWFR,SEDWRL,SEDWRR],colorSet,self.camera,[transX,0,transZ],[0,rot,0],reverse = reverse)
        elif modelType == 2:
            car = Car(TRUCKBODY,TRUCKTRUNK,[SEDWFL,SEDWFR,SEDWRL,SEDWRR],colorSet,self.camera,[transX,0,transZ],[0,rot,0],reverse = reverse)

        car.vspeed = self.gameSpeed
        if transZ == 0:
            car.vspeed *= -1

        self.objectInEachBlock[block].append(car)
        self.cars.append([car,block])

    def updateLines(self,delta):
        for line in self.lines:
            # move line
            line.movement([0, 0, self.gameSpeed], delta = delta)
            # Object3D only update when key occur in loop, so we force it to update after we move it
            line.update(keyOccur = True)
        # if line out of screen pop it out
        if self.lines[0].minz >= 1:
            self.lines.pop(0)
            self.lines.append(Object(ROADLINE, (233, 200, 40), self.camera, [0, 0, -20 * (self.roadNum + 1)]))

    def updateMount(self,delta,key):
        for mntr,mntl in zip(self.mountR,self.mountL):
            mntr.movement([0, 0, self.gameSpeed], delta = delta)
            mntl.movement([0, 0, self.gameSpeed], delta = delta)
            mntr.update(keyOccur = True)
            mntl.update(keyOccur = True)
            # always check if player hit the mountain, so we can stop player from going inside mountain
            if self.player.minx < mntl.maxx and (key[pygame.K_a] or key[pygame.K_LEFT]) \
               or self.player.maxx > mntr.minx and (key[pygame.K_d] or key[pygame.K_RIGHT]):
                self.playerHitMnt = True
            else:
                self.playerHitMnt = False

        # check if front-most mountain is out of screen
        if self.mountR[0].minz >= 1:
            self.mountR.pop(0)
            self.mountR.append(Object(MNTR2,JADE,self.camera,[0,0,-20*(self.roadNum + 1)]))

        if self.mountL[0].minz >= 1:
            self.mountL.pop(0)
            self.mountL.append(Object(MNTL2,JADE,self.camera,[0,0,-20*(self.roadNum + 1)]))

    def updateCars(self,delta):
        for i,carAndBlock in enumerate(self.cars):
            car,block = carAndBlock

            if car.vspeed < 0:
                car.vspeed = -self.gameSpeed
            else:
                car.vspeed = self.gameSpeed

            car.movement([0,0,car.vspeed],delta = delta)
            car.update(keyOccur = True)

            if (car.minz >= 1 and car.vspeed > 0) or (car.minz <= -120 and car.vspeed < 0):
                if car.vspeed > 0: # head in
                     self.occupiedIn[block] = 0
                if car.vspeed < 0: # head out
                     self.occupiedOut[block] = 0
                self.objectInEachBlock[block].pop(0)
                self.cars.pop(i)

            # reset everything after hitting other car
            if self.player.checkCollision(car.body):
                self.player.hit(car,"car")
                self.justHit = True
                self.cars = []
                self.items = []
                self.objectInEachBlock = [[],[],[],[]]
                self.occupiedIn = [0,0,0,0]
                self.occupiedOut = [0,0,0,0]
                self.gameSpeed = self.startAccSpeed
                self.objStartCD = pygame.time.get_ticks()

    def updateItems(self,delta):
        for i, itemAndBlock in enumerate(self.items):
            item, block = itemAndBlock
            item.vspeed = self.gameSpeed
            item.movement([0,0,item.vspeed],[0,90,0],delta)
            item.update(keyOccur = True)

            hit = 0
            if self.player.checkCollision(item.rep):
                PICK.play()
                self.player.hit(item, "item")
                hit = 1

            if item.minz >= 1 or hit:
                self.occupiedIn[block] = 0
                self.objectInEachBlock[block].pop(0)
                self.items.pop(i)

    def updateGui(self):
        self.gasBar.update(self.player.gas)
        self.nitroBar.update(self.player.nitro)
        self.damagedBar.update(self.player.hp)

        seconds = self.playTime / 1000
        hours = seconds // (60 * 60)
        seconds -= hours * (60 * 60)

        minutes = seconds // (60)
        seconds -= minutes * (60)

        seconds = seconds % 60

        # create human readable time
        self.timeString = '0' * (hours < 10) + str(int(hours)) + ':' + '0' * (minutes < 10) + str(int(minutes)) + ':' + '0' * (seconds < 10) + str(int(seconds))
        self.timeText.update(self.timeString)
        # create travel distance
        self.travelString = '0' * (self.travel < 10) + str("%.2f" % round(self.travel, 2)) + " KM"
        self.travelText.update(self.travelString)

        self.gasText.update("GASOLINE : " + str(int(self.player.gas)) + "/" + str(self.player.maxgas))
        self.nitroText.update("BOOST : " + str(int(self.player.nitro)) + "/" + str(self.player.maxnitro))
        self.damagedText.update("DURABILITY : " + str(int(self.player.hp)) + "/" + str(self.player.maxhp))

        self.pauseText.update("SPACE TO CONTINUE")

    def update(self,delta):
        key = pygame.key.get_pressed()
        keyOccur = any(key)

        if key[K_ESCAPE]:
            self.pause = True
        elif key[K_SPACE]:
            self.pause = False

        if self.pause:
            return

        # update page properties
        self.gameSpeed = min(self.gameSpeed + delta/1.4,55)
        self.travel += delta * self.gameSpeed/500
        self.playTime = pygame.time.get_ticks()
        self.player.gas = max(self.player.gas - (self.gameSpeed / self.gameSpeedStart) * delta/2,0)

        # if gas less than 7 play alarm and guarantee gas for player
        if self.player.gas < 7:
            self.gasDroprate = 99
            LOW.play()
        else:
            self.gasDroprate = 1

        # move player when using nitrus
        carMoved = False
        if self.player.nitro <= 0:
            self.gameSpeed = max(self.gameSpeed - 5 * delta, self.startAccSpeed)
            if self.player.minz < -10:
                self.player.movement([0,0,self.player.hspeed],[0,0,0],delta)
                carMoved = True

        # input handler
        if key[K_h]:
            HONK.play()
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.player.nitro > 0:
            # move player up until player z is -12
            if self.player.minz >= -12:
                self.player.movement([0,0,-self.player.hspeed],[0,0,0],delta)
                carMoved = True
            # if it first time move player up
            if not self.acc:
                self.startAccSpeed = self.gameSpeed
            # add game speed and decrease player nitro
            self.gameSpeed = min(self.gameSpeed + 5 * delta,50)
            self.player.nitro = max(self.player.nitro - 2 * delta,0)
            # tell game that righ now player is speed up
            self.acc = True
        # if didn't speed up
        elif not (key[pygame.K_w] or key[pygame.K_UP]):
            # move player down until playerz is -10
            if self.player.minz < -10:
                self.player.movement([0,0,self.player.hspeed],[0,0,0],delta)
                carMoved = True
            # if its first time user release speed up keys
            if self.acc:
                self.gameSpeed = max(self.gameSpeed - 5 * delta,self.startAccSpeed)
                if self.gameSpeed <= self.startAccSpeed:
                    self.acc = False
            # increase nitro
            self.player.nitro = min(self.player.nitro + delta, self.player.maxnitro)

        self.updateItems(delta)
        self.updateCars(delta)
        self.player.update(delta,(keyOccur or carMoved) and not self.playerHitMnt)

        # move lines and mountain every x seconds
        if pygame.time.get_ticks() - self.startMove >= self.envMoveTime:
            self.updateLines(delta)
            self.updateMount(delta,key)
            self.startMove = pygame.time.get_ticks()

        # car generate
        if pygame.time.get_ticks() - self.objStartCD > self.objWaitTime * self.gameSpeedStart/self.gameSpeed + self.objWaitTime * self.justHit and len(self.cars) < self.maxCarNum:
            if self.justHit:
                self.justHit = False
            self.generateCar()
            self.objStartCD = pygame.time.get_ticks()

        # item generate
        if pygame.time.get_ticks() - self.itemStartCD > self.objWaitTime * self.gameSpeedStart/self.gameSpeed + self.objWaitTime * self.justHit and len(self.items) < self.maxItemNum:
            self.generateItem()
            self.itemStartCD = pygame.time.get_ticks()

        self.updateGui()

    def run(self,delta):
        # update everything
        self.update(delta)

        # drawing background
        grad1H = HH - HH / 3
        drawGradient(15, DIGITALNAY, SUNGLOW, (0, 0,SCREENWIDTH,grad1H))
        pygame.draw.circle(SCREEN,SUNGLOW,(HW, grad1H),75)
        pygame.draw.rect(SCREEN,JADE,(0, grad1H + 50, SCREENWIDTH,SCREENHEIGHT - grad1H - 50))

        # run all obj
        for mntr,mntl in zip(self.mountR[::-1],self.mountL[::-1]):
            mntr.run()
            mntl.run()

        for road in self.roads:
            road.run()

        for line in self.lines:
            line.run()

        for block in self.objectInEachBlock:
            if block == []:
                continue
            if block[0].vspeed > 0: # head in
                block = block[::-1]
            for obj in block:
                obj.run()

        self.player.run()

        # run all ui
        pygame.draw.rect(SCREEN,FFFWHITE,(0 , 0.9*SCREENHEIGHT,SCREENWIDTH,0.1*SCREENHEIGHT))
        self.timeText.run()
        self.travelText.run()
        self.gasText.run()
        self.nitroText.run()
        self.damagedText.run()
        self.gasBar.run()
        self.nitroBar.run()
        self.damagedBar.run()

        # if pause draw pause sign
        if self.pause:
            pygame.draw.polygon(SCREEN,FFFWHITE,[(HW - 35,HH - 35),(HW + 35,HH),(HW - 35,HH + 35)])
            self.pauseText.run()

        # check if this page is finish
        self.nextState = 0
        self.backButton.run()
        if self.backButton.is_clicked():
            self.nextState = 1

        # if player out of hp or out of gas, end the game
        if self.player.hp <= 0 or self.player.gas <= 0:
            self.travel = round(self.travel,2)
            self.playTime = round(self.playTime/1000,2)
            self.nextState = 2
