# .toolchain/tests/cases/build.toml

The group `build` checks `.toolchain/tools/build.py`, and the parts of `.toolchain/tools/shared.py` that the tools share.
Its cases run `build.py` or `test.py` on a project in `.toolchain/tests/data/build`, with the output in `{case}/out`.
The cases of the options, of the report and of the files of a project run a short Python program that calls `shared`.

| Project | Content |
| --- | --- |
| `built` | The library `greet`, the program `greeter`, the archive `greet_static` (with the flag `-DGREETING`), the program `greeter_static` that links it, and the artifact `stamped`, with its variant `plain`. |
| `copy` | The artifact `copy.txt` of the kind `file`. The variables `tool`, `source` and `linked` give its tool, its source and its link. |
| `twice` | `[variables] language`, a key that `.toolchain/toolchain.toml` also gives. |
| `builtin` | `[variables] root`, the name of a variable that the tools give. |
| `unknown` | An artifact with the name `{named}`. The variable `named` is `{nothing}`, which has no value. |
| `listed` | An artifact with the name `{named}`. The variable `named` is `{language}`, a list in a text. |
| `targeted` | The artifact `near-{target}.txt`, and its variant `far-{target}.txt` with the target `nowhere`. The project adds `nowhere`, whose `runs_on` is empty. |
| `untargeted` | The same artifact and variant, but the variant has no `target`. |
| `module` | The modules `mod`, `two` and its variant `three`, over the defaults of `[module]`, and the program `pathcheck` that reads their `*_PATH` macros. |
| `config` | The artifact `thing`, stated in a file of `.toolchain/config` and not in `project.toml`. |
| `joined` | The artifact `alpha` in `project.toml`, and the artifact `beta` in `more.toml` of `.toolchain/config`. |
| `clash` | `[variables] word` in `one.toml` and in `two.toml` of `.toolchain/config`. |
| `leaky` | The artifact `stamped`, whose section holds `{root}`: the folder of the project. |
| `archived` | The archive `one`. |
| `started` | The program `sizer`, which calls `stat`. |
| `placed` | The program `placed`, whose kind compiles `src/main.c` with the folder `include`, and `side.c` by its bare name, in the folder `{side}`. `side` is `side`, the folder that holds `side.c`. |
| `cached` | The test artifact `cached`, whose kind writes the cache of zig of its step, in the folder `{build}`. |
| `composed` | No artifact, and the table `[compose.base]`, whose `from` is the variable `place`. `place` is `kept`, the folder that holds `include/kept.h`. |
| `family` | The parts `alpha`, `beta` and `gamma`, each with one artifact `<part>.txt` of the kind `file`. `beta` uses `alpha`, and `gamma` uses `beta`. |
| `ordered` | The parts `alpha` and `zeta`, in `alpha.toml` and `zeta.toml` of `.toolchain/config`. `alpha.txt` links `zeta.txt`, and `alpha` uses `zeta`. |
| `unordered` | The same parts, but `alpha` uses no part. |
| `toolchained` | The artifact `notice.txt` of the kind `taken`, which copies `{place}/header.txt`. `[variables] place` is `{toolchain}`. |
| `runtime` | The library `small` of the kind `library`, the same library `bare` of the kind `bare_library`, which adds no `runtime`, the library `checked`, and the program `checker`, which links `checked`. `tools/inspect.py` builds the project for `x86_64-windows-gnu`, and gives the size or the imports of one library. |

In `built`, `greet` gets its greeting from `defines`.
`greeter` includes `.toolchain/tests/data/build/built/include/greet.h`, links `greet`, and has `greet` beside it in its folder.
`greeter` also compiles `.toolchain/tests/data/build/built/src/<system>/system.c`, and writes `hello from a library, on <system>`.
The case `greeter` of `built` runs `greeter`. Its false variant runs a copy of `greeter` without the library.

The proof source includes `.toolchain/tests/data/build/built/include/greet.h` and `.toolchain/tests/data/build/built/include/sub/extra.h`.
So the proof reads a header from a sub-folder of `include`.
The proof also calls `outside`, which only `.toolchain/tests/data/build/built/tests/package/outside.c` gives.
The package does not hold that file, and `[package] link` names it through the variable `outside`.
`build --pack` builds no test artifact, thus the project has no archive outside the package.
zig compiles a source in the list of links, thus the file does the work of an archive of a different project.

