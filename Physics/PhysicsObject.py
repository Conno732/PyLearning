from HelperClasses import Transform
from imports import *


class PhysicsObject:

    def __init__(self, transform : Transform, collisionModel, mass):
        self.transform = transform
        self.velocity = np.array([0, 0, 0], dtype=np.float32)
        self.Force = np.array([0, 0, 0], dtype=np.float32)
        self.mass : float = mass

        # A collision model reflects what the object is meant to be. Allows for optimizations in collisions
        self.collisionModel = collisionModel


