import numpy as np
import pandas as pd
import os
import pickle

from . import _cards,_board,quads,full,trips,str8_draws,str8_wrap,twopairs,str8_straight,flush,toppair,op,onepair,pocket_plus,pocket,onecard,flushdraw,flushblocker,flushdraw_double,flushdraw_backdoor,str8_blocker,boardpair,flushdraw_backdoor_blocker
from ._cards import wd,pre,str8Lookup

Board=_board.Board
made={
'quads':quads.quads,
'full':full.full,
'trips':trips.trips,
'twopairs':twopairs.twopairs,
'straight': str8_straight.straight,
'flush':flush.flush,
'toppair':toppair.toppair,
}

# Ensembles
def full(a,board,level=0):
    return made['full'](a,board,level) | made['quads'](a,board,0) 

def flush(a,board,level=0):
    return made['flush'](a,board,level) | full(a,board,0) 

def straight(a,board,level=0):
    return made['straight'](a,board,level) | flush(a,board,0) 

def trips(a,board,level=0):
    return made['trips'](a,board,level) | straight(a,board,0) 

def twopairs(a,board,level=0):
    return made['twopairs'](a,board,level) | trips(a,board,0) 

def toppair(a,board,level=0):
    return made['toppair'](a,board,level) | twopairs(a,board,0) | fn['op'](a,board,0) 



fn={
'quads':quads.quads,
'full':full,
'flush':flush,
'straight': straight,
'trips':trips,
'twopairs':twopairs,
'toppair':toppair,
'gutshot':str8_draws.gutshot,
'oesd':str8_draws.oesd,
'wrap':str8_wrap.wrap,
'op':op.op,
'onepair':onepair.onepair,
'pocket_plus':pocket_plus.pocket_plus,
'pocket':pocket.pocket,
'onecard':onecard.onecard,
'flushdraw':flushdraw.flushdraw,
'flushblocker':flushblocker.flushblocker,
'flushdraw_double':flushdraw_double.flushdraw_double,
'flushdraw_backdoor':flushdraw_backdoor.flushdraw_backdoor,
'flushdraw_backdoor_blocker':flushdraw_backdoor_blocker.flushdraw_backdoor_blocker,
'str8_blocker':str8_blocker.str8_blocker,
'boardpair':boardpair.boardpair
}



#np.set_printoptions(edgeitems =1)