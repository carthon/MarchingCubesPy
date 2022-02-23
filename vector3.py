# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:15:46 2022

@author: Mortimer
"""

class Vector3():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    @classmethod
    def from_array(self, array):
        return Vector3(array[0], array[1], array[2])
        
    def __str__(self):
        return "[{},{},{}]".format(self.x,self.y,self.z)
    
    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        return Vector3(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        return Vector3(self.x - other, self.y - other, self.z - other)
    
    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        return Vector3(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other):
        if isinstance(other,Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        return Vector3(self.x / other, self.y / other, self.z / other)
    
    def to_arr(self):
        return [self.x, self.y, self.z]