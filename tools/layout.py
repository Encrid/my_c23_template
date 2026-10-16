# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import re

from shared import arguments, config, ours, public, report

NEEDED = ('.github/workflows/ci.yml', '.github/workflows/release.yml', '.github/workflows/cla.yml',
          '.github/pull_request_template.md', '.gitattributes', '.gitignore', 'cla.md', 'license', 'project.py',
          'project.toml', 'readme.md', 'docs/contributing.md')
FOLDERS = ('tests/cases', 'tools')
ALLOWED = (r'docs/.+|include/.+\.h|src/.+'
           r'|tests/cases/.+\.toml|tests/fixtures/[^/]+/.+|third_party/[^/]+/(?:[^/]+\.patch|license)'
           r'|tools/[^/]+\.py|tools/toolchain\.toml|tools/header\.txt')
INTERN = re.compile(r'(?:src|tests|tools)/.+|third_party/[^/]+/[^/]+\.patch|project\.py')
SNAKE = re.compile(r'[a-z0-9_]+(?:\.[a-z0-9]+)*')
DOTTED = ('.github', '.gitattributes', '.gitignore')
MADE = re.compile(r'.*\.(?:o|obj|a|so|dll|dylib|exe|gch|d|pyc)|.*~|#.*#|a\.out')


def documents(path, public):
    extern = re.compile(r'(?:%s)/.+|project\.(?:py|toml)' % '|'.join(map(re.escape, public)))
    return ['docs/%s/%s.md' % (side, path) for side, pattern in (('intern', INTERN), ('extern', extern))
            if pattern.fullmatch(path)]


def faults(root, paths, public):
    allowed = re.compile('|'.join(map(re.escape, NEEDED)) + '|' + ALLOWED
                         + ''.join('|%s/.+' % re.escape(folder) for folder in public[1:]))
    found = ['%s: the layout needs this file' % path for path in NEEDED if path not in paths]
    found += ['%s/: the layout needs this folder' % folder for folder in FOLDERS
              if not any(path.startswith(folder + '/') for path in paths)]
    described = {}
    for path in paths:
        if not allowed.fullmatch(path):
            found.append('%s: the layout does not allow this file' % path)
        if MADE.fullmatch(path.rsplit('/', 1)[-1]):
            found.append('%s: a compiled or temporary file' % path)
        found += ["%s: '%s' is not in snake_case" % (path, name) for name in path.split('/')
                  if name not in DOTTED and not SNAKE.fullmatch(name)]
        for document in documents(path, public):
            described[document] = path
            if document not in paths:
                found.append('%s: no document %s' % (path, document))
    found += ['%s: no file has this document' % path for path in paths
              if path.startswith('docs/') and path != 'docs/contributing.md' and path not in described]
    for document in described.keys() & paths:
        if (root / document).read_text(encoding='utf-8', errors='replace').split('\n')[0] != '# ' + described[document]:
            found.append('%s: the first line is not # %s' % (document, described[document]))
    return found


def main():
    root = arguments().root
    paths = ours(root)
    report(sorted(faults(root, set(paths), public(config(root)))), len(paths))


if __name__ == '__main__':
    main()
