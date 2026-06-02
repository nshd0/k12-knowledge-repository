import React from 'react'
const sources = [
  { id:'SI-001', name:'Ministry of Education', url:'https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_2020.pdf', authority:'National', pattern:'Policy updates' },
  { id:'SI-002', name:'NCERT', url:'https://ncert.nic.in/focus-group.php?ln=hi', authority:'National', pattern:'Framework updates' },
  { id:'SI-003', name:'CBSE Circulars', url:'https://www.cbse.gov.in/cbsenew/list-of-circulars-related-to-student.html', authority:'National Board', pattern:'Weekly' },
  { id:'SI-004', name:'CBSE SARAS', url:'https://saras.cbse.gov.in/saras/Home/Circulars', authority:'National Board', pattern:'Weekly' },
  { id:'SI-005', name:'Delhi DoE', url:'https://www.edudel.nic.in', authority:'State', pattern:'Weekly' },
  { id:'SI-006', name:'DIKSHA', url:'https://www.india.gov.in/spotlight/diksha-national-digital-infrastructure-teachers', authority:'National', pattern:'Continuous' }
]
export default function SourceIndex(){
  return <section>
    <h1>Source Index</h1>
    <p>All verified official sources used in this repository.</p>
    <table className="source-table">
      <thead><tr><th>ID</th><th>Name</th><th>Authority</th><th>Cadence</th><th>Link</th></tr></thead>
      <tbody>{sources.map(s=><tr key={s.id}><td>{s.id}</td><td>{s.name}</td><td>{s.authority}</td><td>{s.pattern}</td><td><a href={s.url} target="_blank" rel="noreferrer">Visit</a></td></tr>)}</tbody>
    </table>
  </section>
}
