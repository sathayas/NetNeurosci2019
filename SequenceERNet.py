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



# drawing with no edges
plt.figure(figsize=[5,5], facecolor='k')
plt.subplot(111)
nx.draw_networkx_nodes(G, pos, node_size=30, node_color = 'salmon',
                        linewidth=None)
plt.axis('off')
plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
plt.show()


# adding a single edge and drawing
for iEdge in edgeList[:10]:
    G.add_edge(iEdge[0], iEdge[1])
    plt.figure(figsize=[5,5], facecolor='k')
    plt.subplot(111)
    # drawing nodes and edges
    nx.draw_networkx_edges(G, pos, edge_color='skyblue', width=3.0)
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color = 'salmon',
                            linewidth=None)
    # drawing nodes and edges of the giant component
    CC = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    GC = CC[0]
    nx.draw_networkx_edges(G, pos, edgelist = GC.edges(),
                            edge_color='skyblue', width=6.0)
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

    plt.axis('off')
    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    plt.show()
