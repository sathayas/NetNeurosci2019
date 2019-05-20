#
# Generating an ER-network
#
import numpy as np
import networkx as nx
import random
from random import choice
import matplotlib.pyplot as plt

# seeding the random number generator
random.seed(2019)

#
# A function to pick two nodes randomly
#
def choose_nodes(g):
    n1 = choice(list(g.nodes()))
    n2 = choice(list(g.nodes()))
    while (n1 == n2):
        n2 = choice(list(g.nodes()))
    return n1, n2

#
# A function to pick two edges randomly
#
def choose_edges(g):
    e1 = choose_nodes(g)
    while g.has_edge(*e1):   # connectivity check
        e1 = choose_nodes(g)
    e2 = choose_nodes(g)
    while g.has_edge(*e2):   # connectivity check
        e2 = choose_nodes(g)
    return e1, e2

#
# A function to calculate the product of component sizes for an edge
#
def prod_comp(g,e):
    NList1 = nx.node_connected_component(g,e[0])
    NList2 = nx.node_connected_component(g,e[1])
    LenC1 = len(NList1)
    LenC2 = len(NList2)
    prodC = LenC1 * LenC2
    return prodC

#
# A function to add an edge that yields a smaller component size
#
def connect_nodes(g):
    E1, E2 = choose_edges(g)
    Prod1 = prod_comp(g, E1)
    Prod2 = prod_comp(g, E2)
    if Prod1==Prod2:
        NewE = choice([E1, E2])
        RejE = choice([E1, E2])
    else:
        if Prod1>Prod2:
            NewE = E2
            RejE = E1
        else:
            NewE = E1
            RejE = E2
    g.add_edge(*NewE)
    return NewE, RejE


# Parameters
N = 200  # Number of nodes
E = 300  # Number of edges


# Initializing the graph
G = nx.Graph()
G.add_nodes_from(list(range(1,N+1)))  # adding nodes

# initializing the recorders
edgeList = []   # list of edges added
rejList = []    # list of rejected edges

# the loop to add random edges
for iEdge in range(E):
    tmpE, tmpR = connect_nodes(G)
    edgeList.append(tmpE)
    rejList.append(tmpR)



# drawing the graph, just for fun, and to get the coordinates for nodes
plt.figure(figsize=[5,5])
posInit = nx.kamada_kawai_layout(G)
pos = nx.spring_layout(G, k=8.5, iterations=1000, pos=posInit) # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=100)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
plt.axis('off')
plt.show()




# writing out the edge list, in sequential order
fNameEdgeList = 'edges_PR_N%d' % N + '_E%d' % E + '.txt'
f = open(fNameEdgeList,'w')
for iEdge in edgeList:
    f.write('%4d  %4d\n' % iEdge)
f.close()


# writing out the rejected edge list, in sequential order
fNameRejList = 'rejects_PR_N%d' % N + '_E%d' % E + '.txt'
f = open(fNameEdgeList,'w')
for iEdge in rejList:
    f.write('%4d  %4d\n' % iEdge)
f.close()


# writing out the node list, with position
fNameNodeList = 'nodes_PR_N%d' % N + '_E%d' % E + '.txt'
g = open(fNameNodeList,'w')
nodeList=sorted(pos.items())
for iNode, iPos in nodeList:
    g.write('%4d' % iNode)
    g.write('  %10.6f  %10.6f\n' % (iPos[0], iPos[1]))
g.close()
