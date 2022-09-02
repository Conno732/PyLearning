from imports import *

class Shader:

    def __init__(self, vertexPath, fragmentPath):
        with open(vertexPath, 'r') as f:
            vertex_src = f.readlines()
        with open(fragmentPath, 'r') as f:
            fragment_src = f.readlines()

        self.shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

    def use(self):
        glUseProgram(self.shader)

    def setBool(self, name, value):
        pass
    
    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.shader, name), value)

    def setFloatv4(self, name, values):
        glUniform4f(glGetUniformLocation(self.shader, name), values[0], values[1], values[2], values[3] )
        
    def setMatrix4vf(self, name, values):
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, name),
            1, GL_FALSE, values
        )



    def delete(self):
        glDeleteProgram(self.shader)