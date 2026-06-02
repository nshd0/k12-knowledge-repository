import React, { useEffect, useState } from 'react'
export default function Home(){
  const [summary, setSummary] = useState({ total_items:0, active_items:0, categories:[] })
  useEffect(()=>{ fetch('/site-summary.json').then(r=>r.json()).then(setSummary).catch(()=>{}) },[])
  const cards = [
    { role:'Principal', desc:'Compliance, policy, and circulars.' },
    { role:'Teacher', desc:'Pedagogy, assessment, and capacity building.' },
    { role:'Student', desc:'Learning resources and revision.' },
    { role:'Parent', desc:'Notices and academic updates.' },
    { role:'Coordinator', desc:'Source tracking and update logs.' }
  ]
  return <div>
    <section className="hero-card">
      <h1>Education Knowledge Repository</h1>
      <p>Official curriculum, circulars, capacity building, assessment, and pedagogy resources — verified and updated weekly.</p>
      <div className="kpis">
        <div><strong>{summary.total_items}</strong><span>Total items</span></div>
        <div><strong>{summary.active_items}</strong><span>Active</span></div>
        <div><strong>{summary.categories.length}</strong><span>Categories</span></div>
      </div>
    </section>
    <h2>Choose your view</h2>
    <div className="cards">
      {cards.map(({role,desc}) => <a className="card" href={'/stakeholder/'+role.toLowerCase()} key={role}><h3>{role}</h3><p>{desc}</p></a>)}
    </div>
  </div>
}
