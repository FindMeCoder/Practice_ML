# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 21:38:26 2018

@author: 寻ME
"""
#训练算法，AdaBoost是adaptive boosting的缩写

from numpy import *

def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

#单层决策树生成函数
def stumpClassify(dataMatrix,dimen,threshVal,thershIneq):
    retArray=ones((shape(dataMatrix)[0],1))
    if thershIneq=='lt':
        retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray

def buildStump(dataArr,classLabels,D):
    dataMatrix=mat(dataArr);labelMat=mat(classLabels).T
    m,n=shape(dataMatrix)
    numSteps=10.0; bestStump={};bestClasEst=mat(zeros((m,1)))
    minError=inf
    for i in range(n):
        rangeMin=dataMatrix[:,i].min();rangeMax=dataMatrix[:,i].max()
        stepSize=(rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt','gt']:
                threshVal=(rangeMin+float(j)*stepSize)
                predictedVals=stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr=mat(ones((m,1)))
                errArr[predictedVals==labelMat]=0
                weightedError=D.T*errArr
                print("split: dim %d ,thresh %.2f ,thresh inequal %s,\
                      the weighted error is %d"\
                      %(i,threshVal,inequal,weightedError))
                if weightedError<minError:
                    minError=weightedError
                    bestClasEst=predictedVals.copy()
                    bestStump['dim']=i
                    bestStump['thresh']=threshVal
                    bestStump['ineq']=inequal
    return bestStump,minError,bestClasEst

#完整的AdaBoost算法的实现
#每次迭代利用buildStump函数找到最佳的单层决策树，加入到单层决策树数组
#计算alpha，更新权重向量，更新累计类别估计值

#基于单层决策树的Adaboost训练过程
    
def adaBoostTrainDS(dataArr,classLabels,numIt=40): #使用单层决策树构建
    weakClassArr=[]
    m=shape(dataArr)[0]
    D=mat((ones((m,1))/m)) #初始权重
    aggClassEst=mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst=buildStump(dataArr,classLabels,D)
        print("D.T",D.T)
        alpha=float(0.5*log((1-error)/max(error,1e-16)))
        bestStump['alpha']=alpha
        weakClassArr.append(bestStump)
        print("classEst:",classEst.T)
        expon=multiply(-1*alpha*mat(classLabels).T,classEst)
        D=multiply(D,exp(expon))
        D=D/D.sum()
        aggClassEst+=alpha*classEst  #计算加权后的类别
        print("aggClassEst:",aggClassEst.T)
        aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
        errorRate=aggErrors.sum()/m
        print("total error rate: is %d"%(errorRate))
        if errorRate==0.0:
            break
    return weakClassArr,aggClassEst

#测试算法，基于AdaBoost的分类
    
def adaClassify(datToClass,classifierArr):
    dataMatrix=mat(datToClass)
    m=shape(dataMatrix)[0]
    aggClassEst=mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst=stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],\
                               classifierArr[i]['ineq'])
        aggClassEst+=classifierArr[i]['alpha']*classEst
       # print(aggClassEst)
    return sign(aggClassEst)

#在一个数据集上使用AdaBoost
    
def loadDataSet(fileName):
    numFeat=len(open(fileName).readline().split('\t'))
    dataMat=[];labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=[]
        currLine=line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(currLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(currLine[-1]))
    return dataMat,labelMat

#其他分类性能度量指标：正确率召回率以及roc曲线
    
#混淆矩阵
#正确率=TP/(TP+FP) 召回率表示预测正确的正例占所有正例的比例TP/(TP+FN)
#模型应该保持正确率和召回率尽可能的大
#另一个度量分类中的非均衡的工具是ROC曲线，包括两条曲线，横轴为假阳率，横轴为真正率
    
#roc曲线的绘制及AUC计算函数
#predStrength为分类器预测强度
    
def plotROC(predStrengths,classLabels):
    import matplotlib.pyplot as plt
    cur=(1.0,1.0)
    ySum=0.0
    numPosClas=sum(array(classLabels)==1.0)
    xStep=1/float(len(classLabels)-numPosClas);yStep=1/float(numPosClas);
    sortedIndicies=predStrengths.argsort()
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index]==1.0:
            delX=0;delY=yStep;
        else:
            delX=xStep;delY=0;
            ySum+=cur[1]
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY],c='b')
        cur=(cur[0]-delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Postive Rate')
    plt.title('ROC curve for AdaBoost Horse Detection System')
    ax.axis([0,1,0,1])
    plt.show()
    print("The Area under the Curve is %f"%(ySum*xStep))