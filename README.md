# Run-to-Run Variance & Stability Analysis (Exercise B)

## Context & Motivation
In women’s health, incorrect interpretation can be actively harmful.
For example, misclassifying anxiety as “absent” during a high-stress or hormonal phase, or flipping emotional polarity across runs, can invalidate lived experience and erode trust.

Because these journals may influence self-reflection, downstream nudges, or clinician conversations, stability and restraint matter more than recall.

Ashwam works with free-form women’s health journals. These journals are not clean datasets — they are human.

A single journal entry can include:
- Physical symptoms (“dull headache”, “bloating”, “low energy”)
- Emotional states (“edgy”, “anxious”, “not sad today”)
- Mental states (“scattered”, “racing thoughts”)
- Food and lifestyle context

For women especially, **expression naturally varies**:
- Mood and emotions can shift day-to-day
- Symptoms may appear, fade, or be described indirectly
- Hormonal cycles, sleep quality, stress, and context all affect language
- There are **no canonical labels** and no single ground truth

Because of this, **LLM outputs will vary across runs** — and that is expected.  
However, **unsafe variance is not acceptable**, especially in a health context.

The goal of this exercise is **not to maximize recall**, but to ensure that **no user-facing insight is produced unless it is stable and safe across multiple runs**.

---

## What I Built (High-Level Overview)

I built a **run-to-run stability framework** that:

1. Deterministically aligns extracted semantic objects across **3 independent LLM runs**
2. Measures instability using **safety-relevant metrics**
3. Explicitly detects **high-risk variance** (e.g., polarity flips)
4. Produces a **conservative, stable final output** using majority agreement and abstention

The system is intentionally designed to **surface risk rather than hide it**.

---

## Task 1: Formal Definition of “Stability”

Because wording varies naturally, stability cannot mean “exact text match”.

### When are two outputs considered the *same* object?

Two extracted items are considered the same **semantic object** if:
- They belong to the same domain  
  *(symptom / food / emotion / mind)*
- They reference overlapping or identical **evidence spans** in the journal text

Example:
> “felt edgy today” and “snapping at people for no reason”  
→ considered the same emotional signal if grounded in the same text span.

---

### Fields that **MUST be stable** (Safety-Critical)

These fields directly affect meaning and downstream behavior:

- **Polarity** (present ↔ absent)  
- **Domain** (emotion vs symptom, etc.)
- **Evidence grounding**

Any disagreement in these fields is treated as a **hard safety violation**.

Example:
> One run extracts *“anxious”*, another extracts *“not anxious”*  
→ This is unsafe and must not be resolved automatically.

---

### Fields allowed to drift (Within Limits)

These reflect human subjectivity and expression:

- Free-text phrasing
- Intensity / arousal bucket
- Time bucket

Drift here is **monitored**, not eliminated.

---

## Task 2: Matching Algorithm (Deterministic)

### Primary Signal: Evidence Span Overlap

Matching is anchored on **exact evidence span overlap**.

This guarantees:
- Determinism (same input → same output)
- Auditability
- No hallucinated alignment across runs

---

### Fallback (Minimal & Optional)

When wording differs but evidence is clearly related:
- Simple heuristic similarity is applied

I intentionally avoided embeddings or probabilistic matchers to keep the system:
- Transparent
- Easy to reason about
- Safe for production health workflows

---

## Task 3: Stability Metrics (Quantitative)

For each journal (3 runs), the system computes:

### - Agreement Rate
Fraction of semantic objects that consistently appear across runs.

**What it tells us:**  
How stable the extraction is overall.

---

### - Polarity Flip Rate (**High-Risk Metric**)
Percentage of objects whose polarity changes across runs.

Example:
- Run 1: *“Feeling anxious”*
- Run 3: *“Not anxious today”*

This is treated as **critical**, even if rare.

---

### - Bucket Drift Rate
Changes in:
- Intensity
- Arousal (for emotions)
- Time reference

Expected in subjective journaling, but monitored to detect degradation.

---

### How to interpret these metrics

- **High agreement does NOT automatically mean safe**
- **Any polarity flip is unacceptable** in a women’s health context

---

## Task 4: Risk Framing (Women’s Health Context)

### Acceptable Variance

These reflect lived experience and journaling style:
- Different wording for the same feeling
- Intensity shifts (e.g., “medium” ↔ “high”)
- Temporal ambiguity (“today” vs “last night”)

Example:
> “felt tired” vs “low energy by evening”  
→ acceptable variation

---

### Dangerous Variance

These directly affect meaning and care:

- **Polarity flips**  
  (“anxious” ↔ “not anxious”)
- **Domain confusion**  
  (emotion extracted as symptom)

Even a **single polarity flip** can:
- Misrepresent emotional state
- Trigger inappropriate downstream nudges
- Erode user trust

Therefore, polarity disagreement is treated as a **hard stop**, not averaged away.

---

## Task 5: Production Implications
In a women’s health product, unstable outputs can result in emotionally misaligned nudges — for example, offering calming advice when a user is explicitly distressed, or dismissing symptoms during menstruation or sleep deprivation.
This framework prevents such outcomes by abstaining when stability cannot be guaranteed, prioritizing safety and trust over completeness
### Downstream Nudges

If instability is not controlled, users may receive:
- Contradictory reflections
- Confusing or invalid suggestions

This system prevents that by **abstaining when unsafe**.

---

### User Trust

Explicit uncertainty is safer than confident inconsistency.

A user is more likely to trust:
> “I’m not sure yet”  
than  
> Conflicting or flip-flopping insights

---

### Auditability

The system is fully auditable because:
- Matching is deterministic
- All objects are evidence-anchored
- All 3 runs are preserved

This supports post-hoc review and clinical oversight.

---

## Task 6 (Bonus): Stable Final Output (Consensus Builder)

Instead of selecting a “best” run, the system produces a **conservative stable output**.

### Rules Used

- **Majority agreement → keep**
- **Any polarity disagreement → mark as `uncertain`**
- Attribute disagreements → soften or mark unknown
- No forced decisions

---

### Result

Only insights that are stable across runs are surfaced.  
Unstable or risky items are explicitly flagged or withheld.

This aligns directly with Ashwam’s emphasis on **restraint over recall**.

---

## Visualization (Optional)

A simple bar chart summarizes, per journal:
- Agreement rate
- Polarity flip rate
- Bucket drift rate

The goal of this visualization is **risk visibility**, not performance optimization.

---

## Key Assumptions

- Journals are independent and processed per entry
- Evidence spans are reliable anchors for object identity
- Safety is prioritized over completeness
- Abstention is acceptable (and preferred) in ambiguous cases

---

## Tradeoffs & Design Choices

- Chose simple, deterministic logic over complex similarity models
- Avoided over-engineering metrics not required by the brief
- Optimized for **worst-case safety**, not average performance

---

## Limitations & Future Work

Current limitations:
- Evidence overlap may miss deep paraphrases
- Bucket drift thresholds are heuristic
- Negation handling could be further strengthened

With more time, I would:
- Add targeted negation checks
- Track drift trends over time
- Integrate human-in-the-loop review for flagged cases

---

## Final Takeaway

This system is intentionally conservative.

In women’s health, **one unsafe output matters more than many correct ones**.

The framework ensures that LLM variability is **measured, surfaced, and controlled** — not silently passed through to users.
