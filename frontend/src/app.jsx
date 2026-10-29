

import { useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Onboarding from './components/Onboarding'
import Resignation from './components/Resignation'
import Announcements from './components/Announcements'
import Tasks from './components/Tasks'
import Integrations from './components/Integrations'
import Feedback from './components/Feedback'
import Profile from './components/Profile'

function Dashboard() {
  const modules = [
    { title: 'Employee Onboarding', path: '/onboarding', number: 21 },
    { title: 'Resignation Management', path: '/resignation', number: 22 },
    { title: 'Internal Announcements', path: '/announcements', number: 23 },
    { title: 'Task Management', path: '/tasks', number: 24 },
    { title: 'System Integrations', path: '/integrations', number: 25 },
    { title: 'Employee Feedback', path: '/feedback', number: 26 },
    { title: 'Profile & Settings', path: '/profile', number: 27 }
  ]

  return (
    <div className="dashboard">
      <h2>Welcome to WorkSphere HRMS</h2>
      <p>Employee Experience & System Integrations — Phase 4</p>

      <div className="module-grid">
        {modules.map((module) => (
          <Link to={module.path} className="module-card" key={module.number}>
            <span>Module {module.number}</span>
            <h3>{module.title}</h3>
            <p>Open module →</p>
          </Link>
        ))}
      </div>
    </div>
  )
}

function App() {
  const [menuOpen, setMenuOpen] = useState(false)

  const navigation = [
    { name: 'Dashboard', path: '/' },
    { name: 'Onboarding', path: '/onboarding' },
    { name: 'Resignations', path: '/resignation' },
    { name: 'Announcements', path: '/announcements' },
    { name: 'Tasks', path: '/tasks' },
    { name: 'Integrations', path: '/integrations' },
    { name: 'Feedback', path: '/feedback' },
    { name: 'Profile', path: '/profile' }
  ]

  return (
    <div className="app">
      <header className="app-header">
        <Link to="/" className="brand">
          WorkSphere <span>HRMS</span>
        </Link>

        <button
          className="menu-button"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle navigation"
        >
          ☰
        </button>

        <nav className={menuOpen ? 'navigation open' : 'navigation'}>
          {navigation.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => setMenuOpen(false)}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </header>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/resignation" element={<Resignation />} />
          <Route path="/announcements" element={<Announcements />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/integrations" element={<Integrations />} />
          <Route path="/feedback" element={<Feedback />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<h2>Page not found</h2>} />
        </Routes>
      </main>

      <footer className="app-footer">
        <p>© 2026 WorkSphere HRMS | Phase 4</p>
      </footer>
    </div>
  )
}

export default App
