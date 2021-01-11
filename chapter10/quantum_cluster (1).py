import numpy as nump
from scipy.spatial import distance as spatDistance
from sklearn.decomposition import PCA as decomPCA
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D as mplAxes3D

def getVGradient(data:nump.ndarray,sigma,x:nump.ndarray=None,coeffs:nump.ndarray=None):
   
    
    if x is None:
        x = data.copy()
    
    if coeffs is None:
        coeffs = nump.ones((data.shape[0],))
    
        
    twoSigmaSquared = 2*sigma**2
        
    data = data[nump.newaxis,:,:]
    x = x[:,nump.newaxis,:]
    differences = x-data
    squaredDifferences = nump.sum(nump.square(differences),axis=2)
    gaussian = nump.exp(-(1/twoSigmaSquared)*squaredDifferences)
    laplacian = nump.sum(coeffs*gaussian*squaredDifferences,axis=1)
    parzen = nump.sum(coeffs*gaussian,axis=1)
    v = 1 + (1/twoSigmaSquared)*laplacian/parzen

    dv = -1*(1/parzen[:,nump.newaxis])*nump.sum(differences*((coeffs*gaussian)[:,:,nump.newaxis])*(twoSigmaSquared*(v[:,nump.newaxis,nump.newaxis])-(squaredDifferences[:,:,nump.newaxis])),axis=1)
    
    v = v-1
    
    return v, dv

def getSGradient(data:nump.ndarray,sigma,x:nump.ndarray=None,coeffs:nump.ndarray=None):
   
    if x is None:
        x = data.copy()
        
    if coeffs is None:
        coeffs = nump.ones((data.shape[0],))
    
    twoSigmaSquared = 2 * sigma ** 2
    
    data = data[nump.newaxis, :, :]
    x = x[:, nump.newaxis, :]
    differences = x - data
    squaredDifferences = nump.sum(nump.square(differences), axis=2)
    gaussian = nump.exp(-(1 / twoSigmaSquared) * squaredDifferences)
    laplacian = nump.sum(coeffs*gaussian * squaredDifferences, axis=1)
    parzen = nump.sum(coeffs*gaussian, axis=1)
    v = (1 / twoSigmaSquared) * laplacian / parzen
    s = v + nump.log(nump.abs(parzen))
    
    ds = (1 / parzen[:, nump.newaxis]) * nump.sum(differences * ((coeffs*gaussian)[:, :, nump.newaxis]) * (
    twoSigmaSquared * (v[:, nump.newaxis, nump.newaxis]) - (squaredDifferences[:, :, nump.newaxis])), axis=1)
    
    return s, ds

def getPGradient(data:nump.ndarray,sigma,x:nump.ndarray=None,coeffs:nump.ndarray=None):

    if x is None:
        x = data.copy()
        
    if coeffs is None:
        coeffs = nump.ones((data.shape[0],))
    
    twoSigmaSquared = 2 * sigma ** 2
    
    data = data[nump.newaxis, :, :]
    x = x[:, nump.newaxis, :]
    differences = x - data
    squaredDifferences = nump.sum(nump.square(differences), axis=2)
    gaussian = nump.exp(-(1 / twoSigmaSquared) * squaredDifferences)
    p = nump.sum(coeffs*gaussian,axis=1)
    
    dp = -1*nump.sum(differences * ((coeffs*gaussian)[:, :, nump.newaxis]) * twoSigmaSquared,axis=1)
    
    return p, dp

def getApproximateParzenValues(data:nump.ndarray,sigma,voxelSize):

    newData = getUniqueRows(nump.floor(data/voxelSize)*voxelSize+voxelSize/2)[0]
    
    nMat = nump.exp(-1*spatDistance.squareform(nump.square(spatDistance.pdist(newData)))/(4*sigma**2))
    mMat = nump.exp(-1 * nump.square(spatDistance.cdist(newData,data)) / (4 * sigma ** 2))
    cMat = nump.linalg.solve(nMat,mMat)
    coeffs = nump.sum(cMat,axis=1)
    coeffs = data.shape[0]*coeffs/sum(coeffs)
    
    return newData,coeffs

def getUniqueRows(x):
    y = nump.ascontiguousarray(x).view(nump.dtype((nump.void, x.dtype.itemsize * x.shape[1])))
    _, inds,indsInverse,counts = nump.unique(y, return_index=True,return_inverse=True,return_counts=True)

    xUnique = x[inds]
    return xUnique,inds,indsInverse,counts

