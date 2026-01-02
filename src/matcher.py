

def evidence_overlap(span_a: str, span_b: str) -> bool:
    if not span_a or not span_b:
        return False
    a = span_a.lower()
    b = span_b.lower()
    return a in b or b in a
def match_three_runs(run1_items, run2_items, run3_items):
    groups = []

    # start groups from run1
    for obj in run1_items:
        groups.append({
            "domain": obj["domain"],
            "objects": {"run1": obj}
        })

    # helper to attach objects to groups
    def attach(run_key, items):
        nonlocal groups
        for obj in items:
            attached = False
            for group in groups:
                ref_obj = next(iter(group["objects"].values()))
                if obj["domain"] == ref_obj["domain"] and \
                   evidence_overlap(obj["evidence_span"], ref_obj["evidence_span"]):
                    group["objects"][run_key] = obj
                    attached = True
                    break
            if not attached:
                groups.append({
                    "domain": obj["domain"],
                    "objects": {run_key: obj}
                })

    attach("run2", run2_items)
    attach("run3", run3_items)

    return groups
