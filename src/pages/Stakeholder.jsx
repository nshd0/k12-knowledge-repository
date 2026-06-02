import React from 'react'
import { useParams, Link } from 'react-router-dom'
const data = {
  principal: { title:'Principal', desc:'Compliance, circulars, policy updates, and action items.', items:['CBSE circulars','NEP 2020 action plan','Delhi DoE notices','Board exam schedules'] },
  teacher:   { title:'Teacher',   desc:'Pedagogy, assessment, classroom resources, and capacity building.', items:['NCF 2023 framework','DIKSHA training','Competency-based assessment','Classroom strategies'] },
  student:   { title:'Student',   desc:'Learning resources, revision materials, and exam preparation.', items:['Subject-wise notes','Sample papers','NCF learning outcomes','Online learning resources'] },
  parent:    { title:'Parent',    desc:'Simplified notices, exam updates, and school communication.', items:['Academic calendar','Exam timetable','School circulars','Parent guidelines'] },
  coordinator:{ title:'Coordinator', desc:'Source index, update logs, and repository management.', items:['Source index','Update log','Data verification','Circular tracker'] }
}
export default function Stakeholder(){
  const { role } = useParams()
  const d = data[role] || { title: role, desc:'', items:[] }
  return <section className="stakeholder-page">
    <h1>{d.title} View</h1>
    <p className="lead">{d.desc}</p>
    <ul>{d.items.map(i=><li key={i}><Link to={'/browse?q='+encodeURIComponent(i)}>{i}</Link></li>)}</ul>
    <Link className="btn" to="/browse">Browse all resources</Link>
  </section>
}
