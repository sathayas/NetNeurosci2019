#
# Generates a sequence of images of ER network
#
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Parameters
N = 200  # Number of nodes
E = 300  # Number of edges
xLimER = [0, 3.0]
yLimER = [0, 1.0]
outDir = 'ER_Percolation_PNG'
edgeStep = 5

# Initializing the graph
G = nx.Graph()
G.add_nodes_from(list(range(1,N+1)))  # adding nodes


# loading edges in sequential order
fNameEdgeList = 'edges_ER_N%d' % N + '_E%d' % E + '.txt'
f = open(fNameEdgeList,'r')
edgeList = []
while True:
    line = f.readline()
    if not line:
        break
    else:
        e = [int(x) for x in line.strip().split()]
        edgeList.append(e)
f.close()


# loading nodes and their positions
fNameNodeList = 'nodes_ER_N%d' % N + '_E%d' % E + '.txt'
g = open(fNameNodeList,'r')
nodeList = []
pos = {}
while True:
    line = g.readline()
    if not line:
        break
    else:
        nodeData = [x for x in line.strip().split()]
        nodeList.append(int(nodeData[0]))
        pos[int(nodeData[0])] = np.array([float(x) for x in nodeData[1:]])
g.close()



#
# Network drawing with no edge
#
plt.figure(figsize=[8,4], facecolor='k')
# Just the graph on the left panel
plt.subplot(121, position=[0.0,0.0,0.5,1.0])
nx.draw_networkx_nodes(G, pos, node_size=30, node_color = 'salmon',
                        linewidth=None)
plt.xlim([-1.0, 1.0])
plt.ylim([-1.0, 1.0])
plt.axis('off')

# right panel: giant component size
plt.subplot(122, position=[0.65,0.15,0.325,0.6])
plt.plot(0,0,'.', linewidth=2.0, color='skyblue')
ax = plt.gca()
plt.xlim(xLimER)
plt.ylim(yLimER)
plt.title('E=%d\n<k>=%4.2f\n' % (len(G.edges()), 2*len(G.edges())/N),
            color='w', fontsize=18)
plt.ylabel('Giant component\nsize', color='w', fontsize=18)
plt.xlabel('<k>', color='w', fontsize=18)
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(2)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=2, which='major', labelsize=14)
ax.tick_params(axis='x', colors='white', width=2, which='minor')
ax.tick_params(axis='y', colors='white', width=2, which='major', labelsize=14)
ax.tick_params(axis='y', colors='white', width=2, which='minor')

fFig = 'ERNet_%03d.png' % len(G.edges())
plt.savefig(os.path.join(outDir,fFig), dpi=150, facecolor='black')
#plt.show()
plt.close()


#
# adding a single edge and drawing
#
plotX = [0]
plotY = [0]
for iEdge in edgeList[:20]:
    G.add_edge(iEdge[0], iEdge[1])
    plt.figure(figsize=[8,4], facecolor='k')

    # Left panel, network
    plt.subplot(121, position=[0.0,0.0,0.5,1.0])
    # drawing nodes and edges
    nx.draw_networkx_edges(G, pos, edge_color='skyblue', width=2.0)
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color = 'salmon',
                            linewidth=None)
    # drawing nodes and edges of the giant component
    CC = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    GC = CC[0]
    nx.draw_networkx_nodes(G, pos, nodelist = GC.nodes(),
                            node_size=100, node_color = 'orangered',
                            linewidth=None)
    # drawing all the other components
    if len(CC)>0:
        for iCC in CC[1:]:
            if len(iCC)>1:
                nx.draw_networkx_nodes(G, pos, nodelist = iCC.nodes(),
                                        node_size=30, node_color = 'crimson',
                                        linewidth=None)

    plt.xlim([-1.0, 1.0])
    plt.ylim([-1.0, 1.0])
    plt.axis('off')


    # right panel: giant component size
    plotX.append(2*len(G.edges())/N)
    plotY.append(len(GC.nodes())/N)
    plt.subplot(122, position=[0.65,0.15,0.325,0.6])
    plt.plot(plotX, plotY,'-', linewidth=3.0, color='skyblue')
    ax = plt.gca()
    plt.xlim(xLimER)
    plt.ylim(yLimER)
    plt.title('E=%d\n<k>=%4.2f\n' % (len(G.edges()), 2*len(G.edges())/N),
                color='w', fontsize=18)
    plt.ylabel('Giant component\nsize', color='w', fontsize=18)
    plt.xlabel('<k>', color='w', fontsize=18)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(2)
      ax.spines[axis].set_color('white')
    ax.set_facecolor('k')
    ax.tick_params(axis='x', colors='white', width=2, which='major', labelsize=14)
    ax.tick_params(axis='x', colors='white', width=2, which='minor')
    ax.tick_params(axis='y', colors='white', width=2, which='major', labelsize=14)
    ax.tick_params(axis='y', colors='white', width=2, which='minor')

    fFig = 'ERNet_%03d.png' % len(G.edges())
    plt.savefig(os.path.join(outDir,fFig), dpi=150, facecolor='black')
    #plt.show()
    plt.close()

