from collections import Counter

def majority_vote(values):
    counts = Counter(values)
    value, freq = counts.most_common(1)[0]
    return value, freq


def build_stable_output(groups, total_runs=3):
    stable_items = []

    for group in groups:
        objs = list(group["objects"].values())

        # --- Polarity handling (critical) ---
        polarities = [o.get("polarity") for o in objs if o.get("polarity")]

        if len(set(polarities)) > 1:
            stable_items.append({
                "domain": group["domain"],
                "evidence_span": objs[0]["evidence_span"],
                "polarity": "uncertain",
                "reason": "polarity disagreement across runs"
            })
            continue

        polarity = polarities[0]

        # --- Intensity / arousal ---
        intensity_vals = [
            o.get("intensity_bucket") or o.get("arousal_bucket")
            for o in objs
            if o.get("intensity_bucket") != "unknown"
        ]

        intensity = None
        if intensity_vals:
            intensity, _ = majority_vote(intensity_vals)

        # --- Time ---
        time_vals = [o.get("time_bucket") for o in objs if o.get("time_bucket")]
        time_bucket, _ = majority_vote(time_vals)

        stable_items.append({
            "domain": group["domain"],
            "evidence_span": objs[0]["evidence_span"],
            "polarity": polarity,
            "intensity_bucket": intensity or "unknown",
            "time_bucket": time_bucket
        })

    return stable_items
