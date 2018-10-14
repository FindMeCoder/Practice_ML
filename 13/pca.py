# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:57:58 2018

@author: 寻ME
"""
#对数据进行的简化的原因
#（1）使数据集更易使用
#（2）降低计算开销
#（3）去除噪声
#（4）使得结果易懂
#在已标注的数据集上何未标注的数据集上都有降维技术，我们主要关注未标注的数据集上的降维技术。
# 1.第一种技术为主成分分析（PCA），数据转化到新的坐标系下，坐标轴的选择由数据本身确定，第一个坐标轴选择方差最大的方向，第二个选择
#与第一个正交且具有最大方差的方向。我们可以发现，大部分方差都包含在最前边的几个坐标系中，因此，忽略了余下的坐标轴，对数据进行了降维处理
# 2.另一种降维方法是因子分析(FA)，在因子分析中，假设在观察数据中有一些观察不到的隐变量，数据有这些隐变量何何一些噪声的线性组合，那么隐变量的数量
#比观察数据的少，通过找到这些隐变量可以实现对数据的降维。
# 3. 还有一种降维技术是独立成分分析（ICA），ICA假设数据由N个数据源生成的，这一点何因子分析有点像，由多个数据源的混合观测得到的结果，这些数据源在统计上是
#相互独立的，而PCA只假设数据是不相关的。
#PCA
# (1)优点：降低数据的复杂性，识别多个重要的特征
# (2)缺点：损失有用信息
# （3）适用性数据：数值型数据
# （4）通过PCA降维，我们可以同时获得SVM和决策树的优点，一方面，分类间隔何SVM一样好，另一方面，得到了何决策树一样简单的分类器。
# PCA的实现过程：
# （1）.去除平均值
# （2）.计算协方差矩阵
# （3）. 计算协方差矩阵的特征值何特征向量
# （4）. 将特征值排序
# （5）. 保留最上边的N个向量
# （6）将数据转换到上述N各特征向量构成的空间中

from numpy import *

def loadDataSet(fileName,delim='\t'):
    fr=open(fileName)
    stringArr=[line.strip().split(delim) for line in fr.readlines()]
    datArr=[list(map(float,line)) for line in stringArr]
    return mat(datArr)

def pca(dataMat,topNfeat=99999):
    meanVals=mean(dataMat,axis=0)
    meanRemoved=dataMat-meanVals
    covMat=cov(meanRemoved,rowvar=0)
    eigVals,eigVects=linalg.eig(mat(covMat))
    eigValInd=argsort(eigVals)
    eigValInd=eigValInd[:-(topNfeat+1):-1]
    redEigVect=eigVects[:,eigValInd]
    lowDDataMat=meanRemoved*redEigVect
    reconMat=(lowDDataMat*redEigVect.T)+meanVals
    return lowDDataMat,reconMat
def picture():
    import matplotlib
    import matplotlib.pyplot as plt
    
    data=loadDataSet('testSet.txt')
    lowDDataMat,reconMat=pca(data,topNfeat=1)
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(data[:,0].flatten().A[0],data[:,1].flatten().A[0],marker='^',s=90)
    ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')

def replaceNanWithMean():
    dataMat=loadDataSet('secom.data',' ')
    numFeat=shape(dataMat)[1]
    for i in range(numFeat):
        meanVal=mean(dataMat[nonzero(~isnan(dataMat[:,i].A))[0],i])
        dataMat[nonzero(isnan(dataMat[:,i].A))[0],i]=meanVal
    return dataMat


