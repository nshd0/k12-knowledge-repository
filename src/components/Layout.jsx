import React from 'react'
import { NavLink, Outlet } from 'react-router-dom'

const nav = [
  ['/', 'Home'],
  ['/browse', 'Browse All'],
  ['/stakeholder/principal', 'Principal'],
  ['/stakeholder/teacher', 'Teacher'],
  ['/stakeholder/student', 'Student'],
  ['/stakeholder/parent', 'Parent'],
  ['/stakeholder/coordinator', 'Coordinator'],
  ['/updates', 'Updates'],
  ['/sources', 'Sources']
]
export default function Layout(){
  return <div className="shell">
    <aside className="sidebar">
      <div className="logo">K-12 Knowledge</div>
      <nav>{nav.map(([to,label]) => <NavLink key={to} to={to} end={to==='/' ? true : undefined}>{label}</NavLink>)}</nav>
    </aside>
    <main className="content"><Outlet /></main>
  </div>
}
