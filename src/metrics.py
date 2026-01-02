def agreement_rate(groups, total_runs=3):
    stable = 0
    for g in groups:
        if len(g["objects"]) == total_runs:
            stable += 1
    return stable / len(groups) if groups else 0.0
