import React, { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import Fuse from 'fuse.js'

export default function Browse() {
  const [data, setData] = useState([])
  const [q, setQ] = useState('')
  const [cat, setCat] = useState('All')
  const [searchParams] = useSearchParams()

  useEffect(() => {
    fetch('/data-index.json').then(r => r.json()).then(setData).catch(() => {})
  }, [])

  useEffect(() => {
    const catParam = searchParams.get('cat')
    const qParam = searchParams.get('q')
    if (catParam) setCat(catParam)
    if (qParam) setQ(qParam)
  }, [searchParams])

  const cats = ['All', ...new Set(data.map(d => d.category).filter(Boolean))].sort((a, b) => a === 'All' ? -1 : a.localeCompare(b))

  const results = useMemo(() => {
    let list = data
    if (cat !== 'All') list = list.filter(x => x.category === cat)
    if (q.trim()) {
      const fuse = new Fuse(list, {
        keys: ['title', 'category', 'authority', 'tags'],
        threshold: 0.35,
        includeScore: true
      })
      list = fuse.search(q).map(r => r.item)
    }
    return list
  }, [data, q, cat])

  const statusColor = s => ({
    Active: '#16a34a', Archived: '#64748b', Superseded: '#d97706', 'Pending Review': '#2563eb'
  })[s] || '#111'

  return (
    <div className="page-browse">
      <h1>Browse Resources</h1>
      <div className="toolbar">
        <div className="search-wrap">
          <span className="search-icon">🔍</span>
          <input
            value={q}
            onChange={e => setQ(e.target.value)}
            placeholder="Search by topic, board, subject, circular..."
          />
          {q && <button className="clear-btn" onClick={() => setQ('')}>✕</button>}
        </div>
        <div className="chips">
          {cats.map(c => (
            <button key={c} className={cat === c ? 'chip active' : 'chip'} onClick={() => setCat(c)}>{c}</button>
          ))}
        </div>
      </div>
      <p className="result-count">{results.length} result{results.length !== 1 ? 's' : ''}{cat !== 'All' ? ` in ${cat}` : ''}{q ? ` for "${q}"` : ''}</p>
      {data.length === 0 && (
        <div className="empty-state">
          <p>⏳ Loading resources...</p>
          <p className="empty-sub">If this persists, the data index may not be built yet. Deploy the app first.</p>
        </div>
      )}
      <div className="cards">
        {results.map(i => (
          <article className="card" key={i.id + i.title}>
            <div className="card-top">
              <span className="badge">{i.category}</span>
              <span className="status-dot" style={{ color: statusColor(i.status) }}>● {i.status}</span>
            </div>
            <h3>{i.title}</h3>
            {i.authority && <p className="authority">🏛 {i.authority}</p>}
            {i.tags?.length > 0 && (
              <div className="tag-row">
                {i.tags.slice(0, 4).map(t => <span key={t} className="tag">{t}</span>)}
              </div>
            )}
            <div className="card-footer">
              {i.link
                ? <a href={i.link} target="_blank" rel="noreferrer" className="open-link">Open source ↗</a>
                : <span className="no-link">No link</span>
              }
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}
