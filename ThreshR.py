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
        G.add_edge(nodes[ind_edgeR[0][iEdge]], nodes[ind_edgeR[1][iEdge]])
    return G

###### parameters
posTopLeft = [0.1, 0.5, 0.3, 0.3]
posTopRight = [0.5, 0.45, 0.4, 0.45]
posBotLeft = [0.175, 0.1, 0.35, 0.3]
posBotRight = [0.6, 0.1, 0.35, 0.3]
figLeft = 0.085
figRight = 0.95
figTop = 0.9
figBottom = 0.075
figW = 0.3
figH = 0.3
thR = np.arange(0.7,0.5,-0.05)
xLimRGC = [0.4, 0.71]
yLimRGC = [-0.01, 1.01]
xLimKGC = [0.0, 5.0]
yLimKGC = [-0.01, 1.01]

###### Loadin the data saved in .npz file
f_TS = 'Oxford_sub16112_rt2_K200.npz'
infile = np.load(f_TS)
ts = infile['ts']   # time series data: rows: time points, cols: ROIs
nodes = infile['nodes']   # roi indices
xyz = infile['xyz']   # roi center cooridates in 3D
N = len(nodes)

# dictionary of xy-coordinates
pos = {}
for i in range(len(nodes)):
    pos[nodes[i]] = xyz[i,:2]



###### Calculating the correlation matrix
R = np.corrcoef(ts, rowvar=False)
for iRow in range(R.shape[0]):
    R[iRow, iRow] = 0


plt.figure(figsize=[4,4], facecolor='k')

#
# correlation matrix
#
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
plt.show()


#
# For loop for the threshold
#
plotR = []
plotK = []
plotGC_R = []
plotGC_K = []
for iR in thR:
    # Network at this threshold
    G = net_thR(R, nodes, iR)

    #
    # Top left pane, thresholded matrix
    #
    meanK = len(G.edges())/len(G.nodes())
    E = len(G.edges())
    fig = plt.figure(figsize=[6,6], facecolor='k')
    fig.suptitle('Threshold: R>%5.3f, E=%4d, <k>=%5.3f' % (iR, E, meanK),
                 color='w', fontsize=18)

    plt.subplot(221, position=posTopLeft)

    # showing the correlation coefficient
    bR = (R>iR).astype(int)
    plt.imshow(bR, cmap='gray')
    ax = plt.gca()
    plt.title('Thresholded\ncorrelation matrix', color='w', fontsize=12)
    # axis business
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(1)
      ax.spines[axis].set_color('white')
    ax.set_facecolor('k')
    ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=12)
    ax.tick_params(axis='x', colors='white', width=1, which='minor')
    ax.tick_params(axis='y', colors='white', width=1, which='major', labelsize=12)
    ax.tick_params(axis='y', colors='white', width=1, which='minor')



    #
    # Top right pane, network
    #
    plt.subplot(222, position=posTopRight)
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color = 'peachpuff',
                            linewidth=None)
    nx.draw_networkx_edges(G, pos, edge_color='skyblue', width=1.0)

    # drawing nodes and edges of the giant component
    CC = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    GC = CC[0]
    nx.draw_networkx_nodes(G, pos, nodelist = GC.nodes(),
                            node_size=40, node_color = 'orangered',
                            linewidth=None)
    # drawing all the other components
    if len(CC)>0:
        for iCC in CC[1:]:
            if len(iCC)>1:
                nx.draw_networkx_nodes(G, pos, nodelist = iCC.nodes(),
                                        node_size=10, node_color = 'crimson',
                                        linewidth=None)
    plt.axis('off')
    # text for R
    plt.text(38,10,'R', fontsize=12, color='w')



    # bottom left panel: giant component size vs R
    plotR.append(iR)
    plotGC_R.append(len(GC.nodes())/N)
    plt.subplot(223, position=posBotLeft)
    plt.plot(plotR, plotGC_R,'-', linewidth=3.0, color='skyblue')
    ax = plt.gca()
    plt.xlim(xLimRGC)
    plt.ylim(yLimRGC)
    plt.title('GC vs R', color='w', fontsize=12)
    plt.ylabel('Giant component\nsize (relative)', color='w', fontsize=12)
    plt.xlabel('R', color='w', fontsize=12)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(1)
      ax.spines[axis].set_color('white')
    ax.set_facecolor('k')
    ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=11)
    ax.tick_params(axis='x', colors='white', width=1, which='minor')
    ax.tick_params(axis='y', colors='white', width=1, which='major', labelsize=11)
    ax.tick_params(axis='y', colors='white', width=1, which='minor')


    # bottom right panel: giant component size vs <k>
    plotK.append(meanK)
    plotGC_K.append(len(GC.nodes())/N)
    plt.subplot(223, position=posBotRight)
    plt.plot(plotK, plotGC_K,'-', linewidth=3.0, color='skyblue')
    ax = plt.gca()
    plt.xlim(xLimKGC)
    plt.ylim(yLimKGC)
    plt.title('GC vs <k>', color='w', fontsize=12)
    plt.xlabel('<k>', color='w', fontsize=12)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(1)
      ax.spines[axis].set_color('white')
    ax.set_facecolor('k')
    ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=11)
    ax.tick_params(axis='x', colors='white', width=1, which='minor')
    ax.tick_params(axis='y', colors='white', width=1, which='major', labelleft='off')
    ax.tick_params(axis='y', colors='white', width=1, which='minor')


    #plt.subplots_adjust(left=figLeft, right=figRight,
    #                    bottom=figBottom, top=figTop,
    #                    wspace=figW, hspace=figH)
    plt.show()
