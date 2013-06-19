// From: http://solarianprogrammer.com/2013/05/13/opengl-101-drawing-primitives/
// See also: http://content.gpwiki.org/index.php/GLFW:Tutorials:Basics
// Compile with clang++ input.cpp -o opengl_test -lGL -lglfw
// Open a window with GLFW
#include <GL/glfw.h> // For GLFW
#include <FTGL/ftgl.h> // For text
#include <iostream>
#include <cstdio>
#include <fstream>
#include <cstdlib>
#include <string>
#include <cstring>
#include <malloc.h>
#include <cmath>
#include <unistd.h>
#include <fcntl.h>

#define KILOBYTE(x) (x / 1024)
#define MEGABYTE(x) (KILOBYTE(x) / 1024)
#define GIGABYTE(x) (MEGABYTE(x) / 1024)
#define TERABYTE(x) (GIGABYTE(x) / 1024)
#define PETABYTE(x) (TERABYTE(x) / 1024)

const int res_x = 800;
const int res_y = 600;
constexpr int memsize = res_x * res_y;

#if 0
void *BinarySnapShot()
{
	char *memchunk = new char[memsize];
	std::ifstream file(HARD_DRIVE, std::ios_base::binary);
	
	if (file.is_open())
	{
		file.seekg (0, std::ios::beg);
		file.read (memchunk, memsize);
		file.close();
		return memchunk;
	}
	return nullptr;
}
#endif

#define HARD_DRIVE "/dev/sda5"
void *BinarySnapShot()
{
	char *memchunk = new char[memsize];

	int fp = open(HARD_DRIVE, O_RDWR | O_NONBLOCK);
	
	if(fp > 0)
	{
		read(fp, (void*) memchunk, memsize);
		//fgets(memchunk, memsize, fp);
		//fclose(fp);
		close(fp);
		return memchunk;
	}
	
	return nullptr;
}

void Draw()
{
	//printf("Draw!\n");
	char *memblock = (char*)BinarySnapShot();
	
	if(memblock != nullptr)
	{
		//red = 
		glColor3f(1.0, 1.0, 1.0);

		glDrawPixels(res_x, res_y, GL_RGB, GL_BYTE, (void*)memblock);
		
		// Free the memory before we switch buffers
		delete[] memblock;
	}
	else
		printf("failed to capture byte stream: %s\n", strerror(errno));
}

void DrawFPS()
{
	static int fps, lastfps;
	static time_t time1 = 0;
	static FTGLPixmapFont font("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf");
	
	char text[100];
	sprintf(text, "FPS: %d", lastfps);
	
	font.FaceSize(20);
	
	font.Render(text, -1, FTPoint(0.0, res_y - 20.0));
	
	fps++;
	if(time1 <= time(NULL))
	{
		time1 = time(NULL) + 1;
		lastfps = fps;
		fps = 0;
	}
}

int main (int argc, char **argv)
{

	printf("Initializing OpenGL subsystem\n");
	// Initialize GLFW
	if (!glfwInit())
	{
		std::cerr << "Failed to initialize GLFW! I'm out!" << std::endl;
		exit(-1);
	}
	
	printf("Initializing a window\n");
	// Open a window and attach an OpenGL rendering context to the window surface
	if(!glfwOpenWindow(res_x, res_y, 32, 32, 32, 0, 0, 0, GLFW_WINDOW))
	{
		std::cerr << "Failed to open a window! I'm out!" << std::endl;
		glfwTerminate();
		exit(-1);
	}

	// Use red to clear the screen
	glClearColor(0, 0, 0, 0);
	// Set the window title
	glfwSetWindowTitle(HARD_DRIVE " byte stream");

	printf("Entering render loop\n");
	
	// Create a rendering loop
	int running = GL_TRUE;
	while(running != false)
	{
		// Clear the screen
		glClear(GL_COLOR_BUFFER_BIT);
		
		// Draw our various items
		
		Draw();
		DrawFPS();

		// Swap front and back buffers
		glfwSwapBuffers();

		// Check if the window was closed
		running = glfwGetWindowParam(GLFW_OPENED);
		//if(glfwGetKey(GLFW_KEY_ESC) == GLFW_PRESS);
		//	running = GL_FALSE;
		if(glfwGetKey('Q') == GLFW_PRESS)
			running = GL_FALSE;
	}
	
	printf("Shutting down GL subsystem\n");

	// Terminate GLFW
	glfwTerminate();
	
	printf("Exiting program\n");

	return 0;
}

