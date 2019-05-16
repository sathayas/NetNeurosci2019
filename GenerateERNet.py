#
# Generating an ER-network
#
import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt

# seeding the random number generator
random.seed(2019)

# Parameters
N = 100  # Number of nodes
E = 150  # Number of edges


# Initializing the graph
G = nx.Graph()
G.add_nodes_from(list(range(1,N+1)))  # adding nodes

# for loop to add random edges
edgeList = []
for iEdge in range(E):
    # while loop to find an edge that doesnt already exist
    while True:
        # picking a random node
        nodeA = random.randint(1,N)
        # while loop to pick another node that has not been picked
        while True:
            nodeB = random.randint(1,N)
            if nodeA!=nodeB:
                break
        # Checking if there is an edge between nodeA and nodeB
        if nodeB not in G[nodeA]:
            G.add_edge(nodeA, nodeB)
            edgeList.append((nodeA, nodeB))
            break

# drawing the graph, just for fun, and to get the coordinates for nodes
plt.figure(figsize=[5,5])
posInit = nx.kamada_kawai_layout(G)
pos = nx.spring_layout(G, k=13, iterations=1000, pos=posInit) # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=100)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
plt.axis('off')
plt.show()


# writing out the edge list, in sequential order
# fNameEdgeList = 'edges_ER_N%d' % N + '_E%d' % E + '.txt'
# f = open(fNameEdgeList,'w')
# for iEdge in edgeList:
#     f.write('%4d  %4d\n' % iEdge)
# f.close()
