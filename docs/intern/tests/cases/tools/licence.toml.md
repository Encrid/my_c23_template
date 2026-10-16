# tests/cases/tools/licence.toml

The group `tools/licence` checks `tools/licence.py`.
Each case makes a small project in `{case}/p`, and runs `licence.py --root {case}/p`.
Its `folders` copy `license` and `cla.md` of the template into `{case}/p`, and the files of `tests/data/tools/licence` into folders of `{case}/p`.
Its `files` write the readme and the other files.
In this document, each path of the small project starts with `{case}/p`. Thus `xref.py` does not check it in the template.

| File | Content |
| --- | --- |
| `tests/data/tools/licence/license` | A short text that says that all rights are reserved. It is not the licence. |
| `tests/data/tools/licence/reserved.bin` | The byte 0, then the same text. Thus it is not a text file. |

`ours` does not give the files of `tests/data`. Thus `licence.py` does not read these two files in the template.
No case group and no document holds the text of the two files.

| Case | Claim | False variant |
| --- | --- | --- |
| a licence that is not there | `folders` does not copy `license`. `licence.py` writes `license is not there`. | `folders` copies `license`. |
| a licence that is not the published text | `folders` copies `tests/data/tools/licence/license` into `{case}/p`. `licence.py` writes `license is not the published text of the licence`. | `folders` copies `license` of the template. |
| a file that says that all rights are reserved | `folders` copies `tests/data/tools/licence/license` into `{case}/p/src`. `licence.py` writes `src/license:1: says that all rights are reserved`. | `folders` copies nothing into `{case}/p/src`. |
| a file of third_party | `folders` copies `tests/data/tools/licence/license` into `{case}/p/third_party/zlib`. `licence.py` ends with 0. | `folders` also copies it into `{case}/p/src`. |
| a file of tests/data | `folders` copies `tests/data/tools/licence/license` into `{case}/p/tests/data`. `licence.py` ends with 0. | `folders` also copies it into `{case}/p/src`. |
| a file that is not text | `folders` copies `tests/data/tools/licence/reserved.bin` into `{case}/p/src`. `licence.py` ends with 0. | `folders` copies the text file into `{case}/p/src` in place of it. |
| a source with no notice | `{case}/p/third_party/zlib/fix.patch` is there, and its notice is not there. `licence.py` writes `third_party/zlib/license is not there`. | The notice is there. |
| a notice that the readme does not name | `licence.py` writes `readme.md does not name third_party/zlib/license`. | The readme names the notice. |
| an agreement that is not there | `folders` does not copy `cla.md`. `licence.py` writes `cla.md is not there`. | `folders` copies `cla.md`. |
| an agreement that the readme does not name | `licence.py` writes `readme.md does not name cla.md`. | The readme names `cla.md`. |
