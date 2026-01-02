# Run-to-Run Variance & Stability Analysis (Exercise B)
## Context & Motivation

Ashwam processes free-form women’s health journals that include symptoms, food, emotions, and mental states.
These journals are inherently subjective and variable:

- Mood and emotions fluctuate daily
- Symptoms can appear, disappear, or be ambiguously described
- Hormonal cycles, stress, sleep, and context all influence expression
- There are no canonical labels and no single “ground truth”

In this setting, LLM non-determinism is expected, but unsafe variance is not acceptable.
The goal of this exercise is not to maximize recall, but to ensure that no user-facing insight is produced unless it is stable and safe across runs.

## What I Built (High-Level)

I built a run-to-run stability framework that:

1. Deterministically aligns extracted semantic objects across 3 LLM runs
2. Quantifies instability using safety-relevant metrics
3. Explicitly detects high-risk variance (e.g. polarity flips)
4. Produces a conservative stable final output via majority agreement and abstention

The system is designed to surface risk, not hide it.

1. Formal Definition of “Stability”

Two outputs are considered the same semantic object if:

They belong to the same domain (symptom / food / emotion / mind)

They reference overlapping or identical evidence spans in the journal text

Fields that MUST be stable

These are safety-critical:

Polarity (present ↔ absent)

Domain (emotion vs symptom, etc.)

Evidence grounding

Any disagreement here is treated as a hard safety violation.

Fields allowed to drift (within limits)

These reflect subjectivity and phrasing:

Free-text description

Intensity / arousal bucket

Time bucket

Drift in these fields is monitored, not eliminated.

2. Matching Algorithm (Deterministic)
Primary signal

Evidence span overlap (exact substring match)

This ensures:

Determinism

Auditability

No hallucinated alignment

Fallback (minimal & optional)

Simple heuristic similarity when evidence spans are paraphrased

Key design choice

I intentionally avoided embeddings or probabilistic matchers to keep the system:

Transparent

Deterministic

Easy to reason about in production health settings

3. Stability Metrics (Quantitative)

For each journal (3 runs), the system computes:

1️⃣ Agreement Rate

Fraction of semantic objects consistently extracted across runs
Indicates overall stability.

2️⃣ Polarity Flip Rate (High-Risk)

Percentage of objects where polarity changes across runs

This is treated as critical, even if rare.

3️⃣ Bucket Drift Rate

Changes in intensity / arousal / time buckets

Expected in subjective journals, but monitored to detect degradation.

Interpretation

High agreement ≠ safe by itself

Any polarity flip is unacceptable in women’s health contexts

4. Risk Framing (Women’s Health Context)
Acceptable variance

Wording differences

Intensity shifts (e.g., “medium” ↔ “high”)

Temporal ambiguity

These reflect lived experience and journaling style.

Dangerous variance

Polarity flips (e.g., “anxious” ↔ “not anxious”)

Domain confusion (emotion vs symptom)

Even a single polarity flip can:

Misrepresent emotional state

Trigger inappropriate downstream nudges

Erode user trust

Therefore, polarity disagreement is treated as a hard stop, not averaged away.

5. Production Implications
Downstream nudges

Unstable outputs can result in:

Contradictory reflections

Confusing or invalid suggestions

This system prevents that by abstaining when unsafe.

User trust

Explicit uncertainty is safer than confident inconsistency.
Users are more likely to trust a system that says “I’m not sure” than one that contradicts itself.

Auditability

Deterministic matching

Evidence-anchored objects

All runs preserved

This enables post-hoc review and clinical oversight.

6. Bonus: Stable Final Output (Consensus Builder)

Instead of selecting the “best” run, the system produces a conservative stable output:

Rules

Majority agreement → keep

Any polarity disagreement → mark as uncertain

Attribute disagreements → soften or mark unknown

No forced decisions

Result

Only insights that are stable across runs are surfaced.
Unstable or risky items are explicitly flagged or withheld.

This aligns with Ashwam’s emphasis on restraint over recall.

Visualization (Optional)

A simple bar chart summarizes per-journal:

Agreement rate

Polarity flip rate

Bucket drift rate

This visualization is meant to surface risk, not to optimize metrics.

Key Assumptions

Journals are independent and processed per-entry

Evidence spans are reliable anchors for object identity

Safety is prioritized over completeness

Abstention is acceptable (and preferred) in ambiguous cases

Tradeoffs & Design Choices

Chose simple, deterministic logic over complex similarity models

Avoided over-engineering metrics not required by the brief

Optimized for worst-case safety, not average performance

Limitations & Future Work

Evidence overlap may miss deep paraphrases

Bucket drift thresholds are heuristic

Negation handling could be further strengthened

With more time, I would:

Add targeted negation checks

Track drift trends over time

Integrate human-in-the-loop review for flagged cases

Final Takeaway

This system is intentionally conservative.

In women’s health, one unsafe output matters more than many correct ones.
The framework ensures that LLM variability is measured, surfaced, and controlled, rather than silently passed through to users.
