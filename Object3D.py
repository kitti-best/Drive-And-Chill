from numba import *
from Setting import *

@njit
def cal(normal,light,color,lightColor):
    lx, ly, lz = light
    nx, ny, nz = normal

    dp = nx * lx + ny * ly + nz * lz

    r, g, b = color
    lr, lg, lb = lightColor

    r = r - (lr * dp + 0.1) / 10
    g = g - (lg * dp + 0.1) / 10
    b = b - (lb * dp + 0.1) / 10

    r = max(min(r, 255), 0)
    g = max(min(g, 255), 0)
    b = max(min(b, 255), 0)

    return (r, g, b)

class Object(MatrixOperand):
    def __init__(self,model,color,camera,startTrans = [0,0,0],startRot = [0,0,0],scale = 1):
        self.camera = camera

        self.startTrans = startTrans
        self.startRot = startRot

        self.points = np.array(model['vertexes'])
        self.faces = np.array(model['faces'])
        self.color = np.array([float(x) for x in color])

        self.move_speed = OBJSPD
        self.rot_speed = ROTSPD

        self.currXAngle = 0
        self.currYAngle = 0
        self.currZAngle = 0

        self.currXTravel = 0
        self.currYTravel = 0
        self.currZTravel = 0

        self.destroy = False

        self.initPoint(startTrans,startRot,scale)
        self.update(True)

        self.dimensionX = abs(self.maxx - self.minx)
        self.dimensionY = abs(self.maxy - self.miny)
        self.dimensionZ = abs(self.maxz - self.minz)

        self.light = LIGHT
        self.lightColor = LIGHTCOLOR

    def calColor(self,normal):
        return cal(normal,self.light,self.color,self.lightColor)

    def changeCamera(self,camera):
        self.camera = camera

    def findBorder(self):
        # find the leftmost right most top most and closest z of this obj
        self.minz = min(self.points[:, 2])  # farest
        self.maxz = max(self.points[:, 2])  # closest
        self.minx = min(self.points[:, 0])  # left most
        self.maxx = max(self.points[:, 0])  # right most
        self.miny = min(self.points[:, 1])  # top most
        self.maxy = max(self.points[:, 1])  # bottom

        self.center = np.array([round((self.minx + self.maxx) / 2,5),
                                round((self.miny + self.maxy) / 2,5),
                                round((self.minz + self.maxz) / 2,5)])

    def drawPoint(self):
        for i,point in enumerate(self.point2D):
            pointToDraw = point[:2]
            if pointToDraw[0] > 800 or pointToDraw[0] < 0 or pointToDraw[1] > 600 or pointToDraw[1] < 0:
                continue
            pygame.draw.circle(SCREEN,(255,0,0),pointToDraw,5)

    def cross(self, triangleUnit):
        a = triangleUnit[2] - triangleUnit[0]
        b = triangleUnit[1] - triangleUnit[0]
        ax, ay, az = a[0], a[1], a[2]
        bx, by, bz = b[0], b[1], b[2]
        normal = np.array([ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx])
        self.normal = normal
        return normal

    # @lru_cache(5)
    def findValidTriangle(self):
        self.validTri = []
        for face in self.faces:
            triangle2d = []
            triangleUnit = []
            # extract all point that in the face
            for pointNum in face:
                triangle2d.append(self.point2D[pointNum-1])
                triangleUnit.append(self.normalized[pointNum-1])
            # count triangle that out of screen
            forgive = 0
            countOffScreen = 0
            for point in triangleUnit:
                if abs(point[0]) > 1 + forgive or abs(point[1]) > 1 + forgive or abs(point[2]) < 1:
                    countOffScreen += 1
            # find normal of the triangle using cross product
            normal = self.cross(triangleUnit)
            if normal[2] > 0 and countOffScreen <= 1:
                self.validTri.append([triangle2d,normal,normal[2]])

        # self.validTri = sorted(self.validTri,key = itemgetter(2))

    def run(self):
        for triangle,normal,z in self.validTri:
            pygame.draw.polygon(SCREEN, self.calColor(normal), triangle)

    def updatePoint(self):
        self.point2D = self.points @ self.camera.camera_matrix() # translate, rotate using camera as reference points
        self.point2D = self.point2D @ PROJMATRIX # make perspective
        self.point2D /= self.point2D[:, -1].reshape(-1,1) + 0.1 # normalization
        self.normalized = self.point2D[:,:3]
        self.point2D = self.point2D @ to_screen_matrix # scale and offset
        self.point2D = self.point2D[:,:2]

    def update(self,keyOccur = False):
        if not keyOccur:
            return

        self.updatePoint()
        self.findBorder()
        self.findValidTriangle()

    def initPoint(self,trans,angle,scale):
        self.points = self.points @ self.rx(angle[0]) @ self.ry(angle[1]) @ self.rz(angle[2])
        self.points = self.points @ self.scaling(scale)
        self.points = self.points @ self.translate(trans[0],trans[1],trans[2])

        self.startPoints = self.points

    def movement(self,trans = [0,0,0],rot = [0,0,0],delta = 1):
        tx,ty,tz = trans
        ax,ay,az = rot
        self.points = self.startPoints
        self.currXAngle += ax * delta
        self.currYAngle += ay * delta
        self.currZAngle += az * delta
        self.currXTravel += tx * delta
        self.currYTravel += ty * delta
        self.currZTravel += tz * delta
        self.points = self.points @ self.translate(-self.startTrans[0], -self.startTrans[1], -self.startTrans[2])
        self.points = self.points @ self.rx(self.currXAngle) @ self.ry(self.currYAngle) @ self.rz(self.currZAngle)
        self.points = self.points @ self.translate(self.startTrans[0], self.startTrans[1], self.startTrans[2])
        self.points = self.points @ self.translate(self.currXTravel, self.currYTravel, self.currZTravel)

    def resetPosition(self):
        self.points = self.startPoints

    def checkCollision(self,object):
        hit = self.minx <= object.maxx and\
        self.maxx >= object.minx and\
        self.miny <= object.maxy and\
        self.maxy >= object.miny and\
        self.minz <= object.maxz and\
        self.maxz >= object.minz

        if hit:
            return True
        return False
