from app import db


class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stake = db.Column(db.String(10), nullable=False)
    stack = db.Column(db.String(3), nullable=False)
    players = db.Column(db.String(1), nullable=False)
    pos1 = db.Column(db.String(3), nullable=False)
    pos2 = db.Column(db.String(3), nullable=False)
    scenario = db.Column(db.String(3), nullable=False)
    board = db.Column(db.String(10), nullable=False)
    line = db.Column(db.String(50), nullable=False)
    hero = db.Column(db.String(3), nullable=False)
    tree = db.Column(db.BLOB)


class GT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stake = db.Column(db.String(10), nullable=False)
    stack = db.Column(db.Integer, nullable=False)
    players = db.Column(db.Integer, nullable=False)
    pos1 = db.Column(db.String(3), nullable=False)
    pos2 = db.Column(db.String(3), nullable=False)
    scenario = db.Column(db.String(3), nullable=False)
    board = db.Column(db.String(10), nullable=False)
    line = db.Column(db.String(50), nullable=False)
    hero = db.Column(db.String(3), nullable=False)
    table = db.Column(db.BLOB, nullable=False)

    def __repr__(self):
        return self.stake
