# .toolchain/tests/cases/fail.toml

The group `fail` checks `.toolchain/tools/fail.py`, through `test`, `test --branches` and `test --leaks` of `.toolchain/tools/test.py`.
Each case runs `test.py` on a project of `.toolchain/tests/data/fail`, with its output in `{case}/out`: `failed`, or `typed` for three cases.

The program `failed` takes a block with `first_block` of `src/first.c`, and a second block with `malloc` in `src/main.c`.
Then it takes a block with `calloc`, makes it bigger with `realloc`, and opens and shuts a door.
At each step that fails, it writes a line through `said` of `src/said.c`, and ends with the status of the step. It gives back each block that it took.
With an argument, a failed second block keeps the first block.

`tests/door.c` holds `door_open`, `door_lock`, `door_shut` and `say`, as a different project holds its functions. No count counts them.
`[fail] with` names the file of the variable `listed`, which is `tests/fail.toml` by default.
That file lists `door_open` with `-1`, and `door_lock` with `false`. No file of `src` calls `door_lock`.
`tests/no_door.toml` lists only `door_lock`. `tests/misfit_list.toml` also lists `say`, and `tests/misfit_result.toml` also lists `door_shut`.
`tests/twice.toml` also lists `malloc`, which is always in the list.
The project has the dependency `door`, from the folder of the variable `lists`, which is `tests` by default.
Its list `tests/door.txt` holds one key and no file. Thus `take` writes one line `taken: door, package door` each time that it prepares the build.

The program `typed` calls `start_one` and `start_two` of `tests/started.c`, and `[fail.calls]` lists them with `-1`.
`tests/started.h` declares them as a header of a system does, with `#pragma clang system_header`.
The callback of `start_one` has the type `start_fn_t`, a `typedef` with `__attribute__((stdcall))`. The types of `start_two` hold `_Nullable` and `_Nonnull`.
Then `typed` starts a thread: with `pthread_create` in `src/posix/thread.c`, and with `CreateThread` in `src/windows/thread.c`.
The declaration of `pthread_create` on macOS holds `_Nullable` and `_Nonnull`, and the callback of `CreateThread` is a `typedef` with `__attribute__((stdcall))`.
`[fail.calls]` lists `pthread_create` with `EAGAIN` and `CreateThread` with `nullptr`. The project builds with the flags of a project.

Its case `both` states no `fail`. The case `first` makes `start_one` fail, and `second` makes `start_two` fail.
The case `third` makes `pthread_create` and `CreateThread` fail, and each system calls one of them. The false variants state no `fail`.

| Case of the project | `fail` | Claim | False variant |
| --- | --- | --- | --- |
| `whole` | None. | `a door, opened and shut`, and the status 0. | The first call of `malloc` fails. |
| `first` | The first call of `malloc`. | `no first block`, and the status 1. | No `fail`. |
| `second` | The second call of `malloc`. | `no second block`, and the status 2. | The first call of `malloc` fails. |
| `leaky` | The second call of `malloc`, with the argument `keep`. | `no second block, and the first is kept`, and the status 2. | No `fail`. |
| `lost calloc` | The first call of `calloc`. | `no zeroed block`, and the status 3. | No `fail`. |
| `lost realloc` | The first call of `realloc`. | `no bigger block`, and the status 4. | No `fail`. |
| `door` | The first call of `door_open`. | `no door`, and the status 5. | No `fail`. |
| `nowhere` | The first call of `door_lock`. | `a door, opened and shut`, and the status 0. | The first call of `malloc` fails. |

| Case | Claim | False variant |
| --- | --- | --- |
| a listed call fails in a case, and the files of a program share one count | `test -k second` writes `second: as written`, and ends with 0. The first call of `malloc` is in `src/first.c`, and the second is in `src/main.c`. | `--break`, thus the false variant runs. |
| a false variant makes a different call fail | `test --break -k second` writes `second, made false: fails, as it must`, and ends with 0. | No `--break`. |
| calloc and realloc fail with nullptr | `test -k lost` writes that each of the two cases is as written. | `--break`. |
| a call of a different project fails with its own value | `test -k door` writes `door: as written`. | `--break`. |
| a listed call that the code does not make fails nothing | `test -k nowhere` writes `nowhere: as written`. | `--break`. |
| cases with and without failed calls in one run | `test` runs the 8 cases, and writes `failed: 8 cases: 8 as written`. | `--break`. |
| a case that states fail prepares the build one time | `test -k second` makes the build and the run `fail`, and writes `taken: door, package door` one time. | With `--set lists=none`, the list of `door` is not there, and `test` stops. |
| a listed call whose callback is a typedef with a calling convention fails | `test -k first` on `typed` builds the run `fail`, and writes `first: as written`. | `--break`. |
| a listed call whose types hold nullability marks fails | `test -k second` on `typed` builds the run `fail`, and writes `second: as written`. | `--break`. |
| the thread call of each system fails | `test -k third` on `typed` builds the run `fail` with the declaration of the system, and writes `third: as written`. | `--break`. |
| a call that [fail.calls] does not list | With `--set listed=tests/no_door.toml`, `test` stops: `the case door makes door_open fail, and [fail.calls] does not list it`. | No `--set`. |
| a call that two tables list | With `--set listed=tests/twice.toml`, `test` stops: `[fail.calls] lists malloc two times`. | No `--set`. |
| a file of [fail] with that is not there | With `--set listed=tests/none.toml`, `test` stops: `[fail] with: <file> is not there`. | No `--set`. |
| a listed call with no fixed list of arguments | With `tests/misfit_list.toml`, `src/said.c` calls `say`, which has `...`, and `test` stops. | No `--set`. |
| a listed call that gives no result | With `tests/misfit_result.toml`, `src/main.c` calls `door_shut`, which gives `void`, and `test` stops: `door_shut gives no result`. | No `--set`. |
| test --branches reaches the branch of each failed call | `test --branches` writes `branches: 19 outcomes, 19 reached`, and ends with 0. | `-k whole`, thus no call fails. |
| test --leaks counts the path of a failed call | `test --leaks -k leaky` writes `leaks: leaky keeps 1 memory`, and stops. | The case `second`, which gives back the first block. |
| a failed call takes nothing in test --leaks | `test --leaks -k second` writes `second: as written` and `leaks: 1 cases, 1 give back what they take`. | The case `leaky`. |
