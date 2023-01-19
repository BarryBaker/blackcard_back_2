import numpy as np
from ._cards import filt2, filt1, rank_names


def full(a, board, level=0):
    if board.paired == "unpaired":
        return np.full(a.shape[0], False), None
    if board.paired == "paired":
        rank = board.rankMap[0]
        rank_cnt = board.rankMap[1]

        def f(
            ranks,
        ):  # ranks is '(1,2)' type if two different rank needed, just 1 if a rank neede wice
            if ranks >= 10:
                return (
                    filt1(a, rank[ranks % 10])
                    & filt1(a, rank[int(ranks / 10)]),
                    rank_names[rank[ranks % 10]]
                    + rank_names[rank[int(ranks / 10)]],
                )
            return (
                filt2(a, rank[ranks]),
                rank_names[rank[ranks]] + rank_names[rank[ranks]],
            )

        if np.array_equal(rank_cnt, [2, 1]):
            if level == 1:
                return f(10)[0], f(10)[1]
            return f(10)[0] | f(1)[0], " ".join([f(10)[1], f(1)[1]])

        if np.array_equal(rank_cnt, [1, 2]):
            if level == 1:
                return f(0)[0], f(0)[1]
            return f(0)[0] | f(10)[0], " ".join([f(0)[1], f(10)[1]])

        if np.array_equal(rank_cnt, [2, 1, 1]):
            if level == 1:
                return f(10)[0], f(10)[1]
            if level == 2:
                return f(10)[0] | f(20)[0], None
            if level == 3:
                return f(10)[0] | f(20)[0] | f(1)[0], None
            return f(10)[0] | f(20)[0] | f(1)[0] | f(2)[0], " ".join(
                [f(10)[1], f(20)[1], f(1)[1], f(2)[1]]
            )

        if np.array_equal(rank_cnt, [1, 2, 1]):
            if level == 1:
                return f(0)[0], None
            if level == 2:
                return f(0)[0] | f(10)[0], None
            if level == 3:
                return f(0)[0] | f(10)[0] | f(12)[0], None
            return f(0)[0] | f(10)[0] | f(12)[0] | f(2)[0], None

        if np.array_equal(rank_cnt, [1, 1, 2]):
            if level == 1:
                return f(0)[0], None
            if level == 2:
                return f(0)[0] | f(1)[0], None
            if level == 3:
                return f(0)[0] | f(1)[0] | f(20)[0], None
            return f(0)[0] | f(1)[0] | f(20)[0] | f(21)[0], None

        if np.array_equal(rank_cnt, [2, 2]):
            return f(10)[0], None

        if np.array_equal(rank_cnt, [2, 1, 1, 1]):
            if level == 1:
                return f(10)[0], None
            if level == 2:
                return f(10)[0] | f(20)[0], None
            if level == 3:
                return f(10)[0] | f(20)[0] | f(30)[0], None
            if level == 4:
                return f(10)[0] | f(20)[0] | f(30)[0] | f(1)[0], None
            if level == 5:
                return (
                    f(10)[0] | f(20)[0] | f(30)[0] | f(1)[0] | f(2)[0],
                    None,
                )
            return (
                f(10)[0]
                | f(20)[0]
                | f(30)[0]
                | f(1)[0]
                | f(2)[0]
                | f(3)[0],
                None,
            )

        if np.array_equal(rank_cnt, [1, 2, 1, 1]):
            if level == 1:
                return f(0)[0], None
            if level == 2:
                return f(0) | f(10), None
            if level == 3:
                return f(0) | f(10) | f(12), None
            if level == 4:
                return f(0) | f(10) | f(12) | f(13), None
            if level == 5:
                return f(0) | f(10) | f(12) | f(13) | f(2), None
            return (
                f(0)[0]
                | f(10)[0]
                | f(12)[0]
                | f(13)[0]
                | f(2)[0]
                | f(3)[0],
                None,
            )

        if np.array_equal(rank_cnt, [1, 1, 2, 1]):
            if level == 1:
                return f(0)[0], None
            if level == 2:
                return f(0) | f(1), None
            if level == 3:
                return f(0) | f(1) | f(20), None
            if level == 4:
                return f(0) | f(1) | f(20) | f(21), None
            if level == 5:
                return f(0) | f(1) | f(20) | f(21) | f(23), None
            return (
                f(0)[0]
                | f(1)[0]
                | f(20)[0]
                | f(21)[0]
                | f(23)[0]
                | f(3)[0],
                None,
            )

        if np.array_equal(rank_cnt, [1, 1, 1, 2]):
            if level == 1:
                return f(0)[0], None
            if level == 2:
                return f(0) | f(1), None
            if level == 3:
                return f(0) | f(1) | f(2), None
            if level == 4:
                return f(0) | f(1) | f(2) | f(30), None
            if level == 5:
                return f(0) | f(1) | f(2) | f(30) | f(31), None
            return (
                f(0)[0]
                | f(1)[0]
                | f(2)[0]
                | f(30)[0]
                | f(31)[0]
                | f(32)[0],
                None,
            )

        if np.array_equal(rank_cnt, [2, 2, 1]):
            if level == 1:
                return f(10)[0], None
            if level == 2:
                return f(10) | f(20), None
            if level == 3:
                return f(10) | f(20) | f(12), None
            return f(10)[0] | f(20)[0] | f(12)[0] | f(2)[0], None

        if np.array_equal(rank_cnt, [2, 1, 2]):
            if level == 1:
                return f(10)[0], None
            if level == 2:
                return f(10) | f(20), None
            if level == 3:
                return f(10) | f(20) | f(1), None
            return f(10)[0] | f(20)[0] | f(1)[0] | f(12)[0], None

        if np.array_equal(rank_cnt, [1, 2, 2]):
            if level == 1:
                return f(0)[0], None
            if level == 2:
                return f(0) | f(10), None
            if level == 3:
                return f(0) | f(10) | f(20), None
            return f(0)[0] | f(10)[0] | f(20)[0] | f(12)[0], " ".join(
                [f(0)[1], f(10)[1], f(20)[1], f(12)[1]]
            )

    # Tripsnél nagyobb singelekkel a fullok
    trip = board.rankMap[0][board.rankMap[1] >= 3]  # non empty

    singles = board.rankMap[0][board.rankMap[1] == 1]

    singles = singles[singles < trip[0]]
    if len(singles) == 0:
        return np.full(a.shape[0], False), None

    if len(singles) == 2:
        if level == 1:
            return filt2(a, singles[0]), None
        return filt2(a, singles[0]) | filt2(a, singles[1]), None
    if len(singles) == 1:
        return filt2(a, singles[0]), None
