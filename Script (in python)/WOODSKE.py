import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial import distance
import time
NAME = 'HS'
print(NAME)
ORDATA = np.loadtxt('...\\'+str(NAME)+'-SIWOOD.csv', delimiter=',', usecols=(0, 1, 2)) # input woody point clouds (txt/csv)
NUM = ORDATA.shape[0]
def TDT(TT):
    X = np.cov(TT.T)
    eigenvalue, eigvector = np.linalg.eig(X)
    BOB = np.argsort(eigenvalue)
    eigenvalue = np.real(eigenvalue[BOB])
    T1 = eigenvalue[2] / np.sum(eigenvalue)
    T2 = eigenvalue[1] / np.sum(eigenvalue)
    return np.round(T1,2),np.round(T2,2)
ZZC = 0
T = 1
TLSM = ORDATA

start = time.perf_counter()
print('Step One')
while T<4:
    if T==1:
        KDT = cKDTree(TLSM)
    else:
        KDT = cKDTree(TLSM[:,:3])
    t=0
    TLSA = []
    for p in TLSM:
        if t % 10000 == 0 and t > 0:
            print(">>>StepOne>>>" + str(T) + ">>>Process>>>" + str(t))
        if T==1:
            U = KDT.query(p[:3], 2)[0][1]
            KOK = np.sqrt(U)
            Pnum = KDT.query_ball_point(p[:3], KOK)
            PSET = np.resize(TLSM[Pnum], (len(Pnum), int(TLSM.shape[1])))
            Xrange = max(PSET[:, 0]) - min(PSET[:, 0])
            Yrange = max(PSET[:, 1]) - min(PSET[:, 1])
            Zrange = max(PSET[:, 2]) - min(PSET[:, 2])
            h = np.sqrt(Xrange * Xrange + Yrange * Yrange + Zrange * Zrange)
            vmean = np.round(h / 2, 2)
        else:
            vmean = float(p[-1])
        index = KDT.query_ball_point(p[:3], vmean)
        if len(index) >= 3 and T == 1:
            BALL = np.resize(TLSM[index], (int(len(index)), int(TLSM.shape[1])))
            VV1, VV2 = TDT(BALL[:,:3])
            TLSA.append([float(p[0]), float(p[1]), float(p[2]), VV1, VV2, vmean])
        if len(index) >= 3 and T > 1:
            BALL = np.resize(TLSM[index], (int(len(index)), int(TLSM.shape[1])))
            VV1, VV2 = TDT(BALL[:, :3])
            Xc = float(np.mean(BALL[:, 0]))
            Yc = float(np.mean(BALL[:, 1]))
            Zc = float(np.mean(BALL[:, 2]))
            TLSA.append([Xc, Yc, Zc, VV1, VV2, np.round((2 * vmean * (1 - VV1 + VV2)), 2)])
        if len(index) < 3:
            TLSA.append([float(p[0]), float(p[1]), float(p[2]), 1, 0, 0])
        t += 1
    TLSQ = np.resize(np.array(TLSA),(int(len(TLSA)), 6))
    YY, Yindex = np.unique(TLSQ[:, :3], return_index=True, axis=0)
    TLSAA = np.resize(TLSQ[Yindex],(int(len(Yindex)), 6))
    QQQ = isinstance(TLSAA[0][0], float)
    if QQQ == True:
        EDT = cKDTree(TLSAA[:, :3])
        OOE = TLSAA
        for i in TLSAA:
            e = EDT.query_ball_point(i[:3], i[-1])
            if len(e)>5:
                A = np.resize(OOE[e], (int(len(e)), 6))
            else:
                e = EDT.query(i[:3], 6)[1][1:]
            A = np.resize(OOE[e], (int(len(e)), 6))
            i[3] = np.round(np.median(A[:, 3]), 2)
            i[4] = np.round(np.median(A[:, 4]), 2)
            i[-1] = np.round(np.median(A[:, -1]), 2)
        TLSM = np.resize(TLSAA[:, [0, 1, 2, -1]], (int(TLSAA.shape[0]), 4))
        T += 1
    else:
        T = 0
del KDT,TLSA,TLSM,TLSQ

