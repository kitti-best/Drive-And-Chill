import json

import pygame
from operator import itemgetter
from Text import *
from Setting import *

class Summary:
    def __init__(self,travel = 0,finalTime = 0):
        self.finalTravel,self.travelString = travel
        self.finalTime = finalTime
        self.name = ""

        self.decor1 = Text((HW,50 * HEIGHTRATE,HW,HH),centered=True,fontsize=int(70 * WIDTHRATE))
        self.playerScore = Text((HW,130 * HEIGHTRATE,HW,HH),centered=True,fontsize=int(120 * WIDTHRATE))
        self.decor2 = Text((HW,210 * HEIGHTRATE,HW,HH),centered=True,fontsize=int(70 * WIDTHRATE))
        self.playTime = Text((HW,290 * HEIGHTRATE,HW,HH),centered=True,fontsize=int(70 * WIDTHRATE))
        self.playerName = Text((HW,400 * HEIGHTRATE,HW,HH),centered=True,fontsize=int(130 * WIDTHRATE))

        self.id = "summary"
        self.nextState = 0

        self.coolDownTime = 0.1
        self.isCooldown = False
        self.startDel = 0

        WIN.play()

    def update(self):
        self.decor1.update("FINAL DISTANT")
        self.decor2.update("FINAL PLAYTIME")
        self.playerName.update(self.name)
        self.playerScore.update(self.travelString)
        self.playTime.update(self.finalTime)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if key on keyboard have been pressed
            if event.type == pygame.KEYDOWN:
                # if that key is not backspace
                if not event.key == pygame.K_BACKSPACE and not event.key == pygame.K_RETURN:
                    # append the name by event unicode
                    self.name += event.unicode

                # if that key is enter
                elif event.key == pygame.K_RETURN:
                    # we don't like it when player name is empty OR player name filled by SPACE
                    # so we try replace all space by empty and if that player name empty
                    # if so we force the player name to "Unknown"
                    if self.name.replace(" ","") == "":
                        self.name = "Unknown"

                    # you can delete this. I use self.finish to tell my main loop that this page is finish
                    self.nextState = 1

                    # load the file score.json
                    with open('score.json', 'r') as file:
                        playerScore = json.load(file)
                    playerScore.append([self.name,float(self.finalTravel),self.travelString,self.finalTime])
                    # sort the score and reverse so it will be in descending order
                    # and because of "playerScore" is a list which contains other lists
                    # we then have to tell the sorted function which we will use to be the KEY for sorting
                    # explain : playerScore = [[name,score],[name,score]]. we then tell the sort function that the key is score which is in index 1 of elements in playerScore
                    playerScore = sorted(playerScore,reverse = True,key = itemgetter(1))

                    # if the length of playerScore is greater than 5 we POP the last element out
                    if len(playerScore) > 5:
                        playerScore.pop()

                    # over write the score.json file with our new playerScore
                    with open('score.json', 'w+') as file:
                        json.dump(playerScore,file)

        # if now is not in cooldown period and player press the backspace key
        if not self.isCooldown and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            # start cooldown
            self.isCooldown = True
            # get the start time of when player start deleting the name
            self.startDel = pygame.time.get_ticks()
            # if length of name is 1 or lesser we turn the name to empty string
            if len(self.name) <= 1:
                self.name = ""
            # cut the last charactor of name out
            else:
                self.name = self.name[:-1]

        # if length of name if greater than 15 we keep only the first 15 charactor
        if len(self.name) > 15:
            self.name = self.name[:15]

        # if now we are in cooldown and time since player start deleting is more than cooldown time we stop cooldown period
        if (pygame.time.get_ticks() - self.startDel)/1000 >= self.coolDownTime and self.isCooldown:
            self.isCooldown = False

    def run(self,delta):
        self.nextState
        self.update()
        self.decor1.run()
        self.decor2.run()
        self.playTime.run()
        self.playerName.run()
        self.playerScore.run()
