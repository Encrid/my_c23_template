# Coding style

The style of the code of the project is the style of the code of `Bridge`.
The project changes 2 rules of the style.

The first change concerns `G1`.
Every source starts with a legal notice.
The legal notice has a line that states the copyright and has a line that states the licence.
The legal notice has no line that states the path of the source.
The legal notice has no line that describes the source.

The second change concerns `F6`.
No source contains a comment that is not the legal notice.

`tools/style.py` checks the rules of the style.
`tools/c23.py` checks the spellings of `C23`.
`build.config.toml` gives the values of the rules.

## Exceptions

If an exception names a rule and names a file then the file can break the rule.
Every exception is a line that is indented by 4 spaces.
The line states that a rule does not apply to a path.
The line names the rule in a span and names the path in a span.
Some lines that are indented by 8 spaces follow the exception and give a reason.
The path can contain `*`.
The path can end with `:` and the name of a function.
If a file breaks a rule and no exception names the file then `tools/style.py` reports the file.
If an exception names a rule and names no file that breaks the rule then `tools/style.py` reports the exception.
There is no exception.
