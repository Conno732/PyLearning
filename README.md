## Python OpenGL Playground

### What is this project supposed to be?

This is a (in development) 3D rendering application with a physics engine on the (ever so distant) horizon. The purpose of this project is for self learning and a reference for any future related projects.

### Why Python? Why not C++?

C++ is what most people consider the better choice for making a 3D rendering engine (and maybe a physics engine, if I get to that). The obvious reason being that Python runs slower and uses more memory. I am aware of this and still chose Python over C++ because I'm probably not going to be performing enough calculations where such an optimization boost is needed. Additionally I prefer Python when learning new topics. If the need for increased performance rises, I will probably look to translate this project into C++. This is probably not going to happen, since any performance issue is probably due to a need for optimization, rather than the language.

### Features (unchecked features are still in progress, or on the backlog)

- [x] Imports file

- [x] Open a window (Pygame Window)

- [x] Application loop that exits when window is closed

- [x] Shader class, which provides an interface for compiling, using, modifying uniform variables

- [x] Simple shaders, allowing for rendering using vertex data and

- [x] Projection matrix and model matrix for displaying vertices. (Needs to be incapsulated in another object)

- [x] Mesh class, which allocates vertex, texture, normal data in the VBO which is bound to a VAO (maybe add element array objects)

- [x] Ability to import .obj files (finicky, only consistently works with exported blender objects) through a mesh object

- [x] Material class, used for importing image data and sampled by the vertex texture data

- [x] 'Camera' class, allowing for the user to traverse the 3D world.
- [ ] Basic lighting
- [ ] Additional model loading
- [ ] Advanced OpenGL stuff (cool shaders n stuff, skyboxes, frame culling, anti aliasing )
- [ ] Manipulation of vertices during runtime for physics purposes (soft body, destructible, etc.)
- [ ] Properly defined engine with an API to add objects, including adding components, etc.
- [ ] A seperate window to edit and manage objects.

### Physics engine?

At a certain point along the project, physics will slowly be integrated into this project. This will include the following:

- [ ] Dynamic input (gravity, user input) to manipulate position, velocity, acceleration, jerk
- [ ] Object properties, such as mass, associated with specific materials.

- [ ] Collision detection - This one requires a lot more effort, but will most likely contain:
  - [ ] Detection between any two convex 3D objects (maybe concave as well?)
  - [ ] Research and implementation for data structures that optimize which objects need to be checked for collisions
  - [ ] Primitive and advanced collision detection systems may be implemented, depending on what is wanted
- [ ] Collision solving -> solve collisions when they occur, depending on an objects properties
- [ ] Rigid body collision /simulation
- [ ] Soft body simulation

### General Architecture Idea

The main idea for an end product would be as follows (pseudocode mockup):

```
Start Program;

Function Init():
	// Binding the physics engine with the 3D renderer makes a 'game' engine
	Game = GameManager();

	// This creates a generic game object. It contains no properties but is now
	//    tracked by the game engine. The user can now add properties to the object
	Game.add(GameObject("cube"), "name")

	// May not be the best method, but there will be a method for directly
	//   Accessing objects so that they can be modified.
	let Cube = Game.getObject("name")

	// The cube will now be rendered by the rendering engine. The box mesh is a
	//    default mesh that allows for some predefined properties
	Cube.addBoxMesh()


	// This is a general demonstration of an idea for how components of a game
	//    object can be modified.

	// Maybe not the best method, but this method allows for the user to add a
	// 		texture to the mesh. Not adding a texture will leave it gray.
	Cube.getComponent("BoxMesh").addTexture("img")

	// This is a predefined collider that will be managed by the physics system
	//  	Gravity is turned on by default. The cube will fall indefintely
	Cube.addBoxCollider()

	// More research is needed here, but the general idea is that a rigid body
	//    is what responds to collisions
	Cube.getComponent("BoxCollider").addRigidBody()

// more stuff to come
```
