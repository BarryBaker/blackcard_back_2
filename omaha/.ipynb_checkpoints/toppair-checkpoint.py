import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks

def toppair(a,board,level=0):
    if board.paired=='unpaired':
        rank = board.rank
        remaining = rank_list[np.invert(np.isin(rank_list,rank))]
        
        def f(kicker):
            return filt1(a,rank[0]) & filt1(a,remaining[kicker])

        if level ==0 or level >5:
            return filt1(a,rank[0])

        if level==1:
            return f(0)
        if level==2:
            return f(0) | f(1) 
        if level==3:
            return f(0) | f(1) | f(2)
        if level==4:
            return f(0) | f(1) | f(2) | f(3)
        if level==5:
            return f(0) | f(1) | f(2) | f(3) | f(4)


    if board.paired=='paired':   
        rank = board.rankMap[0]
        rank_cnt = board.rankMap[1]
    
        pairs = rank[board.rankMap[1]==2] # non empty
        singles = rank[board.rankMap[1]==1] # non empty
        if len(singles) ==0 :
            return np.full(a.shape[0], False)
        
        if level ==0 or level >5:
            return filt1(a,singles[0])

        singles_higher = singles[singles<pairs[0]] # higher than higher pair

        # new rank list, remove lower singles but always keep highest single 
        rank=np.unique(np.concatenate((pairs,singles_higher,singles[0:1]))) 
        remaining = rank_list[np.invert(np.isin(rank_list,rank))]

        #print(rank,pairs,singles_higher,remaining)

        def fr(reaminingKicker): # filters from remaining
            return filt1(a,singles[0]) & filt1(a,remaining[reaminingKicker])
        def fs(singlesKicker): # filters from singles
            return filt1(a,singles[0]) & filt1(a,singles[singlesKicker])
            
        if len(singles_higher)<=1:
            if level==1:
                return fr(0)
            if level==2:
                return fr(0) | fr(1) 
            if level==3:
                return fr(0) | fr(1) | fr(2)
            if level==4:
                return fr(0) | fr(1) | fr(2) | fr(3)
            if level==5:
                return fr(0) | fr(1) | fr(2) | fr(3) | fr(4)
            
        if len(singles_higher)==2:
            if level==1:
                return fs(1)
            if level==2:
                return fs(1) | fr(0) 
            if level==3:
                return fs(1) | fr(0) | fr(1)
            if level==4:
                return fs(1) | fr(0) | fr(1) | fr(2)
            if level==5:
                return fs(1) | fr(0) | fr(1) | fr(2) | fr(3)

        if len(singles_higher)==3:
            if level==1:
                return fs(1)
            if level==2:
                return fs(1) | fs(2) 
            if level==3:
                return fs(1) | fs(2) | fr(0)
            if level==4:
                return fs(1) | fs(2) | fr(0) | fr(1)
            if level==5:
                return fs(1) | fs(2) | fr(0) | fr(1) | fr(2)
    return np.full(a.shape[0], False)