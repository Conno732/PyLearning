from imports import *

# This is what a user will instantiate whenever they want to generate an 'entity'
# Game object holds a positional value
class GameObject:

    def __init__(self, position=[0, 0, 0]):
        self.position = np.array(position, dtype=np.float32)
        self.render_object = None
        self.physics_object = None

    # called for each game object, will run update code for each component if it has that property

    