# .toolchain/tests/cases/presets.toml

The group `presets` checks the presets of `.toolchain/presets`.
Its case copies the files of a preset into a project in `{case}/proj`, then runs `fetch.py` and `build.py` on that project.
Thus the case fetches the 3 sources of the preset on each target, and checks their urls and their sha256.

`.toolchain/tests/data/presets` holds the other files of the project:

| File | Content |
| --- | --- |
| `project.toml` | The artifact `probe` of the kind `native_module`. Its manifest states the identity `test:probe@1.0.0`, `abi=2`, `config=none`, `pinned=false` and `reloadable=false`. |
| `probe.c` | A native module of the ABI 2 of Bridge. It exports `init`, `reload` and `shutdown`, and adds the systems `tick` and `tock`. `tock` gives the slot of `tick` in `before`, as the macros of BB-Native need. It puts the manifest into its section. |
| `unmarked/probe.c` | The same module, without the manifest. |

| Case | Claim | False variant |
| --- | --- | --- |
| a native module with its manifest | `fetch` and `build` end with 0, and `build` writes the path of `probe{library}`. | The module without the manifest. Thus the step `contains` stops the build. |
