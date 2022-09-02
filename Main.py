from imports import *
from Material import *
from Mesh import *
from Cube import *
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


        self.cube = Cube(
            position= [-2, 0, -6],
            eulers= [0, 0, 0]
        )
        self.cube_mesh = Mesh("meshes/cube.obj")

        self.test_texture = Material("gfx/notha.jpg")

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy= 45, aspect= height/width,
            near= 0.1, far= 10, dtype=np.float32
        )

        self.shader.setMatrix4vf("projection", projection_transform)
        
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.mainLoop()

    def mainLoop(self):
        
        running = True
        vector = .1
        color = 0.0
        colorV = 0.1
        while (running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            
            
            self.cube.position[2] += vector
            
            self.cube.eulers[0] += 2
            
            if (self.cube.eulers[0] > 360):
                self.cube.eulers[0] -= 360

            if (self.cube.position[2] < -10) or self.cube.position[2] > -3:
                vector *= -1

            if color >= 1.0 or color <= -1.0:
                colorV *= -1.0

            color += colorV

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            

            self.shader.use()
            self.test_texture.use()


            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )

            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=[1, 0, -6],
                    dtype=np.float32
                )
            )
            
            self.shader.setFloatv4("myColor", [0.0, 0.5, color, 1.0])
            self.shader.setMatrix4vf("model", model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )

            self.shader.setFloatv4("myColor", [0.0, 0.5, color, 1.0])
            self.shader.setMatrix4vf("model", model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            pg.display.flip() 

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.test_texture.destroy()
        self.shader.delete()
        pg.quit()


if __name__ == "__main__":
    myApp = App(720, 520)