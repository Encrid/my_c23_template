# The build

The script `build.py` builds, tests and checks a project.
The file `build.config.toml` holds all the values that `build.py` uses.
To change the build, change `build.config.toml`. Do not change `build.py`.

## Requirements

- Python 3.11 or a later version. The script reads the configuration with `tomllib`.
- zig at the version in `[zig] version`.

The script uses the zig in `[zig] folder` first. If that zig is not there, the script uses the zig on the path.
The script stops if the version of zig is not the pinned version.

## Commands

    python build.py <command> [--root <folder>] [--target <target>] [--debug] [--out <folder>]
                              [--set <name>=<value>] [--break]

| Command | Result |
| --- | --- |
| `fetch` | Downloads zig for this machine if the pinned zig is not there, and checks the SHA-256 digest of the archive. Then fetches the sources. Then takes the dependencies. |
| `build` | Takes the dependencies and builds all the artifacts. |
| `test` | Builds all the artifacts and the test programs, does the feature check, and runs all the cases. |
| `style` | Runs each tool in `[style] tools`. |

| Option | Result |
| --- | --- |
| `--root <folder>` | Uses the project in this folder. The default is the folder of `build.py`. |
| `--target <target>` | Builds for this target. The default is the target of this machine. |
| `--debug` | Replaces each variable with the value in `[debug]`. |
| `--out <folder>` | Puts the output in this folder. The default is `[build] folder` in the project. |
| `--set <name>=<value>` | Gives a new value to a variable of `[variables]`. You can use this option more than one time. |
| `--break` | Runs the false variant of each case, or makes the claims of the case false. Use it with `test`. |

The `test` command runs only on a machine of the target.

Each project has its own copy of `build.py`, `tools/style.py` and `tools/c23.py`, in its root folder.
Copy the three files from `c23` without a change. Then run `python build.py <command>` in the root folder of the project.

With `--root`, a copy of `build.py` can also build a project in a different folder. For example:

    python ../c23/build.py test --root .

## Output

- The output folder of a target is `<out>/<target>`. With `--debug`, it is `<out>/<target>-debug`.
- An artifact is in the output folder of the target, or in its `folder` in that output folder.
- A test program is `<out>/<target>/tests/<name>`, with the extension of the target.
- The steps of a kind put their temporary files in `<out>/<target>/obj`.
- Each case runs in its own empty folder, `<out>/<target>/cases/<group>/<number>`.
- The caches of zig are in `<out>/<cache>`. Thus a build does not use a cache of the machine.
- The file `<out>/<target>/package.txt` lists the artifacts and the `beside` files, with the SHA-256 digest of each file.
  A different project can use this list to take the artifacts as a dependency.

## Variables

A text in the configuration can contain variables. A variable is a name in braces, for example `{root}`.
The script replaces each variable with its value before it uses the text.

The script gives these variables:

| Variable | Value |
| --- | --- |
| `{root}` | The folder of the project. |
| `{build}` | The output folder, `--out` or `[build] folder`. |
| `{out}` | The output folder of the target. |
| `{target}` | The name of the target. |
| `{home}` | The name of the target of this machine. |
| `{python}` | The Python program that runs `build.py`. |
| `{script}` | The file `build.py`. |
| `{zig}` | The zig program. |
| `{case}` | The folder of a case, in a case only. |
| `{port}` | A free port of this machine, in a case only. Each case gets a new port. |

Each key of `[targets.<target>]` is also a variable, for example `{exe}` and `{library}`.
Each key of `[variables]` is a variable. Each dependency, each source and each tool is a variable too.
A path in a variable uses `/` as the separator, on all systems.

A variable can have a list as its value.
If a list variable is a full item of a list, the items of the variable replace it.
If a list variable is part of a text, give a separator after a colon.
For example, in the TOML text `'{manifest:\0}'`, the separator is the two characters `\0`.
In the TOML text `"{manifest:\u0000}"`, the separator is the character with the code 0.

## Dependencies

A dependency is a folder of files that a different project makes.
Each `[[dependency]]` has a list of its files, with the SHA-256 digest of each file.
The list is a text file. A line is `<key> <value>`, or `<digest>  <file>`.

