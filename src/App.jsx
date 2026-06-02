import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Browse from './pages/Browse'
import Stakeholder from './pages/Stakeholder'
import Updates from './pages/Updates'
import SourceIndex from './pages/SourceIndex'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/browse" element={<Browse />} />
        <Route path="/stakeholder/:role" element={<Stakeholder />} />
        <Route path="/updates" element={<Updates />} />
        <Route path="/sources" element={<SourceIndex />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
