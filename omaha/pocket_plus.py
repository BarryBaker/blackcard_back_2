import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks

def pocket_plus(a,board,level=13): # 1=AA, 2 =KK..13=22
        rank = board.rank
        if level==0:
            level=13
        #rank_cnt = board.rankMap[1]
        #singles = rank[rank_cnt==1] 

        thepocket = rank_list[level-1]

        rank = rank[rank<=thepocket]
        pockets = rank_list[(np.invert(np.isin(rank_list,rank))) & (rank_list<=thepocket)]
        

        logicals=np.empty((0,a.shape[0]),dtype=bool)
    
        for i in rank:
            logicals=np.vstack((logicals,filt1(a,i)))
        for i in pockets:
            logicals=np.vstack((logicals,filt2(a,i)))
        return np.any(logicals,axis=0)