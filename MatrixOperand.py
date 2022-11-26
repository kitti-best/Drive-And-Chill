from Setting import *
from Camera import *
import numpy as np

class MatrixOperand:
    def translate(self,tx, ty, tz):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tz, 1]
        ])


    def scaling(self,scale):
        return np.array([
            [scale, 0, 0, 0],
            [0, scale, 0, 0],
            [0, 0, scale, 0],
            [0, 0, 0, 1]
        ])

    def rx(self,angle):
        return np.array([
            [1, 0, 0, 0],
            [0, cos(radians(angle)), -sin(radians(angle)), 0],
            [0, sin(radians(angle)), cos(radians(angle)), 0],
            [0, 0, 0, 1],
        ])

    def ry(self,angle):
        return np.array([
            [cos(radians(angle)), 0, sin(radians(angle)), 0],
            [0, 1, 0, 0],
            [-sin(radians(angle)), 0, cos(radians(angle)), 0],
            [0, 0, 0, 1]
        ])

    def rz(self,angle):
        return np.array([
            [cos(radians(angle)), -sin(radians(angle)), 0, 0],
            [sin(radians(angle)), cos(radians(angle)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def toZero(self):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def project(self):
        return PROJMATRIX