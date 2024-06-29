import numpy as np
import pylab as plt

data_dms = np.loadtxt('dms_results.dat')
data_cluster=np.loadtxt('clusters12.dat')

fig,ax = plt.subplots(nrows=2,sharex=True)

ax[0].plot(data_dms[:,0],data_dms[:,4],'g-s')
ax0_right=ax[0].twinx()
ax0_right.plot(data_dms[:,0],data_dms[:,5],'r-o')
ax0_right.set_ylabel("E'' (GPa)")
ax[0].set_ylabel("E' (GPa)")


ax[1].set_yscale('log')
ax[1].set_ylim((1E-4,1))
ax[1].errorbar(data_cluster[:,0],data_cluster[:,1],data_cluster[:,2],fmt='-o')
ax[1].errorbar(data_cluster[:,0],data_cluster[:,3],data_cluster[:,4],fmt='-o')

plt.show()