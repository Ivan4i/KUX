# 72_DASHBOARD_REALTIME.md

## Real-time Dashboard with Live Updates

### Main Dashboard Component

```typescript
// src/pages/DashboardPage.tsx
import React, { useEffect } from 'react'
import { useAppStore } from '../store/appStore'
import { wsService } from '../services/websocket'
import StatsPanel from '../components/Dashboard/StatsPanel'
import DeviceGrid from '../components/Dashboard/DeviceGrid'
import ActivityLog from '../components/Dashboard/ActivityLog'
import ChartSection from '../components/Dashboard/ChartSection'

export default function DashboardPage() {
  const { devices, stats, setDevices } = useAppStore()
  
  useEffect(() => {
    // Connect to WebSocket for real-time updates
    wsService.connect()
    
    // Fetch initial data
    fetchDashboardData()
    
    return () => {
      wsService.disconnect()
    }
  }, [])
  
  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/dashboard')
      const data = await response.json()
      
      setDevices(data.devices)
      useAppStore.setState({ stats: data.stats })
    } catch (error) {
      console.error('Failed to fetch dashboard:', error)
    }
  }
  
  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <StatsPanel stats={stats} />
      
      {/* Device Grid */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Connected Devices</h2>
        <DeviceGrid devices={devices} />
      </section>
      
      {/* Charts */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Analytics</h2>
        <ChartSection />
      </section>
      
      {/* Activity Log */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Recent Activity</h2>
        <ActivityLog />
      </section>
    </div>
  )
}
```

### Stats Panel Component

```typescript
// src/components/Dashboard/StatsPanel.tsx
import React from 'react'
import { Stats } from '../../types/workflow'

interface StatsPanelProps {
  stats: Stats
}

export default function StatsPanel({ stats }: StatsPanelProps) {
  const statItems = [
    {
      label: 'Total Devices',
      value: stats.totalDevices,
      icon: '📱',
      color: 'bg-blue-50',
    },
    {
      label: 'Online Devices',
      value: stats.onlineDevices,
      icon: '🟢',
      color: 'bg-green-50',
    },
    {
      label: 'Tasks Running',
      value: stats.tasksRunning,
      icon: '⚙️',
      color: 'bg-purple-50',
    },
    {
      label: 'Tasks Completed',
      value: stats.tasksCompleted,
      icon: '✅',
      color: 'bg-emerald-50',
    },
    {
      label: 'Success Rate',
      value: `${stats.successRate.toFixed(1)}%`,
      icon: '📊',
      color: 'bg-orange-50',
    },
    {
      label: 'Avg Response Time',
      value: `${stats.averageResponseTime.toFixed(0)}ms`,
      icon: '⚡',
      color: 'bg-red-50',
    },
  ]
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {statItems.map((item, idx) => (
        <div
          key={idx}
          className={`${item.color} rounded-lg p-4 border border-gray-200 hover:shadow-lg transition`}
        >
          <div className="flex items-start justify-between">
            <div>
              <p className="text-gray-600 text-sm">{item.label}</p>
              <p className="text-2xl font-bold mt-1">{item.value}</p>
            </div>
            <span className="text-2xl">{item.icon}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
```

### Device Grid Component

