from imports import *
from HelperClasses import *

# This is what a user will instantiate whenever they want to generate an 'entity'
# Game object holds a positional value
class GameObject:
    # each game object has a pointer to the render and physics engine. May not be the best idea, but allows them to make 
    def __init__(self, name, renderEngine, physicsEngine, transform):
        self.name = name
        self.transform = transform
        self.renderEngine = renderEngine
        self.physicsEngine = physicsEngine
        self.render_object = None
        self.physics_object = None

    # called for each game object, will run update code for each component if it has that property

    def addRenderObject(self, mesh, shader, texture = False, color = [0, 0, 0, 0]):
        # maybe turn params into defaults
        self.render_object = self.renderEngine.createRenderObject(self.name, self.transform, mesh, shader, texture, color)

     