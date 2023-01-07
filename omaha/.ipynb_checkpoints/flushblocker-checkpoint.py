import numpy as np
from ._cards import filt2,filt1,allCards
from ._board import Board
from .flush import flush 

def flushblocker(a,board,level=0):
    suit = board.suitMap[0]
    suit_cnt = board.suitMap[1]

    
    if np.max(suit_cnt) == 1:
        return np.full(a.shape[0], False)
    if np.max(suit_cnt) == 2:
        if board.street ==5:
            boardOnTurn = Board(board.bsl[:4])
            flushColor = boardOnTurn.suitMap[0][boardOnTurn.suitMap[1]==2]
        else:
            flushColor = suit[suit_cnt==2] # array with 1 or 2 element
    if np.max(suit_cnt) >= 3:
        flushColor = suit[suit_cnt>=3] # array with 1 element

    def makeLogicals(color): # make the bolean array for one color
        all_flushColor_cards=allCards[allCards&7==color]
        remaining_flushColor_cards=all_flushColor_cards[np.invert(np.isin(all_flushColor_cards,board.np))]

        def f(level):  
            return filt1(a,remaining_flushColor_cards[level])

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
        return filt1(a,color)
    
    none_flush = np.invert(flush(a,board,0))
    
    if len(flushColor)==1:
        return makeLogicals(flushColor[0]) & none_flush
    
    return (makeLogicals(flushColor[0]) | makeLogicals(flushColor[1])) & none_flush
    
    
    