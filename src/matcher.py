

def evidence_overlap(span_a: str, span_b: str) -> bool:
    if not span_a or not span_b:
        return False
    a = span_a.lower()
    b = span_b.lower()
    return a in b or b in a
