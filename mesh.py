# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:17:12 2022

@author: Mortimer
"""
from vector3 import Vector3
from utils import dist_two_points, interpolate, normalize
import triangleconnectiontable
from triangle import Triangle

class Cube():
    def __init__(self, position=Vector3()):
        self.cube_vertex = [Vector3()] * 8
        self.value = [float(0)] * 8
        self.triangles = [] * 5
        self.triangles_edges = []
        self.vertex_list = [0] * 12
        for i in range(8):
            cube_vertex = triangleconnectiontable.cube_vertex[i]
            self.cube_vertex[i] = Vector3(cube_vertex[0], cube_vertex[1], cube_vertex[2]) / 2 + position
    
    def get_intersection_point(self, edge, isolevel):
        vertex1, vertex2 = triangleconnectiontable.edge_connection[edge]
        middle = interpolate(isolevel, self.cube_vertex[vertex1], self.cube_vertex[vertex2],
                            self.value[vertex1], self.value[vertex2])
        return Vector3.from_array(middle)
    
    def __iter__(self):
        for i in self.cube_vertex:
            yield i.to_arr()


class Mesh():
    def __init__(self, isolevel=0.4, grid = Cube(), size = [1,1,1], position = Vector3(), values_function = dist_two_points):
        self.isolevel = isolevel
        self.size = Vector3.from_array(size)
        self.grid = []
        self.position = position
        self.create_cubes()
        self.calculate_values(values_function)
        self.compute_mesh()
    
    def create_cubes(self):
        for x in range(self.size.x):
            self.grid.append([])
            for y in range(self.size.y):
                self.grid[x].append([])
                for z in range(self.size.z):
                    pos = (self.position + Vector3(x,y,z)) - (Vector3(self.size.x, self.size.y, self.size.z) / 2)
                    self.grid[x][y].append(Cube(pos))
                
    def calculate_values(self, function):
        values = []
        max_value = 0
        min_value = 99999
        for i, grid_cell in enumerate(self.grid_to_arr()):
            for j, position in enumerate(grid_cell.cube_vertex):
                value_cell = 0 if function(position, self.position) == 0 else function(position, self.position)
                values.append(value_cell)
                if value_cell < min_value:
                    min_value = value_cell
                if value_cell > max_value:
                    max_value = value_cell
                grid_cell.value[j]= value_cell
        for grid_cell in self.grid_to_arr():
            for j, position in enumerate(grid_cell.cube_vertex):
                grid_cell.value[j] = normalize(grid_cell.value[j], max_value, min_value)

    def compute_mesh(self):
        for cell in self.grid_to_arr():
            cube_index = 0x00
            for i in range(8):
                if cell.value[i] < self.isolevel:
                    cube_index |= 2 ** i
            triangle_val = triangleconnectiontable.cube_edge_flags[cube_index]
            for i, edges in enumerate(triangleconnectiontable.edge_connection):
                if triangle_val & 2 ** i:
                    vertex1, vertex2 = edges
                    cell.vertex_list[i] = interpolate(self.isolevel, cell.cube_vertex[vertex1], cell.cube_vertex[vertex2],
                                              cell.value[vertex1], cell.value[vertex2])
            ntriangle = 0
            i = 0
            while triangleconnectiontable.triangle_connection_table[cube_index][i] != -1:
                edge_index = triangleconnectiontable.triangle_connection_table[cube_index][i:i+3]
                e1, e2, e3 = edge_index
                cell.triangles_edges.append([e1, e2, e3])
                ntriangle += 1
                i += 3
            i = 0
            for triangle in cell.triangles_edges:
                v1 = cell.get_intersection_point(triangle[0], self.isolevel)
                v2 = cell.get_intersection_point(triangle[1], self.isolevel)
                v3 = cell.get_intersection_point(triangle[2], self.isolevel)
                cell.triangles.append(Triangle(v1,v2,v3))
                i+=1

    def grid_to_arr(self):
        array = []
        for x in range(self.size.x):
            for y in range(self.size.y):
                for z in range(self.size.z):
                    array.append(self.grid[x][y][z])
        return array                
        
    def __iter__(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                for z in range(self.size.z):
                    yield self.grid[x][y][z]