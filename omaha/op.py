import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks,rank_names

def op(a,board,return_ak=False):
    rank = board.rank
    op=rank_list[rank_list<rank[0]]
    
    if len(op)==0:
        return np.full(a.shape[0], False)   ,None
    
    if return_ak:
        if len(op)<4:
            return np.full(a.shape[0], False)   ,None
        ak=op[0:2]
        logicals=np.empty((0,a.shape[0]),dtype=bool)
        for i in ak:
            logicals=np.vstack((logicals,filt2(a,i)))
        return np.any(logicals,axis=0)   ,None     
    
    cheat_sheet = rank_names[op[0]]*2 +' - '+rank_names[op[-1]]*2

    logicals=np.empty((0,a.shape[0]),dtype=bool)
    for i in op:
        logicals=np.vstack((logicals,filt2(a,i)))
    return np.any(logicals,axis=0),cheat_sheet