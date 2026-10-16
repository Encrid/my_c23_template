# tests/cases/tools/text.toml

The group `tools/text` checks `tools/text.py`.
Each case runs `text.py` on `{case}`. `files` writes the files of the case, and `folders` copies the other files.
The false variant of a case changes the file that has the fault.

| File | Content |
| --- | --- |
| `project.toml` in `tests/data/tools/text` | The `owner` and the `licence` of the template. Each case copies it, or the next file. |
| `project.toml` in `tests/data/tools/text/unicode` | The same values, and a `[check] unicode` that names `docs/*.md`. |

The project `clean` has five files with no fault:

- `project.toml`,
- the `project.py` of the template, which starts with the legal notice,
- `a.toml` in `tests/cases`, and `ci.yml` in `.github/workflows`, which each have a `#` in a string,
- the document `a.md` in `docs`.

A Python file of a case has no legal notice if the fault of the case is a different fault. Thus the fault is on line 1.

| Case | Claim | False variant |
| --- | --- | --- |
| files with no fault | `text.py` checks `clean`, writes `no fault in 5 files`, and ends with 0. | `a.toml` has a comment. |
| a character that is not ASCII | A line of `a.md` has the letter U+00E9: `docs/a.md:3: a character that is not ASCII`. | The letter `e`. |
| a file that [check] unicode names | `[check] unicode` names `docs/*.md`, thus the letter U+00E9 in `a.md` is not a fault. | `project.toml` has no `[check]`. |
| a Python file without the legal notice | `project.py:1: the file does not start with the legal notice`. | `text.py` checks `{case}/fixed`, which has the `project.py` of the template. |
| a notice with two owners | A second line of copyright, with a different owner, is not a fault. | The second line has no `Copyright (C)`. |
| a notice of a different holder | The line of copyright names `Someone`, not the `owner` of `project.toml`. It is not a fault. | The notice has no line of the licence. |
| a comment in a Python file | `project.py:1: a comment`. | No comment. |
| a string statement | A docstring: `project.py:1: a string statement`. | No docstring. |
| a comment in a TOML file | `tests/cases/a.toml:1: a comment`. | The `#` is in the string. |
| a comment in a YAML file | `.github/workflows/ci.yml:1: a comment`. | The `#` is in a string. |
| a comment in a document | `a.md` has an HTML comment: `docs/a.md:3: a comment`. | No HTML comment. |
