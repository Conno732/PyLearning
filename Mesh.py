from logging.config import listen
from imports import *

class Mesh:
    # TODO Switch to Element Buffer Objects
    def __init__(self, file_path):
        #x, y, z, s, t, nx, ny, nz
        self.veritces = self.loadMesh(file_path)

        self.vertex_count = len(self.veritces) // 8

        self.veritces = np.array(self.veritces, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.veritces.nbytes, self.veritces, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))


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
                    line = line.replace("v  ", "")
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
                    line = line.strip(" ")
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
                        # all the triangles meet at vertex 0
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
