import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks

def boardpair(a,board,level=0): 
        rank = board.rankMap[0]
        rank_cnt = board.rankMap[1]

        singles = rank[rank_cnt==1] 

        if len(singles)==0:
            return np.full(a.shape[0], False)  
        
        if level ==0:
            level=5
        
        thesingle = singles[min(len(singles),level)-1]

        singles = singles[singles<=thesingle]
        
        logical = np.vstack([filt1(a,i) for i in singles])
        return np.any(logical,axis=0)

