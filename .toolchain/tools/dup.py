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
JOIN = '\x01'


def unwrap(line):
    return prose.SPAN.sub(lambda m: JOIN + re.sub(r'[\s|]+', JOIN, m.group()[1:-1]) + JOIN,
                          CITATION.sub(' ', line))


def words(sentence):
    found = []
    for token in prose.WORD.findall(sentence):
        parts = [part for part in (PUNCTUATION.sub('', piece.lower()) for piece in token.split(JOIN)) if part]
        found += [(part, ' '.join(parts) if JOIN in token else '') for part in parts]
    return found


def units(lines):
    text = list(lines)
    for start, end, _ in prose.blocks(lines):
        text[start:end + 1] = [''] * (end + 1 - start)
    found = []
    for n, unit, _ in prose.units([unwrap(line) for line in text]):
        for m in prose.SENTENCE.finditer(unit):
            pairs = words(m.group())
            found.append((n, [word for word, _ in pairs], [span for _, span in pairs]))
    return found


def shared_runs(units_by_file):
    grams = collections.defaultdict(set)
    for name, found in units_by_file.items():
        for _, words, _ in found:
            for i in range(len(words) - RUN + 1):
                grams[' '.join(words[i:i + RUN])].add(name)
    runs, spans = {}, collections.defaultdict(dict)
    for name, found in sorted(units_by_file.items()):
        for line, words, held in found:
            i = 0
            while i <= len(words) - RUN:
                owners = grams[' '.join(words[i:i + RUN])]
                if len(owners) < 2:
                    i += 1
                    continue
                end = i + RUN
                while end < len(words) and grams[' '.join(words[end - RUN + 1:end + 1])] >= owners:
                    end += 1
                run = ' '.join(words[i:end])
                runs.setdefault(run, {}).setdefault(name, line)
                spans[run].setdefault(name, held[i] if len(set(held[i:end])) == 1 else '')
                i = end - RUN + 1
    quotes = {run for run, found in spans.items()
              if len(found) > 1 and all(found.values()) and len(set(found.values())) == len(found)}
    return {run: places for run, places in runs.items()
            if len(places) > 1 and run not in quotes
            and not any(run != other and other not in quotes and ' %s ' % run in ' %s ' % other for other in runs)}


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
