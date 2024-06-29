import sys
from ovito.modifiers import *
from ovito.io import import_file, export_file
import numpy as np

T = "300"
fn = "YDMA380K-100ns.lammpstrj"
argn = len(sys.argv)
if argn >= 2:
    fn = sys.argv[1]
if argn >= 3:
    T = sys.argv[2]
if argn >= 4:
    N = int(sys.argv[3])

cf = 1.3
node = import_file(fn, multiple_frames=True)
data = node.compute()
NA = len(data.particles['Position'])
modifier = CalculateDisplacementsModifier(
    use_frame_offset=True, frame_offset=-1)
node.modifiers.append(modifier)
for frame in range(1, node.source.num_frames):
    node.modifiers.append(ExpressionSelectionModifier(
        expression='DisplacementMagnitude <= 0.8'))
    node.modifiers.append(DeleteSelectedModifier())
    node.modifiers.append(ClusterAnalysisModifier(
        cutoff=cf, sort_by_size=True, compute_gyration=True))
    data = node.compute(frame)
    try:
        export_file(data.tables['clusters'], 'clusters_%s_%s.txt' % (
            T, frame), 'txt/table', key='clusters')
    except:
        print('No clusters found at frame %s' % frame)
        continue