The script copies the files of each dependency into its `into` folder.
It copies a file only if the copy is not there or if the copy is different.
It stops if a file does not have the digest that the list gives.
It also stops if two dependencies do not agree, as each `[[agree]]` tells.
In these two cases, the script does not change a file.

The command `make` of a dependency runs before the script reads the list.

## Sources

A source is an archive of files that a different maker publishes, for example the source code of a program.
Each `[[source]]` gives the address of the archive and its SHA-256 digest.

The command `fetch` does these steps for each source:

1. It removes the files of the `into` folder, and downloads the archive into the folder.
2. It stops if the archive does not have the digest of the source.
3. It unpacks the archive, and removes the archive.
4. It applies each patch of `patches` to the files in the `top` folder, in the order of the list.
5. It writes the file `fetched.txt` in the `into` folder. The file holds the digest of the archive and the digest of each patch.

The script stops if a patch does not apply.
A patch applies only if each line of its context is in the file, at the line that the patch gives.
The script reads a patch with the line ends of Windows or of Linux.

If `fetched.txt` holds the digests of the configuration, `fetch` does not download the archive again.
The commands `build` and `test` do not download a source.
They stop if `fetched.txt` does not hold the digests of the configuration. Then run `fetch`.

## Tools

Each key of `[tools]` is the name of a program, and its value is the path of the program.
The path does not include the extension of the program. The script finds the extension.
The script stops if a program is not there.

## Kinds and artifacts

An artifact is a file that the build makes: a program, a library or a module.
Each `[[artifact]]` has a kind. A kind is a table `[kinds.<kind>]` with the steps that make an artifact of that kind.

A step does one of these actions:

| Key | Action |
| --- | --- |
| `run` | Runs a command, in the folder of the project. |
| `section`, `text` | Adds a custom section of WebAssembly to the artifact, with this name and this text. |
| `contains` | Makes sure that the bytes of the artifact contain this text. |
| `copy` | Copies the first file to the second file. |
| `rename` | Moves the first file to the second file. |

The steps can use these variables of the artifact:

| Variable | Value |
| --- | --- |
| `{name}` | The name of the artifact. |
| `{output}` | The file of the artifact. |
| `{work}` | The start of the name of a temporary file. |
| `{sources}` | The files that match the patterns of `sources`. |
| `{defines}` | Each item of `defines`, after `-D`. |
| `{include}` | Each folder of `include`, after `-I`. |
| `{link}` | The files of `link`. |
| `{manifest}` | The items of `manifest`. |

An artifact can have variants. A variant is a copy of the artifact with a different name and some different keys.
A variant with `unstamped = true` does not do the `section` steps.

If a file of `link` is not there, the script does the `unlinked` steps of the kind, and it does not copy the `beside` files.
Thus a build for a different target can compile the sources and not link them.
If the kind has no `unlinked` steps, the script stops.

## The tests

A case runs a command and makes claims about its exit status and its output.
The test run passes if the claims of each case are true.

### Test programs

The script builds each file in `[test] programs` as one program for the target.
Each test program also gets the sources of the artifact in `[test] artifact`, but not the file in `[test] entry`.
A test program passes if it ends with the exit status 0.
The test programs are the group `programs`.

### Groups of cases

Each file in `[test] groups` is a group of cases. The name of the group is the name of the file, without its extension.
Each `[[case]]` in the file has these keys:

| Key | Value |
| --- | --- |
| `name` | The name of the case. |
| `run` | The command, as a list. |
| `env` | Changes to the environment of the command. The key is the name of a variable. The value is the text of the variable, or `false` to remove the variable. |
| `stdin` | The text that the script writes to the command, after the script of the case. |
| `script` | Steps that the script does while the command runs. |
| `helper` | A second command that runs at the same time. |
| `files` | Text files that the script writes before the command starts. The key is the path, and the value is the text. |
| `folders` | Folders that the script makes before the command starts. The key is the path, and the value is a list of artifacts or files that the script copies into the folder. |
| `claims` | The claims about the command. |
| `false` | The false variant of the case. |

Each case starts in an empty folder, `{case}`.
The script replaces the variables in all the texts of a case.
A case fails if its command does not end in `[test] timeout` seconds. This is also true with `--break`.
If the configuration has no case and no test program, the `test` command says so and ends with the exit status 0.

