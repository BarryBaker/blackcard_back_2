import numpy as np
from ._cards import filt2,filt1,allCards,suit_names,card_names
from ._board import Board
from .flush import flush 
#from .flushdraw import flushdraw 
from functools import reduce

def flushblocker(a,board,level=0):
    suit = board.suitMap[0]
    suit_cnt = board.suitMap[1]

    if np.max(suit_cnt) == 1:
        return np.full(a.shape[0], False),None

    if np.max(suit_cnt) == 2:
        if board.street ==5:
            boardOnTurn = Board(board.bsl[:4])
            if np.max(boardOnTurn.suitMap[1]) == 1:
                return np.full(a.shape[0], False),None
            flushColor = boardOnTurn.suitMap[0][boardOnTurn.suitMap[1]==2]
        else:
            flushColor = suit[suit_cnt==2] # array with 1 or 2 element
    if np.max(suit_cnt) >= 3:
        flushColor = suit[suit_cnt>=3] # array with 1 element

    def makeLogicals(color): # make the bolean array for one color
        all_flushColor_cards = allCards[allCards&7 == color]
        remaining_flushColor_cards = all_flushColor_cards[np.invert(np.isin(all_flushColor_cards,board.np))]

        if level==0:
            return filt1(a,color),suit_names[color]
        return reduce(lambda a,b:a|b, [filt1(a,remaining_flushColor_cards[i]) for i in range(level)]),reduce(lambda a,b:a+' '+b, [card_names[remaining_flushColor_cards[i]] for i in range(level)])
    
    # none_flush = np.invert(flush(a,board,0) | flushdraw(a,board,0))
    none_flush = np.invert(flush(a,board,0))
    
    if len(flushColor)==1:
        return makeLogicals(flushColor[0])[0] & none_flush , makeLogicals(flushColor[0])[1]
    
    return (makeLogicals(flushColor[0])[0] | makeLogicals(flushColor[1])[0]) & none_flush,f'{makeLogicals(flushColor[0])[1]},{makeLogicals(flushColor[1])[1]}'
    
    
    