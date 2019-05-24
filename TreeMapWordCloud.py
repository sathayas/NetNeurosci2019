import os
import numpy as np
import pandas as pd
import squarify
import matplotlib.pyplot as plt
from matplotlib import patches
import random
from wordcloud import WordCloud
import nibabel as nib


# directory info
baseMod_RankTh = '/home/satoru/Projects/Connectome/Data/1000FCP/Oxford/Processed/sub47141/Modules/Network_RankTh'
#baseMod_RankTh = '.'
baseMod_HardThE = '/home/satoru/Projects/Connectome/Data/1000FCP/Oxford/Processed/sub47141/Modules/Network_HardThE'
#baseMod_HardThE = '.'

# Loading AAL atlas info
# AAL template image, re-sliced to the dimension of functional
fAALImg = '/home/satoru/Projects/Connectome/Templates/aal_MNI_V4_r.nii.gz'
#fAALImg = 'aal_MNI_V4_r.nii.gz'
imgAAL = nib.load(fAALImg)
X_AAL = imgAAL.get_data()

# AAL table of brain areas
fAALTable = '/home/satoru/Projects/Connectome/Templates/aal_MNI_V4.txt'
#fAALTable = 'aal_MNI_V4.txt'
AALTable = pd.read_table(fAALTable, skiprows = [0], header=None)
AALTable.columns = ['ROI', 'ROIName']


# initializing various parameters
x = 0.
y = 0.
u = 0.
v = 0.
width = 6000.
height = 6000.
colorVecRed = ['purple','red','darkorange','violet','salmon','goldenrod','fuchsia','lightcoral','chocolate'] * 25
colorVecGreen = ['yellow','darkgreen','royalblue','darkkhaki','limegreen','navy','gold','springgreen','slateblue'] * 25
dVoxel = [5,10,20,30]
bgColor = 'wheat'


# focus on d=10 modules
d = 10


# loading the module info file and image
fName_RankTh = 'Modules_d' + str(d) + '.npz'
fNameImg_RankTh = 'Modules_d' + str(d) + '.nii.gz'
fModInfoRankTh = os.path.join(baseMod_RankTh, fName_RankTh)
fModImgRankTh = os.path.join(baseMod_RankTh, fNameImg_RankTh)
fName_HardThE = 'Modules_EQd' + str(d) + '.npz'
fNameImg_HardThE = 'Modules_EQd' + str(d) + '.nii.gz'
fModInfoHardThE = os.path.join(baseMod_HardThE, fName_HardThE)
fModImgHardThE = os.path.join(baseMod_HardThE, fNameImg_HardThE)

# loading the module info file
inFileRankTh = np.load(fModInfoRankTh)
nNodesRankTh = inFileRankTh['NNodes']
inFileHardThE = np.load(fModInfoHardThE)
nNodesHardThE = inFileHardThE['NNodes']

# loading the module image array
ModImgRankTh = nib.load(fModImgRankTh)
X_ModRankTh = ModImgRankTh.get_data().astype(int)
ModImgHardThE = nib.load(fModImgHardThE)
X_ModHardThE = ModImgHardThE.get_data().astype(int)





#
# getting the tree maps  (RankTh first)
#
widthRankTh = width
heightRankTh = height

snNodesRankTh = sorted(nNodesRankTh, reverse=True)
snNodesRankTh = squarify.normalize_sizes(snNodesRankTh, widthRankTh, heightRankTh)
rectsRankTh = squarify.squarify(snNodesRankTh, x, y, widthRankTh, heightRankTh)



# word cloud for each module
wcList = []
for iMod in range(len(nNodesRankTh)):
    Qmod = np.where(X_ModRankTh==iMod+1)
    VoxAreaList = list(AALTable.ROIName[X_AAL[Qmod]-1])
    VoxText = ' '.join(VoxAreaList)
    # Generate a word cloud image
    wordcloud = WordCloud(background_color=colorVecRed[iMod],
                          width=np.floor(rectsRankTh[iMod]['dx']).astype(int),
                          height=np.floor(rectsRankTh[iMod]['dy']).astype(int),
                          colormap='copper',
                          prefer_horizontal=0.50,
                          collocations=False).generate(VoxText).to_array()
    wcList.append(wordcloud)




# generating the tree map plot
fig = plt.gcf()
fig.set_size_inches(10,10)

