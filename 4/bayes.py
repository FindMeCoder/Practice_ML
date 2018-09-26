# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#使用朴素贝叶斯进行文本分类
from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1代表侮辱性言论，0为正常言论,本实例中只有两个类别0或者1
    return postingList,classVec

def createVocabList(dataset):
    vocabSet=set([])
    for document in dataset:
        vocabSet=vocabSet|set(document)   
    return list(vocabSet)   #创建两个集合的并集

def setofWord2Vec(vocabList,inputSet):#输出文档向量，输入词汇表和文档
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else: print("the word:%s is not in my vocabulary!"%word)
    return returnVec

#训练算法

def trainNB0(trainMatrix,trainCategory):  #trainMatrix文档矩阵和trainCategorx类别标签构成的向量
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    p0Num=ones(numWords);p1Num=ones(numWords)
    p0Demon=2.0;p1Demon=2.0
    for i  in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]
            p1Demon+=sum(trainMatrix[i])
        else:
            p0Num+=trainMatrix[i]
            p0Demon+=sum(trainMatrix[i])
    p1Vect=log(p1Num/p1Demon)
    p0Vect=log(p0Num/p0Demon)
    return p0Vect,p1Vect,pAbusive
#测试文档分类时，由于可能出现多个0连乘，为避免这种影响，我们可以将所有的词出现次数为1，将分母初始化为2
#但是多个小数连乘时，也会出现结果下溢为0，可以对乘积取自然对数

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
    
def testNB():
    postingList,classVec=loadDataSet()
    vocabList=createVocabList(postingList)
    trainMat=[]
    for postdoc in postingList:
        trainMat.append(setofWord2Vec(vocabList,postdoc))
    p0v,p1v,pAb=trainNB0(array(trainMat),array(classVec))
    testEntry=['love','my','dalmation']
    thisDoc=array(setofWord2Vec(vocabList,testEntry))
    print('classfied as %d',classifyNB(thisDoc,p0v,p1v,pAb))
    testEntry=['stupid','garbage']
    thisDoc=array(setofWord2Vec(vocabList,testEntry))
    print('classfied as %d',classifyNB(thisDoc,p0v,p1v,pAb))
    
#文档词袋模型，词集模型中，每个词次数只能为1，词袋模型中可以出现多次
def bagofWord2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec

#使用朴素贝叶斯对电子邮件进行分类
#import re
#mySent='this is best book on M.L.' 
#regEx=re.compile('\\W*')
#listofToken=regEx.split(mySent)
    
#文本解析及完整的垃圾邮件测试函数
def textParse(bigString):
    import re
    listofToken=re.split(r'\W*',bigString)
    return [tok.lower() for tok in listofToken if len(tok)>2]

def spamTest():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        wordList=textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    trainingSet=list(range(50));testSet=[]
    for i in range(10):             #随机构建训练集
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClass=[]
    for docIndex in trainingSet:
        trainMat.append(setofWord2Vec(vocabList,docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0v,p1v,pSpam=trainNB0(array(trainMat),array(trainClass))
    errcount=0
    for docIndex in testSet:
        wordVector=setofWord2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0v,p1v,pSpam)!=classList[docIndex]:
            errcount+=1
    print('the error rate is : %f',float(errcount)/len(testSet))
    
    
    
def calMostFreq(vocabList,fullText):    #计算出现频率
    import operator
    freqDict={}
    for token in vocabList:
        freqDict[token]=fullText.count[token]
    sortedFreq=sorted(freqDict.items(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq

def localWords(feed1,feed0):
    import feedparser
    docList=[];classList=[];fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    top30Words=calMostFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pair[0])
    trainingSet=list(range(2*minLen));testSet=[]
    for i in range(20):             #随机构建训练集
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClass=[]
    for docIndex in trainingSet:
        trainMat.append(bagofWord2VecMN(vocabList,docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0v,p1v,pSpam=trainNB0(array(trainMat),array(trainClass))
    errcount=0
    for docIndex in testSet:
        wordVector=bagofWord2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0v,p1v,pSpam)!=classList[docIndex]:
            errcount+=1
    print('the error rate is : %f',float(errcount)/len(testSet))
    return vocabList,p0v,p1v
    

 ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
 sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
        







    
    
    



    




            











    

















