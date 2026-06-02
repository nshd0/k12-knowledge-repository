import React from 'react'
import { useParams, Link } from 'react-router-dom'

const profiles = {
  principal: {
    label: 'Principal / School Leader', icon: '🏫',
    desc: 'Stay on top of compliance, policy updates, and board circulars.',
    links: [
      { label: 'CBSE Circulars', q: 'Circular' },
      { label: 'NEP 2020 Policy', q: 'NEP' },
      { label: 'Delhi DoE Notifications', q: 'Delhi DoE' },
      { label: 'School Affiliation', q: 'affiliation' },
      { label: 'NCF Framework', q: 'NCF' },
    ]
  },
  teacher: {
    label: 'Teacher', icon: '👩\u200d🏫',
    desc: 'Access pedagogy resources, assessment guides, and training programs.',
    links: [
      { label: 'NISHTHA Training', q: 'NISHTHA' },
      { label: 'DIKSHA Platform', q: 'DIKSHA' },
      { label: 'Pedagogy Guides', q: 'Pedagogy' },
      { label: 'Assessment Tools', q: 'Assessment' },
      { label: 'NCF Learning Outcomes', q: 'learning outcomes' },
    ]
  },
  student: {
    label: 'Student', icon: '🎒',
    desc: 'Find textbooks, sample papers, and digital learning content.',
    links: [
      { label: 'NCERT Textbooks', q: 'NCERT textbook' },
      { label: 'CBSE Sample Papers', q: 'sample paper' },
      { label: 'DIKSHA Learning', q: 'DIKSHA' },
      { label: 'Mathematics Resources', q: 'Mathematics' },
      { label: 'Science Resources', q: 'Science' },
    ]
  },
  parent: {
    label: 'Parent', icon: '👨\u200d👩\u200d👧',
    desc: 'Track exam schedules, admission notices, and school updates.',
    links: [
      { label: 'Exam Date Sheet', q: 'exam datesheet' },
      { label: 'Admission Notifications', q: 'admission' },
      { label: 'School Circulars', q: 'Circular' },
      { label: 'Board Results', q: 'result' },
    ]
  },
  coordinator: {
    label: 'Coordinator', icon: '📋',
    desc: 'Manage the source index, verify links, and run update workflows.',
    links: [
      { label: 'All Sources', q: 'Source' },
      { label: 'Frameworks', q: 'Framework' },
      { label: 'Capacity Building', q: 'Capacity Building' },
      { label: 'Assessment', q: 'Assessment' },
    ]
  }
}

export default function Stakeholder() {
  const { role } = useParams()
  const p = profiles[role] || { label: role, icon: '👤', desc: '', links: [] }
  return (
    <div className="page-stakeholder">
      <div className="s-hero">
        <div className="s-hero-icon">{p.icon}</div>
        <div>
          <h1>{p.label}</h1>
          <p className="lead">{p.desc}</p>
        </div>
      </div>
      <h2>Quick links</h2>
      <ul className="quick-links">
        {p.links.map(l => (
          <li key={l.label}>
            <Link to={`/browse?q=${encodeURIComponent(l.q)}`}>
              <span className="ql-arrow">→</span> {l.label}
            </Link>
          </li>
        ))}
      </ul>
      <Link className="btn-primary" to="/browse">Browse all resources</Link>
    </div>
  )
}
