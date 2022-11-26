from math import *
import pygame
import numpy as np
import json
from Camera import *
from pygame.locals import *

pygame.init()
music = pygame.mixer.init()

flags = FULLSCREEN | DOUBLEBUF

# set screen properties
FPS = 24
SCREENWIDTH = 1280 * 0.5
SCREENHEIGHT = 720 * 0.5
WIDTHRATE = SCREENWIDTH / 1280
HEIGHTRATE = SCREENHEIGHT / 720
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
CLOCK = pygame.time.Clock()
DT = CLOCK.tick(FPS)/1000

# set sound
pygame.mixer.music.load("assets/music/chillBeat.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

PICK = pygame.mixer.Sound("assets/music/pickUpSound.mp3")
HONK = pygame.mixer.Sound("assets/music/horn.wav")
LOW = pygame.mixer.Sound("assets/music/lowAlert.wav")
WIN = pygame.mixer.Sound("assets/music/win.wav")
PICK.set_volume(0.3)
HONK.set_volume(0.2)
LOW.set_volume(0.2)
WIN.set_volume(0.6)

'''
about light
light x : positive mean point from - to + (need extreme value)
light y : positive mean point from - to + (need extreme value)
light z : positive mean point from - to +
'''
# setup for 3d object
LIGHT = np.array([0,0,100])

FAR = 100
NEAR = 0.1
HFOV = radians(80)
VFOV = HFOV*SCREENHEIGHT/SCREENWIDTH
LEFT = tan(HFOV/2) # left = -rigth
TOP = tan(VFOV/2) # top = -bottom
RIGTH = -LEFT
BOTTOM = -TOP

DISTANT = FAR - NEAR

m00 = 2/(RIGTH-LEFT)
m11 = 2/(TOP-BOTTOM)
m22 = (FAR+NEAR)/(FAR-NEAR)
m32 = -2*NEAR*FAR/(FAR-NEAR)

PROJMATRIX = np.array([
    [m00,0,0,0],
    [0,m11,0,0],
    [0,0,m22,1],
    [0,0,m32,0]
])

HW, HH = SCREENWIDTH/2,SCREENHEIGHT/2
to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]])
'''
to screen matrix gives new matrix like this
[x y z w] * [a 0 0 0]
            [0 b 0 0]
            [0 0 1 0]
            [a b 0 1]
=   [x*a + y*0 + z*0 + w*a]
    [x*0 + y*b + z*0 + w*b]
    [x*0 + y*0 + z*1 + w*0]
    [x*0 + y*0 + z*0 + w*1]
=   [x*a + w*a] scale x by a and move x by w*a
    [y*b + w*b] scale y by b and move y by w*b
    [z] keep z
    [w] keep w
'''


OBJSPD = 3*DT
ROTSPD = 120*DT

# read model
with open('assets/obj.json', 'r') as file:
    model = json.load(file)

'''
remember that camera is facing to the negative z
so obj.z + something is moving object to camera
   the more obj.z the it close to the camera
'''
# road
ROADPLAIN = model["roadPlain"]
ROADLINE = model["roadLine"]
ROADEDGE = model["roadEdge"]

# map
MNTL2 = model["mntL2"]
MNTR2 = model["mntR2"]

# nitrus
NITRUSHEAD = model["nitrus"]["head"]
NITRUSTANK = model["nitrus"]["tank"]

# gas
GASTANK = model["gas"]["gasTank"]
GASPIPE = model["gas"]["gasPipe"]

# wrench
WRENCH = model["wrench"]

# sedan
SEDBODY = model["sedan"]["body"]
SEDTRUNK = model["sedan"]["trunk"]
SEDWINF = model["sedan"]["windowF"]
SEDWINR = model["sedan"]["windowR"]
SEDWINL = model["sedan"]["windowL"]
SEDWFR = model["sedan"]["wheelFR"]
SEDWFL = model["sedan"]["wheelFL"]
SEDWRR = model["sedan"]["wheelRR"]
SEDWRL = model["sedan"]["wheelRL"]

# pickup
PICKBODY = model["pickup"]["body"]
PICKTRUNK = model["pickup"]["trunk"]
PICKWINF = model["pickup"]["windowF"]
PICKWINR = model["pickup"]["windowR"]
PICKWINL = model["pickup"]["windowL"]

# truck
TRUCKBODY = model["truck"]["body"]
TRUCKTRUNK = model["truck"]["trunk"]
TRUCKWINF = model["truck"]["windowF"]
TRUCKWINR = model["truck"]["windowR"]
TRUCKWINL = model["truck"]["windowL"]

# ==================================== COLOUR ==================================== #
DESERT = (242, 157, 82)
CRIMSON = (220,20,60)
SEASHELL = (255,245,238)
DEEPSKYBLUE = (0,191,255)
ORANGERED = (242, 107, 29)
MAXYELLOWRED = (242, 180, 65)
INDIANORANGE = (255, 119, 34)
SUNGLOW = (255, 204, 51)
JADE = (0, 168, 107)
TYROLITE = (0, 164, 153)
LUST = (230, 32, 32)
GOLD = (255, 215, 0)
AZURE = (0, 128, 255)
SLATEGRAY = (112, 128, 144)
COVERTBLACK = (22, 22, 27)
PERSIANGREEN =  (44, 161, 128)
HEAVENLYGREEN = (96, 172, 71)
MATTECHARCOAL = (59, 66, 72)
PALEGRAY = (192, 192, 192)
FFFWHITE = (255,255,255)
COSMICPURPLE = (104, 25, 147)
DIGITALNAY = (0, 0, 128)
ELECTRICNAVY = (46, 31, 182)

# color of light
LIGHTCOLOR = GOLD

# color of car (for randoms)
CARCOLOR1 = [CRIMSON,PALEGRAY]
CARCOLOR2 = [TYROLITE,PALEGRAY]
CARCOLOR3 = [INDIANORANGE,PALEGRAY]
CARCOLOR4 = [GOLD,PALEGRAY]

CARCOLORSET = [CARCOLOR1,CARCOLOR2,CARCOLOR3,CARCOLOR4]

# draw rgadient
def drawGradient(lineNum,color1,color2,rect,vertical = True):
    x = rect[0]
    y = rect[1]
    if vertical:
        w = rect[2]
        h = rect[3]//lineNum
    else:
        w = rect[2] // lineNum
        h = rect[3]

    r1,g1,b1 = color1
    r2,g2,b2 = color2
    for i in range(lineNum):
        r = r1 * (lineNum - i)/lineNum + r2 * (i)/lineNum
        g = g1 * (lineNum - i)/lineNum + g2 * (i)/lineNum
        b = b1 * (lineNum - i)/lineNum + b2 * (i)/lineNum
        pygame.draw.rect(SCREEN,(r,g,b),(x + (w * i) * (not vertical),y + (h * i) * vertical,w,h))
