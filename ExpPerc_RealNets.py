#
# The largest component size plot
# Both ascending and descending
#


# appropriate packages are imported
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# parameters
posLeft = [0.1, 0.15, 0.3, 0.7]
xLim = [-0.01, 4.3]
yLim = [-0.01, 1.01]



### Initialization of figure
fig = plt.figure(figsize=[10,4], facecolor='k')


#
# S&P 500 data first
#

# file business
fRankThNet = 'RankThNet_SP500.npz'

# loading the file from the previously run analysis
infile = np.load(fRankThNet)
nNodes = infile['NNodes']  # Number of nodes
GCSize = infile['GCSize']  # Giant component size
nEdges = np.arange(1,len(GCSize)+1)   # Number of edges -- is a series

# calculating variables for plotting
rGCSize= GCSize / nNodes # relative component size
plotX = nEdges / nNodes # <k>

# acual plotting
plt.subplot(131, position=posLeft)
plt.plot(plotX, rGCSize, '-', color='skyblue', linewidth=2)
plt.xlim(xLim)
plt.ylim(yLim)
ax = plt.gca()
plt.title('S&P 500 network\n(N=491)', fontsize=14, color='w')
plt.ylabel('Giant component\nsize (relative)', color='w', fontsize=12)
plt.xlabel('<k>', color='w', fontsize=12)
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1)
  ax.spines[axis].set_color('white')
ax.set_facecolor('k')
ax.tick_params(axis='x', colors='white', width=1, which='major', labelsize=11)
ax.tick_params(axis='x', colors='white', width=1, which='minor')
ax.tick_params(axis='y', colors='white', width=1, which='major', labelsize=11)
ax.tick_params(axis='y', colors='white', width=1, which='minor')

plt.show()




#
# Airline data second
#

# file names
fRankThNet_ascend = '/home/shayasak/Projects/Percolation/RealNetwork/Airline/Analysis/RankThNet_ascend.npz'
fRankThNet_descend = '/home/shayasak/Projects/Percolation/RealNetwork/Airline/Analysis/RankThNet_descend.npz'

# loading the file from the previously run analysis
infile = np.load(fRankThNet_ascend)
d = infile['d']
NNodes = infile['NNodes']
GCSize_ascend = infile['GCSize']
dRecord = infile['dRecord']

infile2 = np.load(fRankThNet_descend)
GCSize_descend = infile2['GCSize']

# figuring out the beginning and end of different d values
dInd = []
for iTop in range(d):
    tmpInd = np.nonzero(np.array(dRecord)==(iTop+1))[0]
    tmpLim = [tmpInd[0],tmpInd[-1]]
    dInd.append(tmpLim)

# calculating variables for plotting
rGCSize_ascend = np.array(GCSize_ascend) / float(NNodes)  # relative component size
rGCSize_descend = np.array(GCSize_descend) / float(NNodes)  # relative component size
t = np.arange(1.0,len(GCSize_ascend)+1.0) / float(NNodes)

# labels
dLabel = ['Largest\nelements', '2nd\nlargest\nelements',
          '3rd\nlargest\nelements', '4th\nlargest\nelements',
          '5th\nlargest\nelements']

# acual plotting
plt.subplot(2, 2, 2)
plt.plot(t[:dInd[2][1]],rGCSize_ascend[:dInd[2][1]], '-', color='r', linewidth=1)
plt.plot(t[:dInd[2][1]],rGCSize_descend[:dInd[2][1]], '-', color='b', linewidth=1)
plt.ylim([0,1.01])
#plt.xlim([0,t.max()])
plt.xlim([0,t[dInd[2][1]]])
ax = plt.gca()
#for ibar in range(d):
for ibar in range(3):
    ax.text((t[dInd[ibar][1]]+t[dInd[ibar][0]])/2, 1.03, dLabel[ibar],
            va='bottom', ha='center', multialignment='left',
            rotation=90, fontsize=7)
    if (ibar % 2)==1:
        plt.axvspan(t[dInd[ibar][0]], t[dInd[ibar][1]],
                    facecolor='0.85', edgecolor='none')
plt.title('(b) Airline network ($n$=1060)', fontsize=9, y=1.30)
plt.xlabel('$t$', fontsize=8)
#plt.ylabel("$S_{max}/n$", fontsize=5)
ax.xaxis.set_ticks(np.arange(0, 2.5, 0.5))
ax.xaxis.set_tick_params(labelsize=7)
ax.yaxis.set_tick_params(labelsize=7)
#plt.subplots_adjust(bottom=0.08, left=0.10, top=0.83, right=0.99, wspace=0.13)
plt.plot([0.870, 0.870], [0.0, 1.01], ':', lw=0.75, color='r')
plt.plot([0.990, 0.990], [0.0, 1.01], ':', lw=0.75, color='b')
legend = plt.legend(['Ascending', 'Descending',
                     r"$t_c = 0.895$" + "\n" + "(ascending)",
                     r"$t_c = 0.974$" + "\n" + "(descending)"],
                    fontsize=7, loc=4)







