#!/usr/bin/env python3
"""
clausecraft_extract.py
----------------------
Turn PDF, DOCX or TXT contracts into plain text and locate key clauses.
"""

from pathlib import Path
import sys
import argparse
import textwrap

# ── third-party libs ───────────────────────────────────────────────────
try:
    from pdfminer.high_level import extract_text as pdf_to_text
except ImportError:
    pdf_to_text = None

try:
    import docx  # python-docx
except ImportError:
    docx = None
# ────────────────────────────────────────────────────────────────────────
from find_clauses import find_clauses   # <–– your regex clause finder
# ────────────────────────────────────────────────────────────────────────


def file_to_text(path: Path) -> str:
    """Return the entire document as UTF-8 text."""
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        if pdf_to_text is None:
            raise ValueError("pdfminer.six not installed – `pip install pdfminer.six`")
        return pdf_to_text(str(path))

    if suffix in {".docx", ".doc"}:
        if docx is None:
            raise ValueError("python-docx not installed – `pip install python-docx`")
        document = docx.Document(str(path))
        return "\n".join(p.text for p in document.paragraphs)

    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")

    raise ValueError(f"Unsupported file type: {suffix}")


def preview(text: str, max_chars: int = 500) -> str:
    text = text.strip().replace("\n", " ")
    return textwrap.shorten(text, width=max_chars, placeholder=" …")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract contract text and optionally locate clauses."
    )
    parser.add_argument("file", help="Path to the contract file")
    parser.add_argument(
        "--clauses",
        nargs="*",
        metavar="CLAUSE",
        default=["confidentiality", "termination"],
        help="Clause names to search (default: confidentiality termination)",
    )
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        sys.exit(f"❌ File not found: {path}")

    try:
        raw = file_to_text(path)
    except Exception as exc:
        sys.exit(f"❌ {exc}")

    # ── preview ────────────────────────────────────────────────────────
    print("\n📄  Text preview (first ~500 chars):\n")
    print(preview(raw))

    # ── clause search ─────────────────────────────────────────────────
    hits = list(find_clauses(raw, selected=args.clauses))
    if hits:
        print("\n🔍  Clause hits:")
        for h in hits:
            print(f"[{h['clause'].upper():15}] …{h['snippet']}…")
    else:
        print("\n🔍  No specified clauses found.")

    # ── save full text ────────────────────────────────────────────────
    out_path = path.with_suffix(".txt")
    out_path.write_text(raw, encoding="utf-8")
    print(f"\n✅ Extraction finished. Full text saved to: {out_path}")


if __name__ == "__main__":
    main()
