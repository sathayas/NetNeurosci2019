import numpy as np
import networkx as nx



def net_builder_RankTh(R, NodeInd, d, cType=1):
    '''
    a function to construct the network by the rank-based thresholding

    input parameters:
          R:         A dense correlation matrix array.
          NodeInd:   A list of nodes in the network.
          d:         The rank threshold for the rank-based thresholding.
          cType:     Type of functional connectivity.
                        1:  Positive correlation only
                        0:  Both positive and negative correlations
                        -1: Negative correlation only
                     The default is 1 (i.e., positive correlation only).
    returns:
          G:         The resulting graph (networkX format)
    '''

    # first, initialize the graph
    G = nx.Graph()
    G.add_nodes_from(NodeInd)
    NNodes = R.shape[0]
    # the working copy of R, depending on the connectivity type
    if cType==1:
        WorkR = np.copy(R)
    elif cType==0:
        WorkR = abs(np.copy(R))
    elif cType==-1:
        WorkR = np.copy(-R)
    # then add edges
    for iRank in range(d):
        I = np.arange(NNodes)
        J = np.argmax(WorkR, axis=1)
        # R has to be non-zero
        trI = [i for i in range(NNodes) if WorkR[i, J[i]]>0]
        trJ = [J[i] for i in range(NNodes) if WorkR[i, J[i]]>0]
        # adding connections (for R>0)
        Elist = np.vstack((NodeInd[trI], NodeInd[trJ])).T
        G.add_edges_from(Elist)
    # finally returning the resultant graph
    return G



def net_builder_HardTh(R, NodeInd, K, cType=1):
    '''
    a function to construct the network by the hard-thresholding.
    input parameters:
          R:         A dense correlation matrix array.
          NodeInd:   A list of nodes in the network.
          K:         The target K, the average connections at each node
          cType:     Type of functional connectivity.
                        1:  Positive correlation only
                        0:  Both positive and negative correlations
                        -1: Negative correlation only
                     The default is 1 (i.e., positive correlation only).

    returns:
          G:         The resulting graph (networkX format)
          RTh:       The R-value of the threshold achieveing the target K.
    '''

    # first, initialize the graph
    G = nx.Graph()
    G.add_nodes_from(NodeInd)
    NNodes = R.shape[0]
    # upper triangle of the correlation matrix only
    I,J = np.triu_indices(NNodes,1)
    # creating a vector of correlation coefficients, depending on cType
    if cType==1:
        VecR = np.squeeze(np.array(R[I,J]))
    elif cType==0:
        VecR = np.squeeze(np.array(abs(R[I,J])))
    elif cType==-1:
        VecR = np.squeeze(np.array(-R[I,J]))
    # the number of elements is too big, so we truncate it
    # first, find the appropriate threshold for R
    NthR = 0
    tmpRth = 0.95
    StepTh = 0.05
    while NthR<K*NNodes/2.0:
        tmpRth -= StepTh
        #print('Threshold = %.2f' % tmpRth)
        NthR = len(np.nonzero(VecR>tmpRth)[0])
    # second, truncate the variables
    IndVecR = np.nonzero(VecR>tmpRth)
    thVecR = VecR[IndVecR]
    thI = I[IndVecR]
    thJ = J[IndVecR]
    # sort the correlation values
    zipR = zip(thVecR, thI, thJ)
    zipsR = sorted(zipR, key = lambda t: t[0], reverse=True)
    sVecR, sI, sJ = zip(*zipsR)
    # then adding edges
    m = int(np.ceil(K*NNodes/2.0))  # the number of edges
    trI = np.array(sI[:m])
    trJ = np.array(sJ[:m])
    Elist = np.vstack((NodeInd[trI], NodeInd[trJ])).T
    G.add_edges_from(Elist)
    # finally returning the resultant graph
    return G
