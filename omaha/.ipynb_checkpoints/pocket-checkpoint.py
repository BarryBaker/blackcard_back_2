import numpy as np
from ._cards import filt2,filt1,rank_list,cards,ranks

def pocket(a,board,level=13): # 1=AA, 2 =KK..13=22
        logical = np.vstack([filt2(a,thepocket) for thepocket in rank_list])
        return np.any(logical,axis=0)
       