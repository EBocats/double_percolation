# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 00:22:15 2022

@author: MrGLi
"""
import re
import glob
import numpy as np
import os
import sys

fout = "sfp.dat"
argn=len(sys.argv)
if argn>=2:
	fout=sys.argv[1]
    
print('T    sigma    sigma_std    fp    fp.std    p    p.std    Sm    Sm.std')   
files = glob.glob('../YDMA*K-100ns.lammpstrj')
files.sort(key=lambda x: int(re.findall('\d+', x)[0]))
for f in files:
    try:
        T = int(re.findall('\d+',f)[0])
        os.system('python table2_im.py %s %s' %(f,T))
        os.system('python get.py')
        os.system('rm clusters_*_*.txt')
    except:
         print('Error in %s' %f)
         continue
    
files = glob.glob('T*.cluster')
lens = len(files)
result = np.zeros([lens,9])
i = 0
for f in files:
    fp = open(f).readlines()
    data = np.loadtxt(fp)
    result[i,:] = data[:]
    i += 1
os.system('rm T*.cluster')
np.savetxt(fout,result,fmt="%d %f %f %f %f %.1f %f %.3f %f")