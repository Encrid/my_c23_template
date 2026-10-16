# tests/cases/sample.toml

The group `sample` checks the program `sample` of the template.
A project replaces this group with the cases of its own artifacts.

| Case | Claim | False variant |
| --- | --- | --- |
| hello | `sample` writes the line `hello, c23`, and ends with 0. `package.txt` lists `sample{exe}`. | A different program writes `hello`. |
