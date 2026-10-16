# tests/cases/tools/commands.toml

The group `tools/commands` checks `project.py`.
Its cases run `project.py` on the project in `tests/data/tools/take`, with the output in `{case}/out`.

| Case | Claim | False variant |
| --- | --- | --- |
| the command fetch | `fetch` writes the path of zig. | `build`. |
| the command build | `build` writes `package.txt`. | `fetch`. |
| the command pack | `pack` writes the path of the zip. | `build`. |
| the command test | `test` writes `no case: tests/cases holds no case`. | `build`. |
| a command that project.py does not know | `project.py nothing` stops: `project.py: name a command: fetch build pack test check cla`. | `test`. |
| the exit status of a tool | `build --target nowhere` ends with the status of `build.py`: `build.py: no target nowhere`. | No `--target`. |

The commands `check` and `cla` have their cases in the groups of their tools.