#
# Yeast gene co-expression data
#


# file names
fRankThNet_ascend = '/home/shayasak/Projects/Percolation/RealNetwork/YeastGeneExp/Analysis/RankThNet_ascend.npz'
fRankThNet_descend = '/home/shayasak/Projects/Percolation/RealNetwork/YeastGeneExp/Analysis/RankThNet_descend.npz'

# loading the file from the previously run analysis
infile = np.load(fRankThNet_ascend)
d = infile['d']
NNodes = infile['NNodes']
GCSize_ascend = infile['GCSize']
dRecord = infile['dRecord']

infile2 = np.load(fRankThNet_descend)
GCSize_descend = infile2['GCSize']

# figuring out the beginning and end of different d values
dInd = []
for iTop in range(d):
    tmpInd = np.nonzero(np.array(dRecord)==(iTop+1))[0]
    tmpLim = [tmpInd[0],tmpInd[-1]]
    dInd.append(tmpLim)

# calculating variables for plotting
rGCSize_ascend = np.array(GCSize_ascend) / float(NNodes)  # relative component size
rGCSize_descend = np.array(GCSize_descend) / float(NNodes)  # relative component size
t = np.arange(1.0,len(GCSize_ascend)+1.0) / float(NNodes)

# labels
dLabel = ['Largest\nelements', '2nd\nlargest\nelements',
          '3rd\nlargest\nelements', '4th\nlargest\nelements',
          '5th\nlargest\nelements']

# acual plotting
plt.subplot(2, 2, 3)
plt.plot(t[:dInd[2][1]],rGCSize_ascend[:dInd[2][1]], '-', color='r', linewidth=1)
plt.plot(t[:dInd[2][1]],rGCSize_descend[:dInd[2][1]], '-', color='b', linewidth=1)
plt.ylim([0,1.01])
#plt.xlim([0,t.max()])
plt.xlim([0,t[dInd[2][1]]])
ax = plt.gca()
#for ibar in range(d):
for ibar in range(3):
    ax.text((t[dInd[ibar][1]]+t[dInd[ibar][0]])/2, 1.03, dLabel[ibar],
            va='bottom', ha='center', multialignment='left',
            rotation=90, fontsize=7)
    if (ibar % 2)==1:
        plt.axvspan(t[dInd[ibar][0]], t[dInd[ibar][1]],
                    facecolor='0.85', edgecolor='none')
plt.title('(c) Gene co-expression ($n$=5168)', fontsize=9, y=1.30)
plt.xlabel('$t$', fontsize=8)
plt.ylabel("$S_{max}/n$", fontsize=8)
ax.xaxis.set_ticks(np.arange(0, 2.5, 0.5))
ax.xaxis.set_tick_params(labelsize=7)
ax.yaxis.set_tick_params(labelsize=7)
#plt.subplots_adjust(bottom=0.07, left=0.10, top=0.85, right=0.99, wspace=0.13, hspace=0.75)
plt.plot([0.870, 0.870], [0.0, 1.01], ':', lw=0.75, color='r')
plt.plot([0.990, 0.990], [0.0, 1.01], ':', lw=0.75, color='b')
legend = plt.legend(['Ascending', 'Descending',
                     r"$t_c = 0.865$" + "\n" + "(ascending)",
                     r"$t_c = 0.850$" + "\n" + "(descending)"],
                    fontsize=7, loc=4)









#
# Brain network data
#

# file names
BaseDir = '/home/shayasak/Projects/Percolation/RealNetwork/fMRI/Oxford/'
DirContents = os.listdir(BaseDir)
DirContents.sort()
SubjID = [DirContents[x] for x in range(len(DirContents)) if 'sub' in DirContents[x]]


# reading the giant component data (ascending)
NNodes = np.array([])
NEdges = np.array([])
GCSize_ascend = []
rGCSize_ascend = []
dInd = []
for iSubj in range(len(SubjID)):
    # loading the file from the previously run analysis
    SubjDir = os.path.join(BaseDir, SubjID[iSubj])
    fRankThNet = os.path.join(SubjDir, 'RankThNet_ascend.npz')
    infile = np.load(fRankThNet)
    tmpd = infile['d']
    tmpNNodes = infile['NNodes']
    tmpGCSize = infile['GCSize']
    tmprGCSize = tmpGCSize / float(tmpNNodes)
    GCSize_ascend.append(tmpGCSize)
    rGCSize_ascend.append(tmprGCSize)
    NNodes = np.append(NNodes, tmpNNodes)
    NEdges = np.append(NEdges, len(tmpGCSize))
    # figuring out the beginning and end of different d values
    dRecord = infile['dRecord']
    tmpdInd = []
    for iTop in range(tmpd):
        tmpInd = np.nonzero(np.array(dRecord)==(iTop+1))[0]
        tmpLim = [tmpInd[0],tmpInd[-1]]
        tmpdInd.append(tmpLim)
    dInd.append(tmpdInd)

