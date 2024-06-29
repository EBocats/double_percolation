Tw = 1000 #ps
timestep=0.01
Amp = 1
LogFilePattern = 'log.%s' 
nskip = 0.5
plotting = not True
# plotting =  True

print('Importing numpy, scipy,re,math, sys and glob ...', end=' ')
import numpy as np
from scipy.optimize import curve_fit
from glob import glob
import re
import math
import pylab as plt
import sys
print('OK')
outFile='dms_results.dat'
if len(sys.argv)>=2:
    outFile=sys.argv[1]
pi=np.pi
print('Outfile: ', outFile)
#fout=open(outFile,'w')
#fout.write('#label  A0  A1  s  E1  E2  tan(s)  n\n')
print('#label\tA0\tA1\ts\tE1\tE2\ttan(s)\tn')
def fun(x,A0,A1,s):
    return A0+A1*np.sin(2*np.pi*x+s)



def  GetBoxLen(T):
    fn = LogFilePattern %T
    #print fn,
    fls = glob(fn)
    #print fls
    nfls=len(fls)
    if  nfls ==0:
        return  0
    flog = fls[0]
    line =open(flog).readlines()[50]
    L=line.split()[-1]
    return float(L)



files=glob('stress.*')
files.sort(key=lambda l : int(re.findall('\d+',l)[-1]))
na = len(files)
dout =np.zeros([na,8])
I = 0
#data=np.loadtxt(f,usecols=(0,1))
ns = 00
#n=len(data)/100.0
for f in files:
    try:
        # print(f)
        T = int(f.split('.')[-1])
        # print(Tw)
        data=np.loadtxt(f,usecols=(0,4))
        data = data[ns:]
        x=data[:,0]*timestep/Tw
        y=data[:,1]*-1.
        n=len(data)/100.0
        if n<nskip: continue

        popt,pcov=curve_fit(fun,x,y)
        if plotting: plt.plot(x,y,'ro',label=f)

        

    except:
        print('#--Exception at ', f)
        continue
    A0,A1,s=popt[0], popt[1],popt[2]
    y_fit = fun(x,A0,A1,s)
    if plotting:
        plt.plot(x,y_fit,'k-')
        plt.legend()
        plt.show()
        s=np.abs(np.arctan(np.tan(s)))
    label = re.findall('\d+', f)[0]
    #--------------------------
#    Lx= GetBoxLen(label)
    #print 'Box Len ', Lx
    # if 0==Lx:
    #     Lx = 71
    #     print('#WARNING: Unable to extract box length, use default value 71 A')
    Lx= 56.8; Factor = Lx/Amp
    E1=np.abs(A1*Factor*math.cos(s)*1.)
    E2=np.abs(A1*Factor*math.sin(s)*1.)
    tan=math.tan(s)
    # fout.write('%s  %s  %s  %s  %s  %s  %s\n' %(label, A0,A1,s,E1,E2,tan))
    print('%s\t%.2f\t%.2f\t%.4f\t%.2f\t%.2f\t%.4f\t%.1f' %(label, A0,A1,s,E1,E2,tan, n))
    dout[I]=[int(label),A0,A1,s,E1,E2,tan,n]
    I+=1

    # print f,
dout = dout[dout[:, 0].argsort()]
#dout = dout[dout[0,:] > 0]
print('--------------------------------------')
#print dout
np.savetxt(outFile,dout,fmt="%.4f")
import pylab as plt
fig, (ax1,ax2,ax3) = plt.subplots(nrows=3, sharex=True)
'''
ax1.set_xscale('log')
ax2.set_xscale('log')
ax3.set_xscale('log')
#ax3.ylim(0,1.6)
'''
ax1.plot(dout[:,0],dout[:,4],'g-s')
ax2.plot(dout[:,0],dout[:,5],'r-o')
ax3.plot(dout[:,0],dout[:,3],'k-^')
plt.show()


