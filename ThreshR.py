import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


###### parameters
posLeft = [0.1, 0.55, 0.33, 0.33]


###### Loadin the data saved in .npz file
f_TS = 'Oxford_sub16112_rt2_K200.npz'
infile = np.load(f_TS)
ts = infile['ts']   # time series data: rows: time points, cols: ROIs
nodes = infile['nodes']   # roi indices
xyz = infile['xyz']   # roi center cooridates in 3D



###### Calculating the correlation matrix
R = np.corrcoef(ts, rowvar=False)


plt.figure(figsize=[8,4], facecolor='k')

#
# Top left pane, correlation matrix
#
plt.subplot(221, position=posLeft)

# showing the correlation coefficient
plt.imshow(R)
plt.title('Correlation matrix' color='w', fontsize=18)
plt.colorbar()
#
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(2)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=2, which='major', labelsize=14)
ax.tick_params(axis='x', colors='white', width=2, which='minor')
ax.tick_params(axis='y', colors='white', width=2, which='major', labelsize=14)
ax.tick_params(axis='y', colors='white', width=2, which='minor')



plt.show()
