import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import {
  RiDashboardLine,
  RiFlowChart,
  RiTaskLine,
  RiRobotLine,
  RiSettings4Line,
  RiFileListLine,
  RiSmartphoneLine,
  RiBarChartBoxLine
} from '@remixicon/react'
import { DashboardPage } from '@/pages/DashboardPage'
import { ScenariosPage } from '@/pages/ScenariosPage'
import { TasksPage } from '@/pages/TasksPage'
import { AgentsPage } from '@/pages/AgentsPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { LogsPage } from '@/pages/LogsPage'
import { DevicesPage } from '@/pages/DevicesPage'
import { AnalyticsPage } from '@/pages/AnalyticsPage'

function NavBar() {
  const navItems = [
    { to: '/', icon: RiDashboardLine, label: 'Dashboard' },
    { to: '/devices', icon: RiSmartphoneLine, label: 'Devices' },
    { to: '/scenarios', icon: RiFlowChart, label: 'Scenarios' },
    { to: '/tasks', icon: RiTaskLine, label: 'Tasks' },
    { to: '/agents', icon: RiRobotLine, label: 'Agents' },
    { to: '/logs', icon: RiFileListLine, label: 'Logs' },
    { to: '/analytics', icon: RiBarChartBoxLine, label: 'Analytics' },
    { to: '/settings', icon: RiSettings4Line, label: 'Settings' },
  ]

  return (
    <nav className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold text-green-400">KUX</span>
            <span className="text-xs text-gray-400">Android Agent Platform</span>
          </div>

          <div className="flex items-center gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  }`
                }
              >
                <item.icon className="size-4" />
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#fff',
            color: '#1f2937',
            border: '1px solid #e5e7eb',
            borderRadius: '0.5rem',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            padding: '12px 16px',
            fontSize: '14px',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      <div className="min-h-screen bg-gray-50">
        <NavBar />
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/devices" element={<DevicesPage />} />
          <Route path="/scenarios" element={<ScenariosPage />} />
          <Route path="/scenarios/:scenarioId" element={<ScenariosPage />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/logs" element={<LogsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
