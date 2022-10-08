from imports import *
from Rendering.RenderObject import *


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


    def createRenderObject(self, name, transform, mesh, shader, texture, isLightable = True, isLight = False, color = [0, 0, 0, 0]):
        self.renderList[name] = RenderObject(
                transform= transform,
                mesh= mesh,
                shader= shader,
                texture= texture,
                isLight= isLight,
                isLightAble= isLightable,
                color= color
            )

        return self.renderList[name]

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
            shaderTmp = self.shaderList[obj.shader]
            textTmp = self.textureList[obj.texture]
            shaderTmp.use()
            
            textTmp.use()

            shaderTmp.setFloatv4("objColor", obj.color)
            model = obj.SRT()
            shaderTmp.setMatrix4vf("model", model)

            if obj.isLightAble: # instead of checking by name, assign a property of 'lightable' or something
                inverse = pyrr.matrix33.inverse(model)
                transpose = inverse.transpose()
                
                shaderTmp.setMatrix3vf("NormalMatrix", transpose)
                shaderTmp.setFloatv3("lightColor", [1.0, 1.0, 1.0])
                shaderTmp.setFloatv3("lightPos", self.renderList["light"].transform.position)
                shaderTmp.setFloatv3("viewPos", camera.cameraPos)
                
            obj.draw(self.meshList[obj.mesh])

        pg.display.flip() 
    
    def destroy(self):
        for texture in self.textureList:
            self.textureList[texture].destroy()
        for mesh in self.meshList:
            self.meshList[mesh].destroy()
        for shader in self.shaderList:
            self.shaderList[shader].delete()