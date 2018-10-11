# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 10:18:24 2018

@author: 寻ME
"""

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def CreateC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset,C1))

def scanD(D,Ck,minSupport):  #包含支持度的字典以备后用 
    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can]=1
                else:
                    ssCnt[can]+=1
    numItems=float(len(D))
    retList=[]
    supportData={}
    for key in ssCnt:
        support=ssCnt[key]/numItems
        if support>=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData

#组织完整的Apriori算法
    
def AprioriGen(Lk,k): #创建Ck,Lk是频繁项与项集元素个数
    retList=[]
    lenLk=len(Lk)
    #print(Lk)
    for i in range(lenLk):  
        for j in range(i+1,lenLk): #排序后只要前边k-2个相同,减少比较次数
            L1=list(Lk[i])[:k-2]
            L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList

def apriori(dataSet,minSupport=0.5):
    C1=CreateC1(dataSet)
    D=list(map(set,dataSet))
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while(len(L[k-2])>0):
        Ck=AprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1
    return L,supportData

#从频繁项集中挖掘关联规则
#量化方法为可信度P->H定义为support(P|H)/support(H),只需要对支持度做一次运算
    
#类似于Apriori算法，从一个频繁项集开始，创建一个规则列表，右部只包含一个元素，然后对这些规则进行测试，接下来合并剩余规则
    
def generateRules(L,supportData,minConf):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item] for item in freqSet)]
            if (i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList

#找到满足最小可行度的要求
def calcConf(freqSet,H,supportData,minConf=0.7):
    prunedH=[]
    for conseq in H:
        conf=supportData[freqSet]/supportData(freqSet-conseq)
        if conf>minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

def ruleFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m=len(H[0])
    if (len(freqSet)>m+1):
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if (len(Hmp1)>1):
            ruleFromConseq(freqSet,Hmp1,supportData,br1,minConf)
            
            






































        
    
    
    
    
    
    
    
    
    
    
    
    
    
            
















