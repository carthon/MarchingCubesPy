# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 17:56:49 2022

@author: Mortimer
"""

import pyglet
from pyglet.gl import *
from pyglet.window import key
from utils import perlin_noise_3d, dist_two_points
import time
from mesh import Mesh

def create_triangle(triangles):
    for triangle in triangles:
        glBegin(GL_TRIANGLES)
        glColor3f(1,1,1)
        for vertex in triangle:
            x,y,z = vertex.to_arr()
            glVertex3f(x,y,z)
        glEnd()

def create_triangle_vertex(triangles):
    vertex_ = []
    for triangle in triangles:
        for vertex in triangle:
            x,y,z = vertex.to_arr()
            vertex_.append(x)
            vertex_.append(y)
            vertex_.append(z)
    return vertex_
    
def create_points(vertices, values = [1]*8,size=1, color=None):
    glEnable(GL_PROGRAM_POINT_SIZE)
    pyglet.gl.glPointSize(10)
    glBegin(GL_POINTS)
    for i, vertex in enumerate(vertices):
        x,y,z = vertex
        value = values[i]
        if color != None:
            glColor3f(color[0], color[1], color[2])
        else:
            glColor3f(value,value,value)
        #if i == selected_vertex:
        #    glColor3f(0, 1, 0);
        glVertex3f(x,y,z)
    glEnd()

def create_edges(vertices):
    for triangle in vertices:
        glBegin(GL_LINES)
        glColor3f(0,0,0)
        for vertex in triangle.to_array():
            x,y,z = vertex.to_arr()
            glVertex3f(x,y,z)
        glEnd()
    
def set_2d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho( -window.width / 2, window.width / 2, -window.height / 2, window.height / 2, -1000.0, 1000.0) # [near, far] = [-1000, 1000]

def model():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def set_3d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, window.width/window.height, 0.1, 500.0)


def draw(mesh):
    triangles_vertex = []
    total_triangles = 0
    for grid_cell in mesh.grid_to_arr():
        for vertex in create_triangle_vertex(grid_cell.triangles):
            triangles_vertex.append(vertex)
    vertices_gl = (GLfloat * len(triangles_vertex * 4))(*triangles_vertex)
    glBufferData(GL_ARRAY_BUFFER_ARB, len(triangles_vertex) * 4, vertices_gl, GL_STATIC_DRAW)
    glVertexPointer(3, GL_FLOAT, 0, 0)
    return triangles_vertex
    
def draw_index(mesh, index):
    triangles_vertex = []
    total_triangles = 0
    for i in range(0, index):
        grid_cell = mesh.grid_to_arr()[i]
        create_points(mesh.grid_to_arr()[index], values = mesh.grid_to_arr()[index].value)
        for vertex in create_triangle_vertex(grid_cell.triangles):
            triangles_vertex.append(vertex)
    vertices_gl = (GLfloat * len(triangles_vertex * 4))(*triangles_vertex)
    glBufferData(GL_ARRAY_BUFFER_ARB, len(triangles_vertex) * 4, vertices_gl, GL_STATIC_DRAW)
    glVertexPointer(3, GL_FLOAT, 0, 0)
    return triangles_vertex
        
def setRender():
    positionBufferObject = GLuint()
    glGenBuffers(1, positionBufferObject)
    glBindBuffer(GL_ARRAY_BUFFER_ARB, positionBufferObject)
            
def render(vertices, fill):
    glColor3f(1,1,1)
    glEnable(GL_BLEND)
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glDrawArrays(GL_TRIANGLES, 0, len(vertices))
    if fill == False:
        glColor3f(0,0,0)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glDrawArrays(GL_TRIANGLES, 0, len(vertices))
        
    #Triangle normals
    
    
def update(dt):
    global pos_z, rot_y, rot_x, index, start_time, fill, completed, max_size
    speed = 50
    if key_handler[pyglet.window.key.RIGHT]:
        #selected_vertex += 1
        if index < max_size:
            index += 1
        #key_handler[pyglet.window.key.RIGHT] = False
    if key_handler[pyglet.window.key.LEFT]:
        #selected_vertex += 1
        if index > 0 and completed:
            index -= 1
        #key_handler[pyglet.window.key.LEFT] = False
    if key_handler[pyglet.window.key.G]:
        #selected_vertex -= 1
        key_handler[pyglet.window.key.G] = False
        fill = not fill
    if key_handler[pyglet.window.key.UP] is True:
        pos[2] += 2 * dt
    if key_handler[pyglet.window.key.DOWN] is True:
        pos[2] -= 2 * dt
    if key_handler[pyglet.window.key.W] is True:
        #pos[2] += 2 * dt
        rot_x -= speed * dt
    if key_handler[pyglet.window.key.S] is True:
        #pos[2] -= 2 * dt
        rot_x += speed * dt
    if key_handler[pyglet.window.key.A] is True:
        rot_y -= speed * dt
    if key_handler[pyglet.window.key.D] is True:
        rot_y += speed * dt
    
    if not completed:
        end_time = time.time()
        if end_time - start_time > 0.2:
            if index < len(marching_cubes.grid_to_arr()) - 1 and not completed:
                start_time = time.time()
                index += 1
            elif not completed:
                completed = True

pos = [0, 0, -5]
rot_y = 0
rot_x = 0
w, h = 640, 480

window = pyglet.window.Window()
pyglet.gl.glClearColor(0.5,0.5,0.5,1)
pyglet.clock.schedule_interval(update, 1/120.0)
key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)

glEnableClientState(GL_VERTEX_ARRAY)

size = [10,10,10]
start_time = time.time()
index = 0
start_time = time.time()
value_map = perlin_noise_3d(size)
end_time = time.time()
max_size = size[0]*size[1]*size[2] - 1
fill = True
completed = False
print("Perlin Noise took: {} seconds.".format(end_time - start_time))
#marching_cubes = Mesh(size=size, function=dist_two_points)
marching_cubes = Mesh(size=size, value_map=value_map)

@window.event
def on_draw():
    window.clear()
    set_2d()
    
    set_3d()
    model()
    #glPushMatrix()
    glTranslatef(*pos)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    setRender()
    vertices = draw(marching_cubes)
    render(vertices, fill)
    
    #glPopMatrix()
    
    glFlush()
    
pyglet.app.run()