# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 16:08:07 2018

@author: 寻ME
"""
#决策树进行分类的时候，将数据集切分成不能再切分为之，或者目标变量完全相同，使用贪心算法，并不能达到全局最优
#CART(classification and regression trees,分类回归树，既可以用于分类，也可以用于回归)
#使用二元切分法处理连续性变量
#使用裁剪数可防止过拟合
#引入更高级的模型树算法，与回归树的做法(在每个叶节点使用各自的均值做预测)

#9.1复杂数据的局部性建模
#使用字典存储树结构
from numpy import *

def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=list(map(float,curLine)) #将每行映射成浮点数
        dataMat.append(fltLine)
    return dataMat

class TreenNode():
    def __init__(self,feat,val,right,left):
        featuretToSplition=feat
        valueOfSplit=val
        rightBranch=right
        leftBranch=left
        
def binSplitDataSet(dataSet,featrue,value): #分别为数据集合，待切分的特征，何特征值
    dataSet=mat(dataSet)
    mat0=dataSet[nonzero(dataSet[:,featrue]>value),:][0]
    mat1=dataSet[nonzero(dataSet[:,featrue]<=value),:][0]
    return mat0,mat1

def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1])*shape(dataSet)[0]


def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):#leafType建立叶节点的函数，errType为误差计算函数，ops为包含树构建所需的其他元组
    feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
    if feat==None:
        return val
    retTree={}
    retTree['spInd']=feat
    retTree['spVal']=val
    lSet,rSet=binSplitDataSet(dataSet,feat,val)
    retTree['left']=createTree(lSet,leafType,errType,ops)
    retTree['right']=createTree(rSet,leafType,errType,ops)
    return retTree

#将CART用于回归，为构建以分段常数为叶节点的树，需要度量数据的一致性
    
#函数chooseBestSplit()使用最佳方式切分数据集何生成相应的叶节点

def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    tolS=ops[0]; tolN=ops[1] #由用户指定的参数，为容许的误差下降值何切分的最少样本数
    dataSet=mat(dataSet)
    if len(set(dataSet[:,-1].T.tolist()[0]))==1: #set具有去重的功能
    #if len(set(dataMat[:,-1].T.tolist()[0]))==1:
        return None,leafType(dataSet)
    m,n=shape(dataSet)
    S=errType(dataSet)
    bestS=inf;bestIndex=0;bestValue=0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if(shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
                continue
            newS=errType(mat0)+errType(mat1)
            if newS<bestS:
                bestIndex=featIndex
                bestValue=splitVal
                bestS=newS
    if (S-bestS)<tolS:  #如果误差减少不大则退出
        return None,leafType(dataSet)
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if(shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolS):
        return None,leafType(dataSet)
    return bestIndex,bestValue

#树剪枝，在chooseBestSplit函数中设定提前终止条件。
#有预剪枝何后剪枝两种做法
#回归剪枝函数
def isTree(obj):
    return (type(obj).__name__=='dict')

def getMean(tree):
    if isTree(tree['right']):
        tree['right']=getMean(tree['right'])
    if isTree(tree['left']):
        tree['left']=getMean(tree['left'])
    return (tree['left']+tree['right'])/2.0

def prune(tree,testData):
    if shape(testData)[0]==0:
        return getMean(tree)
    if (isTree(tree['left'])) or isTree(tree['right']):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']):
        tree['left']=prune(tree['left'],lSet)
    if isTree(tree['right']):
        tree['right']=prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2))+sum(power(rSet[:,-1]-tree['right'],2))
        treeMean=(tree['left']+tree['right'])/2.0
        errMerge=sum(power(testData[:,-1]-treeMean,2))
        if errMerge<errorNoMerge:
            print("merging")
            return treeMean
        else:
            return tree
    else:
        return tree
    
#模型树，除了把树节点设为常数值外，还有种把节点设为分段函数
#是指模型有多个线性片段构成
        
#模型树的节点生成函数
        
def linearSolve(dataSet):
    m,n=shape(dataSet)
    X=mat(ones(m,n));Y=mat(ones(m,1))
    X[:,1:n]=dataSet[:,0:n-1]
    Y=dataSet[:,-1]
    xTx=X.T*X
    if linalg.det(xTx):
        raise NameError("this matrix is singular.cannot do inverse")
    ws=xTx.I*(X.T*Y)
    return ws,X,Y

def modelLeaf(dataSet):
    ws,X,Y=linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws,X,Y=linearSolve(dataSet)
    yHat=X*ws
    return sum(power(y-yHat,2))


#比较那种模型更好可以使用corrcoef(yHat,y,rowvar=0),计算相关系数
    
def regTreeEval(model,inDat):
    return float(model)

def modelTreeEval(model,inDat):  #对叶节点数据预测
    n=shape(inDat)[1]
    X=mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

#用树回归的代码
def treeForeCast(tree,inData,modelEval=regTreeEval):
    if not isTree(tree):
        return modelEval(tree,inData)
    if inData[tree['spInd']]>tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData,modelEval)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData,modelEval)
        else:
            return modelEval(tree['right'],inData)
            
def createForeCast(tree,testData,modelEval=regTreeEval):
    m=len(testData)
    yHat=mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat

