import numpy as np
import sys
from ovito.io import import_file
from ovito.modifiers import *

fin1 = 'dump.575'
fin2 = 'dump.575'
uc = 1.6
argn=len(sys.argv)
if argn>=2:
    fin1=sys.argv[1]
if argn>=3:
    fin2=sys.argv[2]
if argn>=4:
    uc=float(sys.argv[3])

node = import_file(fin1,multiple_frames=True)
displace = CalculateDisplacementsModifier(use_frame_offset = True,frame_offset=-1)
node.modifiers.append(displace)
ff = np.zeros(node.source.num_frames-1)
for frame in range(1, node.source.num_frames):
    node.modifiers.append(ExpressionSelectionModifier(expression = 'DisplacementMagnitude > %s' % uc))
    node.modifiers.append(DeleteSelectedModifier())
    node.modifiers.append(SelectTypeModifier(property='Particle Type', types={1}))
    data = node.compute(frame)
    NA = len(data.particles['Position'])
    ff[frame-1] = data.attributes['SelectType.num_selected']/NA

print(ff.mean(), ff.std())

node = import_file(fin2, multiple_frames=True)
displace = CalculateDisplacementsModifier(
    use_frame_offset=True, frame_offset=-1)
node.modifiers.append(displace)
ff = np.zeros(node.source.num_frames-1)
for frame in range(1, node.source.num_frames):
    node.modifiers.append(ExpressionSelectionModifier(expression = 'DisplacementMagnitude <= %s' % uc))
    node.modifiers.append(DeleteSelectedModifier())
    node.modifiers.append(SelectTypeModifier(property='Particle Type', types={1}))
    data = node.compute(frame)
    NA = len(data.particles['Position'])
    ff[frame-1] = data.attributes['SelectType.num_selected']/NA

print(ff.mean(), ff.std())

