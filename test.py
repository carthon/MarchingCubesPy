# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 12:50:34 2022

@author: Mortimer
"""

from pyglet.gl import *

window = pyglet.window.Window()

vertices = [
    0, 0,
    100, 0,
    100, 200]
vertices_gl = (GLfloat * len(vertices))(*vertices)


glEnableClientState(GL_VERTEX_ARRAY)

buffer=(GLuint)(0)
glGenBuffers(1,buffer)
glBindBuffer(GL_ARRAY_BUFFER_ARB, buffer)
glBufferData(GL_ARRAY_BUFFER_ARB, 6*4,
                    vertices_gl, GL_STATIC_DRAW)


glVertexPointer(2, GL_FLOAT, 0, 0)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 2)

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(gl.GL_MODELVIEW)

pyglet.app.run()