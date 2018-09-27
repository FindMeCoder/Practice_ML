#本实例中的标签我们采用1和-1
def loadDataSet(filename):
    dataMat=[];labelMat=[]
    fr=open(filename);labelMat=[]
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):#i为alpha的下标，m是alpha数目
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):#调整大于H或者小于L的alpha值
    if aj>H:
        aj=H
    if L>aj:
        aj=L
    return aj

#简化版SMO 算法
def smoSimple(dataMatIn,classLabels,c,toler,maxIter):
    dataMatrix=mat(dataMatIn);labelMat=mat(classLabels).transpose()
    b=0;m,n=shape(dataMatrix)
    alphas=mat(zeros(m,1))
    iter=0
    while(iter<maxIter):
        alphaPairsChanged=0
        for i in range(m):
            fXi=float(multiply(alphas,LabelMat).T*\
            (dataMatrix*dataMatrix[i,:].T))+b
            Ei=fXi-float(labelMat[i])
            

















