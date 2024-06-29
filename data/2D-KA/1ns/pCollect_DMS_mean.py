import numpy as np
import pandas as pd
import glob
import pylab as plt
import os,sys

atext='dms_'
argn=len(sys.argv)
if argn>=2:
	atext=sys.argv[1]
folders = glob.glob(r'%s*'%atext) #glob.glob('dsm_*')
print(folders)

pd_data =pd.read_table(folders[0]+r'/dms_results.dat',sep=' ' )
pd_data.columns=['freq','A0','A1','s','E1','E2','tan','N']

for fd in folders[1:]:
	print(fd)
	if not os.path.isfile(fd+r'\dms_results.dat'): continue
	pd_cur=pd.read_table(fd+r'\dms_results.dat',sep=' ' )
	pd_cur.columns=['freq','A0','A1','s','E1','E2','tan','N']

	# pd_data = pd_data.append(pd_cur)
	pd_data=pd.concat([pd_data,pd_cur])

pd_data = pd_data.sort_values(by='freq')

pd_mean=pd_data.groupby(['freq'],as_index=False).mean()
pd_mean.columns=['freq','A0','A1','s','E1','E2','tan','N']
# pd_mean=pd_mean[pd_mean['N']>=4]
# pd_mean=pd_mean[pd_mean['s']<=1.3]
# pd_mean=pd_mean[pd_mean['freq']>=100]

pd_mean.to_csv('mean_dms.dat',float_format='%.3f',sep='\t',index=None)
print(pd_mean)


fig,ax=plt.subplots(2,1,sharex=True)
ax[0].plot(pd_mean['freq'],pd_mean['E1'],'-s')
ax[1].plot(pd_mean['freq'],pd_mean['E2'],'ro')
ax[0].set_ylabel(r"G' (GPa)")
ax[1].set_ylabel(r"G'' (GPa)")
ax[1].set_xlabel(r"T (K)")

plt.show()
