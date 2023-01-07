import numpy as np
from ._cards import filt2,filt1,allCards

def flushdraw_double(a,board,level=0):
    suit = board.suitMap[0]
    suit_cnt = board.suitMap[1]

    if np.max(suit_cnt) != 2 or board.street==5:
        return np.full(a.shape[0], False)
    flushColor = suit[suit_cnt==2]
    if len(flushColor)!=2:
        return np.full(a.shape[0], False)

    return filt2(a,flushColor[0]) & filt2(a,flushColor[1])
    
    
    