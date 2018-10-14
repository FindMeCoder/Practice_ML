# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 19:59:16 2018

@author: 寻ME
"""
#利用SVD简化数据

#从信息中提取所需信息的可以借助奇异值分解来实现（SVD）。常通过隐性语义索引应用于搜索何信息检索领域，然后再介绍SVD
#在推荐系统领域的应用。
#SVD的另一个应用就是推荐系统，简单版本的推荐系统能够计算项与人之间的相似度，更为先进的方法是构建一个主题空间，在改空间下计算相速度

#奇异值分解
# （1）.优点：建华数据，去除噪声，提高算法结果。
# （2）.数据的转换可能难以理解
# （3）.适用数据类型：数值型数据

#矩阵分解,对角元素为奇异值，奇异值与特征值是有关系的，是D*D的特征值得平方根，奇异值矩阵只有从大到小排列的对角元素
#在科学与工程中，一个普遍事实是，在奇异值的数目（r）之后，其他奇异值都置为0，意为这数据集中只有r个特征，其他特征均为
#噪声或者冗余特征
#利用Python实现SVD

from numpy import *
U,Sigma,VT=linalg.svd([[1,1],[7,7]])

def loadExData():
    return[[0, 0, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]
    
def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]


#基于协同过滤的推荐引擎
#协同过滤是通过用户与其他用户的数据实现对比来实现推荐的。当采用矩阵表示用户无物品的关系时，可以通过计算相似度
#来预测用户的喜好。
    
#相似度的计算
# 1.传统的欧氏距离，相似度=1/(1+距离)
# 2. 皮尔逊相关系数，可以用来度量向量之间的相似度，优点在于对于评级的量级并不敏感，取值范围为-1到1之间
# 3. 余弦相似度
    
from numpy import *
from numpy import linalg as la

def euclidSim(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))

def pearsSim(inA,inB):
    if len(inA):
        return 1.0
    return 0.5+0.5*corrcoef(inA,inB,rowVar=0)[0][1]

def cosSim(inA,inB):
    num=inA.T*inB
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

#基于物品的相似度还是基于用户的相似度取决于用户或者物品的数目
#推荐引擎的评价，此时我们没有预测的目标值，也没有用户的满意程度，可以采用前边使用的交叉测试的方法，举起做法是
    #把已知的评分去掉，计算预测值与实际值之间的差异，通常采用的指标是最小均方根误差（RMSE）,计算均方误差的平均值
    #然后取平方根

#实例：餐馆菜肴推荐引擎
#首先找到用户没有尝过的菜肴，然后通过SVD减少特征空间来提高推荐效果


def standEst(dataMat,user,simMeas,item): #输入为用户，物品，数据矩阵，相似度的计算方法
    n=shape(dataMat)[1]
    simTotal=0.0;ratSimTotal=0.0
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0:
            continue
        overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]#寻找与user有关的人
        if len(overLap)==0:
            similarity=0
        else:
            similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])
        simTotal+=similarity
        ratSimTotal+=similarity*userRating
    if simTotal==0:
        return 0
    else:
        return ratSimTotal/simTotal
    

def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=svdEst):
    unratedItems=nonzero(dataMat[user,:].A==0)[1]
    if len(unratedItems)==0:
        return "you rated everything"
    itemScores=[]
    for item in unratedItems:
        estimatedScore=estMethod(dataMat,user,simMeas,item)
        itemScores.append((item,estimatedScore))
    return sorted(itemScores,key=lambda jj:jj[1],reverse=True)[:N]

#使用SVD提高推荐效果，关键是对降维后的三维空间构造一个相似度计算函数


def svdEst(dataMat,user,simMeas,item):
    n=shape(dataMat)[1]
    simTotal=0.0;ratSimTotal=0.0
    U,Sigma,VT=la.svd(dataMat)
    Sig4=mat(eye(4)*Sigma[:4])
    xformedItems=dataMat.T*U[:,:4]*Sig4.I
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0 or j==item:
            continue
        similarity=simMeas(xformedItems[item,:].T,xformedItems[j,:].T)
        print("%d %d %f"%(item,j,similarity))
        simTotal+=similarity
        ratSimTotal+=similarity*userRating
    if simTotal==0:
        return 0
    else:
        return ratSimTotal/simTotal
        















    
    
    
    
    































    

