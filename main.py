#!/usr/bin/env python3
"""Write one word your ex would use to describe you.

The program writes exactly one word to ``entry.txt`` inside the
output directory (``$MAKEFUN_OUTPUT_DIR`` when set, otherwise
``/output``). The word is judged pairwise by a brief that wants the
funniest, most painfully honest word an ex would use:

* it must be exactly one word a real ex would say about a partner
  they once had;
* it must make the judge laugh out loud, through surprise, a sharp
  turn, or a word that lands harder than expected;
* it must sting with recognition, because it is painfully true and
  the entrant plainly knows it;
* it must land instantly, needing no explanation;
* it must feel relatable, naming something people have lived
  through too. A word that stings because it is true beats a word
  that only insults; meanness for its own sake does not count.

Candidates scored against that brief, best first:

* Unreachable — the sharp turn is built in: emotionally unreachable
  and literally never answers the phone. It laughs, it stings, it
  lands in one beat, and everyone has dated someone unreachable or
  been unreachable. Painfully true, never merely mean.
* Flaky — very ex-plausible and relatable, always cancelling, but
  the joke is single-note and it is one of the likeliest picks to
  duplicate.
* Avoidant — therapy-speak that is funny and true, but needs a beat
  for anyone outside the therapy-words crowd.
* Overthinker — painfully true and relatable, but the laugh is soft.
* Exhausting — a strong sting, but closer to an insult than a joke.
* Workaholic — specific and true, but a familiar punchline.
* Indecisive — painfully true, but no surprise in it.
* Clingy — the classic ex-word, and exactly for that reason flat
  and the most duplicated pick in the field.

"Unreachable" wins: the only candidate with a double meaning that
does the laughing and the stinging at once, in a single word that
needs no explanation. 11 characters, well inside the 24-character
gate, and short enough that the byte tie-break favours it.

Standard library only; no network, no randomness, no clock. Fully
deterministic: the same word, byte for byte, on every run.
"""

import os
import sys
from pathlib import Path

# The word: 11 characters, one word, no trailing spaces.
# The file holds the word plus a single trailing newline.
WORD = "Unreachable"

MAX_CHARS = 24


def main() -> int:
    if not WORD or not WORD.strip():
        print("error: entry word is empty", file=sys.stderr)
        return 1
    if len(WORD.split()) != 1:
        print("error: entry must be exactly one word", file=sys.stderr)
        return 1
    if len(WORD) > MAX_CHARS:
        print(
            f"error: entry word is {len(WORD)} characters, "
            f"over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.txt"
        target.write_text(WORD + "\n", encoding="utf-8")
        # Read it back and verify the round trip is exact, and that the
        # file holds exactly one word once the newline is stripped.
        content = target.read_text(encoding="utf-8")
        if content != WORD + "\n" or len(content.rstrip("\n").split()) != 1:
            print("error: entry.txt does not match the word", file=sys.stderr)
            return 1
    except OSError as exc:
        print(f"error: cannot write entry.txt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
