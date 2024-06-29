import os
import glob
import re
import sys
files=glob.glob('dump.*')
files.sort(key=lambda l: int(re.findall('\d+', l)[-1]))
pathing = os.path.abspath(sys.path[0])
print(pathing)
TFrom=0000
frun = open('batch.bat','w')
for f in files:
    T = int(re.findall('\d+',f)[0])
    fsize = os.path.getsize(f)
    print(f,fsize)
    if fsize < int(3074529/2): continue
    
    if T < TFrom: continue
    try:
        dirName=pathing+'/IS/T%s' %T
        print(dirName)
        if os.path.isdir(dirName): print('Dir already there!')
        os.mkdir(dirName)
        os.system('cp IS/code_Bak/*  %s' %dirName)
        frun.write('cd %s \n' %dirName)
        frun.write('ovitos extract_frames.py  ../../dump.%s \n' %T)
        frun.write('python min_IS.py \n' )
        frun.write('python distance_matrix_pair.py \n' )
    except:
        print('File might be there, goahead!')
frun.close()

