#!/usr/bin/env python3
import sys

# External, non-python built-in modules
import os                          # exit, system arguments
import re
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
import time
import pkg_resources
from LandSeed.LibPaths import libRootPath
from LandSeed.LandSeed import generate

path = os.path.dirname(os.path.realpath(__file__))
vs_file = os.path.join(path,"vertex_shader.vert")
fs_file = os.path.join(path,"output.frag")

# ------------ low level OpenGL object wrappers ----------------------------
class Shader:
    """ Helper class to create and automatically destroy shader program """
    @staticmethod
    def _compile_shader(src, shader_type):
        src = open(src, 'r').read() if os.path.exists(src) else src
        src = src.decode('ascii') if isinstance(src, bytes) else src
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, src)
        GL.glCompileShader(shader)
        status = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
        src = ('%3d: %s' % (i+1, l) for i, l in enumerate(src.splitlines()))
        if not status:
            log = GL.glGetShaderInfoLog(shader).decode('ascii')
            GL.glDeleteShader(shader)
            src = '\n'.join(src)
            print('Compile failed for %s' % (shader_type))
            print("---------------------------------------")
            print('Error in %s' % (log.replace(" : ", "\n")), end="")
            print("---------------------------------------")
            print("Remember to generate your shader again after changing something in Features, Utils or input files.")
            return None
        return shader

    def __init__(self, vertex_source, fragment_source):
        """ Shader can be initialized with raw strings or source file names """
        self.glid = None
        vert = self._compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        frag = self._compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        if vert and frag:
            self.glid = GL.glCreateProgram()  # pylint: disable=E1111
            GL.glAttachShader(self.glid, vert)
            GL.glAttachShader(self.glid, frag)
            GL.glLinkProgram(self.glid)
            GL.glDeleteShader(vert)
            GL.glDeleteShader(frag)
            status = GL.glGetProgramiv(self.glid, GL.GL_LINK_STATUS)
            if not status:
                print(GL.glGetProgramInfoLog(self.glid).decode('ascii'))
                GL.glDeleteProgram(self.glid)
                self.glid = None

    def __del__(self):
        GL.glUseProgram(0)
        if self.glid:                      # if this is a valid shader object
            GL.glDeleteProgram(self.glid)  # object dies => destroy GL object


# ------------  simple square -----------------------------------------
class SimpleSquare:
    """Simple square object"""

    def __init__(self):

        # array of vertices (2 triangles, with TRIANGLE_FAN)
        position = np.array(((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)), 'f')

        self.glid = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glid)
        self.buffers = [GL.glGenBuffers(1)]

        # bind the vbo, upload position data to GPU, declare its size and type
        GL.glEnableVertexAttribArray(0)  # activates for current v.array only
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, position, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)

        # cleanup and unbind so no accidental subsequent state update
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def draw(self, shader, mouse_pos, time, aspect_ratio):
        if(shader.glid):
            GL.glUseProgram(shader.glid)

            # send uniform variables to the shader
            GL.glUniform1f(GL.glGetUniformLocation(shader.glid,"time"),time)
            GL.glUniform1f(GL.glGetUniformLocation(shader.glid,"aspectRatio"),aspect_ratio)
            GL.glUniform2f(GL.glGetUniformLocation(shader.glid,"mousePos"),
                           mouse_pos[0],mouse_pos[1])

            # draw triangle as GL_TRIANGLE vertex array, draw array call
            GL.glBindVertexArray(self.glid)
            GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, 4)
            GL.glBindVertexArray(0)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(1, self.buffers)


class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):
        self.size = np.array([width,height])
        self.pause = False
        self.reload = False
        self.begin = None

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)
        self.win = glfw.create_window(width, height, "Viewer", None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())
        print("To pause or resume the renderer, press P")
        print("To see your changes in this file, press R key to reload "+fs_file.replace(libRootPath, ""))
        print("To generate again with the same input file and reload, press G")

        # initialize GL by setting viewport and default render characteristics
        GL.glDisable(GL.GL_DEPTH_TEST) # no need for depth test (just a fragment shader on the entire screen here)
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_mouse_button_callback(self.win,self.on_mouse_button)
        glfw.set_cursor_pos_callback(self.win,self.on_mouse_pos)
        glfw.set_window_size_callback(self.win, self.on_size)

        self.ray_tracer = Shader(vs_file, fs_file)
        self.square = SimpleSquare()
        self.mouse_pos = np.array([0.0,0.0])
        self.mouse_pos_click = np.array([0.0,0.0])
        self.mouse_offset = np.array([0.0,0.0])

    def reload_image(self):
        # clear draw buffer and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # draw our square, mapped on the entire screen
        self.square.draw(self.ray_tracer,self.mouse_pos+self.mouse_offset,
                         time.time()-self.begin,float(self.size[1])/float(self.size[0]))

        # flush render commands, and swap draw buffers
        glfw.swap_buffers(self.win)

    def on_size(self, win, width, height):
        """ window size update => update viewport to new framebuffer size """
        self.size = np.array([width,height])
        GL.glViewport(0, 0, *self.size)
        self.reload = True


    def run(self):
        """ main render loop for this OpenGL window """
        self.begin = time.time()
        while not glfw.window_should_close(self.win):# or self.pause:
            self.reload_image()
            # Poll for and process events
            glfw.poll_events()
            self.reload = False
            while self.pause and not glfw.window_should_close(self.win) and not self.reload:
                glfw.poll_events()


    def on_key(self, _win, key, _scancode, action, _mods):
        if action == glfw.PRESS:
            """ 'Q' or 'Escape' quits """
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            """ 'R' reloads shader files """
            if key == key == glfw.KEY_R:
                self.ray_tracer = Shader(vs_file, fs_file)
                self.reload = True
                if self.ray_tracer.glid:
                    print('Shader successfully reloaded.')

            if key == key == glfw.KEY_P:
                self.pause = not self.pause
                if self.pause:
                    print("Pause on")
                else:
                    print("Pause off")

            if key == glfw.KEY_G:
                f = open(fs_file, "r")
                l = f.readline()
                l2 = f.readline()
                f.close()
                p = re.compile("@FROM (.*)")
                input_path = p.search(l).group(1)
                p = re.compile("@TO (.*)")
                output_dir = p.search(l2).group(1)
                if input_path[0] == "/":
                    input_path = input_path[1:]
                if output_dir[0] == "/":
                    output_dir = output_dir[1:]
                generate(input_path, output_dir, True)
                self.ray_tracer = Shader(vs_file, fs_file)
                self.reload = True
                if self.ray_tracer.glid:
                    print('Shader successfully reloaded.')


    def on_mouse_button(self, _win, _button, action, _mods):
        if not self.pause:
            if action == glfw.PRESS:
                self.mouse_pos_click = np.array(glfw.get_cursor_pos(self.win))/self.size
            elif action == glfw.RELEASE:
                self.mouse_pos += self.mouse_offset
                self.mouse_offset = np.array([0,0])

    def on_mouse_pos(self, _win, x, y):
        if not self.pause:
            if glfw.get_mouse_button(self.win,glfw.MOUSE_BUTTON_LEFT)==glfw.PRESS:
                self.mouse_offset = (([x,y]/self.size)-self.mouse_pos_click)*[2,-2]

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
