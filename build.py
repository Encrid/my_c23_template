import argparse
import hashlib
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import threading
import tomllib
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = re.compile(r'\{([a-z_][a-z0-9_]*)(?::([^{}]*))?\}')
DIGEST = re.compile(r'[0-9a-f]{64}')
KEYS = {'step': {'run', 'section', 'text', 'contains', 'copy', 'rename'},
        'case': {'name', 'run', 'env', 'stdin', 'script', 'helper', 'files', 'folders', 'claims', 'false'},
        'false': {'run', 'env', 'stdin', 'script', 'helper', 'files', 'folders'},
        'helper': {'run', 'wait', 'stdin', 'claims'},
        'script': {'wait', 'put', 'remove', 'type'},
        'claims': {'status', 'status_not', 'line', 'has', 'lacks', 'order', 'files'},
        'source': {'name', 'url', 'sha256', 'into', 'top', 'patches'}}


def die(why):
    sys.exit('build.py: ' + why)


def known(table, what, where):
    unknown = sorted(set(table) - KEYS[what])
    if unknown:
        die('%s: a %s has no key %s' % (where, what, ' '.join(unknown)))
    return table


def located(text, values):
    return Path(values['root']) / expand(text, values)


def expand(text, values):
    def one(m):
        if m.group(1) not in values:
            die('no variable {%s} for %s' % (m.group(1), text))
        value = values[m.group(1)]
        if not isinstance(value, list):
            return expand(str(value), values)
        if m.group(2) is None:
            die('{%s} is a list inside a text: write {%s:<separator>}' % (m.group(1), m.group(1)))
        return m.group(2).join(expanded(value, values))
    return NAME.sub(one, text)


def expanded(items, values):
    out = []
    for item in items:
        whole = NAME.fullmatch(item)
        if whole and whole.group(2) is None and isinstance(values.get(whole.group(1)), list):
            out += expanded(values[whole.group(1)], values)
        else:
            out.append(expand(item, values))
    return out


def files(root, patterns):
    found = [p.relative_to(root).as_posix() for pattern in patterns
             for p in sorted(root.glob(pattern)) if p.is_file()]
    return list(dict.fromkeys(found))


def status(code):
    return '%d (0x%08X)' % (code, code & 0xFFFFFFFF)


