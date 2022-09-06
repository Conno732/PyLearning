from math import radians, cos, sin
from imports import *

class Camera:

    def __init__(self, mode):
        self.cameraPos = pyrr.Vector3([0.0, 0.0, 3.0])
        self.cameraFront = pyrr.Vector3([0.0, 0.0, -1.0])
        self.cameraUp = pyrr.Vector3([0.0, 1.0, 0.0])
        self.up = [0.0, 1.0, 0.0]
        self.pitch = 0.0
        self.yaw = -90.0
        self.mode = mode

    def makeLookAt(self):
        return pyrr.matrix44.create_look_at(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)

    def move(self, position, magnitude):
        if self.mode == "FPS":
            unit = math.sqrt(self.cameraFront[0] ** 2 + self.cameraFront[2] ** 2)
            front = np.array([self.cameraFront[0] / unit, 0, self.cameraFront[2] / unit])
        elif self.mode == "FreeFly":
            front = self.cameraFront

        if position == "forward":
            self.cameraPos += magnitude * front

        elif position == "backward":
            self.cameraPos -= magnitude * front

        elif position == "left":
            self.cameraPos -= pyrr.vector.normalise(pyrr.vector3.cross(front, self.cameraUp)) * magnitude

        elif position == "right":
            self.cameraPos += pyrr.vector.normalise(pyrr.vector3.cross(front, self.cameraUp)) * magnitude

        elif position == "up":
            self.cameraPos += [0, magnitude, 0]
        
        elif position == "down":
            self.cameraPos -= [0, magnitude, 0]

    def rotateWithMouseOffset(self, xOffset, yOffset, sensitivity):
        self.yaw += xOffset * sensitivity
        self.pitch += yOffset * sensitivity
        if self.pitch > 89.0:
            self.pitch = 89.0
        elif self.pitch < -89.0:
            self.pitch = -89.0

        self.cameraFront = pyrr.vector.normalise(pyrr.Vector3([cos(radians(self.yaw)) * cos(radians(self.pitch)), -1.0 * sin(radians(self.pitch)), sin(radians(self.yaw)) * cos(radians(self.pitch))]))