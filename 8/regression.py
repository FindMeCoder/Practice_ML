# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 11:17:31 2018

@author: 寻ME
"""
from numpy import *
import matplotlib.pyplot as plt
from time import sleep
import json
import urllib2


def loadDataSet(filename):
    numFeat=len(open(filename).readline().split('\t'))-1
    dataMat=[]; labelMat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=[]
        currLine=line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(currLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(currLine[-1]))
    return dataMat,labelMat

def standRegress(xArr,yArr): 
    xMat=mat(xArr);yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0.0:
        print("the matrix is singular,cannot do inverse")
        return
    ws=xTx.I*(xMat.T*yMat)
    return ws

#局部线性加权回归，解出回归系数为W(i，i)=(XtWx)-1XTWY,W是权重矩阵
    
def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat=mat(xArr);yMat=mat(yArr).T
    m=shape(xMat)[0]
    weights=mat(eye(m))
    for j in range(m):
        diffMat=testPoint-xMat[j,:]
        weights[j,j]=exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx=xMat.T*(weights*xMat)
    if linalg.det(xTx)==0.0:
        print("This matrix is cannot do inverse")
        return
    ws=xTx.I*(xMat.T*(weights*yMat))
    return testPoint*ws

def lwlrTest(testArr,xArr,yArr,k=0.003):
    m=shape(testArr)[0]
    yHat=zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    return yHat

def draw(xArr,yArr,yHat):
    xMat=mat(xArr)
    srtInd=xMat[:,1].argsort(0)
    xSort=xMat[srtInd][:,0,:]
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(xSort[:,1],yHat[srtInd])
    t,=ax.scatter(xMat[:,1].flatten().A[0],mat(yArr).T.flatten().A[0],s=2,c='red')
    plt.show()

#实例：预测鲍鱼的年龄
    
def rssError(yArr,yHatArr):
    return ((yArr-yHatArr)**2).sum()

#缩减系数来理解数据，用来处理特征比样本点还要多的情况
    
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+eye(shape(xMat)[1])*lam
    if linalg.det(denom)==0.0:
        print("this matrix is singular,connot do inverse")
        return
    ws=denom.I*(xMat.T*yMat)
    return ws

def ridgeTest(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMean=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMean)/xVar
    numTestPts=30
    wMat=zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws=ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

#前向局部回归
    
def regularize(xMat):
    inMat=xMat.copy()
    inMean=mean(inMat,0)
    inVar=var(xMat,0)
    inMat=(xMat-inMean)/inVar
    return inMat
    
def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMat=regularize(xMat)
    m,n=shape(xMat)
    returnMat=zeros((numIt,n))
    ws=zeros((n,1));wsTest=ws.copy();wsMax=ws.copy()
    for i in range(numIt):
        print(ws.T)
        lowestError=inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j]+=eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A)
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    return returnMat

#偏差和方差
    
#预测乐高玩具套装的价格
    
def searchForest(retX,retY,setNum,yr,numPce,oriPrc):
    sleep(10)
    myAPIstr = 'AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY'
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?\
    key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)
    pg = urllib2.urlopen(searchURL) 
    retDict=json.loads(pg.read())
    for i in range(len(retDict('items'))):
        try:
            currItem=retDict['items'][i]
            if currItem['product']['condition']=='new':
                newFlag=1
            else:
                newFlag=0
            listOfInv=currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice=item['price']
                if sellingPrice>oriPrc*0.5:
                    print("%d%t%d%t%d%t%f%t%f"(yr,numPce,newFlag,origPce))
                    retX.append([yr,numPce,newFlag,origPce])
                    ret.append(sellingPrice)
        except:
            print("probelm with item %d"%i)
            
            
def setDataCollect(retX,retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)
    
    
#交叉验证岭回归测试
    

def crossValidation(xArr,yArr,numVal=10):
    m = len(yArr)                           
    indexList = range(m)
    errorMat = zeros((numVal,30))#create error mat 30columns numVal rows
    for i in range(numVal):
        trainX=[]; trainY=[]
        testX = []; testY = []
        random.shuffle(indexList)
        for j in range(m):#create training set based on first 90% of values in indexList
            if j < m*0.9: 
                trainX.append(xArr[indexList[j]])
                trainY.append(yArr[indexList[j]])
            else:
                testX.append(xArr[indexList[j]])
                testY.append(yArr[indexList[j]])
        wMat = ridgeTest(trainX,trainY)    #get 30 weight vectors from ridge
        for k in range(30):#loop over all of the ridge estimates
            matTestX = mat(testX); matTrainX=mat(trainX)
            meanTrain = mean(matTrainX,0)
            varTrain = var(matTrainX,0)
            matTestX = (matTestX-meanTrain)/varTrain #regularize test with training params
            yEst = matTestX * mat(wMat[k,:]).T + mean(trainY)#test ridge results and store
            errorMat[i,k]=rssError(yEst.T.A,array(testY))
            #print errorMat[i,k]
    meanErrors = mean(errorMat,0)#calc avg performance of the different ridge weight vectors
    minMean = float(min(meanErrors))
    bestWeights = wMat[nonzero(meanErrors==minMean)]
    #can unregularize to get model
    #when we regularized we wrote Xreg = (x-meanX)/var(x)
    #we can now write in terms of x not Xreg:  x*w/var(x) - meanX/var(x) +meanY
    xMat = mat(xArr); yMat=mat(yArr).T
    meanX = mean(xMat,0); varX = var(xMat,0)
    unReg = bestWeights/varX
    print "the best model from Ridge Regression is:\n",unReg
    print "with constant term: ",-1*sum(multiply(meanX,unReg)) + mean(yMat)
    








































                    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    