import MatrixOperand
import Setting
from Setting import *
import pygame as pg
from MatrixOperand import *
import math
from math import *

class Camera:
    def __init__(self, position,controlable = True,angle = [0,0,0]):
        self.controlable = controlable
        self.operand = MatrixOperand()
        self.position = np.array([*position, 1.0])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (Setting.SCREENHEIGHT/Setting.SCREENWIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 5
        self.rotation_speed = 120

        self.angleX = angle[0] # X angle
        self.angleZ = angle[2] # Z angle
        self.angleY = angle[1] # Y angle

    def control(self,delta):
        if not self.controlable:
            return
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.position -= self.right * self.moving_speed * delta
        if key[pg.K_RIGHT]:
            self.position += self.right * self.moving_speed * delta
        if key[pg.K_UP]:
            self.position -= self.forward * self.moving_speed * delta
        if key[pg.K_DOWN]:
            self.position += self.forward * self.moving_speed * delta
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed * delta
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed * delta

        if key[pg.K_a]:
            self.camera_yaw(-self.rotation_speed * delta)
        if key[pg.K_d]:
            self.camera_yaw(self.rotation_speed * delta)
        if key[pg.K_z]:
            self.camera_rot(-self.rotation_speed * delta)
        if key[pg.K_x]:
            self.camera_rot(self.rotation_speed * delta)
        if key[pg.K_w]:
            self.camera_pitch(self.rotation_speed * delta)
        if key[pg.K_s]:
            self.camera_pitch(-self.rotation_speed * delta)

    def camera_rot(self, angle):
        self.angleZ += angle

    def camera_yaw(self, angle):
        self.angleY += angle

    def camera_pitch(self, angle):
        self.angleX += angle

    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        # rotate = rotate_y(self.angleY) @ rotate_x(self.angleX)
        rotate = self.operand.rx(self.angleX) @ self.operand.ry(self.angleY) @ self.operand.rz(self.angleZ)  # this concatenation gives right visual
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])