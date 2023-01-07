import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks

def onepair(a,board,level=5): 
        rank = board.rankMap[0]
        rank_cnt = board.rankMap[1]

        singles = rank[rank_cnt==1] 

        if len(singles)==0:
            return np.full(a.shape[0], False)  
        
        if level ==0:
            level=5

        thesingle = singles[min(len(singles),level)-1]

        rank = rank[rank<=thesingle]
        pockets = rank_list[(np.invert(np.isin(rank_list,rank)))&(rank_list<thesingle)]
       
        logicals=np.empty((0,a.shape[0]),dtype=bool)
    
        for i in rank:
            logicals=np.vstack((logicals,filt1(a,i)))
        if len(pockets)>0:
            for i in pockets:
                logicals=np.vstack((logicals,filt2(a,i)))
        return np.any(logicals,axis=0)