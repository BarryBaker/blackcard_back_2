from flask_restful import Resource
from flask import request
from flask import Response

import pandas as pd
import numpy as np
import random

import pickle
import os
import glob

from omaha._cards import card_values
import omaha._cards as o
from omaha import Board, fn
from .utils import best_cuts, sort_order
from .defineColumns import define_columns
from functools import reduce
from app.models import GT, Saved
from app import db
from sqlalchemy import or_, and_

sort_order = {
    "FOLD": 0,
    "CHECK": 1,
    "CALL": 2,
    "MIN": 3,
    "RAISE20": 3.5,
    "RAISE25": 4,
    "RAISE40": 5,
    "RAISE33": 6,
    "RAISE50": 7,
    "RAISE66": 7.5,
    "RAISE75": 8,
    "RAISE100": 9,
    "RAISE": 10,
    "ALLIN": 11,
}

wd = os.path.dirname(os.path.realpath(__file__))
gto = "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO/"
gto_joined = (
    "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO_JOINED/"
)
base_table = {}


def sort_situation(situation):
    return [
        situation["stake"],
        situation["stack_size"],
        situation["number_of_players"],
        situation["position_1"],
        situation["position_2"],
        situation["scenario"],
    ]


class get_boards(Resource):
    def post(self):

        situation = request.json["situation"]

        hero = request.json["hero"]
        boardType = request.json["boardType"]
        layer = request.json["layer"]
        street = 3
        if layer == "turn":
            street = 4
        if layer == "river":
            street = 5

        # line = request.json["line"]
        values = sort_situation(situation)
        a = Saved.query.filter(
            and_(
                Saved.stake == values[0],
                Saved.stack == values[1],
                Saved.players == values[2],
                Saved.pos1 == values[3],
                Saved.pos2 == values[4],
                Saved.scenario == values[5],
                # Saved.board == board,
                # Saved.line == line,
                Saved.hero == hero,
            )
        ).all()

        # file_name = gto + "_".join([str(i) for i in values]) + "_"
        # file_name_joined = (
        #     gto_joined + "_".join([str(i) for i in values]) + "_"
        # )
        # # print(glob.glob(file_name_joined + "*.csv") + [33333333333])

        # a = glob.glob(file_name + "*.csv")
        # a_joined = glob.glob(file_name_joined + "*.csv")
        # a = [i.replace(file_name, "").replace(".csv", "") for i in a]
        # a_joined = [
        #     i.replace(file_name_joined, "").replace(".csv", "")
        #     for i in a_joined
        # ]
        # a = a + a_joined
        # a = [i.split("_") for i in a]

        a = [
            [i.board, i.line]
            for i in a
            if len(i.board) == street * 2 and i.hero == hero
        ]
        if len(a) == 0:
            return {}

        # print([i for i in a if i[1] == "JO"])
        a = pd.DataFrame(a, columns=["board", "line"])
        a = a.groupby(["board", "line"], as_index=False).count()
        a["flopNP"] = a.board.apply(
            lambda x: Board([x[:2], x[2:4], x[4:6]])
        )

        npnp = np.stack(a.flopNP.apply(lambda x: x.np))
        for i in range(3):
            a[f"card{i}"] = o.ranks(npnp[:, i])
        a["paired"] = a.flopNP.apply(lambda x: x.paired == "paired")

        a["str8"] = a.flopNP.apply(lambda x: x.str8)
        a["suited"] = a.flopNP.apply(lambda x: len(x.suitMap[1]) == 2)
        a["mono"] = a.flopNP.apply(lambda x: len(x.suitMap[1]) == 1)
        a = a[
            (a["paired"] if boardType["paired"] else ~a["paired"])
            & (a["str8"] if boardType["str8"] else ~a["str8"])
            & (a["suited"] if boardType["suited"] else ~a["suited"])
            & (a["mono"] if boardType["mono"] else ~a["mono"])
        ]
        # print(o.cards(np.unique(np.stack(a["flopNP_NP"]), axis=0)))
        a = a.sort_values(by=[f"card{i}" for i in range(3)])

        a = a[["board", "line"]]
        result = {}

        for board in a["board"].unique():
            result[board] = {}
            for line in a[a["board"] == board]["line"]:
                try:
                    tree = (
                        Saved.query.filter(
                            and_(
                                Saved.stake == values[0],
                                Saved.stack == values[1],
                                Saved.players == values[2],
                                Saved.pos1 == values[3],
                                Saved.pos2 == values[4],
                                Saved.scenario == values[5],
                                Saved.board == board,
                                Saved.line == line,
                                Saved.hero == hero,
                            )
                        )
                        .first()
                        .tree
                    )

                    saved_tree = pickle.loads(tree)
                except AttributeError:
                    saved_tree = None

                # saved = (
                #     wd
                #     + "/saved/"
                #     + "_".join(
                #         [str(i) for i in values + [board, line, hero]]
                #     )
                # )
                # try:
                #     filehandler = open(f"/{saved}.obj", "rb")
                #     saved_tree = pickle.load(filehandler)
                #     filehandler.close()
                # except FileNotFoundError:
                #     saved_tree = None
                result[board][line] = saved_tree
        return result


