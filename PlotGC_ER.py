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
N = 200  # Number of nodes
E = 300  # Number of edges
nNet = 100 # Number of networks to be generated

# storage for giant compnent sizes
GCSize = np.zeros([nNet,E])
for iNet in range(nNet):

    if (iNet+1)%10 == 0:
        print('Iteration: %d' % (iNet+1))
    # Initializing the graph
    G = nx.Graph()
    G.add_nodes_from(list(range(1,N+1)))  # adding nodes

    # for loop to add random edges
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
                CC = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
                GCSize[iNet,iEdge] = len(CC[0].nodes())
                break