The proof finds the declaration of `outside` in `.toolchain/tests/data/build/built/tests/package/include/outside.h`.
The package does not hold that header either, and `[package] include` names its folder through the variable `outside_include`.

The kind `stamped` copies `.toolchain/tests/data/build/built/src/note.txt` to a work file, renames the work file to the output, and adds the section `said`.
Then it checks that the output contains `{said}`. The default of `said` is `written`, a word of `note.txt`.
The section holds the items of `manifest` with commas between them: `first,second`.
The variant `plain` is unstamped.

In `family`, `beta.txt` links `alpha.txt`, and `gamma.txt` links `beta.txt`. Thus a build of a part fails if a part of its `uses` is not built.
`[compose.alpha]` and `[compose.beta]` take `<part>.h` from `include/<part>`, into the folder of the variable `place`, which is `include`.
The `third_party` of `alpha` is `sample`, and the other parts have none. `beta` has the package proof `tests/beta/package/proof.c`, which includes `beta.h`.
The groups `alpha/alpha` and `beta/beta` each have one case. `gamma` has no group.
The cases of the checks of the parts write a project in `{case}/p` with `files`, with one part `a` and the artifact `note`.

The case of an archive of a release copies `archived` into `{case}/proj`, and runs `build.main` from a short Python program.
The program puts `[build] cache` in that folder, as in a project. A project in `.toolchain/tests/data/build` does not hold the cache.
The cases of a release build for a named target: the archive for Windows, and the program for Linux.
Thus each machine checks a file that holds a path of its machine without the fix.

