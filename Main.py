from Game import *
from imports import *
from Rendering.Material import *
from Rendering.Mesh import *
from Rendering.Shader import *
from Rendering.RenderEngine import *
from Rendering.Camera import *

RFP = "Rendering/"
PFP = "Physics/"
class App:

    def __init__(self, height, width):

        self.renderEngine = RenderEngine(height= height, width= width)
        self.clock = pg.time.Clock()
        self.camera = Camera("FPS")
        self.Game = Game(self.camera, self.renderEngine)

        self.renderEngine.shaderList = {
            "v1" : Shader(RFP + "shaders/v1/vertex.txt", RFP + "shaders/v1/fragment.txt"),
            "v2" : Shader(RFP + "shaders/v2/vertex.txt", RFP + "shaders/v2/fragment.txt"),
            "lighting_v1" : Shader( RFP + "shaders/lighting_v1/vertex.txt", RFP + "shaders/lighting_v1/fragment.txt")
        }

        self.renderEngine.meshList = {
            "sphere" : Mesh(RFP + "meshes/sphere.obj"),
            "terrain" : Mesh(RFP + "meshes/wierdland.obj"),
            "cube" : Mesh(RFP + "meshes/cube.obj")
        }

        self.renderEngine.textureList = {
            "wood" : Material(RFP + "gfx/notha.jpg"),
            "grass" : Material(RFP + "gfx/grass.jpg"),
            "missing" : Material(RFP + "gfx/missing.jpg"),
            "red" : Material(RFP + "gfx/red.jpg")
        }
        

        self.test = self.Game.createObj()
        self.test.addRenderObject("sphere", "v2", "wood")
  

        self.test2 = self.Game.createObj("testCube1")
        self.test2.addRenderObject("cube", "v2", "red")

        self.light = self.Game.createObj("light", 
            Transform(
                position=[0, 10, 0],
                rotation=[0,0,0],
                scale=[1,1,1]))
        self.light.addRenderObject("sphere", "lighting_v1", "red", False, True)

        self.mainLoop()

    def mainLoop(self):
        
        self.running = True
        self.vector = 5
        speed = 5
        sensitivity = 0.15
        self.deltaTime = 1
        oldTime = 0
        self.radius = 20
        self.count = 0

        while (self.running):

            #Time tracking -- Delta time calculation
            #pg.display.set_caption("FPS: " + str(1.0 / (self.deltaTime)))
            time = pg.time.get_ticks()
            self.deltaTime = ((time - oldTime) + 1) / 1000.0
            oldTime = time
            self.count += 0.5 * self.deltaTime
            #End Time Tracking

            #User Input event handling
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    self.running = False
                if event.type == pg.MOUSEMOTION:
                    offsets = event.rel
                    self.camera.rotateWithMouseOffset(offsets[0], offsets[1], sensitivity)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.camera.fovy -= 5
                        if self.camera.fovy < 1:
                            self.camera.fovy = 1
                    if event.button == 5:
                        self.camera.fovy += 5
                        if self.camera.fovy > 120:
                            self.camera.fovy = 120
            key = pg.key.get_pressed()
            self.playerInput(key, speed * self.deltaTime)
            #End User Input handling
            
            # Non user input dynamics
            #self.playground()
            self.test.transform.position[0] += 0.01
            self.test2.transform.rotation[2] += 0.5
            # End Dynamics


            #3D rendering code

                #Current idea is to allow for rendering for multiple windows in the future, maybe.
                #Not sure if this is the best approach, we'll see.
            self.Game.updateEngineStates()

            # End Rendering code


            self.clock.tick(60)
        self.quit()

    def playground(self):
        self.renderList["sphere1"].position[2] += self.vector * self.deltaTime
            
        self.renderList["sphere1"].eulers[0] += 300 * self.deltaTime
            
        if (self.renderList["sphere1"].eulers[0] > 360):
            self.renderList["sphere1"].eulers[0] -= 360
        if (self.renderList["sphere1"].position[2] < -10) or self.renderList["sphere1"].position[2] > 10:
            self.vector *= -1 

        self.renderList["light"].position[0] = (cos(self.count) * self.radius) + 20 
        self.renderList["light"].position[2] = (sin(self.count) * self.radius ) 
        
    def playerInput(self, key, speed):
        if key[pg.K_w]:
            self.camera.move("forward", speed)
        if key[pg.K_a]:
            self.camera.move("left", speed)
        if key[pg.K_s]:
            self.camera.move("backward", speed)
        if key[pg.K_d]:
            self.camera.move("right", speed)
        if key[pg.K_SPACE]:
             self.camera.move("up", speed)
        if key[pg.K_LCTRL]:
             self.camera.move("down", speed)
        if key[pg.K_ESCAPE]:
            self.running = False
        if key[pg.K_0]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if key[pg.K_1]:
            # some sort of 'event handler' should be implemented, as this will create multiple objects
            self.Game.createObj("testcube23").addRenderObject("cube", "v2", "red")
        

    def quit(self):
        self.renderEngine.destroy()

        pg.quit()



if __name__ == "__main__":
    myApp = App(1080, 720)