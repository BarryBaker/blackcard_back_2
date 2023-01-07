import numpy as np
from ._cards import filt2,filt1,allCards

def flush(a,board,level=0):
    suit = board.suitMap[0]
    suit_cnt = board.suitMap[1]

    if np.max(suit_cnt) < 3:
        return np.full(a.shape[0], False)
    flushColor = suit[suit_cnt>=3][0]
    
    all_flushColor_cards=allCards[allCards&7==flushColor]
    remaining_flushColor_cards=all_flushColor_cards[np.invert(np.isin(all_flushColor_cards,board.np))]
    
    def f(level):  
        return filt1(a,remaining_flushColor_cards[level])
    
    if level==1:
        return (f(0)) & filt2(a,flushColor)
    if level==2:
        return (f(0) | f(1)) & filt2(a,flushColor)
    if level==3:
        return (f(0) | f(1) | f(2)) & filt2(a,flushColor)
    if level==4:
        return (f(0) | f(1) | f(2) | f(3)) & filt2(a,flushColor)
    if level==5:
        return (f(0) | f(1) | f(2) | f(3) | f(4)) & filt2(a,flushColor)
    return filt2(a,flushColor)
    
    