# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 17:39:20 2018

@author: 寻ME
"""


#Fp-Growth算法基于Apriori构建，但完成相同任务时采用了不同的技术，将数据集存储在一个特定的数据结构称为Fp树中
#可以利用FP树进行快速挖掘数据对或者平凡项，在一起出现的元素项的集合FP树
#Fp-Growth算法只会扫描两次数据集判断给定模式是否平凡，当处理大的数据集时，会产生较大问题。
#发现频繁集的过程如下：
#（1）构建FP树
#（2）从Fp树中挖掘频繁集

 #为了构建Fp树，利用它挖掘频繁项集，需要对原始项目集扫描两边，第一次对元素项出现次数计数，第二次只考虑那些频繁元素
 #为了构建一棵树，我们使用容器来保存它

class treeNode:
     def __init__(self,nameValue,numOccur,parentNode):
         self.name=nameValue
         self.count=numOccur
         self.nodeLink=None
         self.parent=parentNode
         self.children={}
         
     def inc(self,numOccur):
         self.count+=numOccur
         
     def disp(self,ind=1):
         print(" "*ind,self.name," ",self.count)
         for child in self.children.values():
             child.disp(ind+1)
             
def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict={}
    for trans in dataSet:
        retDict[frozenset(trans)]=1
    
    return retDict

#构建FP树，FP构建函数
             
def createTree(dataSet,minSup=1):
    headTable={}
    for trans in dataSet:
        #print("trans = ",trans)
        for item in trans:
            #print("dataSet[trans] = ",dataSet[trans])
            headTable[item]=headTable.get(item,0)+dataSet[trans]
    
    for k in list(headTable.keys()):
        if headTable[k]<minSup:
            del(headTable[k])
            
    freqItemSet=set(headTable.keys())
    if len(freqItemSet)==0: #为元素的数目
        return None,None
    
    for k in headTable:
        headTable[k]=[headTable[k],None]#对表进行扩展可以保存技术值以及指向每种类型的第一个元素项的指针
    
    retTree=treeNode('Null Set',1,None) #只包含空集的根节点
    
    for tranSet,count in dataSet.items():
        localID={}
       #print("tranSet=",tranSet,"count=",count)
        for item in tranSet:
            if item in freqItemSet:
                localID[item]=headTable[item][0]
        if len(localID)>0:
            #print("sorted(localID.items(),key=lambda p:p[1],reverse=True) = ",sorted(localID.items(),\
            #                    key=lambda p:p[1],reverse=True))#按出现的频度排序
            orderItems=[v[0] for v in sorted(localID.items(),key=lambda p:p[1],reverse=True)]
           # print("orderItems=",orderItems)
            updateTree(orderItems,retTree,headTable,count)
    return retTree,headTable


def updateTree(items,inTree,headTable,count):
   # print("items=",items,"inTree=",inTree,"headTbale=",headTable,"count=",count)
    if items[0] in inTree.children:#测试是否为子节点存在，如果存在，更新计数值
        inTree.children[items[0]].inc(count)
    else:#否则创建一个新的treeNode子节点加入树中
        inTree.children[items[0]]=treeNode(items[0],count,inTree)
        if headTable[items[0]][1]==None:
            headTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headTable[items[0]][1],inTree.children[items[0]])
    if len(items)>1:
        updateTree(items[1::],inTree.children[items[0]],headTable,count)#对剩余元素调用updateTree函数
        

def updateHeader(nodeToTest,targetNode):#确保节点链接指向树中元素项的每一个实例
    while(nodeToTest.nodeLink!=None):
        nodeToTest=nodeToTest.nodeLink
    nodeToTest.nodeLink=targetNode

#从一颗FP树中挖掘频繁集，思路与Apriori算法类似
    #（1）获取条件模式基
    #（2）利用条件模式基，构建一棵条件FP树
    #（3）迭代重复，直到树包含一个元素即可
#条件模式是查找元素项为结尾的路径集合，每条路径是一个前缀路径
    #每条前缀路径与一个计数值相关，给了每条路径r的数目，列出了每一个频繁项的前缀路径
def ascendTree(leafNode,prefixPath):
    if leafNode.parent!=None:
        prefixNode.append(leafNode.node)
        ascendTree(leafNode,prefixPath)
        
def findPrefixPath(basePat,treeNode):
    conPats={}
    while treeNode!=None:
        prefixPath=[]
        ascendTree(treeNode,prefixPath)
        if len(prefixPath)>1:
            conPats[frozenset(prefixPath[1:])]=treeNode.count
        treeNode=treeNode.nodeLink
    return conPats
#创建条件树，前缀路径以及条件基的过程为，对头指针中的元素项按照出现频率进行排序，对一个频繁项添加到频繁项集合中，该条件基
    #被当成一个新的数据集被传给CreatTree()函数，确保他可以用于被重构条件树。
def minTree(inTree,headTable,minSup,preFix,freqItemList):
    bigL=[v[0] for v in sorted(headTable.items(),key=lambda p:p[1])]
    
    for basePat in bigL:
        newFreqSet=preFix.copy()
        hewFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPatBases=findPreFixPath(basePat,headTable[basePat][1])
        myCondTree,myHead=createTree(condPatBases,minSup)
        
        if myHead!=None:
            minTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
    
    
    
    
    
    
    
    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
        
        