#
# Generates a sequence of images of ER network
#
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Parameters
N = 100  # Number of nodes
E = 150  # Number of edges


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



# adding a single edge and drawing
