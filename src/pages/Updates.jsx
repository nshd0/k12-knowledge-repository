import React from 'react'
const sources = [
  { name:'Ministry of Education', url:'https://www.education.gov.in', cadence:'Monthly' },
  { name:'NCERT', url:'https://ncert.nic.in', cadence:'Monthly' },
  { name:'CBSE Circulars', url:'https://www.cbse.gov.in/cbsenew/list-of-circulars-related-to-student.html', cadence:'Weekly' },
  { name:'CBSE SARAS', url:'https://saras.cbse.gov.in/saras/Home/Circulars', cadence:'Weekly' },
  { name:'Delhi DoE', url:'https://www.edudel.nic.in', cadence:'Weekly' },
  { name:'DIKSHA', url:'https://www.india.gov.in/spotlight/diksha-national-digital-infrastructure-teachers', cadence:'Weekly' }
]
export default function Updates(){
  return <section>
    <h1>Source Updates</h1>
    <p>Repository is updated on the following cadence from official sources.</p>
    <table className="source-table">
      <thead><tr><th>Source</th><th>Cadence</th><th>Link</th></tr></thead>
      <tbody>{sources.map(s=><tr key={s.name}><td>{s.name}</td><td><span className={s.cadence==='Weekly'?'badge-green':'badge-blue'}>{s.cadence}</span></td><td><a href={s.url} target="_blank" rel="noreferrer">Visit</a></td></tr>)}</tbody>
    </table>
  </section>
}
