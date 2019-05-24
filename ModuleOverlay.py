import os
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib

# initializing various parameters
colorVecRed = ['purple','red','darkorange','violet','salmon','goldenrod','fuchsia','lightcoral','chocolate'] * 25
colorVecGreen = ['yellow','darkgreen','royalblue','darkkhaki','limegreen','navy','gold','springgreen','slateblue'] * 25
ms = 14.20  # marker size
disp_plane = 'xy'


# focusing on d=10 / EQd=10
d = 10

# coordinate info (d=10 / EQd=10)
# first, template (brain space)
XYZslice_TBrain = [3, -52, 34]
XYZslice_TVox = [87, 74, 106]
XYZslice_fVox = [21, 18, 26]

# aspect ratio info
aspectR = {'xy': [8.81, 10],
           'xz': [8.81, 8.81],
           'yz': [10, 8.81]}

# template image (MNI, 1mm)
#fMNIimg = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'
fMNIimg = 'MNI152_T1_1mm.nii.gz'
MNIimg = nib.load(fMNIimg)
X_MNI = MNIimg.get_data()


# function to return a section as 2D RGB data
def section2D(X, sliceCoord, plane):
    if plane=='xy':
        X2D = X[:,:,sliceCoord[2]]
        X2D_RGB = np.asarray([X2D]*3).T
        r_X2D_RGB = X2D_RGB/np.max(X2D_RGB)
    elif plane=='xz':
        X2D = X[:,sliceCoord[1],:]
        X2D_RGB = np.asarray([X2D]*3).T
        r_X2D_RGB = X2D_RGB/np.max(X2D_RGB)
    else:
        X2D = X[sliceCoord[0],:,:]
        X2D_RGB = np.asarray([X2D]*3).T
        r_X2D_RGB = X2D_RGB/np.max(X2D_RGB)
    return r_X2D_RGB




# directory info
#baseMod_RankTh = '/home/satoru/Projects/Connectome/Data/1000FCP/Oxford/Processed/sub47141/Modules/Network_RankTh'
baseMod_RankTh = '.'
#baseMod_HardThE = '/home/satoru/Projects/Connectome/Data/1000FCP/Oxford/Processed/sub47141/Modules/Network_HardThE'
baseMod_HardThE = '.'



# loading the module info file and image
fName_RankTh = 'Modules_d' + str(d) + '.npz'
fModInfoRankTh = os.path.join(baseMod_RankTh, fName_RankTh)
fNameImg_RankTh = 'Modules_d' + str(d) + '.nii.gz'
fModImgRankTh = os.path.join(baseMod_RankTh, fNameImg_RankTh)
fName_HardThE = 'Modules_EQd' + str(d) + '.npz'
fNameImg_HardThE = 'Modules_EQd' + str(d) + '.nii.gz'
fModInfoHardThE = os.path.join(baseMod_HardThE, fName_HardThE)
fModImgHardThE = os.path.join(baseMod_HardThE, fNameImg_HardThE)

# loading the module info file
inFileRankTh = np.load(fModInfoRankTh)
nNodesRankTh = inFileRankTh['NNodes']
modIDRankTh = inFileRankTh['ModID']
inFileHardThE = np.load(fModInfoHardThE)
nNodesHardThE = inFileHardThE['NNodes']
modIDHardThE = inFileHardThE['ModID']

# sorting the modules
snNodesRankTh, smodIDRankTh = zip(*sorted(zip(nNodesRankTh, modIDRankTh),
                                          reverse=True))
snNodesHardThE, smodIDHardThE = zip(*sorted(zip(nNodesHardThE, modIDHardThE),
                                          reverse=True))
# loading the module image array
ModImgRankTh = nib.load(fModImgRankTh)
X_ModRankTh = ModImgRankTh.get_data().astype(int)
ModImgHardThE = nib.load(fModImgHardThE)
X_ModHardThE = ModImgHardThE.get_data().astype(int)


# function to return module voxel coordinates
def modCoord(X,iMod):
    Q = list(np.where(X==iMod))
    Q.append(np.ones(len(Q[0])).astype(int))
    return np.array(Q)


