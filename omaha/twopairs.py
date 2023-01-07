import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks

def twopairs(a,board,level=0):
    if board.paired=='unpaired':
        rank = board.rank # unique rank
        if level==0:
            level=10
        
        def f(f1,f2):
            return filt1(a,rank[f1]) & filt1(a,rank[f2])
 
        if len(rank)==3:
            logicals=np.empty((0,a.shape[0]),dtype=bool)
            for i in [(0,1),(0,2),(1,2)][:level]:
                logicals=np.vstack((logicals,f(i[0],i[1])))
            return np.any(logicals,axis=0)

        if len(rank)==4:
            logicals=np.empty((0,a.shape[0]),dtype=bool)
            for i in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)][:level]:
                logicals=np.vstack((logicals,f(i[0],i[1])))
            return np.any(logicals,axis=0)

        else:
            logicals=np.empty((0,a.shape[0]),dtype=bool)
            for i in [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)][:level]:
                logicals=np.vstack((logicals,f(i[0],i[1])))
            return np.any(logicals,axis=0)




    return np.full(a.shape[0], False)   