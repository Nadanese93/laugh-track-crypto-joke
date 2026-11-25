"""Write the Laugh Track crypto trading joke entry to entry.txt.

Reads the output directory from MAKEFUN_OUTPUT_DIR and writes
entry.txt (UTF-8, no trailing newline). After writing, the file is
read back and its bytes are compared against the expected entry, so a
truncated or altered write is caught instead of silently passing.
"""

import os
import sys

ENTRY_TEXT = "I set a price alert for Bitcoin at $100,000. It went off. My portfolio is still down."

MAX_CHARS = 200


class BlankError(ValueError):
    """The entry text is empty or whitespace-only."""


class MultiLineError(ValueError):
    """The entry text spans more than one line."""


class LengthError(ValueError):
    """The entry text is outside the 1-200 character gate."""


class WriteMismatchError(RuntimeError):
    """The bytes read back from entry.txt differ from the entry text."""


def validate(text):
    """Validate the entry text against the contest gate.

    Raises a distinct error type for each failure mode so callers can
    tell a blank entry from a multi-line one or a length violation.
    """
    if not text or not text.strip():
        raise BlankError("entry text must not be blank")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry text must be a single line")
    if not 1 <= len(text) <= MAX_CHARS:
        raise LengthError(
            "entry text must be 1-200 characters, got %d" % len(text)
        )


def write_entry(out_dir):
    """Write entry.txt and verify it by reading it back."""
    validate(ENTRY_TEXT)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    expected = ENTRY_TEXT.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(expected)
    with open(out_path, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise WriteMismatchError(
            "entry.txt read-back mismatch: wrote %d bytes, read %d bytes"
            % (len(expected), len(actual))
        )
    return out_path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    write_entry(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
