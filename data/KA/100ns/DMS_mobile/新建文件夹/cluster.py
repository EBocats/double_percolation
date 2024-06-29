import sys
from ovito.modifiers import *
from ovito.io import import_file
import numpy as np
import re
cf = 4
fnout='clusters12.dat'
argn=len(sys.argv)
if argn>=2:
	fnout=sys.argv[1]

def get_cluster12(fn):
	node = import_file(fn,multiple_frames=True)
	data=node.compute()
	NA = len(data.particles['Position'])
	modifier = CalculateDisplacementsModifier(use_frame_offset = True,frame_offset=-1)
	node.modifiers.append(modifier)
	max_val = np.zeros(node.source.num_frames-1)
	second_val=np.zeros(node.source.num_frames-1)
	Rg_val  = np.zeros(node.source.num_frames-1)
	Rg_sec  = np.zeros(node.source.num_frames-1)
	P_all  = np.zeros(node.source.num_frames-1)
	for frame in range(1,node.source.num_frames):
		node.modifiers.append(ExpressionSelectionModifier(expression = 'DisplacementMagnitude <= 1.8'))
		node.modifiers.append(DeleteSelectedModifier())
		node.modifiers.append(ClusterAnalysisModifier(cutoff = cf,sort_by_size = True,compute_gyration=True))

		data = node.compute(frame)
		cluster_sizes = np.bincount(data.particles['Cluster'].array)
		cluster_sizes.sort()
		assert(cluster_sizes.max()==cluster_sizes[-1])
		i = frame-1
		max_val[i] = cluster_sizes[-1];second_val[i]=cluster_sizes[-2]
		Rg_val[i] = data.tables['clusters']['Radius of Gyration'][0]
		P_all[i] = cluster_sizes.sum()
		
		# print(Rg)
	return NA, max_val*1.0/NA,1.0*second_val/NA, Rg_val, P_all



import glob
files=glob.glob('YDMA*K-1000ns.lammpstrj')
fp=open(fnout,'w')
print('T Largest_mean Largest_std Second_mean Second_std Rg_mean Rg_std P_all_mean P_all_std NA')
for f in files:
	# pass
	T = int(re.findall('\d+',f)[0])
	NA,max_val,second_val,Rg_val,P_all = get_cluster12(f)
	# print(f)
	strOut='%d %.5f %.5f %.5f %.5f %.3f %.3f %.3f %.3f %d' %(T,max_val.mean(),max_val.std(),second_val.mean(),second_val.std(),Rg_val.mean(),Rg_val.std(),P_all.mean(),P_all.std(),NA)
	fp.write(strOut+'\n')
	fp.flush()
	print(strOut)

fp.close()
