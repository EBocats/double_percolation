# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:48:51 2022

p(u) and up will be calculated base on displacement magnitude(u)
python39 pu.py u_.txt pu_.txt bin
@author: MrGLi
"""
import numpy as np
import sys

fn = 'u.txt'
fout = 'pu.txt'
bin = 500
SaveSTS = True

argn = len(sys.argv)
if argn >= 2:
	fn = sys.argv[1]
if argn >= 3:
	fout = sys.argv[2]
if argn >= 4:
    bin = int(sys.argv[3])

"""
Load the external files
"""
print('Loading hist file: %s' %fn)
lines = open(fn).readlines()
u = np.loadtxt(lines[9:])
print('Loaded.')

u_max = np.max(u)
detu = u_max/bin 
up=0
if u_max>=detu:
    hist,edges = np.histogram(u,bin,density=True)
    pup=np.max(hist)
    up = edges[np.argmax(hist)]
    print('The up is: %f' %up)
    if SaveSTS:
        sts=np.column_stack((edges[1:],hist))
        np.savetxt(fout,sts)
