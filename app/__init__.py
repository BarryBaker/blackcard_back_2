from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pickle
import os
import glob
from functools import reduce
from sqlalchemy import and_

import pandas as pd
import numpy as np

wd = os.path.dirname(os.path.realpath(__file__))
# from flask_socketio import SocketIO
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

CORS(app)
api = Api(app)
# socketio = SocketIO(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "flassceret"
app.config["DEBUG"] = False if os.environ.get("FLASK_CONFIG") else True

from app import endpoints
from app.models import GT, Saved

gto = "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO/"
gto_joined = (
    "/Users/barrybaker/Documents/easygto/easygto_back/app/GTO_JOINED/"
)


def read_csv():
    for filename in os.listdir(wd + "/saved/"):
        name_as_list = filename.replace(".obj", "").split("_")
        file_path = os.path.join(wd + "/saved/", filename)

        # print(filename)
        filehandler = open(file_path, "rb")
        try:
            saved_tree = pickle.load(filehandler)
        except:
            print(filename)

        filehandler.close()
        # print(saved_tree)
        try:
            db.session.add(
                Saved(
                    stake=name_as_list[0],
                    stack=name_as_list[1],
                    players=name_as_list[2],
                    pos1=name_as_list[3],
                    pos2=name_as_list[4],
                    scenario=name_as_list[5],
                    board=name_as_list[6],
                    line=name_as_list[7],
                    hero=name_as_list[8],
                    tree=pickle.dumps(saved_tree),
                )
            )
        except IndexError:
            print(filename, name_as_list)
        db.session.commit()


def construct_GT_db():

    a = glob.glob(gto + "*.csv")
    a_joined = glob.glob(gto_joined + "*.csv")
    a = [i.replace(gto, "").replace(".csv", "") for i in a]
    a_joined = [
        i.replace(gto_joined, "").replace(".csv", "") for i in a_joined
    ]
    a = a + a_joined
    a = [i.split("_")[:-1] for i in a]

    au = list(set(map(tuple, a)))

    # print(au)
    n = 0
    for situ in au:
        print(n * 100 / len(au), n)

        n = n + 1
        """
        file_name = gto + "_".join([str(i) for i in situ]) + "_"
        file_name_joined = (
            gto_joined + "_".join([str(i) for i in situ]) + "_"
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
            i.split("_")[1] for i in a.columns
        ]  # str.lstrip("weight_")

        a.fillna(0, inplace=True)
        """
        # print(situ)
        saved = wd + "/saved/" + "_".join(situ)
        try:
            filehandler = open(f"/{saved}.obj", "rb")
            saved_tree = pickle.load(filehandler)
            filehandler.close()
        except FileNotFoundError:
            saved_tree = None
        # print(situ)
        if Saved.query.filter(
            and_(
                Saved.stake == situ[0],
                Saved.stack == situ[1],
                Saved.players == situ[2],
                Saved.pos1 == situ[3],
                Saved.pos2 == situ[4],
                Saved.scenario == situ[5],
                Saved.board == situ[6],
                Saved.line == situ[7],
                Saved.hero == situ[8],
            )
        ).first():

            continue
        else:
            db.session.add(
                Saved(
                    stake=situ[0],
                    stack=situ[1],
                    players=situ[2],
                    pos1=situ[3],
                    pos2=situ[4],
                    scenario=situ[5],
                    board=situ[6],
                    line=situ[7],
                    hero=situ[8],
                    tree=pickle.dumps(saved_tree),
                )
            )

        db.session.commit()


with app.app_context():
    db.create_all()
    # read_csv()

    # construct_GT_db()


api.add_resource(endpoints.get_boards, "/get_boards")
api.add_resource(endpoints.save_tree, "/save_tree")
api.add_resource(endpoints.construct_base_table, "/construct_base_table")
api.add_resource(endpoints.get_base_table, "/get_base_table")
api.add_resource(endpoints.generate_joined, "/generate_joined")
api.add_resource(
    endpoints.construct_base_tables_for_train,
    "/construct_base_tables_for_train",
)
api.add_resource(endpoints.pick_hand, "/pick_hand")

api.add_resource(endpoints.get_cards, "/get_cards")
api.add_resource(endpoints.card_list_suits, "/card_list_suits")
