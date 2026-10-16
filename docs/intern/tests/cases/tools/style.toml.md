# tests/cases/tools/style.toml

The group `tools/style` checks `tools/style.py`.
Each case writes a small project into `{case}/p` with `files`, and runs `style.py --root {case}/p`.
`{case}/p/project.toml` gives the `owner` and the `licence` of the legal notice, and the exceptions of the case.
In this document, each path of the small project starts with `{case}/p`. Thus `xref.py` does not check it in the template.

The self-test of `style.py` checks each rule on a text that breaks the rule. Thus the cases do not check each rule again.
They check the files that `style.py` reads, and the exceptions.

| Case | Claim | False variant |
| --- | --- | --- |
| a fault of the style | `{case}/p/src/a.c` has no legal notice. `style.py` writes `src/a.c:1: G1 the file does not start with the legal notice`. | The file starts with the legal notice. |
| an exception | An exception excuses G1 for `{case}/p/src/a.c`, which has no legal notice. `style.py` ends with 0. | No exception. |
| an exception for one function | The body of `long_one` in `{case}/p/src/a.c` has 21 lines. An exception excuses F4 for `long_one`. `style.py` ends with 0. | The exception is for a different function. |
| an exception that excuses nothing | An exception excuses F4 for `{case}/p/src/a.c`, which has no long function. `style.py` writes `the exception for 'src/a.c' excuses nothing`. | The body of a function of the file has 21 lines. |
| a file of tests/data | `{case}/p/tests/data/a.c` has no legal notice. `style.py` ends with 0. | The file is `{case}/p/src/a.c`. |

## Limits

No case runs the failure of the self-test, because a case cannot change `style.py`.