#
# Adding 5 edges until all edges are added
#
for iEdges in range(20,300,edgeStep):
    sublistEdges = edgeList[iEdges:(iEdges+edgeStep)]
    G.add_edges_from(sublistEdges)
    plt.figure(figsize=[8,4], facecolor='k')

    # Left panel, network
    plt.subplot(121, position=[0.0,0.0,0.5,1.0])
    # drawing nodes and edges
    nx.draw_networkx_edges(G, pos, edge_color='skyblue', width=2.0)
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color = 'salmon',
                            linewidth=None)
    # drawing nodes and edges of the giant component
    CC = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    GC = CC[0]
    nx.draw_networkx_nodes(G, pos, nodelist = GC.nodes(),
                            node_size=100, node_color = 'orangered',
                            linewidth=None)
    # drawing all the other components
    if len(CC)>0:
        for iCC in CC[1:]:
            if len(iCC)>1:
                nx.draw_networkx_nodes(G, pos, nodelist = iCC.nodes(),
                                        node_size=30, node_color = 'crimson',
                                        linewidth=None)

    plt.xlim([-1.0, 1.0])
    plt.ylim([-1.0, 1.0])
    plt.axis('off')


    # right panel: giant component size
    plotX.append(2*len(G.edges())/N)
    plotY.append(len(GC.nodes())/N)
    plt.subplot(122, position=[0.65,0.15,0.325,0.6])
    if iEdges < 100:
        plt.plot(plotX, plotY,'-', linewidth=3.0, color='skyblue')
    else:
        plt.plot(plotX[:(plotX.index(1)+1)], plotY[:(plotX.index(1)+1)],
                '-', linewidth=3.0, color='skyblue')
        plt.plot(plotX[plotX.index(1):], plotY[plotX.index(1):],
                '-', linewidth=3.0, color='crimson')
    ax = plt.gca()
    plt.xlim(xLimER)
    plt.ylim(yLimER)
    plt.title('E=%d\n<k>=%4.2f\n' % (len(G.edges()), 2*len(G.edges())/N),
                color='w', fontsize=18)
    plt.ylabel('Giant component\nsize', color='w', fontsize=18)
    plt.xlabel('<k>', color='w', fontsize=18)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(2)
      ax.spines[axis].set_color('white')
    ax.set_facecolor('k')
    ax.tick_params(axis='x', colors='white', width=2, which='major', labelsize=14)
    ax.tick_params(axis='x', colors='white', width=2, which='minor')
    ax.tick_params(axis='y', colors='white', width=2, which='major', labelsize=14)
    ax.tick_params(axis='y', colors='white', width=2, which='minor')

    fFig = 'ERNet_%03d.png' % len(G.edges())
    plt.savefig(os.path.join(outDir,fFig), dpi=150, facecolor='black')
    #plt.show()
    plt.close()
