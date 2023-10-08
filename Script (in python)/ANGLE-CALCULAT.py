import numpy as np
from scipy.spatial import cKDTree
Name = 'AC'
SKE = np.loadtxt('...\\'+str(Name)+'-SIMUSKE.csv', delimiter=',', usecols=(0,1,2)) # input the extracted skeleton (txt/csv)
ORDATA = np.loadtxt('...\\'+str(Name)+'-SIWOOD.csv', delimiter=',') # input woody point clouds (txt/csv)
SEKDT = cKDTree(SKE[:,:3])
def TDT(TT):
    X = np.cov(TT.T)
    eigenvalue, eigvector = np.linalg.eig(X)
    return eigvector[-1]
AAN = np.zeros((int(ORDATA.shape[0]),1))
t = 0
for b in ORDATA:
    index = SEKDT.query(b, 2)[1][1]
    AAN[t] = index
    t += 1
INDEXA = np.column_stack((ORDATA, AAN))
UNI = np.unique(AAN)
ANGLEA = np.zeros((int(ORDATA.shape[0]),1))
for u in UNI:
    indexs = np.argwhere(INDEXA[:,-1]==u)
    Sindex = SEKDT.query_ball_point(SKE[int(u)][:3], 0.1)
    AA = np.resize(SKE[Sindex],(3, 3))
    XR = max(AA[:, 0]) - min(AA[:, 0])
    YR = max(AA[:, 1]) - min(AA[:, 1])
    D = np.sqrt(XR ** 2 + YR ** 2)
    Z = max(AA[:, 2]) - min(AA[:, 2])
    if Z == 0:
        Angl = 0
    else:
        Angl = round(np.arctan(Z / D) * 180 / np.pi, 2)
    for i in indexs:
        ANGLEA [i] = Angl
ARResult = np.column_stack((ORDATA,ANGLEA))
SPKDT = cKDTree(ARResult[:,:-1])
for a in ARResult:
       aindex = SPKDT.query_ball_point(a[:-1], 0.1)
       kaa = np.resize(ARResult[aindex],(len(aindex), 4))
       minT = np.percentile(kaa[:,-1], 25)
       maxT = np.percentile(kaa[:,-1], 75)
       THH = (maxT - minT) / 2
       MIN = minT-1.5*THH
       MAX = maxT+1.5*THH
       if a[-1]<MIN or a[-1]>MAX:
          a[-1] = np.mean(kaa[:,-1])
np.savetxt('...\\'+str(Name)+'-ANGLE.csv', ARResult, fmt='%s', delimiter=',', newline='\n')

