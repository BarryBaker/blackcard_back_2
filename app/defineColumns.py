from omaha import fn


def define_columns(a, range_, board):
    cheat_sheet = {}
    a["FD"] = fn["flushdraw"](range_, board)
    a["NFD"] = fn["flushdraw"](range_, board, 1)

    a["F"] = fn["flush"](range_, board)
    a["NF"] = fn["flush"](range_, board, 1)

    FBL = fn["flushblocker"](range_, board, 0)
    NFBL = fn["flushblocker"](range_, board, 1)
    HFBL = fn["flushblocker"](range_, board, 4)
    a["FBL"], cheat_sheet["FBL"] = FBL[0] & ~a["FD"], FBL[1]
    a["NFBL"], cheat_sheet["NFBL"] = NFBL[0] & ~a["FD"], NFBL[1]
    a["HFBL"], cheat_sheet["HFBL"] = HFBL[0] & ~a["FD"], HFBL[1]

    a["BDFD"], cheat_sheet["BDFD"] = fn["flushdraw_backdoor"](
        range_, board, 0
    )
    a["BDFD1"], cheat_sheet["BDFD1"] = fn["flushdraw_backdoor"](
        range_, board, 1
    )
    a["BDFD2"], cheat_sheet["BDFD2"] = fn["flushdraw_backdoor"](
        range_, board, 2
    )

    a["FULL1"], cheat_sheet["FULL1"] = fn["full"](range_, board, 1)
    a["FULL"], cheat_sheet["FULL"] = fn["full"](range_, board, 0)

    # strong rankmade
    TRIPS = fn["trips"](range_, board, 0)
    TRIPS1 = fn["trips"](range_, board, 1)
    a["TRIPS"], cheat_sheet["TRIPS"] = TRIPS[0] & ~a["FULL"], TRIPS[1]
    a["TRIPS1"], cheat_sheet["TRIPS1"] = (
        TRIPS1[0] & ~a["FULL"],
        TRIPS1[1],
    )

    a["2P"] = fn["twopairs"](range_, board, 0) & ~a["TRIPS"] & ~a["FULL"]
    a["2PT"] = fn["twopairs"](range_, board, 1) & ~a["TRIPS"] & ~a["FULL"]

    # 1pair type
    a["OP"], cheat_sheet["OP"] = fn["op"](range_, board)  # &~a['2P']
    a["AA,KK"], cheat_sheet["AA,KK"] = fn["op"](
        range_, board, True
    )  # &~a['2P']
    a["TP"] = fn["toppair"](range_, board, 0)  # &~a['OP']
    a["TPTK"] = fn["toppair"](range_, board, 1)  # &~a['OP']
    a["BOP"] = fn["boardpair"](range_, board, 0) & ~a["2P"]

    a["LP"], cheat_sheet["LP"] = (
        fn["lowpair"](range_, board)[0]
        & ~(a["2P"] | a["TRIPS"] | a["FULL"]),
        fn["lowpair"](range_, board)[1],
    )
    a["RR"], cheat_sheet["RR"] = fn["pocket"](range_, board, "all")
    a["HRR"], cheat_sheet["HRR"] = fn["pocket"](range_, board, "high")
    a["LRR"], cheat_sheet["LRR"] = fn["pocket"](range_, board, "low")

    # for i in range(1,len(board.rankMap[0])+1):
    #    a[f'RR{i}'] = fn['pocket'](range_,board,i+1)

    STR = fn["straight"](range_, board)
    for i in STR:
        a[i], cheat_sheet[i] = STR[i]

    # str8ts=list(STR.keys())
    # for i in range(3,len(str8ts)):
    #     a[str8ts[i]]=a[str8ts[i]] & ~np.any(np.vstack([a[str8ts[j]] for j in range(i-1,1,-1)]),axis=0)

    a["OESD1"] = a["OESD1"] & ~a["WR"]
    a["OESD"] = a["OESD"] & ~a["WR"]
    a["GS1"] = (a["GS1"]) & ~(a["WR"] | a["OESD"])
    a["GS"] = (a["GS"]) & ~(a["WR"] | a["OESD"])

    a["SD"] = a["GS"] | a["OESD"] | a["WR"]
    cheat_sheet["SD"] = "WR OESD GS"

    # try:
    #    cheat_sheet['SD'] =cheat_sheet['GS']+' '+cheat_sheet['OESD']
    # except TypeError:
    #    cheat_sheet['SD'] =None

    # a['BDSD'] = a['BDSD'] & ~a['SD']
    # print(a.sample(20))
    return a, cheat_sheet
