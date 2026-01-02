from matcher import match_three_runs
from metrics import agreement_rate, polarity_flip_rate, bucket_drift_rate

def generate_report(run1, run2, run3):
    groups = match_three_runs(run1["items"], run2["items"], run3["items"])

    report = {
        "agreement_rate": agreement_rate(groups),
        "polarity_flip_rate": polarity_flip_rate(groups),
        "bucket_drift_rate": bucket_drift_rate(groups),
        "total_objects": len(groups)
    }

    return report
