import string
from imports import *
from HelperClasses import *
from GameObject import *

# This handles the generating of game objects
class Game:

    def __init__(self, camera, renderEngine = False, physicsEngine = False):
        # The game engine is completely decoupled from both of the engines in this manner.
        # As long as it complies with the interfaces (to be defined) it will work correctly.
        # This should ideally make the code more maintainable, but idk.

        self.renderEngine = renderEngine
        self.physicsEngine = physicsEngine
        self.objectList = {}
        # Think about multi camera system in the future
        self.camera = camera
        self.objectCounter = 0

        # create a queue object here TODO
        # self.events = 
        # Idea for contructing events,
        #  events are objects, and they are created from classes bound by the event interface
        #  the events can be triggered, which pushed an object onto the stack for use
        #  so I can create a 'make red cube' event and trigger it multiple times
        #  this would push the event onto the event queue, which will be used to process events
        #  could be a potentially powerful tool?!?

       
    def updateEngineStates(self, dt = 0):
        # Updates both engines to the next state
        
        # Note, the order of updating is signifigant.
        #    The main process is that the physics engine computes the new locations
        #     and the render engine draws those objects with their updated positions

        if self.physicsEngine:
            self.physicsEngine.update(dt)

        if self.renderEngine:
            self.renderEngine.update(self.camera)


    # I think some method of event handling is a good idea
    #    I'm not sure what it should look like at the momment,
    #     But the general idea would be to have a queue of events that anything can add to
    #      These events would fall under an interface, and would have a resolution to them
    #      Events would mainly be related to user input, to prevent certain misshaps on their end
    def handleEvents(self):
        pass

        

    def createObj(self, name : string = False, transform : Transform = False):

        # This function creates a game object:
        #    Param: name -> Default gives it a default value, used to track the game object
        #    Param: transform -> Allows the user to set the object as a predetermined space


        if not transform:
            self.transform = Transform()
        else:
            self.transform = transform

        if name == False:
            name = "object" + str(self.objectCounter)
        self.objectCounter += 1
        self.objectList[name] = GameObject(name, self.renderEngine, self.physicsEngine, self.transform)
        # Have a method for overwriting objects?!?!? How!?!?
        return self.objectList[name]

    def getObj(self, name):
        if self.objectList[name]:
            return self.objectList[name]
        return None
    
    def getObjByTag(self, tag):
        pass