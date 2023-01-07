import numpy as np
import os
import pickle

_s = 1
_h = 2
_d = 3
_c = 4

_A = (1 << 3)
_K = (2 << 3)
_Q = (3 << 3)
_J = (4 << 3)
_T = (5 << 3)
_9 = (6 << 3)
_8 = (7 << 3)
_7 = (8 << 3)
_6 = (9 << 3)
_5 = (10 << 3)
_4 = (11 << 3)
_3 = (12 << 3)
_2 = (13 << 3)

_As = _A | _s
_Ah = _A | _h
_Ad = _A | _d
_Ac = _A | _c
_Ks = _K | _s
_Kh = _K | _h
_Kd = _K | _d
_Kc = _K | _c
_Qs = _Q | _s
_Qh = _Q | _h
_Qd = _Q | _d
_Qc = _Q | _c
_Js = _J | _s
_Jh = _J | _h
_Jd = _J | _d
_Jc = _J | _c
_Ts = _T | _s
_Th = _T | _h
_Td = _T | _d
_Tc = _T | _c
_9s = _9 | _s
_9h = _9 | _h
_9d = _9 | _d
_9c = _9 | _c
_8s = _8 | _s
_8h = _8 | _h
_8d = _8 | _d
_8c = _8 | _c
_7s = _7 | _s
_7h = _7 | _h
_7d = _7 | _d
_7c = _7 | _c
_6s = _6 | _s
_6h = _6 | _h
_6d = _6 | _d
_6c = _6 | _c
_5s = _5 | _s
_5h = _5 | _h
_5d = _5 | _d
_5c = _5 | _c
_4s = _4 | _s
_4h = _4 | _h
_4d = _4 | _d
_4c = _4 | _c
_3s = _3 | _s
_3h = _3 | _h
_3d = _3 | _d
_3c = _3 | _c
_2s = _2 | _s
_2h = _2 | _h
_2d = _2 | _d
_2c = _2 | _c

suit_list=np.array([_s,_h,_d,_c])
rank_list=np.array([_A,_K,_Q,_J,_T,_9,_8,_7,_6,_5,_4,_3,_2])
allCards=np.array([_As,_Ah,_Ad,_Ac,_Ks,_Kh,_Kd,_Kc,_Qs,_Qh,_Qd,_Qc,_Js,
_Jh,_Jd,_Jc,_Ts,_Th,_Td,_Tc,_9s,_9h,_9d,_9c,_8s,_8h,_8d,_8c,_7s,_7h,_7d,
_7c,_6s,_6h,_6d,_6c,_5s,_5h,_5d,_5c,_4s,_4h,_4d,_4c,_3s,_3h,_3d,_3c,_2s,_2h,_2d,_2c])

""" def findname(x):
    return card_names[x]
 """
def suit(card2d):
    return card2d&7
def ranks(card2d):
    return card2d&120
def cards(card2d):
    if card2d.size==0:
        return np.array([])
    def findname(x):
        return card_names[x]
    return np.vectorize(findname)(card2d)

def suits(suit2d):
    if suit2d.size==0:
        return np.array([])
    def findnsuite(x):
        suitnames=['s','h','d','c']
        return suitnames[x-1]
    return np.vectorize(findnsuite)(suit2d)

def cardRanks(card2d):
    if card2d.size==0:
        return np.array([])
    def findname(x):
        return rank_names[x]
    return np.vectorize(findname)(card2d)


def filt1(array,toFind):
    if toFind in suit_list:
        return np.any(suit(array)==toFind,axis=1)
    if toFind in rank_list:
        return np.any(ranks(array)==toFind,axis=1)
    return np.any(array==toFind,axis=1)

def filt2(array,toFind):
    if toFind in suit_list:
        return np.count_nonzero(suit(array)==toFind,axis=1)>=2
    if toFind in rank_list:
        return np.count_nonzero(ranks(array)==toFind,axis=1)>=2
    return 'dont call exact card'

def filt_dead(array,dead):
    return array[np.invert(np.any(np.isin(array,dead,assume_unique=True),axis=1))]

alls=np.unique(ranks(allCards))
alls=np.append(alls,112)

card_values = { "As": _As, "Ah": _Ah, "Ad": _Ad, "Ac": _Ac, "Ks": _Ks, "Kh": _Kh, "Kd": _Kd, "Kc": _Kc, "Qs": _Qs, "Qh": _Qh, "Qd": _Qd, "Qc": _Qc, "Js": _Js, "Jh": _Jh, "Jd": _Jd, "Jc": _Jc, "Ts": _Ts, "Th": _Th, "Td": _Td, "Tc": _Tc, "9s": _9s, "9h": _9h, "9d": _9d, "9c": _9c, "8s": _8s, "8h": _8h, "8d": _8d, "8c": _8c, "7s": _7s, "7h": _7h, "7d": _7d, "7c": _7c, "6s": _6s, "6h": _6h, "6d": _6d, "6c": _6c, "5s": _5s, "5h": _5h, "5d": _5d, "5c": _5c, "4s": _4s, "4h": _4h, "4d": _4d, "4c": _4c, "3s": _3s, "3h": _3h, "3d": _3d, "3c": _3c, "2s": _2s, "2h": _2h, "2d": _2d, "2c": _2c }

card_names={}
for i in card_values:
    card_names[card_values[i]]=i

rank_names = {_A:'A',_K:'K',_Q:'Q',_J:'J',_T:'T',_9:'9',_8:'8',_7:'7',_6:'6',_5:'5',_4:'4',_3:'3',_2:'2'}
suit_names = {1:'s',2:'h',3:'d',4:'c'}

wd = os.path.dirname(os.path.realpath(__file__))
