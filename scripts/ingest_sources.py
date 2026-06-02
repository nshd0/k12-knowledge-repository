from pathlib import Path
import csv

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
OUT = DATA / 'master_repository.csv'
SRC = DATA / 'source_index.csv'

HEADER = ['ID','Category','Subcategory','Title','Description','Issuing Authority','Grade Level','Subject/Theme','Resource Type','Language','Link','File/Location','Date Issued','Last Updated','Valid Until','Status','Tags','Notes','Source Priority','Verified On','Reviewed By']

if __name__ == '__main__':
    if not OUT.exists():
        with OUT.open('w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(HEADER)
    if SRC.exists():
        with SRC.open('r', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        print(f'Loaded {max(len(rows)-1,0)} sources')
    else:
        print('source_index.csv not found')
