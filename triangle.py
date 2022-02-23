# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:15:17 2022

@author: Mortimer
"""
class Triangle():
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def __str__(self):
        return "v1: {} | v2: {} | v3: {} ".format(self.v1, self.v2, self.v3)
    def to_array(self):
        return [self.v1, self.v2, self.v3]
    def __iter__(self):
        yield self.v1
        yield self.v2
        yield self.v3