class construct_base_table(Resource):
    def post(self):
        situ = request.json["situation"]

        file_name = gto + "_".join([str(situ[i]) for i in situ]) + "_"

        file_name_joined = (
            gto_joined + "_".join([str(situ[i]) for i in situ]) + "_"
        )

        action_filenames = glob.glob(file_name + "*.csv")
        action_filenames_joined = glob.glob(file_name_joined + "*.csv")
        actions = {}
        if len(action_filenames) > 0:
            for i in action_filenames:
                actions[
                    i.replace(file_name, "").replace(".csv", "")
                ] = pd.read_csv(i, index_col="combo")
            for i in actions:
                actions[i] = actions[i][actions[i]["weight"] != 0]
        else:
            for i in action_filenames_joined:
                actions[
                    i.replace(file_name_joined, "").replace(".csv", "")
                ] = pd.read_csv(i, index_col="combo")
            for i in actions:
                actions[i] = actions[i][actions[i]["weight"] != 0]
        emptydf = pd.DataFrame({"weight": []})
        emptydf.index.name = "combo"

        a = reduce(
            lambda df, key: df.join(
                actions[key], how="outer", rsuffix="_" + key
            ),
            [emptydf] + list(actions.keys()),
        )
        a.drop("weight", axis=1, inplace=True)

        a.columns = [
            i.split("_")[2] for i in a.columns
        ]  # str.lstrip("weight_")

        a.fillna(0, inplace=True)
        # a = GT.query.filter(
        #     and_(
        #         GT.stake == situ["stake"],
        #         GT.stack == situ["stack_size"],
        #         GT.players == situ["number_of_players"],
        #         GT.pos1 == situ["position_1"],
        #         GT.pos2 == situ["position_2"],
        #         GT.scenario == situ["scenario"],
        #         GT.board == situ["board"],
        #         GT.line == situ["line"],
        #         # GT.hero == hero,
        #     )
        # ).first()
        # a = pickle.loads(a.table)
        # Try filter out when action sum is less than 50. That hand may should not be in the mix in the first place
        a = a[a.sum(axis=1) > 40]

        # base_table["soft_actions"] = a.copy()
        a["action"] = a.idxmax(axis=1)
        a = a[["action"]]
        board = Board(
            [
                situ["board"][i : i + 2]
                for i in range(len(situ["board"]) - 1)
                if (i % 2) == 0
            ]
        )
        # RANGE
        # create 2d array of 4cards aka a wholerange from 'a ' dataframe
        # print(a)
        for i in range(0, 4):
            a[i] = a.index.str[i * 2 : i * 2 + 2]

        range_string = a.drop("action", axis=1)
        range_string = range_string.applymap(lambda x: card_values[x])

        range_ = range_string.values
        a.drop([0, 1, 2, 3], axis=1, inplace=True)

        a, cheat_sheet = define_columns(a, range_, board)
        base_table["base_cols"] = a

        bc = best_cuts(base_table["base_cols"], [], [])

        return {
            # "best_cuts": bc[2].to_json(orient="index"),
            "base_action": bc[1],
            "cheat_sheet": cheat_sheet,
        }


class get_base_table(Resource):
    def post(self):
        js = request.json
        bc = best_cuts(base_table["base_cols"], js["exc"], js["inc"])

        return {
            "best_cuts": bc[2].to_json(orient="index"),
            "rest": {"action": bc[1], "weight": bc[0]},
        }


class get_cards(Resource):
    def post(self):
        js = request.json
        bc = best_cuts(base_table["base_cols"], js["exc"], js["inc"])
        cardlist = bc[3]
        base_table["cardlist"] = cardlist
        action_list = list(np.unique(base_table["base_cols"].action))
        action_list.sort(key=lambda val: sort_order[val])
        a = cardlist.to_frame()
        for i in range(0, 4):
            a[i] = a.index.str[i * 2 : i * 2 + 2]
        range_string = a.drop("action", axis=1)
        range_string = range_string.applymap(lambda x: card_values[x])
        base_table["cardlist2d"] = range_string.values
        ranklist2d = o.ranks(range_string.values)

        ranklist2d_uniq, indicies = np.unique(
            ranklist2d, axis=0, return_inverse=True
        )

        result = []
        for rowNr in range(ranklist2d_uniq.shape[0]):
            item = {
                "ranks": o.cardRanks(ranklist2d_uniq[rowNr, :]).tolist(),
                "action": {},
            }
            rowsize = cardlist[indicies == rowNr].size
            for action in action_list:
                item["action"][action] = (
                    (cardlist[indicies == rowNr] == action).sum()
                    / rowsize
                    * 100
                )
            result.append(item)

        return {"cardlist": result}