ax1 = fig.add_subplot(111, aspect='equal')
for iMod in range(len(rectsRankTh)):
    ax1.add_patch(
        patches.Rectangle(
            (rectsRankTh[iMod]['x'], rectsRankTh[iMod]['y']),   # (x,y)
            rectsRankTh[iMod]['dx'],          # width
            rectsRankTh[iMod]['dy'],          # height
            fill=False,
            ec=bgColor, lw=1.5
        )
    )
    x = np.floor(rectsRankTh[iMod]['x']).astype(int)
    y = np.floor(rectsRankTh[iMod]['y']).astype(int)
    dx = np.floor(rectsRankTh[iMod]['dx']).astype(int)
    dy = np.floor(rectsRankTh[iMod]['dy']).astype(int)
    extent  = [x, x+dx, y, y+dy]
    ax1.imshow(wcList[iMod],extent=extent, interpolation='bilinear')

plt.xlim([0, width])
plt.ylim([0, height])
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig('TreeMap_RankTh_d10.png', dpi=600)
#plt.show()
plt.close(fig)





#
# getting the tree maps  (HardThE next)
#
rHardvsRank = sum(nNodesHardThE) / sum(nNodesRankTh)
widthHardThE = width * np.sqrt(rHardvsRank)
heightHardThE = height * np.sqrt(rHardvsRank)

snNodesHardThE = sorted(nNodesHardThE, reverse=True)
snNodesHardThE = squarify.normalize_sizes(snNodesHardThE, widthHardThE, heightHardThE)
rectsHardThE = squarify.squarify(snNodesHardThE, u, v, widthHardThE, heightHardThE)
offsetWidth = width - widthHardThE
offsetHeight = height - heightHardThE



# word cloud for each module
wcList = []
for iMod in range(len(nNodesHardThE)):
    Qmod = np.where(X_ModHardThE==iMod+1)
    VoxAreaList = list(AALTable.ROIName[X_AAL[Qmod]-1])
    VoxText = ' '.join(VoxAreaList)
    # Generate a word cloud image
    wordcloud = WordCloud(background_color=colorVecGreen[iMod],
                          width=np.floor(rectsHardThE[iMod]['dx']).astype(int),
                          height=np.floor(rectsHardThE[iMod]['dy']).astype(int),
                          colormap='copper',
                          prefer_horizontal=0.50,
                          collocations=False).generate(VoxText).to_array()
    wcList.append(wordcloud)




# generating the tree map plot
fig = plt.gcf()
fig.set_size_inches(10,10)

ax1 = fig.add_subplot(111, aspect='equal')
# first, the blank box to indicate disconnected components
#ax1.add_patch(
#    patches.Rectangle(
#        (0, 0),   # (x,y)
#        width,          # width
#        height,          # height
#        facecolor=None,
#        ec='k',
#        alpha=0.5,
#    )
#)

ax1.add_patch(
    patches.Rectangle(
        (0, 0), width, offsetHeight,
        facecolor=bgColor
    )
)
ax1.add_patch(
    patches.Rectangle(
        (0, offsetHeight), offsetWidth, height,
        facecolor=bgColor
    )
)

for iMod in range(len(rectsHardThE)):
    ax1.add_patch(
        patches.Rectangle(
            (rectsHardThE[iMod]['x']+offsetWidth, 
             rectsHardThE[iMod]['y']+offsetHeight),   # (x,y)
            rectsHardThE[iMod]['dx'],          # width
            rectsHardThE[iMod]['dy'],          # height
            fill=False,
            ec=bgColor, lw=1.5
        )
    )
    x = np.floor(rectsHardThE[iMod]['x']).astype(int)
    y = np.floor(rectsHardThE[iMod]['y']).astype(int)
    dx = np.floor(rectsHardThE[iMod]['dx']).astype(int)
    dy = np.floor(rectsHardThE[iMod]['dy']).astype(int)
    extent  = [x+offsetWidth, 
               x+dx+offsetWidth, 
               y+offsetHeight, 
               y+dy+offsetHeight]
    ax1.imshow(wcList[iMod],extent=extent, interpolation='bilinear')

plt.xlim([0, width])
plt.ylim([0, height])
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig('TreeMap_HardThE_EQd10.png', dpi=600)
#plt.show()
plt.close(fig)


