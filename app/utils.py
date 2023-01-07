import pandas as pd
import numpy as np


def invert(series, invert):
    if invert:
        return ~series
    return series


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


def best_cuts(base_table, exc, inc):
    a = base_table.copy()

    whole_range_count = a.shape[0]

    try:
        excluded = np.vstack([a[i] for i in exc])
        a = a[np.invert(np.any(excluded, axis=0))]
    except:
        pass
    try:
        included = np.vstack([a[i] for i in inc])
        a = a[np.all(included, axis=0)]
    except:
        pass

    action_list = [i for i in a.action.unique()]
    action_list.sort(key=lambda val: sort_order[val])

    # Alapeloszlás
    base_filtered = a["action"]
    base_length = base_filtered.size
    base_counts = base_filtered.value_counts()
    base = {
        action: 100 * base_counts[action] / base_length
        for action in action_list
    }
    filtered_count = round(100 * base_length / whole_range_count, 2)

    hand = []
    filtered_weight = []
    weight = []
    gini = []
    cut = {}

    for i in action_list:
        cut[i] = []

    for col in a.columns.drop(["action"]):

        ct = pd.crosstab(a[col], a["action"])
        ginis = []
        sums = []
        for i in ct.index:
            s = ct.loc[i].sum()
            ginis.append(1 - ((ct.loc[i] / s) ** 2).sum())
            sums.append(s)
        giniresult = sum(
            [ginis[i] * sums[i] / sum(sums) for i in range(len(ginis))]
        )

        filtered = a[a[col]]["action"]

        length = filtered.size

        counts = {}
        for i in action_list:
            counts[i] = (filtered == i).sum()

        if len(counts) == 0 or length == 0:
            continue

        filtered_weight.append(round(100 * length / base_length))
        weight.append(100 * length / whole_range_count)
        gini.append(giniresult)

        hand.append(col)

        for action in cut:
            cut[action].append(100 * counts[action] / length)

    cut["filtered_weight"] = filtered_weight
    cut["weight"] = weight
    cut["gini"] = gini
    cuts = pd.DataFrame(index=hand, data=cut)
    # cuts['max_value'] = cuts.drop(['weight','filtered_weight'],axis=1).max(axis=1)

    cuts = cuts.sort_values("gini")
    cuts.drop("gini", axis=1, inplace=True)

    cuts = cuts[cuts["filtered_weight"] < 100]
    # print(filtered_count,base,cuts,base_filtered)
    return filtered_count, base, cuts, base_filtered
