# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import os
import shutil
import socket
import subprocess
import threading
import tomllib
from pathlib import Path

import build
import shared
from shared import die, expand, expanded, files, known, located, status


def environment(changes, values):
    env = dict(os.environ)
    for name, value in changes.items():
        env.pop(name, None)
        if value is not False:
            env[name] = expand(str(value), values)
    return env


def free_port():
    with socket.socket() as free:
        free.bind(('127.0.0.1', 0))
        return free.getsockname()[1]


def started(argv, root, timeout, env=None):
    proc = subprocess.Popen(argv, cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env)
    late = threading.Event()

    def stop():
        late.set()
        proc.kill()
    watch = threading.Timer(timeout, stop)
    watch.start()
    return {'proc': proc, 'late': late, 'watch': watch, 'said': []}


def waited(running, text):
    for line in iter(running['proc'].stdout.readline, b''):
        running['said'].append(line)
        if text.encode('utf-8') in line:
            return True
    return False


def typed(running, text):
    try:
        running['proc'].stdin.write(text.encode('utf-8'))
        running['proc'].stdin.flush()
    except OSError:
        pass


def ended(running, text):
    typed(running, text)
    try:
        running['proc'].stdin.close()
    except OSError:
        pass
    running['said'].append(running['proc'].stdout.read())
    code = running['proc'].wait()
    running['watch'].cancel()
    said = b''.join(running['said']).decode('utf-8', 'replace').replace('\r', '')
    return None if running['late'].is_set() else code, said


def ordered(wanted, lines):
    rest = iter(lines)
    return all(any(line == one.strip() for one in rest) for line in wanted)


def holding(path, text):
    return path.is_file() and text in path.read_text(encoding='utf-8')


def holds(claims, lacks, code, said, values):
    lines = said.split('\n')
    known(claims, 'claims', 'a case')
    return all([code == claims.get('status', code), code != claims.get('status_not', None),
                all(expand(line, values) in lines for line in claims.get('line', [])),
                all(expand(text, values) in said for text in claims.get('has', [])),
                all(expand(text, values) not in said for text in claims.get('lacks', []) + lacks),
                ordered([expand(line, values) for line in claims.get('order', [])], lines),
                all(holding(located(path, values), expand(text, values))
                    for path, text in claims.get('files', {}).items())])


def source_of(item, outputs, values):
    name = expand(item, values)
    return outputs[name] if name in outputs else Path(values['root']) / name


def placed(use, outputs, values):
    for folder, held in use.get('folders', {}).items():
        located(folder, values).mkdir(parents=True, exist_ok=True)
        for item in held:
            source = source_of(item, outputs, values)
            shutil.copy(source, located(folder, values) / source.name)
    for path, text in use.get('files', {}).items():
        located(path, values).parent.mkdir(parents=True, exist_ok=True)
        located(path, values).write_text(expand(text, values), encoding='utf-8', newline='\n')


def scripted(running, script, outputs, values):
    for step in script:
        if not waited(running, expand(known(step, 'script', 'a case')['wait'], values)):
            return
        for path, item in step.get('put', {}).items():
            shutil.copy(source_of(item, outputs, values), located(path, values))
        for path in step.get('remove', []):
            located(path, values).unlink()
        if 'type' in step:
            typed(running, expand(step['type'], values) + '\n')


def made_false(case):
    false = case.get('false', {})
    merged = dict(case, **false)
    for key in ('files', 'folders'):
        merged[key] = dict(case.get(key, {}), **false.get(key, {}))
    return merged


def tried(config, values, outputs, where, case, broken):
    folder = Path(values['out']) / 'cases' / where
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True, exist_ok=True)
    mine, use = dict(values, case=folder.as_posix(), port=free_port()), made_false(case) if broken else case
    placed(use, outputs, mine)
    root, timeout, helper = values['root'], config['test']['timeout'], use.get('helper')
    beside = started(expanded(helper['run'], mine), root, timeout) if helper else None
    if helper:
        waited(beside, expand(helper['wait'], mine))
    running = started(expanded(use['run'], mine), root, timeout, environment(use.get('env', {}), mine))
    scripted(running, use.get('script', []), outputs, mine)
    ends = [ended(running, expand(use.get('stdin', ''), mine))]
    if helper:
        ends.append(ended(beside, expand(helper.get('stdin', ''), mine)))
    return ends, [use.get('claims', {})] + ([helper.get('claims', {})] if helper else []), mine


def verdict(config, values, outputs, group, index, case, broken):
    ends, claims, mine = tried(config, values, outputs, '%s/%d' % (group, index), case, broken)
    lacks = [rule['lacks'] for rule in config['test'].get('rule', []) if group not in rule.get('exempt', [])]
    if any(code is None for code, _ in ends):
        return False, 'did not end in %d seconds' % config['test']['timeout'], ends
    held = all(holds(claim, lacks, code, said, mine) for claim, (code, said) in zip(claims, ends))
    if broken:
        return not held, 'still as written' if held else 'fails, as it must', ends
    return held, 'as written' if held else 'differs', ends


def test(config, values, outputs, groups, broken):
    wrong = []
    for group, cases in groups:
        right = 0
        for index, case in enumerate(cases):
            ok, how, ends = verdict(config, values, outputs, group, index, case, broken)
            print('%s%s: %s' % (case['name'], ', made false' if broken else '', how))
            right += ok
            if not ok:
                wrong.append(case['name'])
                for whose, (code, said) in zip(('', 'the helper '), ends):
                    print('  %sended with %s, and printed:\n%s' % (whose, 'no status' if code is None else status(code),
                                                                  said.rstrip()))
        print('%s: %d claims made false: %d cases failed' % (group, len(cases), right) if broken else
              '%s: %d cases: %d as written' % (group, len(cases), right))
    if wrong:
        die(('still as written with their claims made false: ' if broken else 'not as written: ') + ', '.join(wrong))


def groups_of(values):
    root, found = Path(values['root']), []
    for path in files(root, ['tests/cases/**/*.toml']):
        cases = tomllib.loads((root / path).read_text(encoding='utf-8')).get('case', [])
        for case in cases:
            known(case, 'case', path)
            known(case.get('false', {}), 'false', path)
            known(case.get('helper', {}), 'helper', path)
            if not case.get('claims'):
                die('%s: the case %s claims nothing' % (path, case['name']))
            if 'false' not in case:
                die('%s: the case %s has no false variant' % (path, case['name']))
        found.append((Path(path).relative_to('tests/cases').with_suffix('').as_posix(), cases))
    return [(group, cases) for group, cases in found if cases]


def main():
    args = shared.arguments(broken='--break')
    config, values, made = build.build(args, True)
    unlinked = [name for name, paths in made if not paths]
    if unlinked:
        die('the cases need what is linked: ' + ' '.join(unlinked))
    groups = groups_of(values)
    if not groups:
        return print('no case: tests/cases holds no case')
    test(config, values, {name: paths[0] for name, paths in made}, groups, args.broken)


if __name__ == '__main__':
    main()
