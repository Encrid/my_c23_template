# tests/cases/tools/licence.toml

The group `tools/licence` checks `tools/licence.py`.
Each case makes a small project in `{case}/p`, and runs `licence.py --root {case}/p`.
Its `folders` copy `license` and `cla.md` of the template into `{case}/p`. Its `files` write the readme and the other files.
In this document, each path of the small project starts with `{case}/p`. Thus `xref.py` does not check it in the template.

`tests/data/tools/licence/license` is a short text that is not the licence.
A text that says that all rights are reserved is in `files`. Its space before `reserved` is the escape ` ` of TOML.
Thus the text of the group does not say it, and `licence.py` does not report the group in the template.

| Case | Claim | False variant |
| --- | --- | --- |
| a licence that is not there | `folders` does not copy `license`. `licence.py` writes `license is not there`. | `folders` copies `license`. |
| a licence that is not the published text | `folders` copies `tests/data/tools/licence/license`. `licence.py` writes `license is not the published text of the licence`. | `folders` copies `license` of the template. |
| a file that says that all rights are reserved | `{case}/p/src/a.c` says it. `licence.py` writes `src/a.c:1: says that all rights are reserved`. | The text says that some rights are reserved. |
| a file of third_party | `{case}/p/third_party/zlib/license` says that all rights are reserved. `licence.py` ends with 0. | `{case}/p/src/a.c` says it too. |
| a file of tests/data | `{case}/p/tests/data/a.txt` says that all rights are reserved. `licence.py` ends with 0. | `{case}/p/src/a.c` says it too. |
| a file that is not text | `{case}/p/src/a.bin` starts with the byte 0, and says that all rights are reserved. `licence.py` ends with 0. | The file does not start with the byte 0. |
| a source with no notice | `{case}/p/third_party/zlib/fix.patch` is there, and its notice is not there. `licence.py` writes `third_party/zlib/license is not there`. | The notice is there. |
| a notice that the readme does not name | `licence.py` writes `readme.md does not name third_party/zlib/license`. | The readme names the notice. |
| an agreement that is not there | `folders` does not copy `cla.md`. `licence.py` writes `cla.md is not there`. | `folders` copies `cla.md`. |
| an agreement that the readme does not name | `licence.py` writes `readme.md does not name cla.md`. | The readme names `cla.md`. |
