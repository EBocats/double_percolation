import sys
from ovito.modifiers import *
from ovito.io import import_file
from ovito.modifiers import ClusterAnalysisModifier
from ovito.io import import_file
import numpy as np
import re
cf = 3.9
fnout='clusters12.dat'
argn=len(sys.argv)
if argn>=2:
	fout=sys.argv[1]

# print(fn,fnout,node.output.number_of_particles)
def get_cluster12(fn):
	node = import_file(fn,multiple_frames=True)
	node.compute()
	NA = node.output.number_of_particles
	
	
	modifier = CalculateDisplacementsModifier(use_frame_offset = True,frame_offset=-1)
	modifier.reference.load(fn,multiple_frames=True)
	node.modifiers.append(modifier)
	
	max_val = np.zeros(node.source.num_frames-1)
	second_val=np.zeros(node.source.num_frames-1)
	for frame in range(1,node.source.num_frames):
		node.modifiers.append(SelectExpressionModifier(expression = 'DisplacementMagnitude >=1.0'))
		node.modifiers.append(DeleteSelectedParticlesModifier())
		node.modifiers.append(ClusterAnalysisModifier(cutoff = cf,sort_by_size = True))

		node.compute(frame)
		cluster_sizes = np.bincount(node.output.particle_properties['Cluster'].array)
		cluster_sizes.sort()
		assert(cluster_sizes.max()==cluster_sizes[-1])
		i = frame-1
		max_val[i] = cluster_sizes[-1];second_val[i]=cluster_sizes[-2]
	return max_val*1.0/NA,1.0*second_val/NA



import glob
files=glob.glob('dump.*')
files.sort(key=lambda s: int(re.findall('\d+',s)[0]))
fp=open(fnout,'w')
print('Largest_mean	Largest_std	Second_mean	Second_std')
for f in files:
	T = int(re.findall('\d+',f)[0])
	try:
		max_val,second_val = get_cluster12(f)
		strOut='%d %.5f %.5f %.5f %.5f'%(T, max_val.mean(),max_val.std(),second_val.mean(),second_val.std())
		fp.write(strOut+'\n')
		fp.flush()
		print(strOut)
	except:
		print('exception: %s' %f)


