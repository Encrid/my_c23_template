# tests/cases/tools/cla.toml

The group `tools/cla` checks `decide` of `tools/cla.py`, through `cla.py --decide`.
The holder is `holder`. The authors are `ann` and `bob`.

| Case | Claim | False variant |
| --- | --- | --- |
| the holder | The author is `holder`. `cla.py` writes `nothing, passes: the holder needs no agreement`. | The author is `ann`. |
| a name of the record | The record holds `bob` and `ann`. `cla.py` writes `nothing, passes: ann has signed cla.md`. | The record holds `bob`. |
| the sentence of the author | `ann` writes the sentence. `cla.py` writes `record, passes: ann signs cla.md`. | `bob` writes the sentence. |
| each other author | `ann` writes `I sign, more or less.`. `cla.py` writes `ask, fails: ann has not signed cla.md`. | `ann` writes the sentence. |
| a decision with too few values | `cla.py --decide ann holder` stops: `usage: cla.py --decide <author> <holder> <signed> [<by> <said>]`. | The record is the third value. |

`docs/intern/tools/cla.py.md` gives the limits of these cases.
