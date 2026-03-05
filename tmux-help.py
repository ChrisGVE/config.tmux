#!/usr/bin/env python3
import subprocess

TABLES = ['prefix', 'root']

KEY_NAMES = {
    'DC':     'Delete',
    'IC':     'Insert',
    'PPage':  'PageUp',
    'NPage':  'PageDown',
    'BTab':   'Shift-Tab',
    'Enter':  'Enter',
    'Escape': 'Escape',
    'Space':  'Space',
    'Tab':    'Tab',
    'Up':     'Up',
    'Down':   'Down',
    'Left':   'Left',
    'Right':  'Right',
    'Home':   'Home',
    'End':    'End',
    'F1':     'F1',  'F2':  'F2',  'F3':  'F3',  'F4':  'F4',
    'F5':     'F5',  'F6':  'F6',  'F7':  'F7',  'F8':  'F8',
    'F9':     'F9',  'F10': 'F10', 'F11': 'F11', 'F12': 'F12',
}

def unescape(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            result.append(s[i + 1])
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

procs = {}
for table in TABLES:
    procs[(table, 'keys')]  = subprocess.Popen(['tmux', 'list-keys', '-T', table],
                                                stdout=subprocess.PIPE, text=True)
    procs[(table, 'notes')] = subprocess.Popen(['tmux', 'list-keys', '-N', '-T', table],
                                                stdout=subprocess.PIPE, text=True)
results = {k: p.communicate()[0] for k, p in procs.items()}

notes = {}
for table in TABLES:
    for line in results[(table, 'notes')].splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            notes[(table, parts[0])] = parts[1].strip()

keys_by_table = {t: [] for t in TABLES}
for table in TABLES:
    for line in results[(table, 'keys')].splitlines():
        parts = line.split(None, 4)
        if len(parts) < 4:
            continue
        if parts[1] == '-r':
            if len(parts) < 5:
                continue
            sub     = parts[4].split(None, 1)
            raw_key = sub[0]
            cmd     = sub[1] if len(sub) == 2 else ''
        else:
            raw_key = parts[3]
            cmd     = parts[4] if len(parts) == 5 else ''
        keys_by_table[table].append((raw_key, cmd))

for table in TABLES:
    rows = keys_by_table[table]
    if not rows:
        continue
    output_rows = []
    for raw_key, cmd in rows:
        key        = unescape(raw_key)
        display    = KEY_NAMES.get(key, key)
        desc       = notes.get((table, key)) or notes.get((table, raw_key)) or unescape(cmd)
        output_rows.append((display, desc))
    col_w = max(len(r[0]) for r in output_rows) + 2
    print(f'=== {table.upper()} ===')
    for display, desc in output_rows:
        print(f'  {display:<{col_w}}{desc}')
    print()
