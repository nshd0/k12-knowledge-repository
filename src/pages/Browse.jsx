import React, { useEffect, useMemo, useState } from 'react'
import Fuse from 'fuse.js'
export default function Browse(){
  const [data, setData] = useState([])
  const [q, setQ] = useState('')
  const [cat, setCat] = useState('All')
  useEffect(()=>{ fetch('/data-index.json').then(r=>r.json()).then(setData).catch(()=>{}) },[])
  const cats = ['All', ...new Set(data.map(d=>d.category).filter(Boolean))]
  const results = useMemo(()=>{
    let list = data
    if (cat !== 'All') list = list.filter(x=>x.category===cat)
    if (q.trim()){
      const fuse = new Fuse(list, { keys:['title','category','authority','tags'], threshold:0.35 })
      list = fuse.search(q).map(r=>r.item)
    }
    return list
  },[data, q, cat])
  return <div>
    <div className="toolbar">
      <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search by topic, board, subject, or circular..." />
      <div className="chips">{cats.map(c=><button key={c} className={cat===c?'active':''} onClick={()=>setCat(c)}>{c}</button>)}</div>
    </div>
    <p className="count">{results.length} result{results.length!==1?'s':''}</p>
    <div className="cards">
      {results.map(i=>
        <article className="card" key={i.id+i.title}>
          <span className="badge">{i.category}</span>
          <h3>{i.title}</h3>
          <p className="authority">{i.authority}</p>
          <div className="card-footer">
            <span className={`status ${i.status.toLowerCase()}`}>{i.status}</span>
            {i.link && <a href={i.link} target="_blank" rel="noreferrer">Open source ↗</a>}
          </div>
        </article>
      )}
    </div>
  </div>
}
