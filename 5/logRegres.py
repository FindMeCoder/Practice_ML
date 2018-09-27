# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:42:26 2018

@author: 寻ME
"""
from numpy import *

def loadSet():
    dataMat=[];labelMat=[]
    fr=open('testset.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn,classLabels):
    dataMatrix=mat(dataMatIn)
    labelMat=mat(classLabels).transpose()
    m,n=shape(dataMatrix)
    alpha=0.001;maxCycles=500
    weights=ones((n,1))
    for k in range(maxCycles):         # loss=(Xw-y)(Xw=y)T求导的结果
        h=sigmoid(dataMatrix*weights)
        err=(labelMat-h)
        weights=weights+alpha*dataMatrix.transpose()*err
    return weights

#画出数据集和Logistic回归礼盒直线的函数
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadSet()
    dataArr=array(dataMat)
    n=shape(dataArr)[0]
    xcord1=[];ycord1=[]
    xcord2=[];ycord2=[]
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x=arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2] #最佳拟合直线
    ax.plot(x,y)
    plt.xlabel('X1');plt.ylabel('Y1')
    plt.show()
    
 #getA()将weights矩阵转换为数组，getA()函数与mat()函数的功能相反
 #修改训练算法，变为随机梯度下降
 
 
def stocGradAscent0(dataMatrix,classLabel):
     m,n=shape(dataMatrix)
     alpha=0.0001
     weights=ones(n)*1.0
     for i in range(m):
         h=sigmoid(sum(dataMatrix[i]*weights))
         err=classLabel[i]-h
         weights=weights+ err *alpha *dataMatrix[i] #优化函数求导得到
     return weights
 
#改进的随机梯度上升算法
def stocGradAscent2(dataMatrix,classLabels,numIter=150):
     m,n=shape(dataMatrix)
     weights=ones(n)
     for j in range(numIter):
         dataIndex=list(range(m))
         for i in range(m):
             alpha=4/(1.0+i+j)+0.0001   #类似于模拟退火算法，永远不会为0
             randIndex=int(random.uniform(0,len(dataIndex)))  #随机选取更新
             h=sigmoid(sum(dataMatrix[i]*weights))
             error=classLabels[randIndex]-h
             weights=weights+alpha*error*dataMatrix[randIndex]
             del(dataIndex[randIndex])
     return weights
 
 
#从疝气病预测病马的死亡率
def classifyVector(inX,weights):
    prob=sigmoid(sum(inX*weights))
    if prob>0.5:
        return 1.0
    else:
        return 0.0
    
def colicTest():
    frTrain=open('horseColicTraining.txt')
    frTest=open('horseColicTest.txt')
    trainingSet=[];trainingLabels=[]
    for line in frTrain.readlines():
        currLine=line.strip().split('\t')
       # print(currLine)
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights=stocGradAscent2(array(trainingSet),trainingLabels,1000)
    #print(trainWeights)
    errcount=0;numTestVec=0.0
    for line in frTest.readlines():
        numTestVec+=1.0
        currLine=line.strip().split('\t')
        #print(currLine)
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        #print(currLine[21])
        if int(classifyVector(array(lineArr),trainWeights))!=int(float(currLine[21])):
            errcount+=1
    errRate=float(errcount)/numTestVec
    print('the error rate is :%f' %errRate)
    return errRate




def multiTest():
    numTest=10;errSum=0.0
    for k in range(numTest):
        errSum+=colicTest()
    print('after %d iterations the average error rate is: %f'%(numTest,float(errSum)/float(numTest)))
    
    
















    


























































       
        

