# tools/test.py

`test.py` builds the project with `build.py`, then runs the cases of `tests/cases`.

## Functions

| Function | Result |
| --- | --- |
| `environment(changes, values)` | Gives the environment of a command, with the changes of `env`. |
| `free_port()` | Gives a free port of this machine. |
| `started(argv, root, timeout, env)` | Starts a command, with a timer that stops it after `timeout` seconds. |
| `waited(running, text)` | Reads the output until a line contains the text. It gives false if the output ends first. |
| `typed(running, text)` | Writes a text to the command. |
| `ended(running, text)` | Writes the text, closes the input, and waits for the end of the command. It gives the status and the output. |
| `ordered(wanted, lines)` | Tells if the lines have each wanted line, in order. |
| `holding(path, text)` | Tells if a file is there and contains the text. |
| `holds(claims, lacks, code, said, values)` | Tells if each claim is true. |
| `source_of(item, outputs, values)` | Gives the file of an artifact, or a file of the project. |
| `placed(use, outputs, values)` | Writes the `files` of a case, and fills its `folders`. |
| `scripted(running, script, outputs, values)` | Does the steps of a script. |
| `made_false(case)` | Gives the false variant of a case. |
| `tried(config, values, outputs, where, case, broken)` | Runs one case. |
| `verdict(config, values, outputs, group, index, case, broken)` | Gives the verdict of one case. |
| `test(config, values, outputs, groups, broken)` | Runs all the groups, and writes each verdict. |
| `groups_of(values)` | Reads and checks the groups of `tests/cases`. |
| `main()` | Runs the command `test`. |

## main

`main` does these steps:

1. It builds with `build`, which stops if the target does not run on this machine.
2. It stops if an artifact is not linked: `the cases need what is linked: <names>`.
3. It reads the groups.
4. If there is no case, it writes `no case: tests/cases holds no case`, and ends.
5. It runs the groups.

The message of step 1 is `<target> does not run here: build it, and test it where it runs`.

## Groups

`groups_of` reads each file `tests/cases/**.toml`, in the order of the paths.
The name of a group is the path of its file in `tests/cases`, without `.toml`.
A file with no case gives no group.
`groups_of` stops if a case:

- has a key that a case does not have, or its false variant or its helper has such a key,
- claims nothing: `<path>: the case <name> claims nothing`,
- has no false variant: `<path>: the case <name> has no false variant`.

## A case

`tried` runs one case:

1. It empties the folder of the case, `<out>/cases/<group>/<number>`.
2. It adds the variables `{case}` and `{port}`. `{port}` is a new free port.
3. With `--break`, it uses the false variant of the case.
4. It writes the files, and fills the folders of the case.
5. If the case has a helper, it starts the helper, and waits for its text `wait`.
6. It starts the command, and does the steps of the script.
7. It writes `stdin` to the command, and waits for the end of the command.
8. If the case has a helper, it writes `stdin` of the helper, and waits for the end of the helper.

`tried` runs each command in the root, with a timer of `[test] timeout` seconds.
The timer stops a command that does not end in time.
`placed` and the steps `put` copy each file with its permissions. Thus a copy of a program can run on Linux and on macOS.

`made_false` makes the false variant: the keys of `false` replace the keys of the case.
For `files` and for `folders`, each path of `false` replaces only that path.

## Verdicts

`verdict` adds the `lacks` of each rule to the claims, but not the rules that exempt the group.

| Run | The claims | Verdict | The case |
| --- | --- | --- | --- |
| `test` | true | `as written` | passes |
| `test` | false | `differs` | fails |
| `test --break` | false | `fails, as it must` | passes |
| `test --break` | true | `still as written` | fails |
| both | a command does not end in time | `did not end in <timeout> seconds` | fails |

`test` writes `<case>: <verdict>` for each case. With `--break`, it writes `<case>, made false: <verdict>`.
For a case that fails, it writes the status and the output of each command.
After each group, it writes the number of its cases and the number of the cases that passed.
If a case failed, `test` stops with the names of the cases that failed.

## Claims

`holds` tells if each claim of a case is true. It replaces the variables in each text of the claims.
The output of a command is what it writes to its output and to its errors, without the carriage returns.
A claim `line` compares full lines. A claim `order` ignores the spaces at the start and at the end of a line.
