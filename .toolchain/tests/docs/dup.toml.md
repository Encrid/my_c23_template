# .toolchain/tests/cases/dup.toml

The group `dup` checks `.toolchain/tools/dup.py`.
Each case but the last writes a small project into `{case}/p` with `files`, and runs `dup.py --root {case}/p`.
The text of each document starts with a heading and an empty line. Thus its third line holds the sentence.

| Case | Claim | False variant |
| --- | --- | --- |
| a passage of 8 shared words | `docs/a.md` and `docs/b.md` hold the same sentence of 8 words. `dup.py` writes `docs/a.md:3, docs/b.md:3: one two three four five six seven eight`, and ends with 1. | The last word of `docs/b.md` differs. |
| a passage of 7 shared words | The 2 documents share a sentence of 7 words. `dup.py` writes `no fault in 2 documents`. | The 2 documents share a sentence of 8 words. |
| a passage across 2 sentences | `docs/a.md` holds the 8 words in 2 sentences, and `docs/b.md` in 1. `dup.py` ends with 0. | `docs/a.md` holds them in 1 sentence. |
| a passage across 2 cells | `docs/a.md` holds the 8 words in 2 cells of a table. `dup.py` ends with 0. | `docs/a.md` holds them in 1 cell. |
| a passage in a fenced block | `docs/a.md` holds the 8 words in a fenced block. `dup.py` ends with 0. | The words are out of the block. |
| a citation in 2 documents | The 2 documents hold the same citation of `docs/c.md`. `dup.py` ends with 0. | The 2 documents hold the same words, with no code span and no heading between asterisks. |
| a passage of 2 scopes | `docs/a.md` and `.toolchain/docs/b.md` share 8 words. `dup.py` ends with 0. | `docs/b.md` also holds the 8 words. |
| the documents of this project | `folders` copies `readme.md`, the 6 guides and the documents of `.toolchain/docs` into `{case}`. `dup.py` writes `no fault in 32 documents`. | `{case}/docs/a.md` holds a sentence of `docs/contributing/tests.md`. |
