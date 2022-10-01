from imports import *


class PhysicsObject:

    def __init__(self, position=[0, 0, 0], collisionModel = None, mass = 1):
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array([0, 0, 0])
        self.Force = np.array([0, 0, 0])
        self.mass = mass
        # A collision model reflects what the object is meant to be. Allows for optimizations in collisions
        self.collisionModel = collisionModel


    
