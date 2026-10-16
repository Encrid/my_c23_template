# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import re
import tomllib

from shared import arguments, ours, report


def named(name, text):
    return re.search(r'(?<!\w)%s(?!\w)' % re.escape(name), text) is not None


def names(text):
    text = re.sub(r'\[\[.*?\]\]\s*', '', text.replace('\\\n', ' '))
    found = re.findall(r'^\s*#\s*define\s+(\w+)\(', text, re.M)
    found += re.findall(r'^(?!typedef\b)[A-Za-z_][^;{}()#=\n]*?\b(\w+)\s*\(', text, re.M)
    found += re.findall(r'\bconstexpr\b[^;=]*?\b(\w+)\s*(?:\[[^\]]*\]\s*)*=', text)
    for body in re.findall(r'\benum\b[^{;]*\{([^}]*)\}', text):
        found += [item.split('=')[0].strip() for item in body.split(',') if item.strip()]
    for tag, body, name in re.findall(r'\b(?:struct|union)\s*(\w*)\s*\{([^}]*)\}\s*(\w*)', text):
        found += [name or tag] + [pointer or field for pointer, field in
                                  re.findall(r'\(\s*\*\s*(\w+)\s*\)|(\w+)\s*(?:\[[^\]]*\]\s*)*;', body)]
    return list(dict.fromkeys(found))


def keys(table):
    for key, value in table.items():
        yield key
        for item in value if isinstance(value, list) else [value]:
            if isinstance(item, dict):
                yield from keys(item)


def spans(root, doc):
    return '\n'.join(re.findall(r'`([^`\n]+)`', (root / doc).read_text(encoding='utf-8'))) if (root / doc).is_file() else ''


def main():
    root = arguments().root
    files = sorted(ours(root))
    cases = '\n'.join(case['name'] for path in files if path.startswith('tests/cases/') and path.endswith('.toml')
                      for case in tomllib.loads((root / path).read_text(encoding='utf-8')).get('case', []))
    read = [path for path in files if path.startswith(('include/', 'presets/'))]
    found = []
    for path in read:
        doc = 'docs/extern/%s.md' % path
        text, source = spans(root, doc), (root / path).read_text(encoding='utf-8')
        if path.startswith('presets/'):
            found += ['%s: %s is not in %s' % (path, key, doc) for key in dict.fromkeys(keys(tomllib.loads(source)))
                      if not named(key, text)]
            continue
        for name in names(source):
            if not named(name, text):
                found.append('%s: %s is not in %s' % (path, name, doc))
            if not named(name, cases):
                found.append('%s: %s is in the name of no case' % (path, name))
    report(found, len(read))


if __name__ == '__main__':
    main()
