import numpy as np
from ._cards import filt2,filt1

def quads(a,board,level=0):
    if board.paired=='unpaired':
        return np.full(a.shape[0], False) # Nothing will be quads from input range
    if board.paired=='paired':
        pairs=board.rankMap[0][board.rankMap[1]==2]

        if len(pairs==1):
            return filt2(a,pairs[0])
        if len(pairs==2):
            return filt2(a,pairs[0]) | filt2(a,pairs[1])
    
    trip=board.rankMap[0][board.rankMap[1]>=3]
    return filt1(a,trip[0])