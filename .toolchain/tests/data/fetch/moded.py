# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import hashlib
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import fetch

case = Path(sys.argv[2])
archive = case / 'tools.zip'
with zipfile.ZipFile(archive, 'w') as packed:
    for name, mode in (('tool', 0o755), ('tool.exe', 0o755), ('note.txt', 0o644)):
        member = zipfile.ZipInfo('tools/' + name)
        member.external_attr = mode << 16
        packed.writestr(member, 'x')
fetch.fetched(archive.as_uri(), hashlib.sha256(archive.read_bytes()).hexdigest(), case / 'out')
print(os.stat(case / 'out' / 'tools' / sys.argv[3]).st_mode & 0o100 != 0)
