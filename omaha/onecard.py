import numpy as np
from ._cards import filt2, filt1, rank_list, cards, ranks


def onecard(a, board, level=13):  # 1=A, 2 =K..13=2
    if level == 0:
        level = 13
    therank = rank_list[level-1]
    return filt1(a, therank)
