import React, { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'

const nav = [
  { to: '/', label: 'Home', icon: '🏠' },
  { to: '/browse', label: 'Browse All', icon: '🔍' },
  { to: '/stakeholder/principal', label: 'Principal', icon: '🏫' },
  { to: '/stakeholder/teacher', label: 'Teacher', icon: '👩\u200d🏫' },
  { to: '/stakeholder/student', label: 'Student', icon: '🎒' },
  { to: '/stakeholder/parent', label: 'Parent', icon: '👨\u200d👩\u200d👧' },
  { to: '/stakeholder/coordinator', label: 'Coordinator', icon: '📋' },
  { to: '/updates', label: 'Updates', icon: '📅' },
  { to: '/sources', label: 'Sources', icon: '🔗' },
]

export default function Layout() {
  const [open, setOpen] = useState(false)
  return (
    <div className="shell">
      <button className="menu-toggle" onClick={() => setOpen(o => !o)} aria-label="Toggle menu">
        {open ? '✕' : '☰'}
      </button>
      <aside className={`sidebar${open ? ' open' : ''}`}>
        <div className="logo">
          <span className="logo-icon">📚</span>
          <span className="logo-text">K-12 Knowledge</span>
        </div>
        <div className="logo-sub">India · NEP · NCF · CBSE</div>
        <nav>
          {nav.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/' ? true : undefined}
              onClick={() => setOpen(false)}
            >
              <span className="nav-icon">{icon}</span>
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">Built by IOE · EdTech for India</div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
