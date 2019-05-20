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


# right panel: giant component size
plotX = np.arange(1,E+1)
plotY = np.mean(GCSize,axis=0)/N

plt.figure(figsize=[4,4], facecolor='k')
plt.subplot(122, position=[0.25,0.15,0.85,0.85])
plt.plot(plotX[plotX<100], plotY[plotX<100],
        '-', linewidth=3.0, color='skyblue')
plt.plot(plotX[plotX>=100], plotY[plotX>=100],
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

plt.show()
