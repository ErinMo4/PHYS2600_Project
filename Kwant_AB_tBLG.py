# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 17:14:17 2021

@author: Erin Morissette
"""

import kwant
import numpy as np
import matplotlib.pyplot as plt

# Create rotation matrix 
def R_matrix(theta):
  theta = theta*np.pi/180
  return np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0],[0,0,1]])


# First sheet of graphene, not rotated 
lat = kwant.lattice.general([(1,0,0), (np.sin(np.pi/6), np.cos(np.pi/6), 0)], 
                           [(0,0,0), (0, 1/np.sqrt(3), 0)])
a, b = lat.sublattices

# Second sheet rotated at angle theta 
plv1 = np.dot(R_matrix(5), np.array([1,0,0]))
plv2 = np.dot(R_matrix(5), np.array([np.sin(np.pi/6), np.cos(np.pi/6), 0]))

lat2 = kwant.lattice.general([plv1, plv2], 
                           [(1/2,1/2/np.sqrt(3),2), (1/2, 3/2/np.sqrt(3), 2)])
c, d = lat2.sublattices



def make_cuboid1(r = 5 , c=5):
    def cuboid_shape(pos):
        x, y, z = pos
        # return 0 <= x < a and 0 <= y < b and 0 <= z < c
        return x**2 + y**2 < r**2 and 0 <= z < c

    sys = kwant.Builder()
    sys[lat.shape(cuboid_shape, (0, 0, 0))] = None
    sys[lat2.shape(cuboid_shape, (0,0,0))] = None
    #sys[lat.neighbors(3)] = 110
    sys[lat.neighbors()] = 1
    sys[lat2.neighbors()] = 1
    sys[lat2.neighbors(2)] = 1
    sys[lat2.neighbors(3)] = 1
    #sys[lat.neighbors(3)] = 0.05

    return sys
  

sys = make_cuboid1(r = 10, c=5)


def family_colors(site):
    if site.family == a:
        return 'g'
    if site.family == b:
        return 'c'
      
    if site.family == c:
        return 'r' 
    if site.family == d:
        return 'b'


kwant.plot(sys, site_size=0.18, site_lw=0.01, hop_lw=0.1,
            site_color=family_colors)
           