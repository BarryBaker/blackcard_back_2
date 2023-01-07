import numpy as np
from ._cards import filt2, filt1, rank_list, cards, ranks,rank_names


def pocket(a, board, level): #level: all,high,low
    board_ranks= board.rankMap[0]
 
    pockets = rank_list[(~np.in1d(rank_list, board_ranks)) & (rank_list>board_ranks[0])]
    if level=='all':
        logical = np.vstack([filt2(a, pocket) for pocket in pockets])
        cheat_sheet=None
        return np.any(logical, axis=0),cheat_sheet

    if len(pockets)<=4:
        return np.full(a.shape[0], False)   ,None

    if level=='high':
        logical = np.vstack([filt2(a, pocket) for pocket in pockets[:int(len(pockets)/2)]])
        cheat_sheet=rank_names[ pockets[int(len(pockets)/2)-1]]*2+'+'
    if level=='low':
        logical = np.vstack([filt2(a, pocket) for pocket in pockets[int(len(pockets)/2):]])
        cheat_sheet=rank_names[ pockets[int(len(pockets)/2)]]*2+'-'
    return np.any(logical, axis=0),cheat_sheet



