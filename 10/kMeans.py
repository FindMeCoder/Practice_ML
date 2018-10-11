# -*- coding: utf-8 -*-
"""
Created on Tue Oct  10 16:08:07 2018

@author: 寻ME
"""

from numpy import *

def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        currLine=line.strip().split('\t')
        fltLine=list(map(float,currLine))
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))

#给给定数据集构建一个k个随机质心的集合
def randCent(dataSet,k):
    n=shape(dataSet)[1]
    centroids=mat(zeros((k,n)))
    for j in range(n):
        minJ=min(dataSet[:,j])
        rangeJ=float(max(dataSet[:,j])-minJ)
        centroids[:,j]=minJ+rangeJ*random.rand(k,1) #rand产生矩阵
    return centroids

def Kmeans(dataSet,k,distMeas=distEclud,createCent=randCent):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    centroids=createCent(dataSet,k)  #随机产生K个质心
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):     
            minDist=inf;minIndex=-1
            for j in range(k):
                distJI=distMeas(centroids[j,:],dataSet[i,:])
                if distJI<minDist:
                    minDist=distJI
                    minIndex=j
            if clusterAssment[i,0]!=minIndex:
                  clusterChanged=True
                 # print(i,j,clusterChanged)
            clusterAssment[i,:]=minIndex,minDist**2
        print(centroids)
        for cent in range(k):  #更新质心距离
             psInClust=dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
             centroids[cent,:]=mean(psInClust,axis=0)
    return centroids,clusterAssment

#使用后处理提高聚类性能
#为了克服K-均值算法收敛于局部最小值的问题，提出了另一个二分K均值的算法
#将所有簇看成一个簇，然后一分为二，选择其中一个可以最大程度降低SSE的值簇

def biKmeans(dataSet,k,distMeas=distEclud):
    m=shape(dataSet)[0]
    dataSet=mat(dataSet)
    clusterAssment=mat(zeros((m,2)))
    centroid0=mean(dataSet,0).tolist()[0]
    cenList=[centroid0]
    for j in range(m):
        clusterAssment[j,1]=distMeas(mat(centroid0),dataSet)**2
    while (len(cenList)<k):
        lowestSSE=inf
        for j in range(m):
            for i in  range(len(cenList)):
                ptsInCurrCluster=dataSet[nonzero(clusterAssment[:,0]==i)[0],:]
            #尝试划分每一簇
                centroidMat,splitClustAss=Kmeans(ptsInCurrCluster,2,distMeas)
                sseSplit=sum(splitClustAss[:,1])
                sseNoSplit=sum(clusterAssment[nonzero(clusterAssment[:,0]!=i)[0]],1)
                print(sseSplit,sseNoSplit)
                if(sseSplit+sseNoSplit)<lowestSSE:
                    bestCentToSplit=i
                    bestNewCents=centroidMat
                    bestClustAss=splitClusAss.copy()
                    lowestSSE=sseSplit+sseNoSplit
                    #更新簇分配的结果
                bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(cenList)#将划分的属于第1簇的编号变更为centList的长度，即放在最后
                bestClustAss[nonzero(bestClustAss[:,0].A==0)[0],0]=bestCentToSplit
                print("the bestCentToSplit is ")
                print(bestCentToSplit)
                print("the len of bestClustAss is %d" %(len(bestClusAss)))
                cenList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]#对应于上面的bestClustAss[:,0].A == 0，
                                                         # 因为使已经存在bestCentToSplit的编号，所以可以是直接替换
                cenList.append(bestNewCents[1, :].tolist()[0])#将新的信息添加到后面
                    #更新簇分配结果矩阵，因为bestClustAss已经经过修改，所以只要把属于第bestCentToSplit簇的信息替换掉即可
                clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return mat(cenList),clusterAssment

def biKmeans1(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    dataSet=mat(dataSet)
    clusterAssment = mat(zeros((m,2)))#创建一个簇分配结果矩阵，第0列记录输入哪一个簇，第1列记录存储误差
    #创建一个初始簇，所有样例都归为1个簇
    centroid0 = mean(dataSet,axis=0).tolist()[0]#质心
    centList = [centroid0]#用于保存质心信息
    for j in range(m):#当所有样例都归为一个簇时，clusterAssment第0列为0，第1列为质心到每个样例的距离的平方(即误差)
        clusterAssment[j,1] = distMeas(mat(centroid0),dataSet[j,:])**2
    #循环产生k个簇
    while len(centList) < k:
        lowestSSE = inf#误差无穷大，根据误差来选择划分
        for i in range(len(centList)):#对现行的簇进行处理
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]#获取属于第i类簇的所有样例
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster,2,distMeas)#对属于第i类簇的所有样例进行2分聚类
            sseSplit = sum(splitClustAss[:,1])#计算划分后的误差
            #计算划分前不属于第i类簇的样例的误差，注意是不属于
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            # print ("sseSplit, and notSplit: ", sseSplit, sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:#因为肯定需要划分的，所以选择误差下降最大的那簇
                bestCentToSplit = i#应该划分原来的哪一簇
                bestNewCents = centroidMat#划分后新的2个质点
                bestClustAss = splitClustAss.copy()#划分后的簇分配结果矩阵
                lowestSSE = sseSplit + sseNotSplit
        #更新簇类别和误差
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)#将划分的属于第1簇的编号变更为centList的长度，即放在最后
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit#将划分的属于第1簇的编号变更为原来划分的编号
        # print ('the bestCentToSplit is: ',bestCentToSplit)
        # print ('the len of bestClustAss is: ', len(bestClustAss))
        #将质心信息加入centList
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]#对应于上面的bestClustAss[:,0].A == 0，
                                                     # 因为使已经存在bestCentToSplit的编号，所以可以是直接替换
        centList.append(bestNewCents[1, :].tolist()[0])#将新的信息添加到后面
        #更新簇分配结果矩阵，因为bestClustAss已经经过修改，所以只要把属于第bestCentToSplit簇的信息替换掉即可
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return mat(centList),clusterAssment