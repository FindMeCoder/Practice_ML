import matplotlib.pyplot as plt

decisionNode=dict(boxstyle="sawtooth",fc="0.8")     #定义文本框和箭头格式
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

def plotNode(nodeTxt,centerPtr,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPtr,\
                            textcoords="axes fraction",va="center",ha="center",bbox=nodeType,\
                            arrowprops=arrow_args)    # 绘制箭头的标注

    
def createPlot1():       
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1=plt.subplot(111,frameon=False)
    plotNode('决策节点',(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode('叶节点',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
    
#构造注解树

def getNumLeafs(myTree):  #获取叶节点的数目个树的层数
    numleafs=0
    firstStr=list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in list(secondDict.keys()):
        if type(secondDict[key]).__name__=='dict':
            numleafs+=getNumLeafs(secondDict[key])
        else:
            numleafs+=1
    return numleafs

def getTreeDepth(mytree): #求树的深度
    maxdepth=0
    firstStr=list(mytree.keys())[0]
    secondDict=mytree[firstStr]
    for key in list(secondDict.keys()):
        if type(secondDict[key]).__name__=='dict':
            thisdepth=1+getTreeDepth(secondDict[key])
        else:
            thisdepth=1
        if thisdepth>maxdepth:
            maxdepth=thisdepth
    return thisdepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]


def plotMidText(centerPt,parentPt,textString):
    xMid=(parentPt[0]-centerPt[0])/2.0+centerPt[0]
    yMid=(parentPt[1]-centerPt[1])/2.0+centerPt[1]
    createPlot.ax1.text(xMid,yMid,textString,va="center", ha="center", rotation=30)
    
    
def plotTree(myTree,parentPt,nodeText):
    numleafs=getNumLeafs(myTree)  #计算宽和高
    depth=getTreeDepth(myTree)
    firstStr=list(myTree.keys())[0]
    centerPt=(plotTree.xOff+(1.0+float(numleafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(centerPt,parentPt,nodeText)
    plotNode(firstStr,centerPt,parentPt,decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff=plotTree.yOff-1.0/plotTree.totalD         #减少y偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],centerPt,str(key))
        else:
            plotTree.xOff=plotTree.xOff+1.0/plotTree.totalW
            plotNode(str(secondDict[key]),(plotTree.xOff,plotTree.yOff),centerPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),centerPt,str(key))
    plotTree.yOff=plotTree.yOff+1.0/plotTree.totalD
    
    
def createPlot(inTree):
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    axprops=dict(xticks=[],yticks=[])
    createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree))
    plotTree.xOff=-0.5/plotTree.totalW
    plotTree.yOff=1.0
    plotTree(inTree,(0.5,1.0),'')
    plt.show()
    
#测试和存储分类器

    
        
        
        
        
            
            
            
            
            
            
            
            
    
    