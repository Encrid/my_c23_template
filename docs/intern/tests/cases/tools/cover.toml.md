# tests/cases/tools/cover.toml

The group `tools/cover` checks `tools/cover.py`.
Each case writes a small project into `{case}/p` with `files`, and runs `cover.py --root {case}/p`.
The project has an empty `{case}/p/project.toml`, the header `{case}/p/include/sample.h`, its document `{case}/p/docs/extern/include/sample.h.md`, and the group `{case}/p/tests/cases/sample.toml`.
In the cases of a public folder, `{case}/p/project.toml` states `[layout] public = ["share"]`, and the folder `{case}/p/share` holds one file with its document.
In this document, each path of the small project starts with `{case}/p`. Thus `xref.py` does not check it in the template.

| Case | Claim | False variant |
| --- | --- | --- |
| a function that its document does not name | The header declares `sample_add`. `cover.py` writes `include/sample.h: sample_add is not in docs/extern/include/sample.h.md`. | The document names `sample_add`. |
| a function that no case names | No case has `sample_add` in its name. `cover.py` writes `include/sample.h: sample_add is in the name of no case`. | A case has the name `sample_add gives the sum`. |
| a function with an attribute | The header declares `[[nodiscard]] int sample_add(int a, int b);`. `cover.py` writes `sample_add is not in`. | The document names `sample_add`. |
| a function static inline | The header defines `sample_twice`. `cover.py` writes `sample_twice is not in`. | The document names `sample_twice`. |
| a macro with arguments | The header defines `SAMPLE_MAX(a, b)`. `cover.py` writes `SAMPLE_MAX is not in`. | The document names `SAMPLE_MAX`. |
| an item of an enum | The `enum` has `SAMPLE_ONE` and `SAMPLE_TWO`, and the document names `SAMPLE_ONE`. `cover.py` writes `SAMPLE_TWO is not in`. | The document names `SAMPLE_TWO` too. |
| a constexpr | The header declares `SAMPLE_SIZE`. `cover.py` writes `SAMPLE_SIZE is not in`. | The document names `SAMPLE_SIZE`. |
| a layout | The layout `sample_point_t` has the field `x`, and the document names `x`. `cover.py` writes `sample_point_t is not in`. | The document names `sample_point_t` too. |
| a field of a layout | The document names `sample_point_t`, but not `x`. `cover.py` writes `x is not in`. | The document names `x` too. |
| a pointer to a function in a layout | The layout `sample_table_t` has the field `run`, a pointer to a function. `cover.py` writes `run is not in`. | The document names `run` too. |
| a layout with no typedef | The header declares `struct sample_pair`. `cover.py` writes `sample_pair is not in`. | The document names `sample_pair`. |
| a key of a file of a public folder | The table `sample` of `share/sample.toml` has the key `threads`, and the document names `sample`. `cover.py` writes `share/sample.toml: threads is not in docs/extern/share/sample.toml.md`. | The document names `threads` too. |
| a file of a public folder that is not TOML | `share/notes.txt` holds `threads = 4`, and its document does not name `threads`. `cover.py` writes `no fault in 1 files`. | The text is in `share/notes.toml`, and its document does not name `threads`. |
