import numpy as np
import pandas as pd
import glob
import pylab as plt
import math,os,sys
import scipy 
from scipy import optimize as op
import pylab as plt
from math import pi
def HN2(w,beta,Gmax,wmax):
    return Gmax/(1 - beta + beta*((beta*wmax/w + (w/wmax)**beta))/(1+beta))
#os.popen('python collect_DMS2.py')

atext='dms_'
argn=len(sys.argv)
if argn>=2:
	atext=sys.argv[1]
folders = glob.glob(r'%s*'%atext) #glob.glob('dsm_*')

print(folders)


pd_data =pd.read_table(folders[0]+r'/dms_results.dat',sep=' ' )
pd_data.columns=['freq','A0','A1','s','E1','E2','tan','N']
# print(pd_data)


for fd in folders[1:]:
	print(fd)
	if not os.path.isfile(fd+r'\dms_results.dat'): continue
	pd_cur=pd.read_table(fd+r'\dms_results.dat',sep=' ' )
	pd_cur.columns=['freq','A0','A1','s','E1','E2','tan','N']

	# pd_data = pd_data.append(pd_cur)
	pd_data=pd.concat([pd_data,pd_cur])

pd_data = pd_data.sort_values(by='freq')
# print(pd_data)

pd_mean=pd_data.groupby(['freq'],as_index=False).mean()
pd_mean.columns=['freq','A0','A1','s','E1','E2','tan','N']
# pd_mean=pd_mean[pd_mean['N']>=4]
# pd_mean=pd_mean[pd_mean['s']<=1.3]
# pd_mean=pd_mean[pd_mean['freq']>=100]

pd_mean.to_csv('mean_dms.dat',float_format='%.3f',sep='\t',index=None)
print(pd_mean)


fig,ax=plt.subplots(2,1,sharex=True)
# ax[0].set_xscale('log')
ax[0].plot(pd_mean['freq'],pd_mean['E1'],'-s')
ax[1].plot(pd_mean['freq'],pd_mean['E2'],'ro')
ax[0].set_ylabel(r"G' (GPa)")
ax[1].set_ylabel(r"G'' (GPa)")
ax[1].set_xlabel(r"T (K)")
# ax1_right = ax[1].twinx()
# ax1_right.plot(pd_mean['freq'],pd_mean['s'],'g-^')
# ax1_right.set_ylabel('$\delta$ (rad.)')


'''fiting range'''

pd_mean=pd_mean[pd_mean['s']<=1.3]
pd_mean=pd_mean[pd_mean['freq']>=100]

f=pd_mean['freq']
E2=pd_mean['E2']
'''
try:
	p1=scipy.polyfit(f,E2,deg=5)
	E1_sm = scipy.polyval(p1, f)
	#ax1.plot(x,y2,'g-')
	beta =-1

	x=2*pi/f
	y=E2
	popt,pcov=op.curve_fit(HN2,x,y)
	beta = popt[0]
	Gmax=popt[1]
	wmax=popt[2]

	# print("Beta_KWW = %.4f" %beta)
	# print(f'Beta={beta}')

	print('=======Fitting=============')
	print('Beta = %.3f' %(beta))
	f_max=2*pi/wmax
	print('F_peak = %.2f' %f_max)

	f_exp = np.logspace(1,6,100)
	x_exp = 2*pi/f_exp

	# y_fit = HN2(x,beta,Gmax,wmax)
	y_fit = HN2(x_exp,beta,Gmax,wmax)
	# print(y_fit)
	# f_exp=np.arange(np.min(f)*.15,np.max(f),100)
	ax[1].plot(f_exp,y_fit,'r-')
	# ax[1].plot(f,y_fit,'r-')
except:
	print('Exception on fitting')
# beta_list.append(beta)
# T_list.append(T_cur)

'''

# ax1.plot(f,E1,'-o',label='%d' %T_cur)
# p2=scipy.polyfit(f,E2,deg=5)
# E2_sm = scipy.polyval(p2, f)

# print()
plt.show()
# ax2.plot(f,E2_sm,'-o')
