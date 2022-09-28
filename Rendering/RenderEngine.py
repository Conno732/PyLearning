from imports import *


class RenderEngine:

    def __init__(self, height, width):
        pg.init()
        pg.display.set_mode((height, width), pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.display.set_caption("3D stuff")
        self.window_height = height
        self.window_width = width
        glClearColor(0.1, 0, 0.1, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_CULL_FACE); 
        
        pg.mouse.set_visible(False)

        self.shaderList = {}
        self.meshList = {}
        self.textureList = {}
        self.renderList = {}

    def setRenderList(self, objs):
        self.renderList = objs

    def setShaderList(self, shaders):
        self.shaderList = shaders


    def update(self, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        # maybe put this in the camera object... If there are multiple cameras, then different windows 
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy= camera.fovy, aspect= self.window_height/self.window_width,
            near= 0.1, far= 100, dtype=np.float32
        )


        for shader in self.shaderList:
            self.shaderList[shader].use()
            self.shaderList[shader].setMatrix4vf("projection", projection_transform)
            self.shaderList[shader].setMatrix4vf("view", camera.makeLookAt())


        for renderObjct in self.renderList:
            obj = self.renderList[renderObjct]
            obj.shader.use()
            if (obj.texture):
                obj.texture.use()
            else:
                self.textureList["missing"].use()

            obj.shader.setFloatv4("objColor", obj.color)
            model = obj.SRT()
            obj.shader.setMatrix4vf("model", model)

            if self.shaderList["v2"] == obj.shader:
                inverse = pyrr.matrix33.inverse(model)
                transpose = inverse.transpose()
                obj.shader.setMatrix3vf("NormalMatrix", transpose)
                obj.shader.setFloatv3("lightColor", [1.0, 1.0, 1.0])
                obj.shader.setFloatv3("lightPos", self.renderList["light"].position)
                obj.shader.setFloatv3("viewPos", camera.cameraPos)
                
            obj.draw()

        pg.display.flip() 
    