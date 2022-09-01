import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr



class App:

    def __init__(self, height, width):
        pg.init()
        pg.display.set_mode((height, width), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        glClearColor(0.1, 0, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        self.cube = Cube(
            position= [0, 0, -6],
            eulers= [0, 0, 0]
        )
        self.cube_mesh = Mesh("meshes/cube.obj")

        self.test_texture = Material("gfx/notha.jpg")

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy= 45, aspect= height/width,
            near= 0.1, far= 10, dtype=np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        self.mainLoop()

    def createShader(self, vertexFilePath, fragmentFilePath):
        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()
        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        
        running = True
        vector = .1
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

           

            

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


            glUseProgram(self.shader)
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
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )


            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            pg.display.flip() 

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        self.test_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Cube:

    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)





class Mesh:

    def __init__(self, file_path):
        #x, y, z, s, t, nx, ny, nz
        self.veritces = self.loadMesh(file_path)

        self.vertex_count = len(self.veritces) // 8

        self.veritces = np.array(self.veritces, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.veritces.nbytes, self.veritces, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

    def loadMesh(self, file_path):
        v = []
        vt = []
        vn = []

        vertices = []
        with open(file_path, "r") as file:
            line = file.readline()
            while line:
                flag = line[0:line.find(" ")]

                if flag == "v":
                    line = line.replace("v ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    v.append(l)

                elif flag == "vt":
                    line = line.replace("vt ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vt.append(l)

                elif flag == "vn":
                    line = line.replace("vn ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vn.append(l)

                elif flag == "f": 
                    line = line.replace("f ", "")
                    line = line.replace("\n", "")
                    line = line.split(" ")

                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    
                    for vertex in line:
                        # v/vt/vn
                        l = vertex.split("/")
                        position = int(l[0]) - 1
                        faceVertices.append(position)
                        texture = int(l[1]) - 1
                        faceTextures.append(texture)
                        normal = int(l[2]) - 1
                        faceNormals.append(normal)
                    
                    face_triangles = len(line) - 2 # amount of vertices - 2

                    vertex_order = []

                    for i in range(face_triangles):
                        # all the triangles meet at vertext 0
                        vertex_order.append(0)
                        vertex_order.append(i+1)
                        vertex_order.append(i+2)

                    for i in vertex_order:
                        for x in v[faceVertices[i]]:
                            vertices.append(x)
                        for x in vt[faceTextures[i]]:
                            vertices.append(x)
                        for x in vn[faceNormals[i]]:
                            vertices.append(x)
                line = file.readline()
        return vertices

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

class Material:

    def __init__(self, filepath):

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))


if __name__ == "__main__":
    myApp = App(720, 520)