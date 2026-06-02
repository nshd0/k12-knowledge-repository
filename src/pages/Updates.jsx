import React from 'react'

const sources = [
  { name: 'CBSE Student Circulars', url: 'https://www.cbse.gov.in/cbsenew/list-of-circulars-related-to-student.html', cadence: 'Weekly', icon: '📢' },
  { name: 'CBSE SARAS Portal', url: 'https://saras.cbse.gov.in/saras/Home/Circulars', cadence: 'Weekly', icon: '📢' },
  { name: 'Delhi DoE', url: 'https://www.edudel.nic.in', cadence: 'Weekly', icon: '🏛' },
  { name: 'DIKSHA', url: 'https://diksha.gov.in', cadence: 'Weekly', icon: '💻' },
  { name: 'Ministry of Education', url: 'https://www.education.gov.in', cadence: 'Monthly', icon: '🇮🇳' },
  { name: 'NCERT', url: 'https://ncert.nic.in', cadence: 'Monthly', icon: '📚' },
  { name: 'CBSE Academic', url: 'https://cbseacademic.nic.in', cadence: 'Monthly', icon: '📝' },
  { name: 'PARAKH', url: 'https://parakh.gov.in', cadence: 'Monthly', icon: '📊' },
  { name: 'NIPUN Bharat', url: 'https://nipunbharat.education.gov.in', cadence: 'Monthly', icon: '🎯' },
  { name: 'NCTE', url: 'https://ncte.gov.in', cadence: 'Quarterly', icon: '🎓' },
  { name: 'iGOT Karmayogi', url: 'https://igotkarmayogi.gov.in', cadence: 'Monthly', icon: '🧑\u200d💼' },
  { name: 'NISHTHA', url: 'https://itpd.ncert.gov.in', cadence: 'Monthly', icon: '🧑\u200d🏫' },
]

const badge = c => ({
  Weekly: 'badge-green',
  Monthly: 'badge-blue',
  Quarterly: 'badge-grey'
})[c] || 'badge-grey'

export default function Updates() {
  return (
    <div className="page-updates">
      <h1>Update Schedule</h1>
      <p className="lead">Repository is refreshed from 12 official sources on a fixed schedule via GitHub Actions.</p>
      <div className="update-grid">
        {sources.map(s => (
          <div className="update-card" key={s.name}>
            <div className="update-top">
              <span className="update-icon">{s.icon}</span>
              <span className={badge(s.cadence)}>{s.cadence}</span>
            </div>
            <div className="update-name">{s.name}</div>
            <a href={s.url} target="_blank" rel="noreferrer" className="update-link">Visit source ↗</a>
          </div>
        ))}
      </div>
    </div>
  )
}
