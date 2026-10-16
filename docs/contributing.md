# Contributing

This document gives the rules of a project that starts from the template `c23`.
The rules are the same in every such project.
Read this document before your first change.

## The flow of the work

The work has 5 steps. Do them in this order:

1. Ideas: find what the change gives, and why.
2. Usage: write the documents of `docs/extern` for the change.
3. Design: write the documents of `docs/intern` for the change.
4. Reflection: check the documents, then write the cases.
5. Implementation: write the code until every case passes.

If a step finds an error of an earlier step, go back to that step.
A change of the code without a change of the documents is incomplete.

## The commands

| Command | Use |
| --- | --- |
| `python project.py fetch` | Get zig, the sources and the dependencies. |
| `python project.py build` | Build every artifact. |
| `python project.py test` | Run every case. |
| `python project.py test --break` | Run the false variant of every case. Every case must fail. |
| `python project.py check` | Run every check. |

Before each commit, run `check`, `test` and `test --break`.

## The layout

The project has these files and folders, and no others:

```text
.github/                 workflows and the template of a pull request
.gitattributes .gitignore cla.md license project.py project.toml readme.md
docs/contributing.md     this document
docs/extern/             a document for every public file
docs/intern/             a document for every file of the code and of the tests
include/                 the public headers
<folder>/                a public folder that [layout] public of project.toml names
src/                     the sources and the private headers
src/os/<system>/         the code of a system: posix or windows
tests/cases/             the groups of cases
tests/fixtures/<name>/   the programs and the libraries that the cases build and run
tests/data/              the files that the cases read
third_party/<source>/    the patches and the notice of a third-party source
tools/                   the tools of the template
build/                   the output, which git ignores
```

`include/`, the public folders, `src/`, `src/os/`, `tests/fixtures/`, `tests/data/` and `third_party/` are optional.
Every other path of the tree is necessary.

A public folder holds files that the package gives to its users, as `include/` does.
`pack` puts each public folder in the archive of a release.

These files come from the template. Do not change them:

- `.github/`, `.gitattributes`, `.gitignore`, `cla.md`, `license` and `project.py`
- `tools/`
- this document, `docs/extern/project.py.md` and `docs/extern/project.toml.md`
- `docs/intern/project.py.md` and `docs/intern/tools/`

The project `c23-tools` holds the source of these files, and the cases of the tools.
Make a change of these files in `c23-tools`. Then copy them into the template `c23`.

## The documents

- `docs/extern` is for the users of the project. `docs/intern` is for the developers.
- Every file of `src/`, `tests/` (but not `tests/data/`), `tools/` and `third_party/` has a document in `docs/intern`.
- Every file of `include/` and of each public folder has a document in `docs/extern`.
- The document of `src/<file>` is `docs/intern/src/<file>.md`. Its first line is `# src/<file>`.
- Every feature of the project has a description in a document.

Write every document in Simplified Technical English (STE):

- Write at most 20 words in a sentence of a procedure, and at most 25 words in other sentences.
- Write at most 6 sentences in a paragraph.
- Use the active voice. Write one instruction in a sentence.
- Use at most 3 nouns in a noun cluster.
- Use the words of the STE dictionary, and the technical names of the project.

You can write pseudo code in a block with the tag `pseudo`.
The pseudo code follows the profile that `docs/intern/tools/pseudo.py.md` describes.
Other blocks have the tag `c`, `toml`, `sh` or `text`.
No document contains a comment. Every character is a character of ASCII, except in the files that `[check] unicode` of `project.toml` names.

The sections of `readme.md` follow the order of Standard Readme.

## The code

- `python project.py check` checks the style of the code. `docs/intern/tools/style.py.md` gives the rules.
- Every file of code starts with the legal notice: a line of the copyright and a line of the licence.
- No file contains a comment that is not the legal notice.
- The project uses one language. Every tool works on every platform.
- Keep every concern in one place. Reuse a thing, and do not copy it.

## The tests

- Every case is in `tests/cases/`. Every case has a false variant.
- If the claim of a case is false, the case fails.
- A case checks every feature that a document describes.
- A case runs every branch of the code.
- Every case runs on every platform of the project.

## The commits

- The message of a commit has 1 line: `type(scope): description`.
- The type is one of `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `build`, `perf`, `style`, `ci` or `revert`.
- The description is a command of STE, with at most 20 words.
- The message has no body, no trailer and no footer.

## The pull requests

Fill in the template of the pull request.
The workflow `ci` runs `check`, `test` and `test --break` on five platforms.
The repository merges a pull request only by rebase. Thus no merge commit breaks the rules of the commits.
Before your first pull request is merged, sign the agreement `cla.md`.

## The licence

The project is under the GNU Affero General Public License, version 3 only.
Every source of third-party code has its notice in `third_party/<source>/license`.
