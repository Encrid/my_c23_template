# Contributing

Read `docs/coding_style.md` and `docs/documentation_style.md` before you write code or documents.

## Before a pull request

Make sure that these commands pass:

1. `python project.py check`
2. `python project.py test`
3. `python project.py test --break`

The workflow `ci` runs them again on five platforms.

## The commits

- The message of a commit has 1 line: `type(scope): description`.
- The type is `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `build`, `perf`, `style`, `ci` or `revert`.
- The description is a command, with at most 20 words.
- The message has no body, no trailer and no footer.

The repository merges a pull request only by rebase. Thus each commit of a pull request must obey these rules.

## The agreement

Before your first pull request is merged, sign `cla.md`. The workflow `cla` tells you how.

## The licence

The project is under the GNU Affero General Public License, version 3 only.
Each source of third-party code has its notice in `third_party/<source>/license`.
