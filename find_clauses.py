import re

PATTERNS = {
    "confidentiality": re.compile(
        r"\b(confidentiality|non[- ]?disclosure|nda)\b", re.I
    ),
    "termination": re.compile(
        r"\b(termination|term\s+and\s+termination)\b", re.I
    ),
}


def find_clauses(text: str, *, selected=None):
    """Yield clause hits; optionally restrict to a subset."""
    selected = set(selected) if selected else PATTERNS.keys()

    for name, pat in PATTERNS.items():
        if name not in selected:
            continue
        for m in pat.finditer(text):
            yield {
                "clause": name,
                "start": m.start(),
                "end": m.end(),
                "snippet": text[m.start() : m.end() + 120].splitlines()[0],
            }