class card_list_suits(Resource):
    def post(self):

        js = request.json
        cards = js["cards"]
        ranks2d = o.ranks(base_table["cardlist2d"])
        rankToFind = o.ranks(Board([i + "s" for i in cards]).np)

        action_list = list(np.unique(base_table["base_cols"].action))
        action_list.sort(key=lambda val: sort_order[val])

        result = {}
        for action in action_list:
            ranks2dFiltered = base_table["cardlist2d"][
                base_table["cardlist"] == action
            ][
                np.all(
                    ranks2d[base_table["cardlist"] == action]
                    == rankToFind,
                    axis=1,
                )
            ]
            result[action] = o.suits(o.suit(ranks2dFiltered)).tolist()
        return {"card_ranks": cards, "suits": result}


class save_tree(Resource):
    def post(self):
        situ = request.json["situation"]
        tree = request.json["tree"]

        # values = sort_situation(js["situation"])
        # utso elotti, mai a line beleirjuk hogz joine, ha joined

        # if js["joined"]:
        #     values[-2] = values[-2] + "-JOINED" #yes

        filename = "_".join([str(situ[i]) for i in situ])
        filehandler = open(wd + "/saved" + f"/{filename}.obj", "wb")
        pickle.dump(tree, filehandler)
        filehandler.close()

        saved = Saved.query.filter(
            and_(
                Saved.stake == situ["stake"],
                Saved.stack == situ["stack_size"],
                Saved.players == situ["number_of_players"],
                Saved.pos1 == situ["position_1"],
                Saved.pos2 == situ["position_2"],
                Saved.scenario == situ["scenario"],
                Saved.board == situ["board"],
                Saved.line == situ["line"],
                Saved.hero == situ["hero"],
            )
        ).first()
        if saved:
            saved.tree = pickle.dumps(tree)
        else:
            db.session.add(
                Saved(
                    stake=situ["stake"],
                    stack=situ["stack_size"],
                    players=situ["number_of_players"],
                    pos1=situ["position_1"],
                    pos2=situ["position_2"],
                    scenario=situ["scenario"],
                    board=situ["board"],
                    line=situ["line"],
                    hero=situ["hero"],
                    tree=pickle.dumps(tree),
                )
            )
        db.session.commit()


