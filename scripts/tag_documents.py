from pathlib import Path
import csv

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
MASTER = DATA / 'master_repository.csv'

KEYWORDS = {
    'CBSE': ['cbse'],
    'NCF': ['ncf'],
    'NEP': ['nep'],
    'Delhi DoE': ['edudel', 'doe', 'directorate of education'],
    'DIKSHA': ['diksha'],
}

if __name__ == '__main__':
    if MASTER.exists():
        with MASTER.open('r', encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            text = ' '.join([r.get('Title',''), r.get('Description',''), r.get('Notes','')]).lower()
            tags = [k for k, vals in KEYWORDS.items() if any(v in text for v in vals)]
            if tags:
                r['Tags'] = ', '.join(tags)
        with MASTER.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
        print(f'Tagged {len(rows)} records')
    else:
        print('master_repository.csv not found')
