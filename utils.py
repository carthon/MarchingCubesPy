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
    if max_value - min_value == 0:
        return 0
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

def density_function(position, surface_level, noise):
    noiseScale = 20
    frequency = noiseScale/100
    noiseWeight = 10
    lacunarity = 1.5
    weightMult = 2
    persistence = 0.7
    amplitude, weight, nois = 1.4, 3, 0
    for i in range(8):
        n = noise[math.floor(position.x)][math.floor(position.z)] * frequency
        v = 1 - abs(n)
        v = v*v
        v *= weight
        weight = max(min(v*weightMult, 1), 0)
        nois+= v * amplitude
        amplitude *= persistence
        frequency *= lacunarity
    surface_y = -position.y + nois * noiseWeight + position.y % surface_level
    return surface_y

def perlin_noise_3d(size_vector, amplitude = 0.2):
    if isinstance(size_vector, Vector3) is not True:
        size_vector = Vector3.from_array(size_vector)
    size_vector = size_vector * 8
    noise = PerlinNoise(octaves=8, seed=time.time_ns())
    pic = []
    for i in range(int(size_vector.x)):
        row_x = []
        for j in range((size_vector.z)):
            noise_val = noise([i/size_vector.x, j/size_vector.y]) * amplitude
            row_x.append(noise_val)
        pic.append(row_x)
    return pic
    #plt.imshow(pic, cmap='gray')
    #plt.show()
    
#perlin_noise_3d(size_vector=Vector3(7, 7, 1))