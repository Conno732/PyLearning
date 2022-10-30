import string
from typing import Dict
from numpy import delete
from Physics.PhysicsObject import PhysicsObject
from imports import *

# General design 

# Dynamics, adding acceleration, velocity and positions (gravity, user input, AI)

# Loop over all of the physics objects

# Detect collisions -> use methods to optimize this (Octal trees? spatial maps??)

# Handle collisions -> Depending on collision model (sphere vs sphere, cube vs plane, etc)
#                   -> Solve these collisions by updating the force vector?

# 

class PhysicsEngine:

    def __init__(self, gravity : float):
        self.gravity = gravity
        self.objectList = {}

    def createPhysicsObject(self, name, transform, collisionModel, mass):
        self.objectList[name] = PhysicsObject(transform=transform, collisionModel=collisionModel, mass=mass)
        return self.objectList[name]


    def deletePhysicsObject(self, name):
        pass

    def update(self, dt):

        for v in self.objectList.values():
            obj : PhysicsObject = v
            obj.Force[1] += obj.mass * self.gravity
            newarr =  (obj.Force / obj.mass) * dt
            obj.velocity[0] += newarr[0]
            obj.velocity[1] += newarr[1]
            obj.velocity[2] += newarr[2]
            obj.transform.position += obj.velocity * dt

            obj.Force = np.array([0, 0, 0])