### Claims

| Key | The claim is true if: |
| --- | --- |
| `status` | The command ends with this exit status. |
| `status_not` | The command does not end with this exit status. |
| `line` | Each text in the list is a full line of the output. |
| `has` | The output contains each text in the list. |
| `lacks` | The output does not contain a text in the list. |
| `order` | The output has each text in the list as a line, in this order. The script ignores the spaces at the start and at the end of a line. |
| `files` | After the command ends, each file contains its text. The key is the path, and the value is the text. |

Each `[[test.rule]]` adds a claim to each case: the output does not contain the text `lacks`.
The rule does not apply to the groups in `exempt`.

### Scripts

Each step of a `script` waits for a line of the output that contains the text `wait`. Then the step does these actions, in this order:

- `put`: copies files. The key is the path, and the value is an artifact or a file.
- `remove`: removes the files in the list.
- `type`: writes this line to the command.

If the output ends before the text comes, the script stops the steps.

### Helpers

A `helper` has a command `run`, a text `wait`, a text `stdin` and its own `claims`.
The script starts the helper first, and waits for a line that contains the text `wait`.
Then it runs the command of the case.
When the command of the case ends, the script writes `stdin` to the helper, and waits for the end of the helper.
The claims of the helper must also be true.
An empty `helper` table means that the case has no helper. Thus a false variant can remove the helper.

### The break run

The command `python build.py test --break` runs each case in a different way:

- If the case has a `false` variant, the script runs the false variant. The claims of the case must be false.
  The keys of `false` replace the keys of the case. Each path in `false.files` and `false.folders` replaces only that path.
- If the case has no `false` variant, the script makes the claims false. The case must then fail.

If a case passes in the break run, the break run fails.
Thus the break run shows that each case can fail.

### The feature check

Each regular expression in `[test] features` has one capture group.
The `test` command applies each expression to the sources of the artifact in `[test] artifact`.
Each captured name must occur in the name or the command of a case, or in a test program.
If a name does not occur, the test run fails and shows the name.
The template captures the name of each function that is not static.

## The coding style

The command `python build.py style` runs each tool in `[style] tools`, from the folder of `build.py`.
Each tool reads `build.config.toml` in the folder of the project.
The tool `tools/style.py` checks the rules of `docs/intern/style.md`.
The tool `tools/c23.py` finds older spellings that C23 replaces, for example `NULL`.

The tool `tools/style.py` checks the names of the files that `git ls-files` shows.
If the folder is not a git repository, the tool checks all the files, but not the files in `[build] folder`.

## Continuous integration

A project that `template.py` makes gets the workflows of a preset in `.github/workflows/`.
The preset `cross-platform` runs `fetch`, `style` and `test` on one runner for each of five targets.
It builds `aarch64-windows-gnu` on the Windows runner, and does not run it.

## The configuration

### [project]

| Key | Value |
| --- | --- |
| `name` | The name of the project. The script `template.py` sets it. |
| `owner` | The owner of the copyright, in the legal notice. |
| `licence` | The line of the licence, in the legal notice. |

### [zig]

| Key | Value |
| --- | --- |
| `version` | The pinned version of zig. |
| `folder` | The folder that `fetch` fills. |
| `url` | The address of the archive. The script puts the values in `{version}`, `{host}` and `{format}`. |
| `archives.<target>` | For a machine of the target: the `host` and the `format` of the archive, and its `sha256` digest. |

### [build]

| Key | Value |
| --- | --- |
| `folder` | The default output folder. |
| `cache` | The folder of the zig caches, in the output folder. |

### [variables] and [debug]

Each key of `[variables]` is a variable. A key must not have the name of a variable that the script gives, or of a key of a target.
With `--debug`, each key of `[debug]` replaces the variable with the same name.

| Key | Value |
| --- | --- |
| `language` | The flags of the language. |
| `optimize` | The flags of the optimization. `[debug]` gives the flags of a debug build. |
| `float` | The flags of the floating-point rules. |
| `sample` | The folder of the example dependency. |
| `sample_patch` | The patch of the example source. |
| `sample_digest` | The digest of the archive of the example source. |

