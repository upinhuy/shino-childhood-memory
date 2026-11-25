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


def count_chars(text: str) -> int:
    """Count Unicode code points, not bytes.

    Python 3 strings are sequences of code points, so len() already does
    this — the helper exists to make the gate's unit explicit and to keep
    the check readable even if the entry ever gains an emoji or accent.
    """
    return sum(1 for _ in text)


def check_length(text: str) -> None:
    """Refuse anything outside the gate's 1 to 280 characters."""
    size = count_chars(text)
    if size < 1:
        raise ValueError("refusing to write a blank entry")
    if size > 280:
        raise ValueError(
            f"refusing to write entry of {size} characters: "
            "gate allows 1 to 280"
        )


def check_single_sentence(text: str) -> None:
    """Refuse anything that is not exactly one sentence."""
    if text.count(".") != 1:
        raise ValueError("entry must contain exactly one sentence")
    if not text.endswith("."):
        raise ValueError("entry must end with a period")


def write_entry(text: str) -> str:
    """Validate, then write the entry and return its path."""
    check_length(text)
    check_single_sentence(text)
    # The grader reads /output/entry.txt; OUTPUT_DIR lets a local run
    # point the same code at a scratch folder instead.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main() -> None:
    path = write_entry(ENTRY)
    print(f"wrote {count_chars(ENTRY)} characters to {path}")


if __name__ == "__main__":
    main()
