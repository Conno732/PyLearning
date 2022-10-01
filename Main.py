from Rendering.Camera import *
from imports import *
from Rendering.Material import *
from Rendering.Mesh import *
from Rendering.RenderObject import *
from Rendering.Shader import *
from Rendering.RenderEngine import *

RFP = "Rendering/"
PFP = "Physics/"
class App:

    def __init__(self, height, width):

        self.renderEngine = RenderEngine(height= height, width= width)
        self.clock = pg.time.Clock()

        self.shaderList = {
            "v1" : Shader(RFP + "shaders/v1/vertex.txt", RFP + "shaders/v1/fragment.txt"),
            "v2" : Shader(RFP + "shaders/v2/vertex.txt", RFP + "shaders/v2/fragment.txt"),
            "lighting_v1" : Shader( RFP + "shaders/lighting_v1/vertex.txt", RFP + "shaders/lighting_v1/fragment.txt")
        }

        self.meshList = {
            "sphere" : Mesh(RFP + "meshes/sphere.obj"),
            "terrain" : Mesh(RFP + "meshes/wierdland.obj"),
            "cube" : Mesh(RFP + "meshes/cube.obj")
        }

        self.textureList = {
            "wood" : Material(RFP + "gfx/notha.jpg"),
            "grass" : Material(RFP + "gfx/grass.jpg"),
            "missing" : Material(RFP + "gfx/missing.jpg"),
            "red" : Material(RFP + "gfx/red.jpg")
        }

        self.renderList = {
            "sphere1" : RenderObject(
                position= [-2, 0, 0],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v2"],
                texture= self.textureList["wood"],
            ),
            "sphere11" : RenderObject(
                position= [0, 2, 4],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v2"],
                texture= self.textureList["wood"],
            ),
             "sphere2" : RenderObject(
                position= [1, 4, 1],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v2"],
                texture= self.textureList["wood"]
            ),
             "sphere3" : RenderObject(
                position= [0, 1, 0],
                eulers= [0, 0, 2],
                scale=[1, 0.4, 1],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v2"],
                texture= self.textureList["wood"]
            ),
            "sphere4" : RenderObject(
                position= [1, 2, -3],
                eulers= [0, 0, 0],
                scale=[0.1, 0.1, 0.1],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v2"],
                texture= self.textureList["wood"]
            ),
            "cube1" : RenderObject(
                position= [20, 10, 0],
                eulers=[0, 2, 4],
                scale=[6, 6, 6],
                mesh= self.meshList["cube"],
                shader= self.shaderList["v2"],
                texture= self.textureList["red"],
                color=[1.0, 0.5, 0.31, 0.0]
            ),
            "terrain" : RenderObject(
                position= [0, -3, 0],
                eulers=[0,0,0],
                scale=[1,1,1],
                mesh= self.meshList["terrain"],
                shader= self.shaderList["v2"],
                texture= self.textureList["grass"],
                color=[1.0, 0.5, 0.31, 0.0]
            ),
            "terrain2" : RenderObject(
                position= [50, -3, 0],
                eulers=[0,0,0],
                scale=[1,1,1],
                mesh= self.meshList["terrain"],
                shader= self.shaderList["v2"],
                texture= self.textureList["grass"],
                color=[1.0, 0.5, 0.31, 0.0]
            ),
            "terrain3" : RenderObject(
                position= [-50, -3, 0],
                eulers=[0,0,0],
                scale=[1,1,1],
                mesh= self.meshList["terrain"],
                shader= self.shaderList["v2"],
                texture= self.textureList["grass"],
                color=[1.0, 0.5, 0.31, 0.0]
            ),
            "terrain4" : RenderObject(
                position= [-50, -3, 80],
                eulers=[0,0,0],
                scale=[1,1,1],
                mesh= self.meshList["terrain"],
                shader= self.shaderList["v2"],
                texture= self.textureList["grass"],
                color=[1.0, 0.5, 0.31, 0.0]
            ),
            "light" : RenderObject(
                position=[0, 10, 0],
                eulers=[0,0,0],
                scale=[1,1,1],
                mesh= self.meshList["cube"],
                shader= self.shaderList["lighting_v1"],
                texture= self.textureList["red"]
            )

        }
       

        self.renderEngine.setRenderList(self.renderList)
        self.renderEngine.setShaderList(self.shaderList)
        self.camera = Camera("FPS")
        
        
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
            self.playground()
            # End Dynamics


            #3D rendering code

                #Current idea is to allow for rendering for multiple windows in the future, maybe.
                #Not sure if this is the best approach, we'll see.
            self.renderEngine.update(self.camera)

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
        

    def quit(self):
        for texture in self.textureList:
            self.textureList[texture].destroy()
        for mesh in self.meshList:
            self.meshList[mesh].destroy()
        for shader in self.shaderList:
            self.shaderList[shader].delete()

        pg.quit()


if __name__ == "__main__":
    myApp = App(1080, 720)