##STEP 2
print('Step Two')
ORKDT = cKDTree(ORDATA[:,:3])
UU, index = np.unique(TLSAA[:,:3], return_index=True, axis=0)
TLSAA = TLSAA[index]
KDT = cKDTree(TLSAA[:, :3])
t = 0
for p in TLSAA:
    if t % 10000 == 0 and t > 0:
        print(">>>Process>>>" + str(t))
    indexA = KDT.query_ball_point(p[:3], p[-1]*2)
    if len(indexA)>1:
        index = KDT.query(p[:3], len(indexA))[1][-1]
        if TLSAA[index][4]>0.2:
            MP = (TLSAA[index] + p) / 2
            p[0] = MP[0]
            p[1] = MP[1]
            p[2] = MP[2]
    t += 1
for t in TLSAA:
    t[-1] = round(ORKDT.query(t[:3], 1)[0], 3)

#################3
print('Step Three')
UU, index = np.unique(TLSAA[:,:3], return_index=True, axis=0)
TLSB = TLSAA[index]
T2T = 0
T2 = 1
T1 = 0
while T1<T2:
   T2T += 1
   # print(T2T, T1, T2, TLSB.shape[0])
   T1 = T2
   KDT = cKDTree(TLSB[:, :3])
   XXUU = TLSB
   BS = np.zeros((int(TLSB.shape[0]), 1))
   TLSB = np.column_stack((TLSB, BS))
   for s in TLSB:
       s[-1] = int(ORKDT.query(s[:3], 1)[1])
   SKE = []
   DEL = []
   for t in TLSB:
       Mindex = KDT.query_ball_point(t[:3], t[-2])
       if len(Mindex) and t[4]>0.2:
           BXA = np.resize(TLSB[Mindex], (int(len(Mindex)), int(TLSB.shape[1])))
           OPOI = ORDATA[int(t[-1])]
           DSA = np.round(np.linalg.norm(BXA[:, :3] - OPOI[:3], axis=1), 3)
           MAXindex = np.argmax(DSA)
           POP = BXA[int(MAXindex)]
           DSB = np.round(np.linalg.norm(BXA[:, :3] - t[:3], axis=1), 3)
           if POP[-1] == t[-1] or POP[-2] > t[-2]:
               t = POP
               t[-1] = 0
           else:
               EUU = np.argwhere(DSA - DSB > 0)
               if len(EUU):
                   EAA = np.resize(BXA[EUU], (int(len(EUU)), int(TLSB.shape[1])))
                   t = np.mean(EAA, axis=0)
                   t[-2] = round(ORKDT.query(t[:3], 1)[0], 3)
                   t[-1] = 1
               else:
                   t[-1] = 0
           SKE.append(t)
       if t[4]<=0.2:
           t[-1] = 1
           SKE.append(t)
   SKEB = np.resize(np.array(SKE), (int(len(SKE)), int(TLSB.shape[1])))
   T2 = np.sum(SKEB[:, -1])
   JJJ,IIU = np.unique(SKEB[:,:3], axis=0, return_index=True)
   SKEB = SKEB[IIU]
   TLSB = SKEB[:, :-1]
Fidnex = np.argwhere(SKEB[:,-1]==1)
SKEG = np.resize(SKEB[Fidnex],(len(Fidnex), int(SKEB.shape[1])))
COARSKE = SKEG[:,:-1]
del TLSB,SKEG,SKEB,KDT

#################4
print('Step Four')
FKDT = cKDTree(COARSKE[:, :3])
WKDT = cKDTree(ORDATA[:, :3])
SKEVV = []
for s in COARSKE:
     s[-1] = np.sum(FKDT.query(s[:3], 5)[0])
for s in COARSKE:
     Mindex = FKDT.query(s[:3], 1000)[1]
     BXA = np.resize(COARSKE[Mindex], (int(len(Mindex)), int(COARSKE.shape[1])))
     TPP = np.argmin(BXA[:,-1])
     THT = np.percentile(BXA[:,-1], [25, 50, 75])
     TTR = THT[2] + (THT[2] - THT[0]) * 3
     if s[-1]>TTR:
          SKEVV.append(BXA[int(TPP)])
     else:
          SKEVV.append(s)
SKEC = np.resize(np.array(SKEVV), (int(len(SKEVV)), int(COARSKE.shape[1])))
SKERESULT = np.unique(SKEC, axis=0)
end = time.perf_counter()
print(end)
print('time cost>>>>',end-start)
np.savetxt('...\\'+str(NAME)+'-SIMUSKE.csv', SKERESULT[:,:3], fmt='%s', delimiter=',', newline='\n')
