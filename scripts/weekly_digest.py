from pathlib import Path
import csv
from collections import Counter

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
MASTER = DATA / 'master_repository.csv'
OUT = BASE / 'docs' / 'weekly_digest.md'

if __name__ == '__main__':
    if not MASTER.exists():
        raise SystemExit('master_repository.csv not found')
    with MASTER.open('r', encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    c = Counter(r.get('Category','Uncategorized') for r in rows)
    lines = ['# Weekly Digest', '', '## Counts']
    lines += [f'- {k}: {v}' for k, v in c.items()]
    lines += ['', '## Active Items']
    for r in rows[:10]:
        lines.append(f'- {r.get("Title","")} ({r.get("Status","")})')
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {OUT}')