```typescript
// src/components/Dashboard/DeviceGrid.tsx
import React from 'react'
import { Device } from '../../types/device'
import DeviceCard from './DeviceCard'

interface DeviceGridProps {
  devices: Device[]
}

export default function DeviceGrid({ devices }: DeviceGridProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'text-green-500'
      case 'busy':
        return 'text-orange-500'
      case 'offline':
        return 'text-gray-500'
      case 'error':
        return 'text-red-500'
      default:
        return 'text-gray-500'
    }
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {devices.map((device) => (
        <DeviceCard key={device.id} device={device} />
      ))}
    </div>
  )
}

// src/components/Dashboard/DeviceCard.tsx
export default function DeviceCard({ device }: { device: Device }) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-lg transition bg-white">
      {/* Status Indicator */}
      <div className="flex items-start justify-between mb-2">
        <div>
          <h3 className="font-semibold">{device.name}</h3>
          <p className="text-sm text-gray-600">{device.model}</p>
        </div>
        <div
          className={`w-3 h-3 rounded-full ${
            device.status === 'online'
              ? 'bg-green-500'
              : device.status === 'offline'
              ? 'bg-gray-500'
              : 'bg-orange-500'
          }`}
        />
      </div>
      
      {/* Stats */}
      <div className="space-y-2 text-sm mb-4">
        <div className="flex justify-between">
          <span className="text-gray-600">Battery:</span>
          <div className="flex items-center gap-1">
            <div className="w-16 h-2 bg-gray-200 rounded">
              <div
                className={`h-full rounded ${
                  device.battery > 50
                    ? 'bg-green-500'
                    : device.battery > 20
                    ? 'bg-orange-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${device.battery}%` }}
              />
            </div>
            <span className="font-semibold">{device.battery}%</span>
          </div>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">Temp:</span>
          <span className="font-semibold">{device.temperature}°C</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-600">Tasks:</span>
          <span className="font-semibold">{device.tasksCompleted}</span>
        </div>
      </div>
      
      {/* Current Task */}
      {device.currentTask && (
        <div className="bg-blue-50 rounded p-2 mb-3">
          <p className="text-xs font-semibold text-blue-900">Current:</p>
          <p className="text-xs text-blue-700">{device.currentTask}</p>
        </div>
      )}
      
      {/* Actions */}
      <div className="flex gap-2">
        <button className="flex-1 px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600">
          Control
        </button>
        <button className="flex-1 px-2 py-1 text-xs border border-gray-300 rounded hover:bg-gray-100">
          Details
        </button>
      </div>
    </div>
  )
}
```

### Charts Section

```typescript
// src/components/Dashboard/ChartSection.tsx
import React, { useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

export default function ChartSection() {
  const [performanceData, setPerformanceData] = useState<any[]>([])
  const [successRateData, setSuccessRateData] = useState<any[]>([])
  
  useEffect(() => {
    // Fetch chart data
    const mockPerformanceData = [
      { time: '00:00', cpu: 20, memory: 30, temperature: 35 },
      { time: '04:00', cpu: 35, memory: 45, temperature: 40 },
      { time: '08:00', cpu: 60, memory: 65, temperature: 50 },
      { time: '12:00', cpu: 85, memory: 75, temperature: 60 },
      { time: '16:00', cpu: 70, memory: 60, temperature: 55 },
      { time: '20:00', cpu: 40, memory: 50, temperature: 45 },
      { time: '23:59', cpu: 25, memory: 35, temperature: 38 },
    ]
    
    const mockSuccessRateData = [
      { device: 'Device 1', successRate: 98 },
      { device: 'Device 2', successRate: 96 },
      { device: 'Device 3', successRate: 99 },
      { device: 'Device 4', successRate: 95 },
      { device: 'Device 5', successRate: 97 },
      { device: 'Device 6', successRate: 94 },
      { device: 'Device 7', successRate: 99 },
    ]
    
    setPerformanceData(mockPerformanceData)
    setSuccessRateData(mockSuccessRateData)
  }, [])
  
  return (
    <div className="space-y-6">
      {/* Performance Over Time */}
      <div className="border rounded-lg p-4 bg-white">
        <h3 className="font-semibold mb-4">System Performance (24h)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={performanceData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="cpu" stroke="#3b82f6" name="CPU %" />
            <Line type="monotone" dataKey="memory" stroke="#10b981" name="Memory %" />
            <Line type="monotone" dataKey="temperature" stroke="#f59e0b" name="Temp °C" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      {/* Success Rate by Device */}
      <div className="border rounded-lg p-4 bg-white">
        <h3 className="font-semibold mb-4">Success Rate by Device</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={successRateData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="device" />
            <YAxis domain={[90, 100]} />
            <Tooltip />
            <Bar dataKey="successRate" fill="#8b5cf6" name="Success Rate %" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
```

### Activity Log Component

```typescript
// src/components/Dashboard/ActivityLog.tsx
import React, { useEffect, useState } from 'react'
import { wsService } from '../../services/websocket'

interface LogEntry {
  id: string
  timestamp: string
  device: string
  action: string
  status: 'success' | 'error' | 'warning'
  message: string
}

export default function ActivityLog() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  
  useEffect(() => {
    // Listen for activity updates
    wsService.emit('subscribe:activity')
    
    // Mock logs
    const mockLogs = [
      {
        id: '1',
        timestamp: new Date().toISOString(),
        device: 'Device 1',
        action: 'Message Sent',
        status: 'success' as const,
        message: 'Successfully sent message to contact',
      },
      {
        id: '2',
        timestamp: new Date(Date.now() - 60000).toISOString(),
        device: 'Device 2',
        action: 'Connection Failed',
        status: 'error' as const,
        message: 'Failed to connect to target device',
      },
    ]
    
    setLogs(mockLogs)
  }, [])
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'bg-green-100 text-green-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      case 'warning':
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }
  
  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="divide-y">
        {logs.slice(0, 10).map((log) => (
          <div key={log.id} className="p-4 hover:bg-gray-50 transition">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold">{log.device}</span>
                  <span
                    className={`px-2 py-0.5 rounded text-xs font-semibold ${getStatusColor(
                      log.status
                    )}`}
                  >
                    {log.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-sm font-medium">{log.action}</p>
                <p className="text-xs text-gray-600 mt-1">{log.message}</p>
              </div>
              <div className="text-xs text-gray-500">
                {new Date(log.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## End of 72_DASHBOARD_REALTIME.md