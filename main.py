#!/usr/bin/env python3
"""Childhood memory entry for the make.fun bounty.

Writes one nostalgic childhood-memory sentence (at most 280 characters)
to /output/entry.txt, the file the house judge reads.

The sentence is a single warm minute from a childhood evening: steam
from grandmother's rice pot fogging a pair of glasses, a radio humming
low, and nobody asking the child to grow up yet.
"""

import os

ENTRY = (
    "At dusk my grandmother would lift the lid off the rice pot and the steam "
    "would fog my glasses, and for one warm minute the whole world was just "
    "her kitchen, the radio humming low, and nobody asking me to grow up yet."
)


GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 280


def count_chars(text: str) -> int:
    """Count Unicode code points, not bytes.

    The gate counts characters, so walk the string one code point at a
    time and tally them by hand. A byte count would over-count any
    multi-byte character — an emoji is one character here, not four
    bytes — so the explicit loop keeps the unit honest even if the
    entry ever gains an accent or an emoji.
    """
    total = 0
    for _ch in text:
        total += 1
    return total


def check_length(text: str) -> None:
    """Refuse anything outside the gate's 1 to 280 characters."""
    size = count_chars(text)
    if size < GATE_MIN_CHARS:
        raise ValueError(
            f"entry is empty ({size} characters); "
            f"gate needs at least {GATE_MIN_CHARS}"
        )
    if size > GATE_MAX_CHARS:
        raise ValueError(
            f"entry has {size} characters; "
            f"gate allows at most {GATE_MAX_CHARS}"
        )


def check_single_sentence(text: str) -> None:
    """Refuse anything that is not exactly one sentence.

    One sentence means exactly one full stop, and it must sit at the
    very end — no trailing words after it, no second stop hiding in
    an abbreviation. The count and the ending are checked separately
    so a failure says which rule broke.
    """
    stops = text.count(".")
    if stops != 1:
        raise ValueError(
            f"entry has {stops} full stops; exactly one sentence is required"
        )
    if text[-1] != ".":
        raise ValueError("entry must close with its single full stop")


def write_entry(text: str) -> str:
    """Validate the entry, then write it and return its path."""
    check_length(text)
    check_single_sentence(text)
    # The grader reads /output/entry.txt; OUTPUT_DIR lets a local run
    # point the same code at a scratch folder instead of the real one.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return path


def main() -> None:
    path = write_entry(ENTRY)
    print(f"wrote {count_chars(ENTRY)} characters to {path}")


if __name__ == "__main__":
    main()
