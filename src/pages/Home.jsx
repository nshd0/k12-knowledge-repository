import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const stakeholders = [
  { role: 'principal', label: 'Principal', icon: '🏫', desc: 'Compliance, policy circulars, NEP action items, affiliation updates.' },
  { role: 'teacher', label: 'Teacher', icon: '👩\u200d🏫', desc: 'Pedagogy guides, NISHTHA training, assessment tools, DIKSHA resources.' },
  { role: 'student', label: 'Student', icon: '🎒', desc: 'NCERT textbooks, CBSE sample papers, DIKSHA content, revision aids.' },
  { role: 'parent', label: 'Parent', icon: '👨\u200d👩\u200d👧', desc: 'Exam schedules, admission notices, school circulars, simplified summaries.' },
  { role: 'coordinator', label: 'Coordinator', icon: '📋', desc: 'Source index, update logs, weekly digest, repository management.' },
]

const categories = [
  { label: 'Frameworks', icon: '📜', q: 'Framework', color: '#dbeafe' },
  { label: 'Circulars', icon: '📢', q: 'Circular', color: '#fef9c3' },
  { label: 'Capacity Building', icon: '🧑\u200d💻', q: 'Capacity Building', color: '#dcfce7' },
  { label: 'Assessment', icon: '📝', q: 'Assessment', color: '#fce7f3' },
  { label: 'Pedagogy', icon: '🎓', q: 'Pedagogy', color: '#ede9fe' },
  { label: 'Subject Resources', icon: '📖', q: 'Subject Resource', color: '#ffedd5' },
]

export default function Home() {
  const [summary, setSummary] = useState({ total_items: 0, active_items: 0, categories: [] })
  useEffect(() => {
    fetch('/site-summary.json').then(r => r.json()).then(setSummary).catch(() => {})
  }, [])

  return (
    <div className="page-home">
      <section className="hero">
        <div className="hero-badge">🇮🇳 Official K-12 Education Resources</div>
        <h1>Education Knowledge Repository</h1>
        <p className="hero-sub">
          Verified resources from Ministry of Education, NCERT, CBSE, Delhi DoE, DIKSHA, PARAKH and NIPUN Bharat —
          updated weekly and aligned with NEP 2020 &amp; NCF 2023.
        </p>
        <div className="hero-actions">
          <Link className="btn-primary" to="/browse">Browse all resources</Link>
          <Link className="btn-secondary" to="/updates">View update schedule</Link>
        </div>
        <div className="kpis">
          <div className="kpi"><strong>{summary.total_items || '51+'}</strong><span>Total resources</span></div>
          <div className="kpi"><strong>{summary.active_items || '51+'}</strong><span>Active</span></div>
          <div className="kpi"><strong>{summary.categories?.length || 6}</strong><span>Categories</span></div>
          <div className="kpi"><strong>12</strong><span>Official sources</span></div>
        </div>
      </section>

      <section className="section">
        <h2>Browse by category</h2>
        <div className="cat-grid">
          {categories.map(c => (
            <Link key={c.label} to={`/browse?cat=${encodeURIComponent(c.q)}`} className="cat-card" style={{ background: c.color }}>
              <span className="cat-icon">{c.icon}</span>
              <span className="cat-label">{c.label}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Choose your stakeholder view</h2>
        <div className="stakeholder-grid">
          {stakeholders.map(s => (
            <Link key={s.role} to={`/stakeholder/${s.role}`} className="s-card">
              <div className="s-icon">{s.icon}</div>
              <div>
                <h3>{s.label}</h3>
                <p>{s.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
