from imports import *


class CollisionPoints:

    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.normal = None # todo
        self.depth = None 
        self.hasCollision = None


class Transform:

    def __init__(self, position = [0, 0, 0], rotation = [0, 0, 0], scale = [1, 1, 1]):
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        self.scale = np.array(scale, dtype=np.float32)
        