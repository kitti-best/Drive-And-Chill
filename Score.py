from Button import *
from Text import *

class Score:
    def __init__(self):
        # setup ui
        self.backButton = Button((HW - 100 * WIDTHRATE,
                                  600 * HEIGHTRATE,
                                  200 * WIDTHRATE,
                                  60 * HEIGHTRATE)
                                 ,None,"BACK",int(34 * WIDTHRATE),(255,255,255),5,(255,255,255))
        self.header = Text((HW, 50 * HEIGHTRATE, HW, HH), centered=True, fontsize=int(100 * WIDTHRATE))
        self.nameLabel = Text((100 * WIDTHRATE,90 * HEIGHTRATE, HW, HH), fontsize=int(70 * WIDTHRATE))
        self.travelLabel = Text((395 * WIDTHRATE,90 * HEIGHTRATE, HW, HH), fontsize=int(70 * WIDTHRATE))
        self.timeLabel = Text((900 * WIDTHRATE, 90 * HEIGHTRATE, HW, HH), fontsize=int(70 * WIDTHRATE))

        self.id = "score"
        self.nextState = 0

    def update(self):
        self.header.update("BEST PLAYER")
        self.nameLabel.update("Name")
        self.travelLabel.update("Travel Distance")
        self.timeLabel.update("Play Time")

        with open('score.json', 'r') as file:
            self.playerScore = json.load(file)

        # save necessary information
        self.alltext = []
        for i,score in enumerate(self.playerScore):
            name = Text((100 * WIDTHRATE, (160+70*i) * HEIGHTRATE, HW, HH), fontsize=int(50 * WIDTHRATE))
            travel = Text((395 * WIDTHRATE, (160+70*i) * HEIGHTRATE, HW, HH), fontsize=int(50 * WIDTHRATE))
            time = Text((900 * WIDTHRATE, (160+70*i) * HEIGHTRATE, HW, HH), fontsize=int(50 * WIDTHRATE))
            self.alltext.append([name,travel,time])

    def run(self,delta = 1):
        self.update()

        # run all text
        self.header.run()
        self.nameLabel.run()
        self.travelLabel.run()
        self.timeLabel.run()

        # draw everything from
        for text,label in zip(self.playerScore,self.alltext):
            label[0].update(text[0])
            label[1].update(text[2])
            label[2].update(text[3])
            label[0].run()
            label[1].run()
            label[2].run()

        # check if this page is done
        self.nextState = 0

        self.backButton.run()
        if self.backButton.is_clicked():
            self.nextState = 1