# coordinate conversion: voxel space (functional) to voxel space (template)
def voxCoordConv(xyzMat, header_f, header_T):
    imat_vox2brain_f = np.array([header_f['srow_x'],
                                 header_f['srow_y'],
                                 header_f['srow_z'],
                                 [0,0,0,1]])
    imat_vox2brain_T = np.array([header_T['srow_x'],
                                 header_T['srow_y'],
                                 header_T['srow_z'],
                                 [0,0,0,1]])
    invmat_brain2vox_T = np.linalg.inv(imat_vox2brain_T)
    xyzMatVox = np.matmul(invmat_brain2vox_T, 
                          np.matmul(imat_vox2brain_f, xyzMat))
    return xyzMatVox


def planeCoord(xyzMat, sliceCoord, plane):
    voxSize = 4
    if plane == 'xy':
        Q1 = np.where((sliceCoord[2]-voxSize/2)<=xyzMat[2])[0]
        Q2 = np.where(xyzMat[2]<(sliceCoord[2]+voxSize))[0]
        Q = sorted(np.array(list(set(Q1) & set(Q2))))
        X = xyzMat[0][Q]
        Y = xyzMat[1][Q]
    elif plane == 'xz':
        Q1 = np.where((sliceCoord[1]-voxSize/2)<=xyzMat[1])[0]
        Q2 = np.where(xyzMat[1]<(sliceCoord[1]+voxSize))[0]
        Q = sorted(np.array(list(set(Q1) & set(Q2))))
        X = xyzMat[0][Q]
        Y = xyzMat[2][Q]
    else:
        Q1 = np.where((sliceCoord[0]-voxSize/2)<=xyzMat[0])[0]
        Q2 = np.where(xyzMat[0]<(sliceCoord[0]+voxSize))[0]
        Q = sorted(np.array(list(set(Q1) & set(Q2))))
        X = xyzMat[1][Q]
        Y = xyzMat[2][Q]
    return X, Y


def hexTiling(x, y, s=4.0):
    # spacing parameter to be adjusted
    newX = []
    newY = []
    for i in range(len(x)):
        X = x[i]
        Y = y[i]
        newX.append(X)
        newY.append(Y)
        tmpX = [X+0.75*s, X+0.75*s, X, X-0.75*s, X-0.75*s, X]
        tmpY = [Y-0.5*s, Y+0.5*s, Y+s, Y+0.5*s, Y-0.5*s, Y-s]
        newX += tmpX
        newY += tmpY
    return newX, newY



# for fun, modules (RankTh)
fig = plt.figure(figsize=aspectR[disp_plane])
ax1 = fig.add_subplot(111)
# axial slice
r_plane = section2D(X_MNI, XYZslice_TVox, disp_plane)
plt.imshow(r_plane, interpolation='bilinear')
for iMod in range(len(nNodesRankTh)):
    modXYZ = modCoord(X_ModRankTh, smodIDRankTh[iMod])
    modXYZVox = voxCoordConv(modXYZ, ModImgRankTh.header, MNIimg.header)
    X, Y = planeCoord(modXYZVox, XYZslice_TVox, disp_plane)
    #newX, newY = hexTiling(X, Y, 2.0)
    plt.plot(X, Y,
             marker='8',
             markersize=ms, c=colorVecRed[iMod],
             linewidth=0)
plt.gca().invert_yaxis()
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
fOutRankTh = 'ModuleOverlay_RankTh_' + disp_plane + '.png'
plt.savefig(fOutRankTh, dpi=600)
#plt.show()



# for fun, modules (HardThE)
fig = plt.figure(figsize=aspectR[disp_plane])
ax1 = fig.add_subplot(111)
# axial slice
r_plane = section2D(X_MNI, XYZslice_TVox, disp_plane)
plt.imshow(r_plane, interpolation='bilinear')
for iMod in range(len(nNodesHardThE)):
    modXYZ = modCoord(X_ModHardThE, smodIDHardThE[iMod])
    modXYZVox = voxCoordConv(modXYZ, ModImgHardThE.header, MNIimg.header)
    X, Y = planeCoord(modXYZVox, XYZslice_TVox, disp_plane)
    #newX, newY = hexTiling(X, Y, 2.0)
    plt.plot(X, Y,
             marker='8',
             markersize=ms, c=colorVecGreen[iMod],
             linewidth=0)
plt.gca().invert_yaxis()
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
fOutHardThE = 'ModuleOverlay_HardThE_' + disp_plane + '.png'
plt.savefig(fOutHardThE, dpi=600)
#plt.show()

