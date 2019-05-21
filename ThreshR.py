import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


###### Function to return a graph defined at a give threshold on R
def net_thR(R, nodes, thR):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    bR = (R>thR).astype(int)
    ind_triubR = np.triu_indices_from(bR,1)
    triubR = bR[ind_triubR]
    ind_edgeR = [ind_triubR[0][triubR>0], ind_triubR[1][triubR>0]]
    for iEdge in range(len(ind_edgeR[0])):
        G.add_edge(nodes[ind_edge[0][iEdge]], nodes[ind_edge[1][iEdge]])
    return G

###### parameters
posTopLeft = [0.05, 0.625, 0.2, 0.2]
posTopRight = [0.55, 0.625, 0.2, 0.2]
figLeft = 0.085
figRight = 0.95
figTop = 0.9
figBottom = 0.075
figW = 0.3
figH = 0.3
thR = 0.45

###### Loadin the data saved in .npz file
f_TS = 'Oxford_sub16112_rt2_K200.npz'
infile = np.load(f_TS)
ts = infile['ts']   # time series data: rows: time points, cols: ROIs
nodes = infile['nodes']   # roi indices
xyz = infile['xyz']   # roi center cooridates in 3D



###### Calculating the correlation matrix
R = np.corrcoef(ts, rowvar=False)


plt.figure(figsize=[6,6], facecolor='k')

#
# Top left pane, correlation matrix
#
plt.subplot(221, position=posTopLeft)

# showing the correlation coefficient
plt.imshow(R)
ax = plt.gca()
plt.title('Correlation matrix\n', color='w', fontsize=18)
# axis business
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(2)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=12)
ax.tick_params(axis='x', colors='white', width=1, which='minor')
ax.tick_params(axis='y', colors='white', width=1, which='major', labelsize=12)
ax.tick_params(axis='y', colors='white', width=1, which='minor')

# color bar business
cb = plt.colorbar(shrink=0.66)
#cb.set_label('Correlation', color='w')
cb.ax.yaxis.set_tick_params(color='w', labelsize=10)
cb.outline.set_edgecolor('w')
plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='w')





#
# Top right pane, thresholded matrix
#
plt.subplot(222, position=posTopRight)

# showing the correlation coefficient
for iRow in range(R.shape[0]):
    R[iRow, iRow] = 0
bR = (R>thR).astype(int)
plt.imshow(bR, cmap='gray')
ax = plt.gca()
plt.title('Threshold: R=%5.3f' % thR, color='w', fontsize=18)
# axis business
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(2)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=12)
ax.tick_params(axis='x', colors='white', width=1, which='minor')
ax.tick_params(axis='y', colors='white', width=1, which='major', labelsize=12)
ax.tick_params(axis='y', colors='white', width=1, which='minor')





plt.subplots_adjust(left=figLeft, right=figRight,
                    bottom=figBottom, top=figTop,
                    wspace=figW, hspace=figH)
plt.show()