| Case | Claim | False variant |
| --- | --- | --- |
| a program linked with a library | `test` on `built` passes the cases `greeter` and `greeter_static`: the archive and its flag work. | `test --break`. |
| a variant without its section | With `--set said=first,second`, `build` stops: `plain.txt does not hold 'first,second'`. | No `--set`. |
| a build for debugging | With `--debug`, `package.txt` is in `{case}/out/{target}-debug`. | No `--debug`. |
| a package in a zip | `build --pack` writes the path of the zip, and the names of the files in it. The proof builds with the nested header `include/sub/extra.h`. `greeter_static` has `test = true`, thus no name of the zip starts with `greeter_static/`. | No `--pack`. |
| the proof links the files of [package] link | `build --pack` writes `package proof: built ran`. The proof calls `outside`, and only the linked `outside.c` gives it. | `--set outside={case}/none.c`, a file that is not there. Thus `build` stops before the proof links. |
| the proof includes the folders of [package] include | `build --pack` writes `package proof: built ran`. The proof includes `outside.h`, and only the folder that `[package] include` names holds it. | `--set outside_include={case}/none`, a folder that is not there. Thus the proof does not compile. |
| a module over the defaults, with a path | `build` on `module` builds `mod` from the default sources, `two` and its variant `three`, and `pathcheck` with their `*_PATH` macros. | `build` on `copy`. |
| the files of config merge | `build` on `config` makes `thing`, whose `[[artifact]]` is in a file of `.toolchain/config`, not `project.toml`. | `build` on `copy`. |
| a variable that [variables] does not have | `--set nowhere=1` stops `build`: `--set nowhere=1: [variables] has no nowhere`. | No `--set`. |
| a key in project.toml and in toolchain.toml | `build` on `twice` stops: `project.toml states variables.language, and toolchain.toml states it too`. | `build` on `copy`. |
| a list of tables in two files | `build` on `joined` makes `alpha` and `beta`. | `build` on `config`. |
| a key in two files of config | `build` on `clash` stops: `config/two.toml states variables.word, and config/one.toml states it too`. | `build` on `copy`. |
| a built-in variable in [variables] | `build` on `builtin` stops: `[variables] names a built-in variable or a key of a target: root`. | `build` on `copy`. |
| a target that the toolchain does not have | `--target nowhere` stops `build`: `no target nowhere; the targets:`. | No `--target`. |
| a tool that is not there | `--set tool=nowhere` stops `build`: `the tool interpreter is not at nowhere`. | No `--set`. |
| sources that match no file | `--set source=none.txt` stops `build`: `no file matches the sources of copy.txt`. | No `--set`. |
| a link that is not there | `--set linked=missing.txt` stops `build`: `missing.txt is not there, and copy.txt is linked with it`. | No `--set`. |
| a variable that has no value | `build` on `unknown` stops: `no variable`. | `--set named=named.txt`. |
| a list variable in a text | `build` on `listed` stops: `is a list inside a text`. | `--set named=named.txt`. |
| an artifact for a different target | `build` on `targeted` lists `far-nowhere.txt` in `package.txt`. No machine runs that target. | `build` on `untargeted`. |
| an option with a value | `shared.arguments('--commits')` gets `--commits a..b`, and the program writes `a..b`. | No `--commits`, thus the program writes `None`. |
| a report with faults | `shared.report` gets two faults. It writes them and `faults: 2`, and the status is 1. | No fault. |
| a report with no fault | `shared.report` gets no fault, 12 and `commits`. It writes `no fault in 12 commits`, and the status is 0. | One fault. |
| the files of a project, walked | `shared.repository` writes `False` for `{case}/w`. `shared.ours` gives `{case}/w/a.txt` and `{case}/w/src/build/e.txt`. It leaves out `tests`, the folder `build` at the root and `__pycache__`. | `{case}/w/src/b.txt` is also there. |
| the files of a project, from git | The program makes `{case}/g` a repository of git, and `shared.repository` writes `True`. `shared.ours` gives `a.txt` and `.gitignore`, but not `tests` or a file that git ignores. | `{case}/g/src/b.txt` is also there. |
| a package that holds a path of its machine is refused | `build --pack` on `leaky` stops: `stamped.txt` holds the folder of the project. | No `--pack`. |
| the cache of zig is a path from the folder of the project | `build.prepared` on the template, which holds the cache, sets `ZIG_LOCAL_CACHE_DIR` to `build/zig-cache/local`. | `build.prepared` on `built`, which does not hold the cache: a whole path. |
| an archive of a release holds no path of its machine | `build --pack --target x86_64-windows-gnu` on the copy of `archived` writes its zip, thus `one.a` holds no folder of the machine. Without `-fstrip`, each object of `one.a` holds its own path. | `--debug`: the debug information of `one.a` holds the folder of the project, thus `pack` stops. |
| a program of a release holds no path of its machine | `build --pack --target x86_64-linux-gnu` on `started` writes its zip, thus `sizer` holds no folder of the machine. `sizer` links objects that zig builds for glibc, with their debug information. Without `-s`, `sizer` keeps it. | `--debug`: the debug information of `sizer` holds the folder of the project, thus `pack` stops. |
| the headers of a table start from its folder | `build` on `composed` writes `include/kept.h`, and `{case}/out/{target}/include/kept.h` holds the header of `kept`. | `--set place=.`: the folder of the project has no `include/kept.h`. |
| a step that runs in a folder | `build` on `placed` builds `placed{exe}`: from the folder `side`, the step finds `side.c`, `src/main.c` and `include/placed.h`. | `--set side=.`: the folder of the project has no `side.c`. |
| a step that runs in a folder that is not there | With `--set side=nowhere`, `build` stops: `<folder>/nowhere is not there, and a step of placed runs in it`. | No `--set`. |
| a step that runs in a folder gets the caches of zig as whole paths | A short Python program puts `[build] cache` in `{case}/proj`, as the case of an archive does, and builds `cached`. The step writes `{case}/proj/build/zig-cache/local`, a whole path. | The program does not move the cache, so the step writes the cache of this project. |
| a program of a package keeps its execute bits | A short Python program runs `build --pack` on `built`, and writes `True`: the zip records an execute bit for `greeter{exe}`. On Windows, the name `greeter.exe` gives the bit. | The program reads the mode of `include/greet.h`, a header with no execute bit. |
| a build of a part makes the parts that it uses, and their uses | `build --part gamma` on `family` builds `alpha.txt`, `beta.txt` and `gamma.txt`. | `--part beta`, which does not build `gamma.txt`. |
| a build of a part makes no other part | `build --part alpha` on `family` builds `alpha.txt`, and not `beta.txt` or `gamma.txt`. | No `--part`. |
| a part that the project does not have | `build --part nowhere` on `family` stops: `no part nowhere; the parts: alpha beta gamma`. | `--part alpha`. |
| an artifact with no part, in a project with parts | The artifact `note` states no part: `note states no part, and the project has parts`. | `note` states the part `a`. |
| a table of [compose] with no part, in a project with parts | `[compose.headers]` states no part: `[compose.headers] states no part, and the project has parts`. | The table states the part `a`. |
| an artifact of a part that [parts] does not have | In a project with no `[parts]`, `note` states the part `a`: `note states the part a, and [parts] does not have it`. | `note` states no part. |
| a part that states no uses | `[parts.a]` has no `uses`: `[parts.a] states no uses`. | `uses = []`. |
| a key that a part does not have | `[parts.a]` has the key `use`: `[parts.a]: a part has no key use`. | No `use`. |
| a pack of a part writes the zip of the part | `pack --part beta` on `family` writes `Family-Beta-{target}.zip` with `beta.txt`, `include/beta.h` and `license`, and runs the proof of `beta`. The zip holds no `alpha.txt` and no licence of `third_party`. | `--part alpha`. |
| the zip of a part holds the licences of its third_party | `pack --part alpha` on `family` writes `Family-Alpha-{target}.zip` with `third_party/sample/license`. | `--part gamma`. |
| a folder of third_party with no licence | The `third_party` of `a` is `sample`, which has no licence: `third_party/sample/license is not there, and the deliverable needs it`. | The project has the licence. |
| a pack with no part writes the zip of each part | `pack` on `family` writes `Family-Alpha-{target}.zip`, `Family-Beta-{target}.zip` and `Family-Gamma-{target}.zip`, and runs the proof of `beta`. | `--part alpha`. |
| the headers of a table go into the folder into | `build --part alpha` on `family` writes `include/alpha.h`, and `{case}/out/{target}/include/alpha.h` holds the header. | `--set place=other`. |
| a join makes one zip with a folder for each target | A short Python program packs `alpha` of `family` for each of the 6 targets, then runs `build --join --part alpha`. `Family-Alpha.zip` holds `<target>/alpha.txt` for each target. | The program packs 5 targets, thus `join` stops. |
| a join with no part joins nothing | `build --join` on `family` writes no zip and ends with 0. | `--part alpha`: the zips of the targets are not there. |
| the tag of a part names the part | `build --tag alpha-v0.1.0` on `family` builds `alpha.txt` and not `beta.txt`. The name of the part does not start with `v`. | `--tag v0.1.0`, the tag of the project. |
| a tag that is not the tag of a release | `build --tag alpha-0.1.0` stops: `the tag alpha-0.1.0 is not v<major>.<minor>.<patch> or <part>-v<major>.<minor>.<patch>`. | `--tag alpha-v0.1.0`. |
| a build makes each part after the parts that it uses | `build` on `ordered` builds `zeta.txt`, then `alpha.txt`, though `alpha.toml` comes first. | `unordered`: `alpha.txt` comes first, and its link is not there. |
| a build of a part makes the parts that it uses first | `build --part alpha` on `ordered` builds `zeta.txt`, then `alpha.txt`. | `unordered`, which builds only `alpha.txt`. |
| parts that use each other | `a` uses `b`, and `b` uses `a`: `the uses of the parts make a cycle: `, and the parts. | `b` uses no part. |
| a part that uses a part that [parts] does not have | With no `--part`, `uses = ["nowhere"]` stops: `no part nowhere; the parts: a`. | `uses = []`. |
| the variable toolchain names the toolchain of the tools | `build` on `toolchained` copies `header.txt` of the toolchain that runs, though the root holds no toolchain. | `--set place=.toolchain`: the `.toolchain` of the root has no `header.txt`, thus `build` stops. |
| a library of x86_64-windows-gnu links no compiler_rt | `inspect.py size` writes `small.dll: under 16 KB`. | `bare.dll`, which links compiler_rt: `16 KB or more`. |
| a library of x86_64-windows-gnu takes its moves and its fills from Windows | `inspect.py imports` writes `KERNEL32.dll: RtlMoveMemory` and `KERNEL32.dll: RtlFillMemory` for `small.dll`. | `bare.dll`, which imports neither. |
| a library moves, fills, compares and counts each byte, and touches no byte outside its buffers | `test` on `runtime` builds for the target of the machine, and the case `checker` writes `bad 0`: `checker: 1 cases: 1 as written`. | `--break`: `checker` gets the argument `wrong`, and writes `bad 1`. |

`.toolchain/docs/build.py.md` gives the limits of these cases.
