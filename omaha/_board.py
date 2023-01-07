import numpy as np
from ._cards import card_values, ranks, card_names, suit


class Board:
    def __init__(self, boardStringList):
        self.board = np.sort(
            np.array([card_values[i] for i in boardStringList])
        )
        self.boardStringList = boardStringList

    @property
    def bsl(self):
        return self.boardStringList

    @property
    def np(self):  # get numpy array
        return self.board

    @property
    def suit(self):
        return suit(self.board)

    @property
    def rank(self):
        return np.sort(ranks(self.board))

    @property
    def street(self):
        return len(self.board)

    @property
    def paired(self):
        _, unique_board_counts = np.unique(
            ranks(self.board), return_counts=True
        )
        if np.max(unique_board_counts) == 1:
            return "unpaired"
        if np.max(unique_board_counts) == 2:
            return "paired"
        return "trips"

    @property
    def str8(self):
        uranks, counts = np.unique(ranks(self.board), return_counts=True)

        if len(counts) != 3:
            return False
        if np.max(uranks) - np.min(uranks) <= 32:
            return True
        if 8 in uranks:
            uranks[uranks == 8] = 112
            if np.max(uranks) - np.min(uranks) <= 32:
                return True
        return False

    @property
    def rankMap(self):
        return np.unique(ranks(self.board), return_counts=True)

    @property
    def suitMap(self):
        return np.unique(suit(self.board), return_counts=True)

    def __repr__(self):
        return np.array2string(
            self.board, formatter={"int": lambda x: card_names[x]}
        )
