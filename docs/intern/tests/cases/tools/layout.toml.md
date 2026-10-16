# tests/cases/tools/layout.toml

The group `tools/layout` checks `tools/layout.py`.
Each case writes a project into `{case}/project` with `files`, and runs `layout.py` on that project.
Each file of a project is empty, but a document holds its first line.
The project of each case has a `project.toml`, because `config` reads it.

The false variant of a case changes or adds a file of the project.
If the fault is a path, the false variant runs `layout.py` on `{case}/fixed`, which holds the project without that path.

The project `full` has these files, and the document of each file that needs one:

| Folder | Files |
| --- | --- |
| The root, `.github` and `docs` | Each file that the layout needs. |
| `tools` | `check.py` and `toolchain.toml`. |
| `src` | `sample.c`. |
| `src/os` | `os.h`, and `os.c` in the folders `posix` and `windows`. |
| `include` | `sample.h`. |
| `presets` | `sample.toml`. |
| `tests/cases` | `sample.toml`. |
| `tests/fixtures/ask` | `ask.c`. |
| `third_party/sample` | `fix.patch` and `license`. |
| `tests/data` | `Any Name.txt`. |

| Case | Claim | False variant |
| --- | --- | --- |
| a full project | `layout.py` checks `full`, writes `no fault in 39 files`, and ends with 0. | `full` also has `notes.txt`. |
| a path that the layout does not allow | `notes.txt: the layout does not allow this file`. | No `notes.txt`. |
| a file that the layout needs | A project with no `license`: `license: the layout needs this file`. | The project has `license`. |
| the folders that the layout needs | A project with no file in `src`, `tests/cases` and `tools`: `src/: the layout needs this folder`, and the same line for `tests/cases/` and for `tools/`. | The project has a file in each of the three folders. |
| a source without its document | `src/a.c: no document docs/intern/src/a.c.md`. | The project has the document. |
| a public header without its document | `include/a.h: no document docs/extern/include/a.h.md`. | The project has the document. |
| a document without its file | `docs/intern/src/gone.c.md: no file has this document`. | The project has the source `gone.c` in `src`. |
| a document in the wrong folder | A source has a document in `docs/extern`: `docs/extern/src/a.c.md: no file has this document`. | The source has no document in `docs/extern`. |
| a file of docs that is not a document | `docs/notes.txt: no file has this document`. | No `notes.txt` in `docs`. |
| the first line of a document | The document of a source starts with `# a.c`: `the first line is not # src/a.c`. | The first line is `# src/a.c`. |
| a name that is not in snake_case | `src/Notes.c: 'Notes.c' is not in snake_case`. | `notes.c` in place of `Notes.c`. |
| a compiled file | `src/sample.o: a compiled or temporary file`. | `sample.c` in place of `sample.o`. |
| a system that no target has | `src/os/linux/os.c: the layout does not allow this file`. | The folder `posix` in place of `linux`. |
| a file of tests/data | `Any Name.txt` in `tests/data` has no document, and its name is not in snake_case. No line of the output names it. | The file is in `tests`, not in `tests/data`. |
