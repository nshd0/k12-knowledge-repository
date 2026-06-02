import React from 'react'

const sources = [
  { id: 'SI-001', name: 'Ministry of Education', url: 'https://www.education.gov.in', authority: 'National', pattern: 'Monthly' },
  { id: 'SI-002', name: 'NCERT', url: 'https://ncert.nic.in', authority: 'National', pattern: 'Monthly' },
  { id: 'SI-003', name: 'CBSE Student Circulars', url: 'https://www.cbse.gov.in/cbsenew/list-of-circulars-related-to-student.html', authority: 'National Board', pattern: 'Weekly' },
  { id: 'SI-004', name: 'CBSE SARAS', url: 'https://saras.cbse.gov.in/saras/Home/Circulars', authority: 'National Board', pattern: 'Weekly' },
  { id: 'SI-005', name: 'CBSE Academic', url: 'https://cbseacademic.nic.in', authority: 'National Board', pattern: 'Monthly' },
  { id: 'SI-006', name: 'Delhi DoE', url: 'https://www.edudel.nic.in', authority: 'State', pattern: 'Weekly' },
  { id: 'SI-007', name: 'DIKSHA', url: 'https://diksha.gov.in', authority: 'National', pattern: 'Weekly' },
  { id: 'SI-008', name: 'NIPUN Bharat', url: 'https://nipunbharat.education.gov.in', authority: 'National', pattern: 'Monthly' },
  { id: 'SI-009', name: 'PARAKH', url: 'https://parakh.gov.in', authority: 'National', pattern: 'Monthly' },
  { id: 'SI-010', name: 'NCTE', url: 'https://ncte.gov.in', authority: 'National', pattern: 'Quarterly' },
  { id: 'SI-011', name: 'iGOT Karmayogi', url: 'https://igotkarmayogi.gov.in', authority: 'National', pattern: 'Monthly' },
  { id: 'SI-012', name: 'NISHTHA', url: 'https://itpd.ncert.gov.in', authority: 'National', pattern: 'Monthly' },
]

export default function SourceIndex() {
  return (
    <div className="page-sources">
      <h1>Source Index</h1>
      <p className="lead">All 12 verified official sources used in this repository.</p>
      <div className="source-grid">
        {sources.map(s => (
          <div className="source-card" key={s.id}>
            <div className="source-top">
              <span className="source-id">{s.id}</span>
              <span className="source-authority">{s.authority}</span>
            </div>
            <div className="source-name">{s.name}</div>
            <div className="source-pattern">Updated: {s.pattern}</div>
            <a href={s.url} target="_blank" rel="noreferrer" className="source-link">Visit ↗</a>
          </div>
        ))}
      </div>
    </div>
  )
}
