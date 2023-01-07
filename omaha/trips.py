import numpy as np
from ._cards import filt2,filt1,rank_list,rank_names
from functools import reduce

def trips(a,board,level=0):
    if board.paired=='unpaired':
        rank = board.rank # unique rank
        
        logical_cnt=len(rank) if level==0 else min(len(rank),level)
        logical = np.vstack([filt2(a,rank[i]) for i in range(logical_cnt)])
        cheat_sheet=' '.join([rank_names[rank[i]]*2 for i in range(logical_cnt)])
        return np.any(logical,axis=0),cheat_sheet


    if board.paired=='paired':
        rank = board.rankMap[0]
        rank_cnt = board.rankMap[1]
        remaining = rank_list[np.invert(np.isin(rank_list,rank))]
        
        pairs=rank[rank_cnt==2]
      
        if level ==0 or level >5:
            if len(pairs)==1:
                return filt1(a,pairs[0]),rank_names[pairs[0]]
            if len(pairs)==2:
                return filt1(a,pairs[0]) | filt1(a,pairs[1]),rank_names[pairs[0]]+', '+rank_names[pairs[1]]

        return reduce(lambda a,b:a|b,[filt1(a,pairs[0]) & filt1(a,remaining[kicker]) for kicker in range(level)]),reduce(lambda a,b:a +' '+b ,[rank_names[pairs[0]]+rank_names[remaining[kicker]] for kicker in range(level)])
       

    return np.full(a.shape[0], False),None