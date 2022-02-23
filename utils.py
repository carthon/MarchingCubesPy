# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:11:34 2022

@author: Mortimer
"""
import math
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from vector3 import Vector3
import time

def normalize(value, max_value, min_value):
    return (value - min_value) / (max_value - min_value)

def dist_two_points(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)

def interpolate(isolevel, p1, p2, valp1, valp2):
    if abs(isolevel - valp1) < 0.0000001:
        return p1
    if abs(isolevel - valp2) < 0.0000001:
        return p2
    if abs(valp1 - valp2) < 0.0000001:
        return p1
    mu = (isolevel - valp1) / (valp2 - valp1)
    x = p1.x + mu * (p2.x - p1.x)
    y = p1.y + mu * (p2.y - p1.y)
    z = p1.z + mu * (p2.z - p1.z)
    
    return [x,y,z]

def perlin_noise_3d(size_vector, offset_vector):
    noise_xy = PerlinNoise(octaves=2, seed=time.time_ns())
    noise = PerlinNoise(octaves=6, seed=time.time_ns())
    print(offset_vector)
    print(size_vector)
    size_vector = size_vector * 2
    pic = []
    for i in range(int(size_vector.x)):
        row_x = []
        for j in range((size_vector.y)):
            row_y = []
            noise_val = noise_xy([i/size_vector.x, j/size_vector.y])
            for k in range((size_vector.z)):
                noise_val += 0.5 * noise([noise_val, k/size_vector.z])
                row_y.append(noise_val)
            row_x.append(row_y)
        pic.append(row_x)
    final_value = pic[int(offset_vector.x)][int(offset_vector.y)][int(offset_vector.z)]
    print(final_value)
    return final_value
    #plt.imshow(pic, cmap='gray')
    #plt.show()
    
#perlin_noise_3d(size_vector=Vector3(100, 100, 1), offset_vector=0)