# The build

`build.py` builds the artifacts of a project and tests the project.
`build.config.toml` contains every value of the build.
`build.py` contains no value of a project.

## The root

Every project contains a copy of `build.py`.
Every project contains a copy of `tools/style.py`.
Every project contains a copy of `tools/c23.py`.
Every copy is identical to the file of `c23`.
If `--root` names a folder then the folder is the root of the project.
If `--root` names no folder then the folder of `build.py` is the root of the project.
`build.py` reads `build.config.toml` that is in the root.

## Variables

A text of `build.config.toml` can contain a variable.
A variable is a name that is between 2 braces.
`build.py` replaces every variable with the value of the variable.

- `build.py` gives `{root}` and `{build}` and `{out}` and `{target}` and `{home}` and `{python}` and `{script}` and `{zig}`.
- Every key of the target is a variable.
- Every key of `[variables]` is a variable.
- If `--debug` is given then every key of `[debug]` replaces the variable that has the name of the key.
- If `--set` gives a name and gives a value then the value replaces the value of the variable that has the name.
- If a key of `[variables]` has the name of a variable that `build.py` gives then `build.py` stops.

If the value of a variable is a list and the variable is an item of a list then the items of the value replace the item.
If the value of a variable is a list and the variable is a part of a text then the variable must give a separator.

## Dependencies

A dependency is a folder that a different project makes.
Every dependency has a list.
The list gives the files of the dependency and gives the digest of every file.
Every dependency names a folder.

- `build.py` copies every file of every dependency into the folder that the dependency names.
- If a copy has the digest of the file then `build.py` does not copy the file.
- If a file does not have the digest that the list gives then `build.py` stops and changes no file.
- If 2 dependencies do not agree then `build.py` stops and changes no file.
- If a dependency has `make` then `build.py` runs `make` first.
- If the list of a dependency does not exist and the dependency is optional then `build.py` does not take the dependency.

## Sources

A source is an archive that a maker publishes.
Every source has an address and has a digest and has a folder.
A source can have some patches.
The stamp of a source is a text that contains the digest of the source and contains the digest of every patch of the source.

- If `fetch` runs and the folder of a source does not contain the stamp of the source then `build.py` empties the folder and downloads the archive into the folder.
- If the archive does not have the digest of the source then `build.py` stops.
- `build.py` unpacks the archive and applies every patch of the source.
- If a patch does not apply then `build.py` stops.
- If every patch applies then `build.py` writes the stamp of the source into the folder.
- If `build` runs and the folder of a source does not contain the stamp of the source then `build.py` stops.
- If `test` runs and the folder of a source does not contain the stamp of the source then `build.py` stops.

A patch has some hunks.
Every hunk has a place and has a context.
The context of a hunk contains some lines.
If every line of the context of every hunk of a patch is in the file at the place of the hunk then the patch applies.

## Tools

Every tool is a program.
`build.py` finds every tool.
If `build.py` does not find a tool then `build.py` stops.

## Kinds and artifacts

Every artifact has a kind.
Every kind contains `steps`.
A kind can contain `unlinked`.
`steps` is a list that contains some steps.
`unlinked` is a list that contains some steps.

- A step can run a command.
- A step can add a section to the artifact.
- A step can check that the artifact contains a text.
- A step can copy a file.
- A step can rename a file.

If every file that an artifact links exists then `build.py` makes the artifact with `steps`.
If a file that an artifact links does not exist then `build.py` makes the artifact with `unlinked`.
If a file that an artifact links does not exist and the kind of the artifact does not contain `unlinked` then `build.py` stops.
A variant is a copy of an artifact.
A variant has a different name.
If a variant sets `unstamped` then the variant adds no section.
If the name of an artifact contains a variable then `build.py` replaces the variable.
`build.py` writes a list that names every file that the build makes and gives the digest of every file.
A different project can take the files with the list.

## Cases

A group is a file that contains some cases.
Every case runs a command.
Every case has some claims.
If every claim of a case is true then the case passes.

- `build.py` gives every case an empty folder.
- `build.py` gives every case a free port.
- A case can change the environment of the command.
- `build.py` writes the files of the case into the folder before the run of the command.
- A claim can name a file and a text.
- If a claim names a file and a text then the file must contain the text.
- A script waits for a text.
- If the command prints the text then the script changes a file or types a line.
- A helper is a second command.
- `build.py` starts the helper first.
- Every helper has some claims.
- If a rule names a text then no case prints the text.
- If a rule names a group then the rule does not apply to the group.
- If a command does not end in the time that `[test]` gives then the case fails.
- If no case exists then `build.py` says that no case exists.

If `--break` is given and a case has a false variant then `build.py` runs the false variant and the claims of the case must be false.
If `--break` is given and a case has no false variant then the claims of the case must be true.
If a case passes and `--break` is given then the case fails.

## Style

`build.py` runs every tool of `[style]`.
Every tool of `[style]` is in the folder of `build.py`.
Every tool of `[style]` reads `build.config.toml` that is in the root.
