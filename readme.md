# c23

This folder is a template for a project in C23.
The compiler is zig, at one pinned version.
The project builds for six targets: three operating systems on two types of processor.
The file `build.config.toml` holds all the values of the build.
The file `build.py` holds no values.

## Start

1. Install Python 3.11 or a later version.
2. Put zig on the path at the pinned version, or run `python build.py fetch`.
3. Run `python build.py test`.

## Commands

| Command | Result |
| --- | --- |
| `python build.py fetch` | Downloads zig into `build/zig` if the pinned zig is not there, and checks the SHA-256 digest of the archive. Then downloads each source that is not there, checks its digest and applies its patches. Then takes the dependencies. |
| `python build.py build` | Builds all the artifacts for this machine. |
| `python build.py test` | Builds the artifacts and the test programs, and runs all the cases. |
| `python build.py test --break` | Runs the false variant of each case, or makes the claims of the case false. Each case must then fail. |
| `python build.py style` | Checks the coding style. |

## Your project

- Put the C sources in `src/`.
- Put each test program in `tests/`, as one `.c` file.
- Put each group of cases in `tests/`, as one `.toml` file.
- Change the values in `build.config.toml`. Do not change `build.py`.
- Change this file for your project.

The template has examples that test `build.py`: the artifacts `greet`, `greeter`, `ask` and `note`, the dependency `sample`, the source `sample_source`, and their files in `tests/`.
If your project does not need them, remove them.

The file `docs/extern/build.md` describes the build, the tests and the configuration.
The file `docs/intern/style.md` gives the coding style.
The file `docs/intern/build.md` tells how `build.py` works.
