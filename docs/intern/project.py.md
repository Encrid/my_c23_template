# project.py

`project.py` gives each command to one tool of the folder `tools`.
It holds no other logic.

## Commands

`COMMANDS` gives the tool of each command, and the options that the tool gets first.

| Command | Tool | First options |
| --- | --- | --- |
| `fetch` | `tools/fetch.py` | |
| `build` | `tools/build.py` | |
| `pack` | `tools/build.py` | `--pack` |
| `test` | `tools/test.py` | |
| `check` | `tools/check.py` | |
| `cla` | `tools/cla.py` | |

## main

`main` does these steps:

1. It reads the command, which is the first argument.
2. If `COMMANDS` does not have the command, it stops: `project.py: name a command:`, then the commands.
3. It runs the tool with the Python that runs `project.py`.
4. It gives the tool the first options, then the other arguments.
5. It ends with the exit status of the tool.
