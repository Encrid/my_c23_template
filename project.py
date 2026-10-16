# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import subprocess
import sys
from pathlib import Path

COMMANDS = {'fetch': ['fetch.py'], 'build': ['build.py'], 'pack': ['build.py', '--pack'], 'test': ['test.py'],
            'check': ['check.py'], 'cla': ['cla.py']}


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command not in COMMANDS:
        sys.exit('project.py: name a command: ' + ' '.join(COMMANDS))
    tool, *first = COMMANDS[command]
    tools = Path(__file__).resolve().parent / 'tools'
    sys.exit(subprocess.run([sys.executable, str(tools / tool)] + first + sys.argv[2:]).returncode)


if __name__ == '__main__':
    main()
