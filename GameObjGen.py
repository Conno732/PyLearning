import imp
from imports import *
from HelperClasses import *
from GameObject import *

# This handles the generating of game objects
class GameObjGen:

    def __init__(self, renderEngine, physicsEngine = False):
        self.renderEngine = renderEngine
        self.physicsEngine = physicsEngine

    def createGameObj(self, name, transform = False):
        if not transform:
            self.transform = Transform()
        else:
            self.transform = transform
        return GameObject(name, self.renderEngine, self.physicsEngine, self.transform)