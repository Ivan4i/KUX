# 70_FRONTEND_ARCHITECTURE.md

## Frontend Architecture: Dashboard & Control Panel

### Tech Stack

```
Frontend Stack:
┌─────────────────────────────────────┐
│  Web Framework: React 18            │
│  Build Tool: Vite                   │
│  State Management: Zustand          │
│  UI Library: Shadcn/ui + Tailwind   │
│  Real-time: WebSocket (Socket.IO)   │
│  Charts: Recharts                   │
│  Database ORM: TanStack Query       │
└─────────────────────────────────────┘

Why these tools?
✅ React: Industry standard, large ecosystem
✅ Vite: Fast build, great DX
✅ Zustand: Lightweight state (vs Redux bloat)
✅ Shadcn/ui: Pre-built, customizable components
✅ Socket.IO: Real-time updates (not polling)
✅ Recharts: Beautiful, React-native charts
```

### Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DeviceGrid.tsx
│   │   │   ├── StatsPanel.tsx
│   │   │   └── ActivityLog.tsx
│   │   ├── WorkflowBuilder/
│   │   │   ├── WorkflowBuilder.tsx
│   │   │   ├── CanvasEditor.tsx
│   │   │   ├── NodePalette.tsx
│   │   │   └── PropertyPanel.tsx
│   │   ├── DeviceManager/
│   │   │   ├── DeviceList.tsx
│   │   │   ├── DeviceCard.tsx
│   │   │   ├── DeviceStats.tsx
│   │   │   └── DeviceControl.tsx
│   │   └── Common/
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── ThemeToggle.tsx
│   │
│   ├── hooks/
│   │   ├── useWebSocket.ts
│   │   ├── useDevices.ts
│   │   ├── useWorkflows.ts
│   │   └── useStats.ts
│   │
│   ├── store/
│   │   ├── appStore.ts          (Zustand)
│   │   ├── workflowStore.ts
│   │   ├── deviceStore.ts
│   │   └── uiStore.ts
│   │
│   ├── services/
│   │   ├── api.ts
│   │   ├── websocket.ts
│   │   └── analytics.ts
│   │
│   ├── types/
│   │   ├── device.ts
│   │   ├── workflow.ts
│   │   ├── api.ts
│   │   └── ui.ts
│   │
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── WorkflowsPage.tsx
│   │   ├── DevicesPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   └── SettingsPage.tsx
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── vite.config.ts
├── tailwind.config.js
└── package.json
```

### Installation & Setup

```bash
# Create React project with Vite
npm create vite@latest frontend -- --template react
cd frontend

# Install dependencies
npm install react-router-dom zustand socket.io-client axios
npm install -D tailwindcss postcss autoprefixer
npm install -D @types/react @types/react-dom typescript

# Setup Tailwind
npx tailwindcss init -p

# Install Shadcn/ui components
npm install @radix-ui/react-slot clsx class-variance-authority lucide-react
npx shadcn-ui@latest init

# Install charting library
npm install recharts

# Development mode
npm run dev   # http://localhost:5173
```

### Core Application Layout

```typescript
// src/App.tsx
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Header from './components/Common/Header'
import Sidebar from './components/Common/Sidebar'

// Pages
import DashboardPage from './pages/DashboardPage'
import WorkflowsPage from './pages/WorkflowsPage'
import DevicesPage from './pages/DevicesPage'
import AnalyticsPage from './pages/AnalyticsPage'

export default function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="flex h-screen bg-background">
          {/* Sidebar Navigation */}
          <Sidebar />
          
          {/* Main Content */}
          <div className="flex-1 flex flex-col">
            {/* Top Header */}
            <Header />
            
            {/* Page Content */}
            <main className="flex-1 overflow-auto p-6">
              <Routes>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/workflows" element={<WorkflowsPage />} />
                <Route path="/devices" element={<DevicesPage />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  )
}
```

### State Management (Zustand)

```typescript
// src/store/appStore.ts
import { create } from 'zustand'

interface AppState {
  // UI State
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  currentPage: string
  
  // Data State
  devices: Device[]
  workflows: Workflow[]
  stats: Stats
  
  // Loading State
  isLoading: boolean
  error: string | null
  
  // Actions
  setTheme: (theme: 'light' | 'dark') => void
  setSidebarOpen: (open: boolean) => void
  setCurrentPage: (page: string) => void
  setDevices: (devices: Device[]) => void
  setError: (error: string | null) => void
  clearError: () => void
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  theme: 'light',
  sidebarOpen: true,
  currentPage: '/',
  devices: [],
  workflows: [],
  stats: {},
  isLoading: false,
  error: null,
  
  // Actions
  setTheme: (theme) => set({ theme }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setCurrentPage: (page) => set({ currentPage: page }),
  setDevices: (devices) => set({ devices }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}))
```

### Real-time WebSocket Integration

```typescript
// src/services/websocket.ts
import { io } from 'socket.io-client'
import { useAppStore } from '../store/appStore'

class WebSocketService {
  private socket: any
  
  connect(url: string = 'http://localhost:8000') {
    this.socket = io(url, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    })
    
    // Device status updates
    this.socket.on('device:status', (data) => {
      useAppStore.setState({ devices: data })
    })
    
    // Task updates
    this.socket.on('task:update', (data) => {
      console.log('Task update:', data)
    })
    
    // Error notifications
    this.socket.on('error', (error) => {
      useAppStore.setState({ error: error.message })
    })
    
    // Connection status
    this.socket.on('connect', () => {
      console.log('✅ Connected to backend')
    })
    
    this.socket.on('disconnect', () => {
      console.log('❌ Disconnected from backend')
    })
  }
  
  emit(event: string, data: any) {
    this.socket.emit(event, data)
  }
  
  disconnect() {
    this.socket.disconnect()
  }
}

export const wsService = new WebSocketService()
```

### Type Definitions

```typescript
// src/types/device.ts
export interface Device {
  id: string
  name: string
  model: string
  androidVersion: string
  battery: number
  temperature: number
  status: 'online' | 'offline' | 'busy' | 'error'
  lastSeen: string
  currentTask?: string
  tasksCompleted: number
}

// src/types/workflow.ts
export interface Workflow {
  id: string
  name: string
  description: string
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
  status: 'draft' | 'active' | 'paused'
  createdAt: string
  updatedAt: string
  successRate: number
  totalRuns: number
}

export interface WorkflowNode {
  id: string
  type: 'start' | 'action' | 'condition' | 'end'
  label: string
  position: { x: number; y: number }
  data: Record<string, any>
}

export interface WorkflowEdge {
  id: string
  source: string
  target: string
  label?: string
}

// src/types/stats.ts
export interface Stats {
  totalDevices: number
  onlineDevices: number
  tasksRunning: number
  tasksCompleted: number
  successRate: number
  averageResponseTime: number
  errors: Error[]
}
```

---

## End of 70_FRONTEND_ARCHITECTURE.md