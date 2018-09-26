from math import log
import operator
import matplotlib.pyplot as plt

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortclassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortclassCount[0][0]


def createDataSet():
    dataset=[['1','1','1','yes'],
             ['1','1','2','yes'],
             ['1','0','3','no'],
             ['0','1','2','no'],
             ['0','1','1','no']]
    labels=['no surfacing','flippers']
    return dataset,labels

def calcshanonEnt(dataset):             #计算香农熵
    numEntries=len(dataset)
    labelcount={}
    for featvec in dataset:
        currentlabel=featvec[-1]
        if currentlabel not in labelcount.keys():
            labelcount[currentlabel]=0
        labelcount[currentlabel]=1
    shannonEnt=0.0
    for key in  labelcount:
        prob=float(labelcount[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataset,axis,value):       #按照给定数据划分数据集
    retDataset=[]
    for featvec in dataset:
        #print ('%d  %d'%(value,int(featvec[axis])))
        if (featvec[axis])==(value):
            reducedfeatvec=featvec[:axis]
           # print(featvec)
            reducedfeatvec.extend(featvec[axis+1:])
           # print(reducedfeatvec)
            retDataset.append(reducedfeatvec)
    return retDataset

def chooseBestFeatureToSplit(dataset):
    numFeatures=len(dataset[0])-1
    baseEntropy=calcshanonEnt(dataset)
    bestInfoGain=0.0;bestFeature=-1
    for i in range(numFeatures):
        feaList=[example[i] for example in dataset]
        uniqueVals=set(feaList)      
        newEntropy=0.0
        for value in uniqueVals:
            subdataset=splitDataSet(dataset,i,value)
            prob=len(subdataset)/float(len(dataset))
            newEntropy+=prob*calcshanonEnt(subdataset)
        infoGain=baseEntropy-newEntropy
        #print(infoGain)
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

#递归构建决策树
#结束的条件是遍历完所有的划分数据集的属性，或者每个分支下的所有实例有相同的类别
def createTree(dataset,labels):
    classList=[example[-1] for example in dataset]
    if classList.count(classList[0])==len(classList):#类别完全相同
        return classList[0]
    if len(dataset[0])==1: #使用完了所有的特征，任然不能分类
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataset)
    bestFeatlabel=labels[bestFeat]
    myTree={bestFeatlabel:{}}   #python字典树存储树结构
    del(labels[bestFeat])  #del作用在对象上
    featvalues=[example[bestFeat] for example in dataset]
    uniquevals=set(featvalues)
    for value in uniquevals:
        sublabels=labels[:]
        #print(sublabels)
        myTree[bestFeatlabel][value]=createTree(splitDataSet(dataset,bestFeat,value),sublabels)
    return myTree

#在Python中使用matplotlib注解绘制树形图

#测试分类器
def classify(inputTree,featLabels,testVec):
    firstStr=list(inputTree.keys())[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    for key in list(secondDict.keys()):
        if testVec[featIndex]==key:  #测试集子节点的值与测试值对比
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel

#决策树的存储，为了提高计算速度，每次执行分类时构造好决策树，分类时调用，使用pickle来持久化决策树
def storeTree(inputTree,filename):
    import pickle
    fw=open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr=open(filename)
    return pickle.load(fr)
    


    






    







    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    

 






    