# project.py

`project.py` runs the tools of the project.
Each command runs one tool of the folder `tools`.
The tools read their values from `tools/toolchain.toml` and from `project.toml`.
`docs/extern/project.toml.md` describes these values.
Do not change `project.py` or the files of `tools`.

## Requirements

- Python 3.11 or a later version.
- zig at the version of `[zig] version` in `tools/toolchain.toml`. The command `fetch` downloads this zig.

The tools use the zig in `build/zig` of the folder of `project.py` first.
If that zig is not there, the tools use the zig on the path.
The tools stop if the version of zig is not the pinned version.

## Commands

```sh
python project.py <command> [<option> ...]
```

| Command | Tool | Result |
| --- | --- | --- |
| `fetch` | `tools/fetch.py` | Downloads zig if zig is not there. Then fetches the sources and takes the dependencies. |
| `build` | `tools/build.py` | Takes the dependencies and builds all the artifacts. |
| `pack` | `tools/build.py --pack` | Builds all the artifacts. Then puts the package into a zip file. |
| `test` | `tools/test.py` | Builds all the artifacts. Then runs all the cases. |
| `check` | `tools/check.py` | Runs all the checks of the project. |
| `cla` | `tools/cla.py` | Decides if the author of a pull request signed `cla.md`. |

`project.py` gives its options to the tool without a change.
It ends with the exit status of the tool.
You can also run a tool alone, for example `python tools/build.py --debug`.
If the command is not in the table, `project.py` stops with the message
`project.py: name a command: fetch build pack test check cla`.

## Options

| Option | Result |
| --- | --- |
| `--root <folder>` | Uses the project in this folder. The default is the folder of `project.py`. |
| `--target <target>` | Builds for this target. The default is the target of this machine. |
| `--debug` | Replaces each variable that `[debug]` names with the value of `[debug]`. |
| `--out <folder>` | Puts the output into this folder. The default is the folder `build` of the project. |
| `--set <name>=<value>` | Gives a new value to a key of `[variables]`. You can use this option more than one time. |
| `--pack` | Puts the package into a zip file. The command `pack` gives this option to `tools/build.py`. |
| `--break` | Runs the false variant of each case. It is an option of `test` only. |
| `--commits <range>` | Checks the messages of the commits of this range of git. It is an option of `check` only. |

The command `fetch` always uses the target of this machine.
The command `test` runs only on a machine of the target.
With `--root`, the tools of one project can work on a different project, for example a project in `tests/data`.
zig and its caches stay in the folder of `project.py`.

## Output

- The output folder is `--out`, or the folder `build` of the project. Here, its name is `<build>`.
- The output folder of a target is `<build>/<target>`. With `--debug`, it is `<build>/<target>-debug`.
- An artifact is in the output folder of the target, or in its `folder` in that output folder.
- The steps of a kind put their temporary files into `<build>/<target>/obj`.
- `<build>/<target>/package.txt` lists the artifacts and the `beside` files, with the SHA-256 digest of each file.
  A different project can take these files as a dependency.
- `pack` writes one zip file, `<build>/<project>-<target>.zip`. `<project>` is the value of `[project] name`.
- Each case runs in its own empty folder, `<build>/<target>/cases/<group>/<number>`.
- `test` writes the output of the commands of all the cases into `<build>/<target>/said.txt`, but not with `--break`.
- The caches of zig are in `build/zig-cache` of the folder of `project.py`. Thus a build does not use a cache of the machine.

`build` writes the path of each artifact.
`pack` also writes the path of the zip, then the name of each file in the zip.

### The zip

`pack` puts these files into the zip:

- `package.txt`, and each file that `package.txt` lists, at its path in the output folder of the target.
- Each file of `include` and of each public folder, at its path in the project.
- `license`, and `license` of each folder of `third_party`.

## Cases

A case runs a command, and makes claims about its exit status and its output.
A group is a file of cases in `tests/cases`, or in a folder of `tests/cases`.
The name of a group is the path of the file in `tests/cases`, without `.toml`.
For example, the name of the group `tests/cases/tools/build.toml` is `tools/build`.
The command `test` passes if the claims of each case are true.

Each `[[case]]` has these keys:

| Key | Value |
| --- | --- |
| `name` | The name of the case. |
| `run` | The command, as a list. |
| `env` | Changes to the environment of the command. The key is the name of a variable. The value is a text, or `false` to remove the variable. |
| `stdin` | The text that `test` writes to the command, after the script of the case. |
| `script` | The steps that `test` does while the command runs. |
| `helper` | A second command that runs at the same time. |
| `files` | The text files that `test` writes before the command starts. The key is the path, and the value is the text. |
| `folders` | The folders that `test` makes before the command starts. The key is the path. The value is a list of artifacts or files to copy into the folder. |
| `claims` | The claims about the command. A case must make one claim or more. |
| `false` | The false variant of the case. Each case must have one. |

Each case starts in an empty folder, `{case}`.
The command runs in the folder of the project.
`test` replaces the variables in all the texts of a case, also in the texts of `files`.
`test` copies the files of `folders` without a change, and keeps their permissions. Thus a copy of a program can run.

A case fails if its command does not end in `[test] timeout` seconds. This is also true with `--break`.
If `tests/cases` holds no case, `test` writes `no case: tests/cases holds no case` and ends with the exit status 0.

### Claims

| Key | The claim is true if: |
| --- | --- |
| `status` | The command ends with this exit status. |
| `status_not` | The command does not end with this exit status. |
| `line` | Each text of the list is a full line of the output. |
| `has` | The output contains each text of the list. |
| `lacks` | The output contains no text of the list. |
| `order` | The output has each text of the list as a line, in this order. The spaces at the start and at the end of a line do not count. |
| `files` | After the command ends, each file contains its text. The key is the path, and the value is the text. |

The output is the text that the command writes to its output and to its errors.
Each `[[test.rule]]` of `project.toml` adds a claim to each case of its groups.

### Scripts

Each step of a `script` waits for a line of the output that contains the text `wait`.
Then the step does these actions, in this order:

1. `put` copies files. The key is the path, and the value is an artifact or a file.
2. `remove` removes the files of the list.
3. `type` writes this line to the command.

If the output ends before the text comes, `test` stops the steps.

### Helpers

A `helper` has a command `run`, a text `wait`, a text `stdin` and its own `claims`.
`test` starts the helper first, and waits for a line of its output that contains the text `wait`.
Then `test` starts the command of the case.
When the command of the case ends, `test` writes `stdin` to the helper, and waits for the end of the helper.
The claims of the helper must also be true.

An empty `helper` table means that the case has no helper. Thus a false variant can remove the helper.

### The break run

`python project.py test --break` runs the false variant of each case.
The keys of `false` replace the keys of the case.
Each path of `false.files` and of `false.folders` replaces only that path.
The claims of the case must then be false. A case that passes makes the break run fail.
Thus the break run shows that each case can fail.

`test` refuses a case that has no false variant, also without `--break`.
