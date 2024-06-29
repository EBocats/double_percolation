# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 22:36:55 2022

@author: MrGLi
"""
import numpy as np
import glob
import sys

def get_sfp(f):
    fp = open(f).readlines()
    T = f.split('_')[1]
    fdata = np.loadtxt(fp)
    if len(fp) > 3:        
        S = fdata[:,1]
        Rg = fdata[:,2]
        p = S.sum()
        fp = S[0]/p
        sigma = np.sqrt(2 * np.sum(Rg**2 * S**2)/np.sum(S**2))
    else:
        S = fdata[1]
        Rg = fdata[2]
        p = S
        fp = S/p
        sigma = np.sqrt(2 * Rg**2 * S**2/S**2)

    return int(T), sigma, fp, p, S.mean()

files = glob.glob('clusters_*_*.txt')
lens = len(files)
data = np.zeros([lens,5])
result = np.zeros([1,9])
i = 0
for f in files:
    try:
        data[i,0], data[i,1], data[i,2], data[i,3], data[i,4] = get_sfp(f)    
        i += 1
    except:
        print('Exception:%s' % f)
        continue
result[:,0] = data[0,0]
for i in range(1,9):
    if i%2 == 0: 
        result[:,i] = data[:,int(i/2)].std()
    else:
        result[:,i] = data[:,int((i+1)/2)].mean()

fout = "T%s.cluster" %int(data[0,0])
np.savetxt(fout,result,fmt="%d %f %f %f %f %.1f %f %.3f %f")
strOut='%d %f %f %f %f %.1f %f %.3f %f' %(result[:,0], result[:,1], result[:,2], result[:,3], result[:,4], result[:,5], result[:,6], result[:,7], result[:,8])
print(strOut)