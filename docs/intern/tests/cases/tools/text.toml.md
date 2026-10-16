# tests/cases/tools/text.toml

The group `tools/text` checks `tools/text.py`.
Each case writes a project into `{case}` with `files`, and runs `text.py` on `{case}`.
The `project.toml` of each project gives the `owner` and the `licence` of the template.
The false variant of a case changes the file that has the fault.

The project `clean` has five files with no fault:

- `project.toml`,
- `project.py`, which starts with the legal notice,
- `a.toml` in `tests/cases`, and `ci.yml` in `.github/workflows`,
- the document `a.md` in `docs`.

In `project.py`, `a.toml` and `ci.yml`, a `#` is in a string.

| Case | Claim | False variant |
| --- | --- | --- |
| files with no fault | `text.py` checks `clean`, writes `no fault in 5 files`, and ends with 0. | `a.toml` has a comment. |
| a character that is not ASCII | A line of `a.md` has the letter U+00E9: `docs/a.md:3: a character that is not ASCII`. | The letter `e`. |
| a file that [check] unicode names | `[check] unicode` names `docs/*.md`, thus the letter U+00E9 in `a.md` is not a fault. | `project.toml` has no `[check]`. |
| a Python file without the legal notice | `project.py:1: the file does not start with the legal notice`. | `project.py` starts with the notice. |
| a notice with two owners | A second line of copyright, with a different owner, is not a fault. | The second line has no `Copyright (C)`. |
| a comment in a Python file | `project.py:4: a comment`. | No comment. |
| a string statement | A docstring: `project.py:4: a string statement`. | No docstring. |
| a comment in a TOML file | `tests/cases/a.toml:1: a comment`. | The `#` is in the string. |
| a comment in a YAML file | `.github/workflows/ci.yml:1: a comment`. | The `#` is in a string. |
| a comment in a document | `a.md` has an HTML comment: `docs/a.md:3: a comment`. | No HTML comment. |
