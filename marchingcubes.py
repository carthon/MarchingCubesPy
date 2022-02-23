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
    for grid_cell in mesh.grid_to_arr():
        #create_points(grid_cell, values = grid_cell.value)
        create_triangle(grid_cell.triangles)
        create_edges(grid_cell.triangles)
    
def draw_index(mesh, index):
    for i in range(0, index):
        grid_cell = mesh.grid_to_arr()[i]
        create_points(grid_cell, values = grid_cell.value)
        create_triangle(grid_cell.triangles)
        create_edges(grid_cell.triangles)
        create_points(mesh.grid_to_arr()[index], values = mesh.grid_to_arr()[index].value)

def update(dt):
    global pos_z, rot_y, rot_x, index, start_time
    speed = 50
    if key_handler[pyglet.window.key.RIGHT]:
        #selected_vertex += 1
        key_handler[pyglet.window.key.RIGHT] = False
    if key_handler[pyglet.window.key.LEFT]:
        #selected_vertex -= 1
        key_handler[pyglet.window.key.LEFT] = False
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
    
    end_time = time.time()
    if end_time - start_time > 0.2:
        if index < len(marching_cubes.grid_to_arr()) - 1:
            start_time = time.time()
            index += 1
    
pos = [0, 0, -5]
rot_y = 0
rot_x = 0
w, h = 640, 480

window = pyglet.window.Window()
pyglet.gl.glClearColor(0.5,0.5,0.5,1)
pyglet.clock.schedule_interval(update, 1/120.0)
key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)
size = [20,20,20]
start_time = time.time()
index = 0
value_map = perlin_noise_3d(size)
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
    draw(marching_cubes)
    #glPopMatrix()
    
    glFlush()
    
pyglet.app.run()