from ._board import Board
#from .str8_wrap import wrap
from .str8_draws import gutshot, oesd
import numpy as np
from ._cards import rank_names,rank_list,filt1,filt2
#from.str8_helpers import str8_helper


def str8_backdoor(a, board, level=0):  # 1 wrap, 2 NOESD, 3 OESD, 4 NGS, 5 GS
    if board.street > 3:
        return np.full(a.shape[0], False),None
    rank = board.rank
    remaining = rank_list[np.invert(np.isin(rank_list,rank))]
    
    gs_now=gutshot(a, board, 0)
    oesd_now=oesd(a, board, 0)
    sd_now=np.vstack([gs_now[2],oesd_now[2]])
    #sd_hands_now=np.any(np.vstack([gs_now[0],oesd_now[0]]),axis=0)##
    
    #logicals=np.empty((0,a.shape[0]),dtype=bool) ## concat of boolean arrays gonna be evaluated with 'or'
    cheat_sheet=np.empty((0,2),dtype=int)

    for turn in remaining:
        new_board = Board(board.bsl+[rank_names[turn]+'s'])
        gs=oesd(a, new_board, 0)
       
        #logicals=np.vstack([logicals,gs[0]])##
        cheat_sheet=np.vstack([cheat_sheet,gs[2]])
    
    cheat_sheet=np.unique(cheat_sheet,axis=0)
    cheat_sheet = cheat_sheet[~(cheat_sheet[:, None] == sd_now).all(-1).any(-1)] # kidobjuk a sd-ket
    cheat_sheet=cheat_sheet[np.invert(np.any(np.isin(cheat_sheet,rank),axis=1))] # kidobjuk boardparokat
    
    # ez egylöremegvan d elehetne még optimalizálni
    logicals=np.empty((0,a.shape[0]),dtype=bool)
    for i in range(cheat_sheet.shape[0]):
        logicals=np.vstack([logicals,filt1(a, cheat_sheet[i,:][0]) & filt1(a, cheat_sheet[i,:][1])])
    
    return np.any(logicals,axis=0),' '.join(np.apply_along_axis(lambda row:rank_names[row[0]]+rank_names[row[1]],1,cheat_sheet))




    # if level == 1:
    #     card_number = np.sum([wrap(a, Board(board.bsl+[i+'s']), 0)
    #                           for i in rank_names.values()], axis=0)

    #     return card_number > 0

    # if level == 2:
    #     card_number = np.sum([oesd(a, Board(board.bsl+[i+'s']), 1)
    #                           for i in rank_names.values()], axis=0)

    #     return card_number > 0

    # if level == 3:
    #     card_number = np.sum([oesd(a, Board(board.bsl+[i+'s']), 0)
    #                           for i in rank_names.values()], axis=0)

    #     return card_number > 0

    # if level == 4:
    #     card_number = np.sum([gutshot(a, Board(board.bsl+[i+'s']), 1)
    #                           for i in rank_names.values()], axis=0)

    #     return card_number > 0

    # if level == 5:
    #     card_number = np.sum([gutshot(a, Board(board.bsl+[i+'s']), 0)
    #                           for i in rank_names.values()], axis=0)

    #     return card_number > 0
