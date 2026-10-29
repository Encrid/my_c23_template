# .toolchain/tests/cases/fail.toml

The group `fail` checks `.toolchain/tools/fail.py`, through `test`, `test --branches` and `test --leaks` of `.toolchain/tools/test.py`.
Each case runs `test.py` on the project `.toolchain/tests/data/fail/failed`, with its output in `{case}/out`.

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
| a call that [fail.calls] does not list | With `--set listed=tests/no_door.toml`, `test` stops: `the case door makes door_open fail, and [fail.calls] does not list it`. | No `--set`. |
| a call that two tables list | With `--set listed=tests/twice.toml`, `test` stops: `[fail.calls] lists malloc two times`. | No `--set`. |
| a file of [fail] with that is not there | With `--set listed=tests/none.toml`, `test` stops: `[fail] with: <file> is not there`. | No `--set`. |
| a listed call with no fixed list of arguments | With `tests/misfit_list.toml`, `src/said.c` calls `say`, which has `...`, and `test` stops. | No `--set`. |
| a listed call that gives no result | With `tests/misfit_result.toml`, `src/main.c` calls `door_shut`, which gives `void`, and `test` stops: `door_shut gives no result`. | No `--set`. |
| test --branches reaches the branch of each failed call | `test --branches` writes `branches: 19 outcomes, 19 reached`, and ends with 0. | `-k whole`, thus no call fails. |
| test --leaks counts the path of a failed call | `test --leaks -k leaky` writes `leaks: leaky keeps 1 memory`, and stops. | The case `second`, which gives back the first block. |
| a failed call takes nothing in test --leaks | `test --leaks -k second` writes `second: as written` and `leaks: 1 cases, 1 give back what they take`. | The case `leaky`. |
