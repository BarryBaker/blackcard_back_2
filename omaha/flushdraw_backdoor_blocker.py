import numpy as np
from ._cards import filt2,filt1,allCards,card_names

def flushdraw_backdoor_blocker(a,board,level=0):
    suit = board.suitMap[0]
    suit_cnt = board.suitMap[1]

    if np.max(suit_cnt) == 3 or board.street!=3:
        return np.full(a.shape[0], False)
    flushColor = suit[suit_cnt==1] #array of 1 or 3

    def makeLogicals(color): # make the bolean array for one color - we need exacctly one of that color
        return filt1(a,color) & np.invert(filt2(a,color))

    if len(flushColor)==1:
        #if board.np[board.np&7==flushColor[0]]&120==8: #A a color
        #    nutblocker=16+flushColor[0]
        #else: nutblocker=8+flushColor[0]
        #print(card_names[nutblocker])
        return makeLogicals(flushColor[0])
    
    # if flop is rainbow
    bdfd_cnt = np.sum(np.vstack([makeLogicals(flushColor[i]) for i in range(3)]),axis=0) # number of bd fd-s
    #print(np.vstack([makeLogicals(flushColor[i]) for i in range(3)]))
    if level==1: 
        return bdfd_cnt == 1
    if level==2: 
        return bdfd_cnt == 2  
    if level==3: 
        return bdfd_cnt == 3  
    return bdfd_cnt > 0
    
    
    