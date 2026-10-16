# tools/layout.py

`layout.py` checks the tree of the project: the paths, the needed files, the documents and the names.
It reads the files that `ours` gives. `ours` leaves out the files of `tests/data`, thus no rule of `layout.py` applies to them.

## Functions

| Function | Result |
| --- | --- |
| `documents(path, public)` | Gives the documents that a file needs: none, one or two. |
| `faults(root, paths, public)` | Gives the faults of the tree. `public` holds the public folders that `shared.public` gives. |
| `main()` | Runs the check. |

## The paths

The layout allows only the paths of this table.
`<name>` is one name of a file or of a folder.
`**` is one name or more, with a `/` between two names.

| Path | Rule |
| --- | --- |
| `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `.github/workflows/cla.yml` | Needed. |
| `.github/pull_request_template.md` | Needed. |
| `.gitattributes`, `.gitignore`, `cla.md`, `license` | Needed. |
| `project.py`, `project.toml`, `readme.md` | Needed. |
| `docs/contributing.md` | Needed. |
| `docs/**` | The documents. The section *The documents* gives their rules. |
| `include/**.h` | The public headers. |
| `<folder>/**` | The files of a public folder that `[layout] public` of `project.toml` names. |
| `src/**` | The sources, the private headers and the other inputs of a build. |
| `tests/cases/**.toml` | Needed: one file or more. The groups of cases. |
| `tests/fixtures/<name>/**` | The files of the fixture `<name>`. |
| `tests/data/**` | The files that the cases read. |
| `third_party/<source>/<name>.patch` | A patch of a source. |
| `third_party/<source>/license` | The licence of a source. |
| `tools/<name>.py`, `tools/toolchain.toml` and `tools/header.txt` | Needed: one file or more. The tools of the template. |

The messages are:

- `<path>: the layout does not allow this file`
- `<path>: the layout needs this file`
- `<folder>/: the layout needs this folder`

## The documents

Each file of this table needs its documents.
For example, the document of `src/<file>` in `docs/intern` is `docs/intern/src/<file>.md`.

| File | Its documents |
| --- | --- |
| A file of `src` or of `tools` | In `docs/intern`. |
| A file of `tests`, but not of `tests/data` | In `docs/intern`. |
| A patch of `third_party` | In `docs/intern`. |
| `project.py` | In `docs/intern` and in `docs/extern`. |
| `project.toml` | In `docs/extern`. |
| A file of a public folder: `include`, or a folder of `[layout] public` | In `docs/extern`. |

`project.py` needs a document in `docs/intern` and in `docs/extern`, thus these two folders are always there.
The first line of a document is `#`, a space, and the path of its file.
Each other file of `docs` is a fault. `docs/contributing.md` is the only exception.
Thus a document is a fault if its file is not there, or if it is in the wrong folder.

The messages are:

- `<path>: no document <document>`
- `<document>: no file has this document`
- `<document>: the first line is not # <path>`

## The names

Each name of a path is in snake_case.
Such a name has lower-case letters, digits and `_`, then each extension: a `.`, then lower-case letters and digits.
`.github`, `.gitattributes` and `.gitignore` are the only exceptions.

A file that a build or an editor makes is a fault. Its name has one of these forms:

- It ends with `.o`, `.obj`, `.a`, `.so`, `.dll`, `.dylib`, `.exe`, `.gch`, `.d` or `.pyc`.
- It ends with `~`, or it starts and ends with `#`.
- It is `a.out`.

The messages are:

- `<path>: '<name>' is not in snake_case`
- `<path>: a compiled or temporary file`

## Output

`main` gives the faults to `report` of `shared.py`, in the order of the paths.
Thus the output is the faults, then `faults: <number>`, or else `no fault in <number> files`.
