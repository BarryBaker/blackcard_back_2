from re import I
import numpy as np
from ._cards import filt2, filt1, allCards, card_names,suit_names


def flushdraw_backdoor(a, board, level=0):
    suit = board.suitMap[0]
    suit_cnt = board.suitMap[1]
    
    if np.max(suit_cnt) == 3 or board.street != 3:
        return np.full(a.shape[0], False),None
    flushColor = suit[suit_cnt == 1]  # array of 1 or 3

    def makeLogicals(color):  # make the bolean array for one color
        return filt2(a, color)

    if len(flushColor) == 1: 
        if level==0:
            return filt2(a, flushColor[0]),suit_names[flushColor[0]]*2
        else:
            return np.full(a.shape[0], False),None
    
    # if flop is rainbow
    bdfd_cnt = np.sum(np.vstack([filt2(a,flushColor[i]) 
                      for i in range(3)]), axis=0)  # number of bd fd-s
    cheat_sheet=' '.join([suit_names[i]*2 for i in flushColor])
    if level == 1:
        return bdfd_cnt == 1,cheat_sheet
    if level == 2:
        return bdfd_cnt == 2,cheat_sheet

    return bdfd_cnt > 0,cheat_sheet
