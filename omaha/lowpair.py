import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks,rank_names

def lowpair(a,board):
    rank = board.rankMap[0]
    
    if len(rank)<=2:
        return np.full(a.shape[0], False),None
    
    lowranks = rank[2:]
    
    cheat_sheet = ' '.join([rank_names[i] for i in lowranks]) 

    logicals=np.empty((0,a.shape[0]),dtype=bool)
    for i in lowranks:
        logicals=np.vstack((logicals,filt1(a,i)))
    return np.any(logicals,axis=0),cheat_sheet