### [targets.\<target\>]

| Key | Value |
| --- | --- |
| `runs_on` | The system and the processor that Python gives for a machine of the target. An empty list means: build only. |
| `triple` | The target for zig, with the range of versions of the system. |
| `cpu` | The processor model. |
| `exe` | The extension of a program. |
| `library` | The extension of a shared library. |
| `define` | The macros that the system needs. |
| `pic` | The flags for code that a shared library can hold. |
| `rpath` | The flags that tell a program to find a library in its own folder. |
| `soname` | The flags that give a shared library its name, without its folder. |
| `stack` | The linker flag for the size of the stack. |
| `errno` | The flag that tells if a math function sets `errno`. |

A project can add more keys. Each key is a variable.

### [tools]

| Key | Value |
| --- | --- |
| `<name>` | The path of the program, without its extension. |

### [[dependency]]

| Key | Value |
| --- | --- |
| `name` | The name of the dependency. The variable `{<name>}` is its `into` folder. |
| `from` | The folder that has the files. |
| `list` | The list of the files, in `from`. |
| `into` | The folder that gets the copies. |
| `make` | Optional. A command that runs first. |
| `optional` | Optional. If `true` and the list is not there, the script does not take the dependency and continues. |

### [[source]]

| Key | Value |
| --- | --- |
| `name` | The name of the source. The variable `{<name>}` is its `top` folder, in its `into` folder. |
| `url` | The address of the archive. If the text has no `://`, it is a file of the project. |
| `sha256` | The SHA-256 digest of the archive. |
| `into` | The folder that gets the files. |
| `top` | Optional. The folder in the archive that holds the files. |
| `patches` | Optional. The patches, as files of the project, in the order that the script applies them. |

### [[agree]]

| Key | Value |
| --- | --- |
| `keys` | The keys that must have the same value, as `<dependency>.<key>`. The script ignores a dependency that it did not take. |
| `length` | The number of characters at the start of each value that the script compares. |

### [kinds.\<kind\>]

| Key | Value |
| --- | --- |
| `output` | The name of the file of an artifact. |
| `steps` | The steps that make an artifact. |
| `unlinked` | Optional. The steps if a file of `link` is not there. |

### [[artifact]]

| Key | Value |
| --- | --- |
| `name` | The name of the artifact. It can contain variables, for example `{system}`. |
| `kind` | The kind of the artifact. |
| `sources` | The patterns of the sources, from the folder of the project. |
| `include` | Optional. The folders of the headers. |
| `defines` | Optional. The macros, without `-D`. |
| `link` | Optional. The files that the artifact links. |
| `beside` | Optional. The files that the script copies into the folder of the artifact. |
| `manifest` | Optional. A list of texts for the steps. |
| `folder` | Optional. The folder of the artifact, in the output folder of the target. |
| `target` | Optional. The target of the artifact, if it is not the target of the build. |
| `variants` | Optional. The variants. Each variant has a `name`, and can have the other keys and `unstamped`. |

### [test]

| Key | Value |
| --- | --- |
| `timeout` | The maximum time of a case, in seconds. |
| `artifact` | The artifact of the test programs and of the feature check. Optional if `programs` and `features` are empty. |
| `entry` | The source with the `main` function. The test programs do not get it. Optional if `programs` is empty. |
| `programs` | The patterns of the test programs. |
| `groups` | The patterns of the files of the groups of cases. |
| `features` | The regular expressions of the feature check. |
| `rule` | Optional. The rules of the groups. Each rule has `lacks` and `exempt`. |

### [style]

| Key | Value |
| --- | --- |
| `root` | The root of the project, relative to `build.config.toml`. |
| `tools` | The tools that `style` runs, relative to the folder of `build.py`. |
| `ours` | The patterns of the C files of the project. |
| `held` | The patterns of the files that must follow the style. |
| `exceptions` | The page with the section "Exceptions". |
| `columns` | The maximum number of columns in a line. |
| `lines` | The maximum number of lines in the body of a function. |
| `functions` | The maximum number of functions in a file. |
| `arguments` | The maximum number of arguments of a function. |
| `branches` | The maximum number of branches in one `if`. |
| `depth` | The maximum depth of nested branches. |
