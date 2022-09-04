from imports import *

class RenderObject:

    def __init__(self, position, eulers, scale):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.scale = np.array(scale, dtype=np.float32)

    def SRT(self):
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)


        model_transform = pyrr.matrix44.multiply(
            m1 = model_transform,
            m2 = pyrr.matrix44.create_from_scale(
                scale= self.scale,
                dtype=np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_eulers(
                eulers=np.radians(self.eulers),
                dtype=np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_translation(
                vec= self.position,
                dtype=np.float32
            )
        )

        return model_transform

    def draw(self):
        pass
