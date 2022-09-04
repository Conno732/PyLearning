from Camera import Camera
from imports import *
from Material import *
from Mesh import *
from RenderObject import *
from Shader import *

class App:

    def __init__(self, height, width):
        pg.init()
        pg.display.set_mode((height, width), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        glClearColor(0.1, 0, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = Shader("shaders/vertex.txt", "shaders/fragment.txt")
        self.shader.use()
        self.shader.setInt("imageTexture", 0)

        sphere_mesh = Mesh("meshes/sphere.obj")

        self.renderList = {
            "sphere1" : RenderObject(
                position= [-2, 0, 0],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= sphere_mesh
            ),
             "sphere2" : RenderObject(
                position= [1, 0, 1],
                eulers= [0, 0, 0],
                scale=[1, 1, 2],
                mesh= sphere_mesh
            ),
             "sphere3" : RenderObject(
                position= [0, 1, 0],
                eulers= [0, 0, 2],
                scale=[1, 0.4, 1],
                mesh= sphere_mesh
            ),
            "sphere4" : RenderObject(
                position= [1, 2, -3],
                eulers= [0, 0, 0],
                scale=[0.1, 0.1, 0.1],
                mesh= sphere_mesh
            )

        }
       
        self.test_texture = Material("gfx/notha.jpg")

        
        # cameraPos = pyrr.Vector3([0.0, 0.0, 3.0])
        # cameraTarget = pyrr.Vector3([0.0, 0.0, -1.0])
        # self.cameraDirction = pyrr.vector.normalise(self.cameraPos -self.cameraTarget)
        # self.upVector = [0.0, 1.0, 0.0]
        # self.cameraRight = pyrr.vector.normalise(pyrr.vector3.cross(self.upVector, self.cameraDirction))
        # self.cameraUp = pyrr.vector3.cross(self.cameraDirction, self.cameraRight)

        self.camera = Camera()


        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy= 45, aspect= height/width,
            near= 0.1, far= 20, dtype=np.float32
        )

        self.shader.setMatrix4vf("projection", projection_transform)
        
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.mainLoop()

    def mainLoop(self):
        
        running = True
        self.vector = .1
        self.color = 0.0
        self.colorV = 0.1
        oldTime = pg.time.get_ticks()
        speed = 0.1
        while (running):
            deltaTime = oldTime - pg.time.get_ticks()
            oldTime = deltaTime
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            key = pg.key.get_pressed()
            if key[pg.K_w]:
                self.camera.move("forward", speed)
            elif key[pg.K_a]:
                self.camera.move("left", speed)
            elif key[pg.K_s]:
                self.camera.move("backward", speed)
            elif key[pg.K_d]:
                self.camera.move("right", speed)
           
            
            self.playground()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            
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

    def quit(self):
        self.cube_mesh.destroy()
        self.test_texture.destroy()
        self.shader.delete()
        pg.quit()


if __name__ == "__main__":
    myApp = App(720, 520)