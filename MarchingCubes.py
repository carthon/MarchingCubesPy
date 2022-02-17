# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 17:56:49 2022

@author: Mortimer
"""

import pyglet
from pyglet.gl import *
from pyglet.window import key
import triangleconnectiontable
import random

class MarchingCube():
    def __init__(self):
       self.grid = []
       
       for i in range(8):
           self.grid.append(random.random())
           
       self.cube_vertex = [[1,1,1],[-1,1,1],[-1,-1,1],[1,-1,1],
                         [1,1,-1],[-1,1,-1],[-1,-1,-1],[1,-1,-1]]
       self.isolevel = 0.5
       self.vert_list = [None] * 12
       self.triangles = []
       self.triangle_vertices = []
       self.update()
     
    def get_intersection_point(self, edge):
       vertex1, vertex2 = triangleconnectiontable.edge_connection[edge]
       middle = interpolate(self.isolevel, self.cube_vertex[vertex1], self.cube_vertex[vertex2],
                            self.grid[vertex1], self.grid[vertex2])
       return middle
    def update(self):
        cube_index = 0
        self.triangles = []
        self.triangle_vertices = []
        for i in range(8):
            if self.grid[i] < self.isolevel:
                cube_index |= 2 ** i
        triangle_val = triangleconnectiontable.cube_edge_flags[cube_index]
        for i, edges in enumerate(triangleconnectiontable.edge_connection):
            if triangle_val & 2 ** i:
                vertex1, vertex2 = edges
                self.vert_list[i] = interpolate(self.isolevel, self.cube_vertex[vertex1], self.cube_vertex[vertex2],
                                          self.grid[vertex1], self.grid[vertex2])
        ntriangle = 0
        i = 0
        while triangleconnectiontable.triangle_connection_table[cube_index][i] != -1:
            self.triangles.append(triangleconnectiontable.triangle_connection_table[cube_index][i:i+3])
            ntriangle += 1
            i += 3
        for triangle in self.triangles:
            v1 = self.get_intersection_point(triangle[0])
            v2 = self.get_intersection_point(triangle[1])
            v3 = self.get_intersection_point(triangle[2])
            self.triangle_vertices.append([v1,v2,v3])

        
    def add_iso(self, vertex):
        self.grid[vertex] += 0.2
        self.update()
    def remove_iso(self, vertex):
        self.grid[vertex] -= 0.2
        self.update()

def interpolate(isolevel, p1, p2, valp1, valp2):
    if abs(isolevel - valp1) < 0.0000001:
        return p1
    if abs(isolevel - valp2) < 0.0000001:
        return p2
    if abs(valp1 - valp2) < 0.0000001:
        return p1
    mu = (isolevel - valp1) / (valp2 - valp1)
    x = p1[0] + mu * (p2[0] - p1[0])
    y = p1[1] + mu * (p2[1] - p1[1])
    z = p1[2] + mu * (p2[2] - p1[2])
    
    return [x,y,z]
    
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


def update(dt):
    global pos_z, rot_y, rot_x, selected_vertex
    speed = 50
    if key_handler[pyglet.window.key.RIGHT]:
        selected_vertex += 1
        key_handler[pyglet.window.key.RIGHT] = False
    if key_handler[pyglet.window.key.LEFT]:
        selected_vertex -= 1
        key_handler[pyglet.window.key.LEFT] = False
    if key_handler[pyglet.window.key.W] is True:
        #pos[2] += 2 * dt
        rot_x += speed * dt
    if key_handler[pyglet.window.key.S] is True:
        #pos[2] -= 2 * dt
        rot_x -= speed * dt
    if key_handler[pyglet.window.key.A] is True:
        rot_y -= speed * dt
    if key_handler[pyglet.window.key.D] is True:
        rot_y += speed * dt
    if key_handler[pyglet.window.key.PLUS] is True:
        marching_cubes.add_iso(selected_vertex)
    if key_handler[pyglet.window.key.MINUS] is True:
        marching_cubes.remove_iso(selected_vertex)
    selected_vertex = selected_vertex % 8
    print()

def create_triangle(vertices):
    glBegin(GL_TRIANGLES)
    for vertex in vertices:
        x,y,z = vertex
        glVertex3f(x,y,z)
    glEnd()

    
def create_points(vertices, size=1):
    glEnable(GL_PROGRAM_POINT_SIZE)
    pyglet.gl.glPointSize(10)
    glBegin(GL_POINTS)
    for i, vertex in enumerate(vertices):
        x,y,z = vertex
        glColor3f(1,1,1)
        if i == selected_vertex:
            glColor3f(0, 1, 0);
        glVertex3f(x,y,z)
    glEnd()

def create_edges(vertices):
    glBegin(GL_LINES)
    glColor3f(1,1,1)
    for vertex in vertices:
        x,y,z = vertex
        glVertex3f(x,y,z)
    glEnd()
    
pos = [0, 0, -5]
rot_y = 0
rot_x = 0
w, h = 640, 480

window = pyglet.window.Window()
pyglet.clock.schedule_interval(update, 1/120.0)
key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)
labels =[]
marching_cubes = MarchingCube()
selected_vertex = 0

@window.event
def on_draw():
    window.clear()
    set_2d()
    text = "Selected vertex: " + str(selected_vertex)
    label = pyglet.text.Label(text=text, font_name = 'Arial', font_size=16, x=100, y= 0)
    label.draw()
    text = "ISO: " + str(marching_cubes.grid[selected_vertex])
    label2 = pyglet.text.Label(text=text, font_name = 'Arial', font_size=16, x=100, y=20)
    label2.draw()
    
    set_3d()
    model()
    #glPushMatrix()
    glTranslatef(*pos)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    #glPopMatrix()
    
    create_points(marching_cubes.cube_vertex)
    for triangle in marching_cubes.triangle_vertices:
        create_triangle(triangle)
    for i in triangleconnectiontable.edge_connection:
        vertex1, vertex2 = i
        create_edges([marching_cubes.cube_vertex[vertex1], marching_cubes.cube_vertex[vertex2]])
    
    glFlush()
    
pyglet.app.run()