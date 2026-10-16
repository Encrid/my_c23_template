# tests/cases/tools/check.toml

The group `tools/check` checks `tools/check.py`.
The first two cases run `check.py` on the project that runs the cases.
Thus they pass only if each check of that project passes.

| Case | Claim | False variant |
| --- | --- | --- |
| every check | `check.py` writes the name of each tool in the order of `TOOLS`, then `every check passes`, and ends with 0. | `check.py` checks the empty folder `{case}`. |
| a range of commits | With `--commits nothing..nowhere`, only `commits.py` fails: `check.py: failed: commits`. | No `--commits`. |
| a tool that is not there | `folders` copies `check.py`, `shared.py` and `toolchain.toml` into `{case}/tools`. That copy finds no other tool: `check.py: failed: layout text prose pseudo xref cover licence commits style c23`. | The `check.py` of the project checks `{case}`. Some checks pass there. |
