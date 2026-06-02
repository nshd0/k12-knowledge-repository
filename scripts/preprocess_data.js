import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const base = path.resolve(__dirname, '..')
const input = path.join(base, 'data', 'master_repository.csv')
const dist = path.join(base, 'dist')
fs.mkdirSync(dist, { recursive: true })

const parseCSV = (text) => {
  const lines = text.trim().split(/\r?\n/)
  const headers = lines.shift().split(',')
  return lines.map(line => {
    const cols = []
    let cur = '', q = false
    for (let i = 0; i < line.length; i++) {
      const c = line[i]
      if (c === '"') { q = !q; continue }
      if (c === ',' && !q) { cols.push(cur); cur=''; continue }
      cur += c
    }
    cols.push(cur)
    return Object.fromEntries(headers.map((h, i) => [h, cols[i] || '']))
  })
}

const rows = fs.existsSync(input) ? parseCSV(fs.readFileSync(input, 'utf8')) : []
const normalize = s => (s || '').toLowerCase().replace(/\s+/g, ' ').trim()
const tokens = s => Array.from(new Set(normalize(s).match(/[a-z0-9]+/g) || []))

const index = rows.map(r => ({
  id: r.ID || '',
  title: r.Title || '',
  category: r.Category || '',
  status: r.Status || '',
  link: r.Link || '',
  authority: r['Issuing Authority'] || '',
  tags: normalize(r.Tags || '').split(',').map(x => x.trim()).filter(Boolean),
  tokens: tokens([r.Title, r.Description, r.Tags, r.Notes, r.Category, r['Subject/Theme'], r['Issuing Authority']].join(' '))
}))

const summary = {
  total_items: index.length,
  active_items: rows.filter(r => normalize(r.Status) === 'active').length,
  categories: [...new Set(index.map(i => i.category))].sort()
}

fs.writeFileSync(path.join(dist, 'data-index.json'), JSON.stringify(index))
fs.writeFileSync(path.join(dist, 'site-summary.json'), JSON.stringify(summary))
fs.writeFileSync(path.join(dist, 'search-manifest.json'), JSON.stringify({ count: index.length, categories: summary.categories }))
console.log('preprocessed', index.length, 'items')
