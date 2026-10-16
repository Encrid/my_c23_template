# tests/cases/tools/build.toml

The group `tools/build` checks `tools/build.py`, and the configuration and the variables of `tools/shared.py`.
Its cases run `build.py` or `test.py` on a project in `tests/data/tools/build`, with the output in `{case}/out`.

| Project | Content |
| --- | --- |
| `built` | The library `greet`, the program `greeter`, and the artifact `stamped` with its variant `plain`. |
| `copy` | The artifact `copy.txt` of the kind `file`. The variables `tool`, `source` and `linked` give its tool, its source and its link. |
| `twice` | `[variables] language`, a key that `tools/toolchain.toml` also gives. |
| `builtin` | `[variables] root`, the name of a variable that the tools give. |
| `unknown` | An artifact with the name `{named}`. The variable `named` is `{nothing}`, which has no value. |
| `listed` | An artifact with the name `{named}`. The variable `named` is `{language}`, a list in a text. |

In `built`, `greet` gets its greeting from `defines`.
`greeter` includes `include/greet.h`, links `greet`, and has `greet` beside it in its folder.
`greeter` also compiles `src/os/{system}/os.c`, and writes `hello from a library, on <system>`.
The case `greeter` of `built` runs `greeter`. Its false variant runs a copy of `greeter` without the library.

The kind `stamped` copies `src/note.txt` to a work file, renames the work file to the output, and adds the section `said`.
Then it checks that the output contains `{said}`. The default of `said` is `written`, a word of `note.txt`.
The section holds the items of `manifest` with commas between them: `first,second`.
The variant `plain` is unstamped.

| Case | Claim | False variant |
| --- | --- | --- |
| a program linked with a library | `test` on `built` passes the case `greeter`. | `test --break`. |
| a variant without its section | With `--set said=first,second`, `build` stops: `plain.txt does not hold 'first,second'`. | No `--set`. |
| a build for debugging | With `--debug`, `package.txt` is in `{case}/out/{target}-debug`. | No `--debug`. |
| a package in a zip | `build --pack` writes the path of the zip, and the names of the files in it. | No `--pack`. |
| a variable that [variables] does not have | `--set nowhere=1` stops `build`: `--set nowhere=1: [variables] has no nowhere`. | No `--set`. |
| a key in project.toml and in toolchain.toml | `build` on `twice` stops: `project.toml states variables.language, and toolchain.toml states it too`. | `build` on `copy`. |
| a built-in variable in [variables] | `build` on `builtin` stops: `[variables] names a built-in variable or a key of a target: root`. | `build` on `copy`. |
| a target that the toolchain does not have | `--target nowhere` stops `build`: `no target nowhere; the targets:`. | No `--target`. |
| a tool that is not there | `--set tool=nowhere` stops `build`: `the tool interpreter is not at nowhere`. | No `--set`. |
| sources that match no file | `--set source=none.txt` stops `build`: `no file matches the sources of copy.txt`. | No `--set`. |
| a link that is not there | `--set linked=missing.txt` stops `build`: `missing.txt is not there, and copy.txt is linked with it`. | No `--set`. |
| a variable that has no value | `build` on `unknown` stops: `no variable`. | `--set named=named.txt`. |
| a list variable in a text | `build` on `listed` stops: `is a list inside a text`. | `--set named=named.txt`. |

`docs/intern/tools/build.py.md` gives the limits of these cases.
