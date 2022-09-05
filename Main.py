from Camera import *
from imports import *
from Material import *
from Mesh import *
from RenderObject import *
from Shader import *

class App:

    def __init__(self, height, width):
        pg.init()
        pg.display.set_mode((height, width), pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.window_height = height
        self.window_width = width
        glClearColor(0.1, 0, 0.1, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        pg.mouse.set_visible(False)

        self.shaderList = {
            "v1" : Shader("shaders/v1/vertex.txt", "shaders/v1/fragment.txt")
        }

        self.meshList = {
            "sphere" : Mesh("meshes/sphere.obj"),
            "terrain" : Mesh("meshes/wierdland.obj"),
            "cube" : Mesh("meshes/cube.obj")
        }

        self.textureList = {
            "wood" : Material("gfx/notha.jpg"),
            "grass" : Material("gfx/grass.jpg"),
            "missing" : Material("gfx/missing.jpg"),
            "red" : Material("gfx/red.jpg")
        }

        self.renderList = {
            "sphere1" : RenderObject(
                position= [-2, 0, 0],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v1"],
                texture= self.textureList["wood"],
            ),
             "sphere2" : RenderObject(
                position= [1, 0, 1],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v1"],
                texture= self.textureList["wood"]
            ),
             "sphere3" : RenderObject(
                position= [0, 1, 0],
                eulers= [0, 0, 2],
                scale=[1, 0.4, 1],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v1"],
                texture= self.textureList["wood"]
            ),
            "sphere4" : RenderObject(
                position= [1, 2, -3],
                eulers= [0, 0, 0],
                scale=[0.1, 0.1, 0.1],
                mesh= self.meshList["sphere"],
                shader= self.shaderList["v1"],
                texture= self.textureList["wood"]
            ),
            "cube1" : RenderObject(
                position= [20, 10, 0],
                eulers=[0, 2, 4],
                scale=[10, 10, 10],
                mesh= self.meshList["cube"],
                shader= self.shaderList["v1"],
                texture= self.textureList["red"],
                color=[0, 0.5, 0.0, 0.0]
            ),
            "terrain" : RenderObject(
                position= [0, -3, 0],
                eulers=[0,0,0],
                scale=[1,1,1],
                mesh= self.meshList["terrain"],
                shader= self.shaderList["v1"],
                texture= self.textureList["grass"]
            )

        }
       
        
        self.camera = Camera("FPS")
        
        
        self.mainLoop()

    def mainLoop(self):
        
        self.running = True
        self.vector = 5
        oldTime = pg.time.get_ticks()
        speed = 5
        sensitivity = 0.15
        fovy = 90
        self.deltaTime = 1
        oldTime = 0
        while (self.running):
            pg.display.set_caption("FPS: " + str(1.0 / (self.deltaTime)))
            time = pg.time.get_ticks()
            self.deltaTime = ((time - oldTime) + 1) / 1000.0
            oldTime = time
            

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    self.running = False
                if event.type == pg.MOUSEMOTION:
                    offsets = event.rel
                    self.camera.rotateWithMouseOffset(offsets[0], offsets[1], sensitivity)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        fovy -= 5
                        if fovy < 1:
                            fovy = 1
                    if event.button == 5:
                        fovy += 5
                        if fovy > 120:
                            fovy = 120

                    
        
                    
            key = pg.key.get_pressed()

            self.playerInput(key, speed * self.deltaTime)
            
            
            self.playground()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # maybe put this in the camera object... If there are multiple cameras, then different windows 
            projection_transform = pyrr.matrix44.create_perspective_projection(
                fovy= fovy, aspect= self.window_height/self.window_width,
                near= 0.1, far= 100, dtype=np.float32
            )


            for shader in self.shaderList:
                self.shaderList[shader].use()
                self.shaderList[shader].setMatrix4vf("projection", projection_transform)
                self.shaderList[shader].setMatrix4vf("view", self.camera.makeLookAt())


            for renderObjct in self.renderList:
                obj = self.renderList[renderObjct]
                obj.shader.use()
                if (obj.texture):
                    obj.texture.use()
                else:
                    self.textureList["missing"].use()

                obj.shader.setFloatv4("myColor", obj.color)
                obj.shader.setMatrix4vf("model", obj.SRT())
                obj.draw()

            pg.display.flip() 

            #self.clock.tick(60)
        self.quit()

    def playground(self):
        self.renderList["sphere1"].position[2] += self.vector * self.deltaTime
            
        self.renderList["sphere1"].eulers[0] += 300 * self.deltaTime
            
        if (self.renderList["sphere1"].eulers[0] > 360):
            self.renderList["sphere1"].eulers[0] -= 360
        if (self.renderList["sphere1"].position[2] < -10) or self.renderList["sphere1"].position[2] > 10:
            self.vector *= -1


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