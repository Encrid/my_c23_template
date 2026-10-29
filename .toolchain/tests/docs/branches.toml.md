# .toolchain/tests/cases/branches.toml

The group `branches` checks `.toolchain/tools/branches.py`, through `test --branches` of `.toolchain/tools/test.py`.
Each case runs `test.py` on a project of `.toolchain/tests/data/branches`, with its output in `{case}/out`.

| Project | Content |
| --- | --- |
| `missed` | The program `branchy` and its header `branchy.h`. One case runs it with `1`. Thus one function, two labels and six outcomes of conditions are not reached. One test with `\|\|` is in an argument of the macro `CHECKED`. |
| `reached` | The same program, with no function that no case calls and no macro. Four cases reach each outcome. |
| `empty` | A project with no source and no case. |
| `excused` | The program `defend`, whose guard no case reaches, and an exemption of `project.toml` that excuses the guard. |
| `badexempt` | The same program, with an exemption that states no reason and an exemption that matches no outcome. |
| `loaded` | The library `chooser`, with one condition, and the test program `loader` that opens it, calls it and closes it. The case `both` calls it with 1 and with 0. The case `one` calls it with 1. |
| `ended` | The program `ender`. With the argument `exit` it ends with `_Exit(1)`, with a different argument it calls `abort`, and with no argument it ends with 0. Its three cases run the three paths. Only the paths of `_Exit` and of `abort` make the condition `count > 1` true. |

| Case | Claim | False variant |
| --- | --- | --- |
| branches that no case reaches | `test` writes a line for a function, a label, a condition never false, a condition never true, a condition in a macro and a condition of the header. Then it writes `branches: 17 outcomes, 9 reached`, and stops. | The project `reached`. |
| each branch reached | `test` writes `branches: 16 outcomes, 16 reached`, and ends with 0. | The project `missed`. |
| branches of a project with no source | `test` writes `branches: 0 outcomes, 0 reached`, and ends with 0. | The project `reached`. |
| branches with a false variant | `test --branches --break` stops: `--branches runs each case one time`. | No `--break`. |
| an exemption excuses an unreached branch | `test` writes `branches: 4 outcomes, 3 reached, 1 exempt`, and ends with 0. | The project `badexempt`. |
| an outcome stays when the program ends with _Exit or abort | `test` on `ended` writes `branches: 7 outcomes, 7 reached`, and ends with 0. | `-k plain`, thus no case ends with `_Exit` or `abort`. |
| a closed library keeps its outcomes | `test` writes `branches: 3 outcomes, 3 reached`, and ends with 0. On macOS this needs the constructor that keeps the library mapped. | `-k one`, thus the condition is never false. |
| an exemption with no reason or no target is a fault | `test` writes the unreached branch, `this exemption states no reason` and `this exemption excuses no unreached outcome`, and stops. | The project `excused`. |
