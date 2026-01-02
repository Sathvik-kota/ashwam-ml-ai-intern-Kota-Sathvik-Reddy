"""
Entry point for Exercise B: Run-to-Run Variance & Stability Analysis.

Loads journals and three LLM runs per journal,
computes stability metrics, and produces a conservative stable output.
"""

import json
import os
from report import generate_report
from stable_output import build_stable_output
from matcher import match_three_runs

# Path to llm runs
runs_dir = "data/llm_runs"

# Get all run files, sorted (VERY IMPORTANT)
run_files = sorted(os.listdir(runs_dir))

assert len(run_files) % 3 == 0, "Run files must be in multiples of 3"

all_results = []

# Process in chunks of 3 (one journal at a time)
for i in range(0, len(run_files), 3):
    run1_file = run_files[i]
    run2_file = run_files[i + 1]
    run3_file = run_files[i + 2]

    with open(os.path.join(runs_dir, run1_file)) as f:
        run1 = json.load(f)

    with open(os.path.join(runs_dir, run2_file)) as f:
        run2 = json.load(f)

    with open(os.path.join(runs_dir, run3_file)) as f:
        run3 = json.load(f)

    # ---- Metrics report ----
    report = generate_report(run1, run2, run3)

    # ---- Matching + stable output ----
    groups = match_three_runs(
        run1["items"],
        run2["items"],
        run3["items"]
    )

    stable_items = build_stable_output(groups)

    journal_id = run1.get("journal_id", f"journal_{i//3 + 1}")

    print(f"\nJournal {journal_id} stability report:")
    print(report)

    print(f"Journal {journal_id} stable final output:")
    for item in stable_items:
        print(item)

    all_results.append({
        "journal_id": journal_id,
        "metrics": report,
        "stable_output": stable_items
    })