# reading the giant component data (descending)
GCSize_descend = []
rGCSize_descend = []
for iSubj in range(len(SubjID)):
    # loading the file from the previously run analysis
    SubjDir = os.path.join(BaseDir, SubjID[iSubj])
    fRankThNet = os.path.join(SubjDir, 'RankThNet_descend.npz')
    infile = np.load(fRankThNet)
    tmpNNodes = infile['NNodes']
    tmpGCSize = infile['GCSize']
    tmprGCSize = tmpGCSize / float(tmpNNodes)
    GCSize_descend.append(tmpGCSize)
    rGCSize_descend.append(tmprGCSize)

# calculating the mean of the giant component size data
MaxE = np.min(NEdges)
for iSubj in range(len(SubjID)):
    if iSubj == 0:
        SumGC_ascend = rGCSize_ascend[0][:MaxE]
        SumGC_descend = rGCSize_descend[0][:MaxE]
    else:
        SumGC_ascend += rGCSize_ascend[iSubj][:MaxE]
        SumGC_descend += rGCSize_descend[iSubj][:MaxE]
meanrGCSize_ascend = SumGC_ascend / float(len(SubjID))
meanrGCSize_descend = SumGC_descend / float(len(SubjID))

# caluclating the mean locations of 1st, 2nd, 3rd, ... etc edges
d = tmpd
meandInd = []
for iTop in range(tmpd):
    tmpInd_min=[dInd[i][iTop][0] for i in range(len(SubjID))]
    tmpInd_max=[dInd[i][iTop][1] for i in range(len(SubjID))]
    meandInd.append([np.mean(tmpInd_min), np.mean(tmpInd_max)])
meandInd_t = np.array(meandInd) / NNodes.mean()

# calculating variables for plotting
t = np.arange(1.0,MaxE+1.0) / NNodes.mean()

# labels
dLabel = ['Largest\nelements', '2nd\nlargest\nelements',
          '3rd\nlargest\nelements', '4th\nlargest\nelements',
          '5th\nlargest\nelements']

# acual plotting
plt.subplot(2, 2, 4)
plt.plot(t[:meandInd[2][1]],meanrGCSize_ascend[:meandInd[2][1]], '-', color='r', lw=1)
plt.plot(t[:meandInd[2][1]],meanrGCSize_descend[:meandInd[2][1]], '-', color='b', lw=1)
plt.ylim([0,1.01])
#plt.xlim([0,t.max()])
plt.xlim([0,t[meandInd[2][1]]])
ax = plt.gca()
#for ibar in range(d):
for ibar in range(3):
    ax.text((meandInd_t[ibar][0] + meandInd_t[ibar][1])/2, 1.03, dLabel[ibar],
            va='bottom', ha='center', multialignment='left',
            rotation=90, fontsize=7)
    if (ibar % 2)==1:
        plt.axvspan(meandInd_t[ibar][0], meandInd_t[ibar][1],
                    facecolor='0.85', edgecolor='none')
plt.title('(d) Brain network ($\\langle n \\rangle$=18990)', fontsize=9, y=1.30)
plt.xlabel('$t$', fontsize=8)
#plt.ylabel("$S_{max}/n$", fontsize=5)
ax.xaxis.set_ticks(np.arange(0, 2.5, 0.5))
ax.xaxis.set_tick_params(labelsize=7)
ax.yaxis.set_tick_params(labelsize=7)
plt.subplots_adjust(bottom=0.07, left=0.10, top=0.85, right=0.99, wspace=0.13, hspace=0.75)
plt.plot([0.847, 0.847], [0.0, 1.01], ':', lw=0.75, color='r')
plt.plot([0.825, 0.825], [0.0, 1.01], ':', lw=0.75, color='b')
legend = plt.legend(['Ascending', 'Descending',
                     r"$\langle t_c \rangle = 0.847$" + "\n" + "(ascending)",
                     r"$\langle t_c \rangle = 0.825$" + "\n" + "(descending)"],
                    fontsize=7, loc=4)
plt.savefig(OutFig, format='eps', dpi=500)
#plt.savefig(OutFig, dpi=300)
plt.show()
