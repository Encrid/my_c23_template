# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import collections
import re

import prose
from shared import arguments, report

RUN = 8
CITATION = re.compile(r'`[^`\n]*\.md`(?:,\s*\*[^*\n]+\*)?')
PUNCTUATION = re.compile(r'[^a-z0-9]')


def unwrap(line):
    return prose.SPAN.sub(lambda m: m.group()[1:-1].replace('|', ' '), CITATION.sub(' ', line))


def words(sentence):
    return [PUNCTUATION.sub('', word.lower()) for word in prose.WORD.findall(sentence)]


def units(lines):
    text = list(lines)
    for start, end, _ in prose.blocks(lines):
        text[start:end + 1] = [''] * (end + 1 - start)
    return [(n, words(m.group())) for n, unit, _ in prose.units([unwrap(line) for line in text])
            for m in prose.SENTENCE.finditer(unit)]


def shared_runs(units_by_file):
    grams = collections.defaultdict(set)
    for name, found in units_by_file.items():
        for _, words in found:
            for i in range(len(words) - RUN + 1):
                grams[' '.join(words[i:i + RUN])].add(name)
    runs = {}
    for name, found in sorted(units_by_file.items()):
        for line, words in found:
            i = 0
            while i <= len(words) - RUN:
                owners = grams[' '.join(words[i:i + RUN])]
                if len(owners) < 2:
                    i += 1
                    continue
                end = i + RUN
                while end < len(words) and grams[' '.join(words[end - RUN + 1:end + 1])] >= owners:
                    end += 1
                runs.setdefault(' '.join(words[i:end]), {}).setdefault(name, line)
                i = end - RUN + 1
    return {run: places for run, places in runs.items()
            if len(places) > 1 and not any(run != other and ' %s ' % run in ' %s ' % other for other in runs)}


def scopes(documents):
    toolchain = {path: lines for path, lines in documents if path.startswith('.toolchain/')}
    return [{path: lines for path, lines in documents if path not in toolchain}, toolchain]


def main():
    root = arguments().root
    documents = prose.documents(root)
    faults = []
    for scope in scopes(documents):
        found = shared_runs({path: units(lines) for path, lines in scope.items()})
        faults += ['%s: %s' % (', '.join('%s:%d' % place for place in sorted(places.items())), run)
                   for run, places in sorted(found.items(), key=lambda item: sorted(item[1].items()))]
    report(faults, len(documents), 'documents')


if __name__ == '__main__':
    main()
