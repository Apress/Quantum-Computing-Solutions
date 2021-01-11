import numpy as nump
import quantum_cluster



types = ['f8', 'f8', 'f8','f8','U50']

data_res = nump.loadtxt('iris_input.csv', delimiter=',')

print(data_res)
data_res = data_res[:,:4]

sigma_val=0.55
repetitionsVal=100
stepSizeVal=0.1
clusteringTypeVal='v'
isRecalculate=False
isReturnHistory=True
isStopCondition=True
voxelSizeVal = None

xval,xHistoryVal = quantum_cluster.getGradientDescent(data_res,sigma=sigma_val,repetitions=repetitionsVal,stepSize=stepSizeVal,clusteringType=clusteringTypeVal,recalculate=isRecalculate,returnHistory=isReturnHistory,stopCondition=isStopCondition,voxelSize=voxelSizeVal)

clusters_res = quantum_cluster.PerformFinalClusteringAlgo(xval,stepSizeVal)

quantum_cluster.displayClusteringValues(xHistoryVal,clusters_res)