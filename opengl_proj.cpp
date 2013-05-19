// From: http://solarianprogrammer.com/2013/05/13/opengl-101-drawing-primitives/
// See also: http://content.gpwiki.org/index.php/GLFW:Tutorials:Basics
// Compile with clang++ input.cpp -o opengl_test -lGL -lglfw
// Open a window with GLFW
#include <GL/glfw.h>
#include <cstdlib>
#include <iostream>

int main () {
	// Initialize GLFW
	if ( !glfwInit()) {
		std::cerr << "Failed to initialize GLFW! I'm out!" << std::endl;
		exit(-1);
	}

	// Open a window and attach an OpenGL rendering context to the window surface
	if( !glfwOpenWindow(800, 600, 8, 8, 8, 0, 0, 0, GLFW_WINDOW)) {
		std::cerr << "Failed to open a window! I'm out!" << std::endl;
		glfwTerminate();
		exit(-1);
	}

	// Use red to clear the screen
	glClearColor(1, 0, 0, 1);

	// Set the window title
	glfwSetWindowTitle("A basic program!");

	// Create a rendering loop
	int running = GL_TRUE;
	while(running) {
		glClear(GL_COLOR_BUFFER_BIT);

		// Swap front and back buffers
		glfwSwapBuffers();

		// Check if the window was closed
		running = glfwGetWindowParam(GLFW_OPENED);
		if(glfwGetKey(GLFW_KEY_ESC) == GLFW_PRESS);
			running = GL_FALSE;
		if(glfwGetKey('Q') == GLFW_PRESS)
			running = GL_FALSE;
	}

	// Terminate GLFW
	glfwTerminate();

	return 0;
}

