from imports import *


class PhysicsObject:

    def __init__(self, transform, collisionModel = None, mass = 1):
        self.transform = transform
        self.velocity = np.array([0, 0, 0])
        self.Force = np.array([0, 0, 0])
        self.mass = mass
        # A collision model reflects what the object is meant to be. Allows for optimizations in collisions
        self.collisionModel = collisionModel


    
