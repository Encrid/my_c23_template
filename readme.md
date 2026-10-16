# c23

The template of a project in C23, with one layout, one entry point and the checks of the method.

## Background

A project starts as a copy of this folder.
Its tools come from the project `c23-tools`, which also holds the cases of the tools.
The compiler is zig, at one pinned version.
A project builds for six targets: three operating systems on two types of processor.

The layout of the project is fixed.
`python project.py check` refuses a file or a folder that the layout does not allow.
`docs/contributing.md` gives the layout, the flow of the work and every rule.

## Install

1. Install Python 3.11 or a later version.
2. Copy this folder.
3. In `project.toml`, set `name` and `owner` in `[project]`, and `holder` in `[cla]`. The holder is a login on GitHub.
4. Run `python project.py fetch`. The command downloads zig and the sources, and takes the dependencies.

## Usage

| Command | Result |
| --- | --- |
| `python project.py fetch` | Downloads zig and each source of `project.toml`, checks their digests, and takes the dependencies. |
| `python project.py build` | Builds every artifact for this machine. |
| `python project.py pack` | Puts the package of a target into one archive, for a release. |
| `python project.py test` | Builds every artifact and runs every case. |
| `python project.py test --break` | Runs the false variant of every case. Every case must then fail. |
| `python project.py check` | Runs every check of the project: the layout, the text, the documents, the code and the commits. |
| `python project.py cla` | Decides on the agreement of a pull request. Only the workflow `cla` runs it. |

`docs/extern/project.py.md` describes the commands.
`docs/extern/project.toml.md` describes the configuration.

## Contributing

Read `docs/contributing.md` first.
A contribution needs the agreement `cla.md`. The workflow `cla` asks you to sign it in your first pull request.

## License

The GNU Affero General Public License, version 3 only. The file `license` holds the text.
