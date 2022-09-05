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
        glClearColor(0.1, 0, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = Shader("shaders/vertex.txt", "shaders/fragment.txt")
        self.shader.use()
        self.shader.setInt("imageTexture", 0)
        pg.mouse.set_visible(False)
        self.sphere_mesh = Mesh("meshes/sphere.obj")

        self.renderList = {
            "sphere1" : RenderObject(
                position= [-2, 0, 0],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.sphere_mesh
            ),
             "sphere2" : RenderObject(
                position= [1, 0, 1],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= self.sphere_mesh
            ),
             "sphere3" : RenderObject(
                position= [0, 1, 0],
                eulers= [0, 0, 2],
                scale=[1, 0.4, 1],
                mesh= self.sphere_mesh
            ),
            "sphere4" : RenderObject(
                position= [1, 2, -3],
                eulers= [0, 0, 0],
                scale=[0.1, 0.1, 0.1],
                mesh= self.sphere_mesh
            )

        }
       
        self.test_texture = Material("gfx/notha.jpg")

        self.camera = Camera("FPS")
        
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.mainLoop()

    def mainLoop(self):
        
        self.running = True
        self.vector = .1
        self.color = 0.0
        self.colorV = 0.1
        oldTime = pg.time.get_ticks()
        speed = 0.1
        sensitivity = 0.15
        fovy = 90
        while (self.running):
            deltaTime = oldTime - pg.time.get_ticks()
            oldTime = deltaTime
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

            self.playerInput(key, speed)
            
            
            self.playground()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            
            projection_transform = pyrr.matrix44.create_perspective_projection(
                fovy= fovy, aspect= self.window_height/self.window_width,
                near= 0.1, far= 100, dtype=np.float32
            )


            self.shader.setMatrix4vf("projection", projection_transform)

            self.shader.use()   
            self.test_texture.use()
            self.shader.setMatrix4vf("view", self.camera.makeLookAt())

            for renderObjct in self.renderList:
                self.shader.setFloatv4("myColor", [self.color * -1.0, 0.5, self.color, 1.0])
                self.shader.setMatrix4vf("model", self.renderList[renderObjct].SRT())
                self.renderList[renderObjct].draw()

            pg.display.flip() 

            self.clock.tick(60)
        self.quit()

    def playground(self):
        self.renderList["sphere1"].position[2] += self.vector
            
        self.renderList["sphere1"].eulers[0] += 2
            
        if (self.renderList["sphere1"].eulers[0] > 360):
            self.renderList["sphere1"].eulers[0] -= 360
        if (self.renderList["sphere1"].position[2] < -10) or self.renderList["sphere1"].position[2] > 10:
            self.vector *= -1

        if self.color >= 1.0 or self.color <= -1.0:
            self.colorV *= -1.0

        self.color += self.colorV

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
        

    def quit(self):
        self.sphere_mesh.destroy()
        self.test_texture.destroy()
        self.shader.delete()
        pg.quit()


if __name__ == "__main__":
    myApp = App(1080, 720)