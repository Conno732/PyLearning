from imports import *

class Camera:

    def __init__(self):
        self.cameraPos = pyrr.Vector3([0.0, 0.0, 3.0])
        self.cameraFront = pyrr.Vector3([0.0, 0.0, -1.0])
        self.cameraUp = pyrr.Vector3([0.0, 1.0, 0.0])
        self.up = [0.0, 1.0, 0.0]

    def lookAt(self, position, target):
        # cameraDirction = pyrr.vector.normalise(self.cameraPos -self.cameraTarget)
        # self.cameraRight = pyrr.vector.normalise(pyrr.vector3.cross(self.up, self.cameraDirction))
        # self.cameraUp = pyrr.vector3.cross(self.cameraDirction, self.cameraRight)
        # return pyrr.matrix44.create_look_at(self.cameraPos, target, self.cameraUp)
        pass

    def makeLookAt(self):
        return pyrr.matrix44.create_look_at(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)

    def move(self, position, magnitude):
        if position == "forward":
            self.cameraPos += magnitude * self.cameraFront

        elif position == "backward":
            self.cameraPos -= magnitude * self.cameraFront

        elif position == "left":
            self.cameraPos -= pyrr.vector.normalise(pyrr.vector3.cross(self.cameraFront, self.cameraUp)) * magnitude

        elif position == "right":
            self.cameraPos += pyrr.vector.normalise(pyrr.vector3.cross(self.cameraFront, self.cameraUp)) * magnitude