def run(argv, root):
    done = subprocess.run(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    said = done.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    if done.returncode:
        die('%s\n  ended with %s\n%s' % (' '.join(argv), status(done.returncode), said))
    sys.stdout.write(said)


def this_target(targets):
    machine = [platform.system(), platform.machine()]
    return next((name for name, row in targets.items() if row['runs_on'] == machine), None)


def zig_found(root, zig):
    fetched = [p for p in (root / zig['folder']).glob('*/zig*') if p.name in ('zig', 'zig.exe')]
    path = str(fetched[0]) if fetched else shutil.which('zig')
    version = path and subprocess.run([path, 'version'], capture_output=True, text=True).stdout.strip()
    return Path(path).as_posix() if version == zig['version'] else None


def fetched(url, digest, folder):
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    path = folder / url.rsplit('/', 1)[1]
    with urllib.request.urlopen(url) as got, open(path, 'wb') as f:
        shutil.copyfileobj(got, f)
    with open(path, 'rb') as f:
        found = hashlib.file_digest(f, 'sha256').hexdigest()
    if found != digest:
        path.unlink()
        die('%s is not what the maker publishes: its sha256 is %s' % (path.name, found))
    shutil.unpack_archive(path, folder)
    path.unlink()


def fetch_zig(root, zig, home):
    archive = zig['archives'].get(home) or die('zig is fetched on a machine that runs a target')
    url = zig['url'].format(version=zig['version'], host=archive['host'], format=archive['format'])
    fetched(url, archive['sha256'], root / zig['folder'])
    return zig_found(root, zig) or die('the archive holds no zig %s' % zig['version'])


def hunks(part):
    lines = part.split('\n')
    for at, line in enumerate(lines):
        m = re.match(r'@@ -(\d+)(?:,(\d+))? \+\d+(?:,(\d+))? @@', line)
        old, new = [], []
        for body in lines[at + 1:] if m else []:
            if len(old) == int(m.group(2) or 1) and len(new) == int(m.group(3) or 1):
                break
            if not body.startswith('\\'):
                old += [body[1:]] if body[:1] in ('', ' ', '-') else []
                new += [body[1:]] if body[:1] in ('', ' ', '+') else []
        if m:
            yield int(m.group(1)) - 1, old, new


def patched(tree, patch):
    for part in re.split(r'(?m)^diff --git ', patch.read_text(encoding='utf-8').replace('\r\n', '\n'))[1:]:
        name = re.search(r'(?m)^\+\+\+ b/(.+)$', part).group(1)
        lines, shift = (tree / name).read_bytes().decode('utf-8').split('\n'), 0
        for at, old, new in hunks(part):
            if lines[at + shift:at + shift + len(old)] != old:
                die('%s does not apply to %s' % (patch.as_posix(), name))
            lines[at + shift:at + shift + len(old)] = new
            shift += len(new) - len(old)
        (tree / name).write_bytes('\n'.join(lines).encode('utf-8'))


def sources(config, values, fetching):
    for source in config.get('source', []):
        known(source, 'source', 'a source')
        into, patches = located(source['into'], values), [located(p, values) for p in source.get('patches', [])]
        tree, stamp = into / expand(source.get('top', ''), values), expand(source['sha256'], values)
        values[source['name']] = tree.as_posix()
        stamp = ' '.join([stamp] + [sha256(patch.read_bytes()) for patch in patches])
        if (into / 'fetched.txt').is_file() and (into / 'fetched.txt').read_text(encoding='utf-8') == stamp:
            continue
        if not fetching:
            die('%s is not fetched as build.config.toml states: run fetch' % source['name'])
        url = expand(source['url'], values)
        fetched(url if '://' in url else located(url, values).as_uri(), stamp.split(' ')[0], into)
        for patch in patches:
            patched(tree, patch)
        (into / 'fetched.txt').write_text(stamp, encoding='utf-8')


def variables(config, args, root, target, zig):
    build = (args.out or root / config['build']['folder']).resolve()
    values = {'root': root.as_posix(), 'build': build.as_posix(), 'home': this_target(config['targets']) or '',
              'out': (build / (target + ('-debug' if args.debug else ''))).as_posix(), 'target': target,
              'python': Path(sys.executable).as_posix(), 'script': Path(__file__).resolve().as_posix(), 'zig': zig}
    values.update(config['targets'][target])
    own = config.get('variables', {})
    if set(own) & set(values):
        die('[variables] names a built-in variable or a key of a target: ' + ' '.join(sorted(set(own) & set(values))))
    values.update(own)
    if args.debug:
        values.update(config.get('debug', {}))
    for setting in args.set:
        name, _, value = setting.partition('=')
        if name not in own:
            die('--set %s: [variables] has no %s' % (setting, name))
        values[name] = value
    return values


def tools(config, values):
    for name, path in config.get('tools', {}).items():
        found = shutil.which(located(path, values)) or die('the tool %s is not at %s' % (name, expand(path, values)))
        values[name] = Path(found).as_posix()


def listed(path):
    keys, digests = {}, {}
    for line in path.read_text(encoding='utf-8').splitlines():
        head, _, rest = line.partition(' ')
        if DIGEST.fullmatch(head):
            digests[rest.strip()] = head
        elif head:
            keys[head] = rest.strip()
    return keys, digests


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def copies(found):
    out = []
    for taken in found.values():
        for file, digest in taken['digests'].items():
            source, copy = taken['source'] / file, taken['into'] / file
            if copy.is_file() and sha256(copy.read_bytes()) == digest:
                continue
            if not source.is_file():
                die('%s is not there' % source.as_posix())
            if sha256(source.read_bytes()) != digest:
                die('refused: %s is not what %s states' % (source.as_posix(), taken['listing'].as_posix()))
            out.append((copy, source.read_bytes()))
    return out


def take(config, values):
    found = {}
    for dependency in config.get('dependency', []):
        if 'make' in dependency:
            run(expanded(dependency['make'], values), values['root'])
        source, into = located(dependency['from'], values), located(dependency['into'], values)
        listing = source / dependency['list']
        values[dependency['name']] = into.as_posix()
        if not listing.is_file() and not dependency.get('optional'):
            die('%s is not there' % listing.as_posix())
        if not listing.is_file():
            print('not taken: %s is not there' % listing.as_posix())
            continue
        keys, digests = listed(listing)
        found[dependency['name']] = {'source': source, 'listing': listing, 'into': into, 'keys': keys,
                                     'digests': digests}
    for rule in config.get('agree', []):
        said = {key: found[key.split('.')[0]]['keys'].get(key.split('.')[1], '')[:rule['length']]
                for key in rule['keys'] if key.split('.')[0] in found}
        if len(set(said.values())) > 1:
            die('refused: the dependencies do not agree: ' + ', '.join('%s %s' % pair for pair in said.items()))
    for path, data in copies(found):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for name, taken in found.items():
        print('taken: %s, %s' % (name, ', '.join('%s %s' % pair for pair in taken['keys'].items())))


def leb(n):
    return bytes((n >> shift & 0x7f) | (0x80 if n >> shift + 7 else 0) for shift in range(0, max(n.bit_length(), 1), 7))


def do(step, values, unstamped):
    root = Path(values['root'])
    if 'run' in step:
        run(expanded(step['run'], values), values['root'])
    if 'section' in step and not unstamped:
        name = step['section'].encode('utf-8')
        content = leb(len(name)) + name + expand(step['text'], values).encode('utf-8')
        with open(values['output'], 'ab') as f:
            f.write(b'\0' + leb(len(content)) + content)
    if 'contains' in step and expand(step['contains'], values).encode('utf-8') not in Path(values['output']).read_bytes():
        die('%s does not hold %r' % (values['output'], expand(step['contains'], values)))
    if 'copy' in step:
        shutil.copyfile(*[root / path for path in expanded(step['copy'], values)])
    if 'rename' in step:
        os.replace(*[root / path for path in expanded(step['rename'], values)])


def put(path, data):
    if not path.is_file() or path.read_bytes() != data:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def built(config, values, artifact):
    kind = config['kinds'][artifact['kind']]
    mine = dict(values)
    if 'target' in artifact:
        mine.update(config['targets'][artifact['target']], target=artifact['target'])
    name = expand(artifact['name'], mine)
    mine['name'] = name
    sources = files(Path(values['root']), [expand(pattern, mine) for pattern in artifact['sources']])
    if not sources:
        die('no file matches the sources of %s' % name)
    output = Path(values['out']) / artifact.get('folder', '') / expand(kind['output'], mine)
    work = Path(values['out']) / 'obj' / name
    mine.update(sources=sources, output=output.as_posix(), work=work.as_posix(),
                defines=['-D' + define for define in expanded(artifact.get('defines', []), mine)],
                include=['-I' + folder for folder in expanded(artifact.get('include', []), mine)],
                link=expanded(artifact.get('link', []), mine), manifest=expanded(artifact.get('manifest', []), mine))
    output.parent.mkdir(parents=True, exist_ok=True)
    work.parent.mkdir(parents=True, exist_ok=True)
    missing = [file for file in mine['link'] if not Path(file).is_file()]
    if missing and 'unlinked' not in kind:
        die('%s is not there, and %s is linked with it' % (missing[0], name))
    if missing:
        print('compiled, not linked: %s: %s is not there' % (name, missing[0]))
    for step in kind['unlinked' if missing else 'steps']:
        do(known(step, 'step', artifact['kind']), mine, artifact.get('unstamped', False))
    if missing:
        return name, []
    besides = [Path(file) for file in expanded(artifact.get('beside', []), mine)]
    for file in besides:
        put(output.parent / file.name, file.read_bytes())
    return name, [output] + [output.parent / file.name for file in besides]


def packaged(config, values, made):
    out = Path(values['out'])
    lines = ['package %s' % config['project']['name'], 'target %s' % values['target']]
    lines += ['%s  %s' % (sha256(path.read_bytes()), path.relative_to(out).as_posix()) for path in dict.fromkeys(made)]
    (out / 'package.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')


def artifacts(config):
    for artifact in config.get('artifact', []):
        yield artifact
        for variant in artifact.get('variants', []):
            yield dict(artifact, **variant)


def named(config, name):
    return next((a for a in config.get('artifact', []) if a['name'] == name), None) or die('no artifact %s' % name)


def programs(config, values):
    test, root = config['test'], Path(values['root'])
    if not test['programs']:
        return []
    main = named(config, test['artifact'])
    linked = [source for source in files(root, [expand(p, values) for p in main['sources']]) if source != test['entry']]
    return [dict(main, name=Path(program).stem, folder='tests', sources=linked + [program])
            for program in files(root, test['programs'])]


def uncovered(config, values, groups):
    test, root = config['test'], Path(values['root'])
    if not test['features']:
        return []
    names = set()
    for source in files(root, [expand(p, values) for p in named(config, test['artifact'])['sources']]):
        text = (root / source).read_text(encoding='utf-8')
        names.update(name for pattern in test['features'] for name in re.findall(pattern, text))
    said = [' '.join([case['name']] + case.get('run', [])) for _, cases in groups for case in cases]
    said += [(root / program).read_text(encoding='utf-8') for program in files(root, test['programs'])]
    text = '\n'.join(said)
    return sorted(name for name in names if not re.search(r'(?<!\w)%s(?!\w)' % re.escape(name), text))


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
            shutil.copyfile(source, located(folder, values) / source.name)
    for path, text in use.get('files', {}).items():
        located(path, values).parent.mkdir(parents=True, exist_ok=True)
        located(path, values).write_text(expand(text, values), encoding='utf-8', newline='\n')


def scripted(running, script, outputs, values):
    for step in script:
        if not waited(running, expand(known(step, 'script', 'a case')['wait'], values)):
            return
        for path, item in step.get('put', {}).items():
            shutil.copyfile(source_of(item, outputs, values), located(path, values))
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
        right = held != ('false' in case)
        return right, 'fails, as it must' if right else 'still as written', ends
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


def groups_of(config, values, exes):
    root, test = Path(values['root']), config['test']
    found = [('programs', [{'name': name, 'run': [exe.as_posix()], 'claims': {'status': 0}} for name, exe in exes])]
    for path in files(root, test['groups']):
        cases = tomllib.loads((root / path).read_text(encoding='utf-8')).get('case', [])
        for case in cases:
            known(case, 'case', path)
            known(case.get('false', {}), 'false', path)
            known(case.get('helper', {}), 'helper', path)
            if not case.get('claims'):
                die('%s: the case %s claims nothing' % (path, case['name']))
        found.append((Path(path).stem, cases))
    return [(group, cases) for group, cases in found if cases]


def style(config, root):
    failed = [tool for tool in config['style']['tools']
              if subprocess.run([sys.executable, str(HERE / tool)], cwd=root).returncode]
    if failed:
        die('the coding style does not hold: ' + ' '.join(failed))


def main():
    ap = argparse.ArgumentParser(prog='build.py')
    ap.add_argument('command', choices=['fetch', 'build', 'test', 'style'])
    ap.add_argument('--root', type=Path, default=HERE)
    ap.add_argument('--target')
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--out', type=Path)
    ap.add_argument('--set', action='append', default=[], metavar='NAME=VALUE')
    ap.add_argument('--break', dest='broken', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve()
    config = tomllib.loads((root / 'build.config.toml').read_text(encoding='utf-8'))
    if args.command == 'style':
        return style(config, root)
    home = this_target(config['targets'])
    if args.command == 'fetch':
        home = home or die('fetch runs on a machine of a target')
        zig = zig_found(root, config['zig']) or fetch_zig(root, config['zig'], home)
        print(zig)
        values = variables(config, args, root, home, zig)
        sources(config, values, True)
        return take(config, values)
    target = args.target or home or die('no target runs on %s %s: name one' % (platform.system(), platform.machine()))
    if target not in config['targets']:
        die('no target %s; the targets: %s' % (target, ' '.join(config['targets'])))
    if args.command == 'test' and target != home:
        die('%s does not run here: build it, and test it where it runs' % target)
    base = (args.out or root / config['build']['folder']).resolve()
    os.environ['ZIG_GLOBAL_CACHE_DIR'] = str(base / config['build']['cache'] / 'global')
    os.environ['ZIG_LOCAL_CACHE_DIR'] = str(base / config['build']['cache'] / 'local')
    zig = zig_found(root, config['zig']) or die('zig %s is neither fetched nor on the path' % config['zig']['version'])
    values = variables(config, args, root, target, zig)
    sources(config, values, False)
    tools(config, values)
    take(config, values)
    made = [built(config, values, artifact) for artifact in artifacts(config)]
    packaged(config, values, [path for _, paths in made for path in paths])
    outputs = {name: paths[0] for name, paths in made if paths}
    if args.command == 'build':
        return print('\n'.join(path.as_posix() for path in outputs.values()))
    unlinked = [name for name, paths in made if not paths]
    if unlinked:
        die('the cases need what is linked: ' + ' '.join(unlinked))
    exes = [(program['sources'][-1], built(config, values, program)[1][0]) for program in programs(config, values)]
    groups = groups_of(config, values, exes)
    missing = uncovered(config, values, groups)
    if missing:
        die('no case and no test program names: ' + ' '.join(missing))
    if not groups:
        return print('no case: [test] names no group of cases and no test program')
    test(config, values, outputs, groups, args.broken)


if __name__ == '__main__':
    main()
