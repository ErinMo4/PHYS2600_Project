# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 17:14:17 2021

@author: Erin Morissette
"""

import kwant
import numpy as np


lat = kwant.lattice.general([(1,0,0), (np.sin(np.pi/6), np.cos(np.pi/6), 0)], 
                           [(0,0,0), (0, 1/np.sqrt(3), 0), (1/2, 1/2/np.sqrt(3), 1.1), (1/2, 3/2/np.sqrt(3), 1.1)])
a, b, c, d = lat.sublattices

def make_cuboid(r = 5 , c=5):
    def cuboid_shape(pos):
        x, y, z = pos
        # return 0 <= x < a and 0 <= y < b and 0 <= z < c
        return x**2 + y**2 < r**2 and 0 <= z < c

    sys = kwant.Builder()
    sys[lat.shape(cuboid_shape, (0, 0, 0))] = None
    sys[lat.neighbors()] = 1
    #sys[lat.neighbors(2)] = 110
    sys[lat.neighbors(3)] = 1

    return sys

sys = make_cuboid(r = 5, c=5)

def family_colors(site):
    if site.family == a:
        return 'r'
    if site.family == b:
        return 'b'
    if site.family == c:
        return 'g' 
    if site.family == d:
        return 'c'

kwant.plot(sys, site_size=0.18, site_lw=0.01, hop_lw=0.05,
            site_color=family_colors);