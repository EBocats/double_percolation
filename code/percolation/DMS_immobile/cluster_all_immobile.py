import sys
from ovito.modifiers import *
from ovito.io import import_file
import numpy as np
import re
cf = 4
fnout='clusters_im_12.dat'
argn=len(sys.argv)
if argn>=2:
	fout=sys.argv[1]

def get_cluster12(fn):
	node = import_file(fn,multiple_frames=True)
	data = node.compute()
	NA = len(data.particles['Position'])
	modifier = CalculateDisplacementsModifier(use_frame_offset = True,frame_offset=-1)
	node.modifiers.append(modifier)
	max_val = np.zeros(node.source.num_frames-1)
	second_val=np.zeros(node.source.num_frames-1)
	Rg_val  = np.zeros(node.source.num_frames-1)
	Pspan = 0.0
	for frame in range(1,node.source.num_frames):
		node.modifiers.append(ExpressionSelectionModifier(expression = 'DisplacementMagnitude >=1.8'))
		node.modifiers.append(DeleteSelectedModifier())
		node.modifiers.append(ClusterAnalysisModifier(cutoff = cf,sort_by_size = True,compute_gyration=True))

		data = node.compute(frame)
		cluster_sizes = np.bincount(data.particles['Cluster'].array)
		cluster_sizes.sort()
		assert(cluster_sizes.max()==cluster_sizes[-1])
		i = frame-1
		max_val[i] = cluster_sizes[-1];second_val[i]=cluster_sizes[-2]
		Rg_val[i] =data.tables['clusters']['Radius of Gyration'][0]
		Lx = data.cell.matrix[0,0]
		if Rg_val[i] >= Lx/2.0:
			Pspan += 1.0
	return max_val*1.0/NA,1.0*second_val/NA, Rg_val, Pspan/(node.source.num_frames-1)



import glob
files=glob.glob('../YDMA*K-1000ns.lammpstrj')
files.sort(key=lambda s: int(re.findall('\d+',s)[0]))
fp=open(fnout,'w')
print('Largest_mean	Largest_std	Second_mean	Second_std Rg Pspan')
for f in files:
	# pass
	try:
		T = int(re.findall('\d+',f)[0])
		max_val,second_val,Rg_val,Pspan = get_cluster12(f)
		# print(f)
		strOut='%d %.5f %.5f %.5f %.5f %.3f %.3f %.3f'%(T, max_val.mean(),max_val.std(),second_val.mean(),second_val.std(),Rg_val.mean(),Rg_val.std(),Pspan)
		fp.write(strOut+'\n')
		fp.flush()
		print(strOut)
	except:
		print('Exception:%s' % f)

fp.close()

