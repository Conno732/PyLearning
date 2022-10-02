from imports import *
from HelperClasses import *

from Rendering.Mesh import *

class RenderObject:

    def __init__(self, transform, mesh, shader, texture = False, color = [0, 0, 0, 0]):
        self.transform = transform
        self.mesh = mesh
        self.texture = texture
        self.color = color
        self.shader = shader
       # self.shader.use()
        #self.shader.setInt("imageTexture", 0)

    def SRT(self):
        # This translates the object into the world space

        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        

        model_transform = pyrr.matrix44.multiply(
            m1 = model_transform,
            m2 = pyrr.matrix44.create_from_scale(
                scale= self.transform.scale,
                dtype=np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_eulers(
                eulers=np.radians(self.transform.rotation),
                dtype=np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_translation(
                vec= self.transform.position,
                dtype=np.float32
            )
        )
        return model_transform

    def draw(self, mesh):
        glBindVertexArray(mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)
