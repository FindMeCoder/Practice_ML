#本实例中的标签我们采用1和-1
from numpy import *
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
def smoSimple(dataMatIn,classLabels,C,toler,maxIter):   #toler为容错率
    dataMatrix=mat(dataMatIn);labelMat=mat(classLabels).transpose()
    b=0;m,n=shape(dataMatrix)
    alphas=mat(zeros((m,1)))
    iter=0
    while(iter<maxIter):
        alphaPairChanged=0
        for i in range(m):
            fXi=float(multiply(alphas,labelMat).T*\
             (dataMatrix*dataMatrix[i,:].T))+b
            Ei=fXi-float(labelMat[i])
            if ((labelMat[i]*Ei<-toler) and (alphas[i]<C)) or (\
               (labelMat[i]*Ei>toler) and (alphas[i]>0)):
                j=selectJrand(i,m)
                fXj=float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                Ej=fXj-float(labelMat[j])
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                if (labelMat[i]!=labelMat[j]): #保证alpha在0到C之间
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[i]+alphas[j])
                if L==H: 
                    print("L==H")
                    continue
                eta =2.0* dataMatrix[i,:]*dataMatrix[j,:].T -\
                dataMatrix[i,:]*dataMatrix[i,:].T-\
                dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >=0 :
                    print("eta>=0")
                    continue
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                if (abs(alphas[j] -alphaJold)<0.00001):
                    print("j not moving enough")
                    continue
                alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*\
                dataMatrix[i,:]*dataMatrix[i,:].T-\
                labelMat[j]*(alphas[j]-alphaJold)*(dataMatrix[i,:]*dataMatrix[j,:].T)
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T-\
                labelMat[j]*(alphas[j]-alphaJold)*\
                dataMatrix[j,:]*dataMatrix[j,:].T
                if (0<alphas[i]) and (C>alphas[i]):
                    b=b1
                elif (0<alphas[j]) and (C>alphas[j]):
                    b=b2
                else:
                    b=(b1+b2)/2.0
                alphaPairChanged+=1
                print("iter: %d i:%d ,pair changed %d"%(iter,i,alphaPairChanged))
        if (alphaPairChanged==0): iter+=1
        else:iter=0
        print("iteration number:%d"%iter)
    return b,alphas
            
#利用完整SMO算法进行加速
    















