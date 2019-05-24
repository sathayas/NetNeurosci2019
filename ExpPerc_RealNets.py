#
# The largest component size plot
# Both ascending and descending
#


# appropriate packages are imported
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# parameters
posLeft = [0.09, 0.15, 0.28, 0.7]
posMid = [0.39, 0.15, 0.28, 0.7]
posRight = [0.70, 0.15, 0.28, 0.7]
xLim = [-0.01, 3.01]
yLim = [-0.01, 1.01]



### Initialization of figure
fig = plt.figure(figsize=[10,4], facecolor='k')


#
# S&P 500 data first
#

# file business
fRankThNet = 'RankThNet_SP500.npz'

# loading the file from the previously run analysis
infile = np.load(fRankThNet)
nNodes = infile['NNodes']  # Number of nodes
GCSize = infile['GCSize']  # Giant component size
nEdges = np.arange(1,len(GCSize)+1)   # Number of edges -- is a series

# calculating variables for plotting
rGCSize= GCSize / nNodes # relative component size
plotX = nEdges / nNodes # <k>

# acual plotting
plt.subplot(131, position=posLeft)
plt.plot(plotX, rGCSize, '-', color='skyblue', linewidth=2)
plt.xlim(xLim)
plt.ylim(yLim)
ax = plt.gca()
plt.title('S&P 500 network\n(491 nodes)', fontsize=14, color='w')
plt.ylabel('Giant component\nsize (relative)', color='w', fontsize=12)
plt.xlabel('<k>', color='w', fontsize=12)
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=11)
ax.tick_params(axis='x', colors='white', width=1, which='minor')
ax.tick_params(axis='y', colors='white', width=1, which='major', labelsize=11)
ax.tick_params(axis='y', colors='white', width=1, which='minor')



#
# Yeast gene co-expressiond network
#

# file business
fRankThNet = 'RankThNet_Yeast.npz'

# loading the file from the previously run analysis
infile = np.load(fRankThNet)
nNodes = infile['NNodes']  # Number of nodes
GCSize = infile['GCSize']  # Giant component size
nEdges = np.arange(1,len(GCSize)+1)   # Number of edges -- is a series

# calculating variables for plotting
rGCSize= GCSize / nNodes # relative component size
plotX = nEdges / nNodes # <k>

# acual plotting
plt.subplot(132, position=posMid)
plt.plot(plotX, rGCSize, '-', color='skyblue', linewidth=2)
plt.xlim(xLim)
plt.ylim(yLim)
ax = plt.gca()
plt.title('Gene co-expression network\n(5168 nodes)', fontsize=14, color='w')
plt.xlabel('<k>', color='w', fontsize=12)
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=11)
ax.tick_params(axis='x', colors='white', width=1, which='minor')
ax.tick_params(axis='y', colors='white', width=1, which='major', labelleft='off')
ax.tick_params(axis='y', colors='white', width=1, which='minor')




#
# fMRI network
#

# file business
fRankThNet = 'RankThNet_sub16112.npz'

# loading the file from the previously run analysis
infile = np.load(fRankThNet)
nNodes = infile['NNodes']  # Number of nodes
GCSize = infile['GCSize']  # Giant component size
nEdges = np.arange(1,len(GCSize)+1)   # Number of edges -- is a series

# calculating variables for plotting
rGCSize= GCSize / nNodes # relative component size
plotX = nEdges / nNodes # <k>

# acual plotting
plt.subplot(133, position=posRight)
plt.plot(plotX, rGCSize, '-', color='skyblue', linewidth=2)
plt.xlim(xLim)
plt.ylim(yLim)
ax = plt.gca()
plt.title('Voxel-level rs-fMRI network\n(19215 nodes)', fontsize=14, color='w')
plt.xlabel('<k>', color='w', fontsize=12)
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=11)
ax.tick_params(axis='x', colors='white', width=1, which='minor')
ax.tick_params(axis='y', colors='white', width=1, which='major', labelleft='off')
ax.tick_params(axis='y', colors='white', width=1, which='minor')



plt.savefig('ExpPerc_RealNets.png', dpi=128, facecolor='black')
plt.show()
