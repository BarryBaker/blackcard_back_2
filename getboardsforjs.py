import pandas as pd
import numpy as np

import pickle
import os
import glob
import json
from omaha._cards import card_values
import omaha._cards as o
from omaha import Board, fn

from functools import reduce
from app.models import Saved
from app import db
from sqlalchemy import or_, and_

wd = os.path.dirname(os.path.realpath(__file__))
print(wd)
gto = "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO/"
gto_joined = (
    "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO_JOINED/"
)

file_name = gto  # + "_".join([str(i) for i in values]) + "_"
file_name_joined = gto_joined  # + "_".join([str(i) for i in values]) + "_"
# print(glob.glob(file_name_joined + "*.csv") + [33333333333])

a = glob.glob(file_name + "*.csv")
a_joined = glob.glob(file_name_joined + "*.csv")
a = [i.replace(file_name, "").replace(".csv", "") for i in a]
a_joined = [
    i.replace(file_name_joined, "").replace(".csv", "") for i in a_joined
]
a = a + a_joined
a = [i.split("_")[:-1] for i in a]
au = list(set(map(tuple, a)))

# print(au)
# a = [
#     [i.board, i.line]
#     for i in a
#     if len(i.board) == street * 2 and i.hero == hero
# ]


# print([i for i in a if i[1] == "JO"])
a = pd.DataFrame(
    au,
    columns=[
        "stake",
        "stack",
        "players",
        "pos1",
        "pos2",
        "scenario",
        "board",
        "line",
        "hero",
    ],
)

# a = a.groupby(["board", "line"], as_index=False).count()
a["flopNP"] = a.board.apply(lambda x: Board([x[:2], x[2:4], x[4:6]]))

npnp = np.stack(a.flopNP.apply(lambda x: x.np))
for i in range(3):
    a[f"card{i}"] = o.ranks(npnp[:, i])

a["paired"] = a.flopNP.apply(lambda x: x.paired == "paired")
a["str8"] = a.flopNP.apply(lambda x: x.str8)
a["suited"] = a.flopNP.apply(lambda x: len(x.suitMap[1]) == 2)
a["mono"] = a.flopNP.apply(lambda x: len(x.suitMap[1]) == 1)
# a = a[
#     (a["paired"] if boardType["paired"] else ~a["paired"])
#     & (a["str8"] if boardType["str8"] else ~a["str8"])
#     & (a["suited"] if boardType["suited"] else ~a["suited"])
#     & (a["mono"] if boardType["mono"] else ~a["mono"])
# ]
# print(o.cards(np.unique(np.stack(a["flopNP_NP"]), axis=0)))
a = a.sort_values(by=[f"card{i}" for i in range(3)])
a["layer"] = a.board.apply(
    lambda x: "flop" if len(x) == 6 else "turn" if len(x) == 8 else "river"
)

a = a.drop(["flopNP", "card0", "card1", "card2"], axis=1)


def find_saved_tree(row):
    saved = (
        "/Users/barrybaker/Documents/blackcard/blackcard_back/app"
        + "/saved/"
        + "_".join(
            [
                str(i)
                for i in [
                    row["stake"],
                    row["stack"],
                    row["players"],
                    row["pos1"],
                    row["pos2"],
                    row["scenario"],
                    row["board"],
                    row["line"],
                    row["hero"],
                ]
            ]
        )
    )
    try:
        filehandler = open(f"/{saved}.obj", "rb")
        saved_tree = pickle.load(filehandler)
        filehandler.close()
    except FileNotFoundError:
        saved_tree = None
    # try:
    #     tree = (
    #         Saved.query.filter(
    #             and_(
    #                 Saved.stake == row["stake"],
    #                 Saved.stack == row["stack"],
    #                 Saved.players == row["players"],
    #                 Saved.pos1 == row["pos1"],
    #                 Saved.pos2 == row["pos2"],
    #                 Saved.scenario == row["scenario"],
    #                 Saved.board == row["board"],
    #                 Saved.line == row["line"],
    #                 Saved.hero == row["hero"],
    #             )
    #         )
    #         .first()
    #         .tree
    #     )

    #     saved_tree = pickle.loads(tree)
    # except AttributeError:
    #     saved_tree = None

    return saved_tree


a["tree"] = a.apply(lambda x: find_saved_tree(x), axis=1)


with open(
    "/Users/barrybaker/Documents/blackcard/blackcard/src/assets/trees.json",
    "w",
) as fp:
    json.dump(a.to_json(orient="records"), fp)