class generate_joined(Resource):
    def post(self):
        situ = request.json["situation"]
        hero = request.json["hero"]
        # if Saved.query.filter(
        #     and_(
        #         Saved.stake == situ["stake"],
        #         Saved.stack == situ["stack_size"],
        #         Saved.players == situ["number_of_players"],
        #         Saved.pos1 == situ["position_1"],
        #         Saved.pos2 == situ["position_2"],
        #         Saved.scenario == situ["scenario"],
        #         Saved.board == situ["board"],
        #         Saved.line == situ["line"] + "JO"
        #         # GT.hero == hero,
        #     )
        # ).first():
        #     return None
        file_name = gto + "_".join([str(situ[i]) for i in situ]) + "_"

        action_filenames = glob.glob(file_name + "*.csv")

        actions = {}
        for i in action_filenames:
            actions[
                i.replace(file_name, "").replace(".csv", "")
            ] = pd.read_csv(i, index_col="combo")
        for i in actions:
            actions[i] = actions[i][actions[i]["weight"] != 0]

        emptydf = pd.DataFrame({"weight": []})
        emptydf.index.name = "combo"

        a = reduce(
            lambda df, key: df.join(
                actions[key], how="outer", rsuffix="_" + key
            ),
            [emptydf] + list(actions.keys()),
        )
        a.drop("weight", axis=1, inplace=True)

        a.columns = [
            i.split("_")[2] for i in a.columns
        ]  # str.lstrip("weight_")
        a.fillna(0, inplace=True)
        # Try filter out when action sum is less than 50. That hand may should not be in the mix in the first place
        # item = GT.query.filter(
        #     and_(
        #         GT.stake == situ["stake"],
        #         GT.stack == situ["stack_size"],
        #         GT.players == situ["number_of_players"],
        #         GT.pos1 == situ["position_1"],
        #         GT.pos2 == situ["position_2"],
        #         GT.scenario == situ["scenario"],
        #         GT.board == situ["board"],
        #         GT.line == situ["line"],
        #         # GT.hero == hero,
        #     )
        # ).first()
        # a = pickle.loads(item.table).copy()

        raises = [i for i in a.columns if "RAISE" in i or i == "ALLIN"]

        if len(raises) == 2:
            a["RAISE"] = a.apply(
                lambda row: row[raises[0]] + row[raises[1]], axis=1
            )

            if (
                "RAISE100" in raises
                and a["RAISE100"].sum()
                > a[[i for i in raises if i != "RAISE100"][0]].sum()
            ):
                a.drop(raises, axis=1, inplace=True)
                a.rename(columns={"RAISE": "RAISE100"}, inplace=True)

            elif (
                "ALLIN" in raises
                and a["ALLIN"].sum()
                > a[[i for i in raises if i != "ALLIN"][0]].sum()
            ):
                a.drop(raises, axis=1, inplace=True)
                a.rename(columns={"RAISE": "ALLIN"}, inplace=True)
            else:
                a.drop(raises, axis=1, inplace=True)

            if not Saved.query.filter(
                and_(
                    Saved.stake == situ["stake"],
                    Saved.stack == situ["stack_size"],
                    Saved.players == situ["number_of_players"],
                    Saved.pos1 == situ["position_1"],
                    Saved.pos2 == situ["position_2"],
                    Saved.scenario == situ["scenario"],
                    Saved.board == situ["board"],
                    Saved.line == situ["line"] + "-JO",
                    Saved.hero == hero,
                )
            ).first():

                db.session.add(
                    Saved(
                        stake=situ["stake"],
                        stack=situ["stack_size"],
                        players=situ["number_of_players"],
                        pos1=situ["position_1"],
                        pos2=situ["position_2"],
                        scenario=situ["scenario"],
                        board=situ["board"],
                        line=situ["line"] + "-JO",
                        hero=hero,
                        tree=pickle.dumps(None),
                    )
                )

            db.session.commit()

        situ["line"] = situ["line"] + "-JO"
        for i in a.columns:
            res = a[i]
            res.name = "weight"
            res.to_csv(
                f"{gto_joined}{'_'.join([str(situ[j]) for j in situ])}_{hero}_{i}.csv"
            )
        return None


class construct_base_tables_for_train(Resource):
    def post(self):
        situation = request.json["situation"]
        boardlines = request.json["boardlines"]
        base_tables = {}
        for boardline in boardlines:
            situ = situation | boardline
            file_name = gto + "_".join([str(situ[i]) for i in situ]) + "_"

            file_name_joined = (
                gto_joined + "_".join([str(situ[i]) for i in situ]) + "_"
            )

            action_filenames = glob.glob(file_name + "*.csv")

            action_filenames_joined = glob.glob(file_name_joined + "*.csv")
            actions = {}
            if len(action_filenames) > 0:
                for i in action_filenames:
                    actions[
                        i.replace(file_name, "").replace(".csv", "")
                    ] = pd.read_csv(i, index_col="combo")
                for i in actions:
                    actions[i] = actions[i][actions[i]["weight"] != 0]
            else:
                for i in action_filenames_joined:
                    actions[
                        i.replace(file_name_joined, "").replace(".csv", "")
                    ] = pd.read_csv(i, index_col="combo")
                for i in actions:
                    actions[i] = actions[i][actions[i]["weight"] != 0]
            emptydf = pd.DataFrame({"weight": []})
            emptydf.index.name = "combo"

            a = reduce(
                lambda df, key: df.join(
                    actions[key], how="outer", rsuffix="_" + key
                ),
                [emptydf] + list(actions.keys()),
            )
            a.drop("weight", axis=1, inplace=True)

            a.columns = [
                i.split("_")[2] for i in a.columns
            ]  # str.lstrip("weight_")

            a.fillna(0, inplace=True)
            a = a[a.sum(axis=1) > 40]

            # base_table["soft_actions"] = a.copy()
            a["action"] = a.idxmax(axis=1)
            a = a[["action"]]
            base_tables[(boardline["board"], boardline["line"])] = a
        base_table["train"] = base_tables
        return "done"


class pick_hand(Resource):
    def get(self):

        boardline, table = random.choice(list(base_table["train"].items()))
        hand = table.sample().to_dict(orient="dict")["action"]

        options = list(np.unique(table.action))
        options.sort(key=lambda val: sort_order[val])
        return {
            "board": boardline[0],
            "line": boardline[1],
            "hand": list(hand.keys())[0],
            "result": list(hand.values())[0],
            "options": options,
        }
