#from omaha import allCards,wd,pre,suit_list,cards
import omaha._cards as o
import numpy as np
from itertools import combinations

def straight(a,board):
    b=board.rankMap[0]

    #Str8ts-----------------
    straights = {}

    for card2 in combinations(o.rank_list,2):

        if 8 in card2:
                remainingBoard = b[~np.isin(b,np.append(card2,112))]
    
        else:
                remainingBoard = b[~np.isin(b,card2)]

        if len(remainingBoard)<3: # Nincs 3 rank a boardrol ami nem a kiválasztott 2 rank az összes rankbol
                continue
        else:
            for board3 in combinations(remainingBoard,3):
                arr = np.array([*card2,*board3])
                isstraight=np.amax(arr)-np.amin(arr)==32
            
                if 8 in card2 and not(isstraight):
                    new_card2 = card2[card2!=8]
                    new_card2 = np.append(new_card2,112)
                    
                    arr = np.array([*new_card2,*board3])
                    isstraight=np.amax(arr)-np.amin(arr)==32

                elif 8 in board3 and not(isstraight):
                    new_board3 = board3[board3!=8]
                    new_board3 = np.append(new_board3,112)
                    
                    arr = np.array([*card2,*new_board3])
                    isstraight=np.amax(arr)-np.amin(arr)==32

                if isstraight:
                    if tuple(card2) in straights:
                        straights[tuple(card2)].append(np.amin(arr))
                    else:
                        straights[tuple(card2)]=[np.amin(arr)]
                
    for key in straights:
        straights[key]=min(straights[key])

    if len(straights)>0:
        nuthighstr8=min(straights.values()) # ha ez van akkor minden egyéb str8dr ami alá huz nem lesz nut
    else: nuthighstr8=100

    # for key in straights:
    #         if straights[key]==nuthighstr8:
    #             nut='NUT'
    #         else: nut=''
    #         print(tuple([o.rank_names[i] for i in key]),nut,'STR')


    # Str8draws---------------
    if 8 in b:
        remaining = o.rank_list[~np.isin(o.rank_list,np.append(b,112))]
    else:
        remaining = np.append(o.rank_list[~np.isin(o.rank_list,b)],112)

    strHighs={} # possible high straigths for each turn
    straightsInTurns = np.empty(shape=(0, 4), dtype=int) # turn, card1,card2,strhigh
    straightDrawsInTurns = np.empty(shape=(0, 2), dtype=int) # card1,card2

    for turn in remaining:
        strHighs[turn]=[]
    
        turnBoard=np.sort(np.append(b,turn)) 
        for card2 in combinations(o.rank_list,2):
            if tuple(card2) in straights:
                continue
            # ha A benne van a holecardok között akkor a boadrol nem válaszhatjuk a 8-at nyilávn de 112-t se, 
            # ha nicns akkor mehet mindkettö
            if 8 in card2:
                remainingTurnBoard = turnBoard[~np.isin(turnBoard,np.append(card2,112))]
            else:
                remainingTurnBoard = turnBoard[~np.isin(turnBoard,card2)]
            
            if len(remainingTurnBoard)<3:
                continue
            
            else:
                
                for board3 in combinations(remainingTurnBoard,3):
                    arr = np.array([*card2,*board3])
                    isstraight=np.amax(arr)-np.amin(arr)==32

                    if 8 in card2 and not(isstraight):
                        new_card2 = card2[card2!=8]
                        new_card2 = np.append(new_card2,112)
                        arr = np.array([*new_card2,*board3])
                        isstraight=np.amax(arr)-np.amin(arr)==32

                    elif 8 in board3 and not(isstraight):
                        new_board3 = board3[board3!=8]
                        new_board3 = np.append(new_board3,112)
                    
                        arr = np.array([*card2,*new_board3])
                        isstraight=np.amax(arr)-np.amin(arr)==32
                    
                    if isstraight:
                        if turn ==112:
                            turn=8
                        strHighs[turn].append(np.amin(arr))
                       
                        straightsInTurns = np.vstack([straightsInTurns,[turn,*card2,np.amin(arr)]])
                       
                # BDSD
                for board2 in combinations(remainingTurnBoard,2):
                    if not(np.any(np.isin(b,card2))) and board.street==3:
                        arr = np.array([*card2,*board2])
                        isstraightDraw=np.amax(arr)-np.amin(arr)==24 and np.amin(arr)!=8 and np.amax(arr)!=104
                        
                        if isstraightDraw:          
                            straightDrawsInTurns = np.vstack([straightDrawsInTurns,[*card2]])

    
    for i in strHighs:
        if len (strHighs[i])>0:
            strHighs[i]=min(strHighs[i]+[nuthighstr8]) 
            # az eredeti sort el kell étni, néha huzhatunk annál jobbra bizonyos turnökön, 
            # ott azt kell elérni, de roszabbra nem

    card2_dir={}
    for i in range(straightsInTurns.shape[0]):
        
        if tuple(straightsInTurns[i,1:3]) in card2_dir:
            # true ha ne nut, false ha nut
            # ha már benne volt ezzel a turnnel ,akkor csak akkor irja felül, ha false lesz a strhigh, azaz nut
            if (straightsInTurns[i,0] in card2_dir[tuple(straightsInTurns[i,1:3])]):
                if card2_dir[tuple(straightsInTurns[i,1:3])][straightsInTurns[i,0]]:
                    card2_dir[tuple(straightsInTurns[i,1:3])][straightsInTurns[i,0]]=strHighs[straightsInTurns[i,0]]!=straightsInTurns[i,3]
            else:
                card2_dir[tuple(straightsInTurns[i,1:3])][straightsInTurns[i,0]]=strHighs[straightsInTurns[i,0]]!=straightsInTurns[i,3]
                
        else:
            card2_dir[tuple(straightsInTurns[i,1:3])]={} 
            card2_dir[tuple(straightsInTurns[i,1:3])][straightsInTurns[i,0]]=strHighs[straightsInTurns[i,0]]!=straightsInTurns[i,3]
    
    str_draw_cards=np.unique(straightsInTurns[:,1:3])
    if straightDrawsInTurns.shape[0]>0:
        straightDrawsInTurns=np.unique(straightDrawsInTurns,axis=0)
    straightDrawsInTurns = straightDrawsInTurns[~(straightDrawsInTurns[:, None] == straightsInTurns[:,1:3]).all(-1).any(-1)]
    
    card3_dir={}
    for card2 in card2_dir:
        for card3rd in str_draw_cards[~np.isin(str_draw_cards,np.array([card2]))]:
            card3 = np.sort(np.append(np.array([card2]),card3rd))
            
            one_of_the_2cards_makes_straight = False
            for i in combinations(card3,2):
                if i in straights:
                    one_of_the_2cards_makes_straight = True
                    continue
            if one_of_the_2cards_makes_straight:
                continue

            card3_str8_list=[card2_dir[i] for i in combinations(card3,2) if i in card2_dir]
            
            card3_str8_list=[[i,subdir[i]] for subdir in card3_str8_list for i in subdir]

            #kidobjuk ha egy turn többszr is szerepel
            card3_str8_list_uniq={}
            for i in card3_str8_list:
                if i[0] in card3_str8_list_uniq:
                    if i[1]< card3_str8_list_uniq[i[0]]:
                        card3_str8_list_uniq[i[0]]=i[1]    
                else:
                    card3_str8_list_uniq[i[0]]=i[1]
            card3_dir[tuple(card3)]=card3_str8_list_uniq

    for i in list(card3_dir.keys()):
        if len(card3_dir[i])<=1: # ami hármas csomagban is gs maradt az kuka, mert kettesben is jó
            del card3_dir[i]
        elif len(card3_dir[i])>2: # wrapok
            pass
        else:
            # megnézzük hogy ez a 3mas mit tud
            number_of_str8s= len(card3_dir[i])
            card3areNutStr8s = max(card3_dir[i].values())==0
            
            card2_performances=[]
            for j in combinations(i,2):
                if j in card2_dir:
                    card2_performances.append((len(card2_dir[j]),max(card2_dir[j].values())==0))
            
            # nut oesdbol nut oesd
            if card3areNutStr8s and (2,True) in card2_performances:
                del card3_dir[i]
            #oesdbol oesd
            elif not(card3areNutStr8s) and (2,False) in card2_performances:
                del card3_dir[i]

    #----------------------------------------
    card4_dir={}
    for card2 in card2_dir:
        for card3rd4th in combinations(str_draw_cards[~np.isin(str_draw_cards,np.array([card2]))],2):
            card4 = np.sort(np.append(np.array([card2]),np.array(card3rd4th)))
            
            one_of_the_2cards_makes_straight = False
            for i in combinations(card4,2):
                if i in straights:
                    one_of_the_2cards_makes_straight = True
                    continue
            if one_of_the_2cards_makes_straight:
                continue
            
            card4_str8_list=[card2_dir[i] for i in combinations(card4,2) if i in card2_dir]
            
            card4_str8_list=[[i,subdir[i]] for subdir in card4_str8_list for i in subdir]
        
            #kidobjuk ha egy turn többszr is szerepel
            card4_str8_list_uniq={}
            for i in card4_str8_list:
                if i[0] in card4_str8_list_uniq:
                    if i[1]< card4_str8_list_uniq[i[0]]:
                        card4_str8_list_uniq[i[0]]=i[1]    
                else:
                    card4_str8_list_uniq[i[0]]=i[1]
            card4_dir[tuple(card4)]=card4_str8_list_uniq

    for i in list(card4_dir.keys()):
        # megtartjuk azokat a 4esekt, mik egy hármason segiteni zudnak
    
        if len(card4_dir[i])==1: # ami négyes csomagban is gs maradt az kuka, mert kettesben is jó
            del card4_dir[i]
        else: 
            # megnézzük hogy ez a 4mas mennyivel csinál sort és nutok e
            number_of_str8s= len(card4_dir[i])
            card4areNutStr8s = max(card4_dir[i].values())==0

            # egnézüük összes 3as komobt a 4esbol hogy a 3mas ditben hogy tlejesit: mennyi sort csinál, nutok-e
            card3_performances=[]
            for j in combinations(i,3):
                if j in card3_dir:
                    #print(card3_dir[j].values()) max values==0 elégséges e a nutsorhuzo def-ra?
                    card3_performances.append((len(card3_dir[j]),max(card3_dir[j].values())==0))
            
            # nincs 3as részlet, de 2es még lehet
            if len(card3_performances)==0:
                continue

            # eleve wrap volt
            elif max([i[0] for i in card3_performances])>2: 
                del card4_dir[i]

            # nut oesdbol nut oesd
            elif card4areNutStr8s and (2,True) in card3_performances:
                del card4_dir[i]
            #oesdbol oesd
            elif not(card4areNutStr8s) and (2,False) in card3_performances:
                del card4_dir[i]

    # mégegy  négyesre, 2es somgaokkal
    for i in list(card4_dir.keys()):
                
            # megnézzük hogy ez a 4mas mennyivel csinál sort és nutok e
            number_of_str8s= len(card4_dir[i])
            card4areNutStr8s = max(card4_dir[i].values())==0

            # egnézüük összes 3as komobt a 4esbol hogy a 3mas ditben hogy tlejesit: mennyi sort csinál, nutok-e
            card2_performances=[]
            for j in combinations(i,2):
                if j in card2_dir:
                    #print(card3_dir[j].values()) max values==0 elégséges e a nutsorhuzo def-ra?
                    card2_performances.append((len(card2_dir[j]),max(card2_dir[j].values())==0))
            
            # nincs 3as részlet, de 2es még lehet
            if len(card2_performances)==0:
                continue

            # nut oesdbol nut oesd
            elif (card4areNutStr8s and (2,True) in card2_performances) and number_of_str8s<3:
                del card4_dir[i]
            #oesdbol oesd
            elif (not(card4areNutStr8s) and (2,False) in card2_performances) and number_of_str8s<3:
                del card4_dir[i]

    result={
        'STR1':[[],[]],
        'STR':[[],[]],
        'WR1':[[],[]],
        'WR':[[],[]],
        'OESD1':[[],[]],
        'OESD':[[],[]],
        'GS1':[[],[]],
        'GS':[[],[]],    
      #  'BDSD':[[],[]],
        'SDBL':[[],[]]
    }

    for key in straights:
        result['STR'][0].append(list(key))
        result['STR'][1].append(''.join([o.rank_names[i] for i in key]))
        if straights[key]==nuthighstr8:
            result['STR1'][0].append(list(key))
            result['STR1'][1].append(''.join([o.rank_names[i] for i in key]))
 
    for i in [card2_dir,card3_dir,card4_dir]:
        if board.street<5:
            for key in i:
                if len(i[key])==1:
                    str8type='GS'
                elif len(i[key])==2:
                    str8type='OESD'
                else:
                    str8type='WR'

                result[str8type][0].append(list(key))
                result[str8type][1].append(''.join([o.rank_names[i] for i in key]))

                if max(i[key].values())==0:
                    result[str8type+'1'][0].append(list(key))
                    result[str8type+'1'][1].append(''.join([o.rank_names[i] for i in key]))
    
    #BDSD
    #for i in range(straightDrawsInTurns.shape[0]):
    #    result['BDSD'][0].append(list(straightDrawsInTurns[i,:]))
    #    result['BDSD'][1].append(''.join([o.rank_names[i] for i in straightDrawsInTurns[i,:]]))
    
   

    #SDBL
    result['SDBL'][0] = [[j] for k in result['OESD1'][0] for j in k if len(k)==2] + [[j] for k in result['STR1'][0] for j in k if len(k)==2]
    result['SDBL'][1] = [j for k in result['OESD1'][1] for j in k if len(k)==2] + [j for k in result['STR1'][1] for j in k if len(k)==2]
    sdbl0=result['SDBL'][0].copy()
    
    for i in result:  
            if len(result[i][0])>0:
                result[i][1]=' '.join(result[i][1])
                result[i][0]=np.any(
                    np.vstack([np.all(np.vstack(
                        [o.filt1(a,card) for card in filt]),axis=0) for filt in result[i][0]]),axis=0)
            else:
                result[i][1]=None
                result[i][0]=np.full(a.shape[0], False)
    
    #DSDBL
    result['DSDBL']=[[],[]]
    if len(sdbl0)>0:
                #print(result['SDBL'])
                result['DSDBL'][1]=' '.join([i+i for i in result['SDBL'][1]])
                result['DSDBL'][0]=np.any(
                    np.vstack([np.all(np.vstack(
                        [o.filt2(a,card) for card in filt]),axis=0) for filt in sdbl0]),axis=0)
    else:
        result['DSDBL'][1]=None
        result['DSDBL'][0]=np.full(a.shape[0], False)
    #print(result['DSDBL'])
    return result
        


