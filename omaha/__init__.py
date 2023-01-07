import numpy as np
import pandas as pd
import os
import pickle

from . import _cards, _board, quads, full, trips, str8, twopairs,  flush, toppair, op, onepair, pocket_plus, pocket, onecard, flushdraw, flushblocker, flushdraw_double, flushdraw_backdoor, boardpair, flushdraw_backdoor_blocker,lowpair#, str8_backdoor
from ._cards import wd

Board = _board.Board
# made = {
#     'quads': quads.quads,
#     'full': full.full,
#     'trips': trips.trips,
#     'twopairs': twopairs.twopairs,
#     'straight': str8.straight,
#     'flush': flush.flush,
#     'toppair': toppair.toppair,
# }

# Exact stregnths


# def full(a, board, level=0):
#     return made['full'](a, board, level)


# def flush(a, board, level=0):
#     return made['flush'](a, board, level)

# def trips(a, board, level=0):
#     return made['trips'](a, board, level)

# def twopairs(a, board, level=0):
#     return made['twopairs'](a, board, level)


# def toppair(a, board, level=0):
#     return made['toppair'](a, board, level)


fn = {
    'quads': quads.quads,
    'full': full.full,
    'flush': flush.flush,
    'straight': str8.straight,
    'trips': trips.trips,
    'twopairs': twopairs.twopairs,
    'toppair': toppair.toppair,
    'op': op.op,
    'onepair': onepair.onepair,
    'pocket_plus': pocket_plus.pocket_plus,
    'pocket': pocket.pocket,
    'onecard': onecard.onecard,
    'flushdraw': flushdraw.flushdraw,
    'flushblocker': flushblocker.flushblocker,
    'flushdraw_double': flushdraw_double.flushdraw_double,
    'flushdraw_backdoor': flushdraw_backdoor.flushdraw_backdoor,
    'flushdraw_backdoor_blocker': flushdraw_backdoor_blocker.flushdraw_backdoor_blocker,
    'lowpair':lowpair.lowpair,
    #'str8_backdoor': str8_backdoor.str8_backdoor,
    'boardpair': boardpair.boardpair
}


#np.set_printoptions(edgeitems =1)
