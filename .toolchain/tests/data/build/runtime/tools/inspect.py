import struct
import subprocess
import sys
from pathlib import Path

TARGET = 'x86_64-windows-gnu'


def built(root, out):
    data = Path(root) / '.toolchain' / 'tests' / 'data' / 'build' / 'runtime'
    done = subprocess.run([sys.executable, str(Path(root) / '.toolchain' / 'tools' / 'build.py'), '--root', str(data),
                           '--out', out, '--target', TARGET], capture_output=True, text=True)
    if done.returncode:
        raise SystemExit(done.stdout + done.stderr)
    return Path(out) / TARGET


def sections(data):
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    count = struct.unpack_from('<H', data, pe + 6)[0]
    size = struct.unpack_from('<H', data, pe + 20)[0]
    rows = [struct.unpack_from('<8sIIII', data, pe + 24 + size + 40 * i) for i in range(count)]
    return pe + 24, rows


def offset(rows, rva):
    for _, virtual, address, raw, at in rows:
        if address <= rva < address + max(virtual, raw):
            return rva - address + at
    raise SystemExit('no section holds the address %#x' % rva)


def text(data, at):
    return data[at:data.index(b'\0', at)].decode()


def imports(path):
    data = path.read_bytes()
    optional, rows = sections(data)
    table = offset(rows, struct.unpack_from('<I', data, optional + 120)[0])
    found = []
    while struct.unpack_from('<I', data, table + 12)[0]:
        names, _, _, dll, _ = struct.unpack_from('<IIIII', data, table)
        at = offset(rows, names)
        while struct.unpack_from('<Q', data, at)[0]:
            entry = struct.unpack_from('<Q', data, at)[0]
            if not entry >> 63:
                found.append('%s: %s' % (text(data, offset(rows, dll)), text(data, offset(rows, entry) + 2)))
            at += 8
        table += 20
    return found


def main():
    mode, root, out, name = sys.argv[1:5]
    dll = built(root, out) / (name + '.dll')
    if mode == 'size':
        print('%s.dll: %s' % (name, 'under 16 KB' if dll.stat().st_size < 16384 else '16 KB or more'))
    else:
        print('\n'.join(imports(dll)))


if __name__ == '__main__':
    main()
