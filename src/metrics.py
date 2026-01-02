def agreement_rate(groups, total_runs=3):
    stable = 0
    for g in groups:
        if len(g["objects"]) == total_runs:
            stable += 1
    return stable / len(groups) if groups else 0.0


def polarity_flip_rate(groups):
    flips = 0
    total = 0

    for g in groups:
        polarities = set()
        for obj in g["objects"].values():
            polarities.add(obj.get("polarity"))

        if len(polarities) > 1:
            flips += 1
        total += 1

    return flips / total if total else 0.0
