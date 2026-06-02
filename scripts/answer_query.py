from pathlib import Path
import csv, sys

BASE = Path(__file__).resolve().parents[1]
MASTER = BASE / 'data' / 'master_repository.csv'

q = ' '.join(sys.argv[1:]).lower().strip()
if not q:
    raise SystemExit('Provide a query')
with MASTER.open('r', encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
hits = []
for r in rows:
    hay = ' '.join(r.get(k,'') for k in ['Title','Description','Tags','Notes','Category','Subcategory','Subject/Theme']).lower()
    if all(t in hay for t in q.split()):
        hits.append(r)
for r in hits[:10]:
    print(f"{r.get('Title')} | {r.get('Status')} | {r.get('Link')}")