def getGradientDescent(data,sigma,repetitions=1,stepSize=None,clusteringType='v',recalculate=False,returnHistory=False,stopCondition=True,voxelSize=None):
    
    n = data.shape[0]

    useApproximation = (voxelSize is not None)
    
    if stepSize is None:
        stepSize = sigma/10
    
    if clusteringType == 'v':
        gradientFunction = getVGradient
    elif clusteringType == 's':
        gradientFunction = getSGradient
    else:
        gradientFunction = getPGradient

    if useApproximation:
        newData, coeffs = getApproximateParzenValues(data, sigma, voxelSize)
    else:
        coeffs = None

    if recalculate:
        if useApproximation:
            x = nump.vstack((data,newData))
            data = x[data.shape[0]:]
        else:
            x = data
    else:
        if useApproximation:
            x = data
            data = newData
        else:
            x = data.copy()
        
        
    if returnHistory:
        xHistory = nump.zeros((n,x.shape[1],repetitions+1))
        xHistory[:,:,0] = x[:n,:].copy()
        
    if stopCondition:
        prevX = x[:n].copy()

    for i in range(repetitions):
        if ((i>0) and (i%10==0)):
            if stopCondition:
                if nump.all(nump.linalg.norm(x[:n]-prevX,axis=1) < nump.sqrt(3*stepSize**2)):
                    i = i-1
                    break
                prevX = x[:n].copy()
            
        f,df = gradientFunction(data,sigma,x,coeffs)
        df = df/nump.linalg.norm(df,axis=1)[:,nump.newaxis]
        x[:] = x + stepSize*df

        if returnHistory:
            xHistory[:, :, i+1] = x[:n].copy()
            
    x = x[:n]

    if returnHistory:
        xHistory = xHistory[:,:,:(i+2)]
        return x,xHistory
    else:
        return x

def PerformFinalClusteringAlgo(data,stepSize):
    clusters = nump.zeros((data.shape[0]))
    i = nump.array([0])
    c = 0
    spatDistances = spatDistance.squareform(spatDistance.pdist(data))
    while i.shape[0]>0:
        i = i[0]
        inds = nump.argwhere(clusters==0)
        clusters[inds[spatDistances[i,inds] <= 3*stepSize]] = c
        c += 1
        i = nump.argwhere(clusters==0)
    return clusters

def displayClusteringValues(xHistory,clusters=None):

    plot.ion()
    plot.figure(figsize=(20, 12))
    if clusters is None:
        clusters = nump.zeros((xHistory.shape[0],))
    if xHistory.shape[1] == 1:

        sc = plot.scatter(xHistory[:,:,0],xHistory[:,:,0]*0,c=clusters,s=10)
        plot.xlim((nump.min(xHistory),nump.max(xHistory)))
        plot.ylim((-1,1))
        for i in range(xHistory.shape[2]):
            sc.set_offsets(xHistory[:, :, i])
            plot.title('step #' + str(i) + '/' + str(xHistory.shape[2]-1))
            plot.pause(0.05)
    elif xHistory.shape[1] == 2:

        sc = plot.scatter(xHistory[:, 0, 0], xHistory[:, 1, 0] , c=clusters, s=20)
        plot.xlim((nump.min(xHistory[:,0,:]), nump.max(xHistory[:,0,:])))
        plot.ylim((nump.min(xHistory[:, 1, :]), nump.max(xHistory[:, 1, :])))
        for i in range(xHistory.shape[2]):
            sc.set_offsets(xHistory[:, :, i])
            plot.title('step #' + str(i) + '/' + str(xHistory.shape[2]-1))
            plot.pause(0.2)
    else:
        if xHistory.shape[1] > 3:
            pca = decomPCA(3)
            pca.fit(xHistory[:,:,0])
            newXHistory = nump.zeros((xHistory.shape[0],3,xHistory.shape[2]))
            for i in range(xHistory.shape[2]):
                newXHistory[:,:,i] = pca.transform(xHistory[:,:,i])
            xHistory = newXHistory


        ax = plot.axes(projection='3d')
        sc = ax.scatter(xHistory[:, 0, 0], xHistory[:, 1, 0],xHistory[:, 2, 0], c=clusters, s=20)
        ax.set_xlim((nump.min(xHistory[:, 0, :]), nump.max(xHistory[:, 0, :])))
        ax.set_ylim((nump.min(xHistory[:, 1, :]), nump.max(xHistory[:, 1, :])))
        ax.set_zlim((nump.min(xHistory[:, 2, :]), nump.max(xHistory[:, 2, :])))
        for i in range(xHistory.shape[2]):
            sc._offsets3d =  (nump.ravel(xHistory[:, 0, i]),nump.ravel(xHistory[:, 1, i]),nump.ravel(xHistory[:, 2, i]))
            plot.gcf().suptitle('step #' + str(i) + '/' + str(xHistory.shape[2]-1))
            plot.pause(0.01)
            
    plot.show()        

