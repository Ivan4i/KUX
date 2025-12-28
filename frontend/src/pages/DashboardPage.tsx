import { useState, useEffect, useCallback } from 'react'
import toast from 'react-hot-toast'
import { Button } from '@/components/common/Button'
import { DeviceCard } from '@/components/dashboard/DeviceCard'
import { CurrentActivity } from '@/components/dashboard/CurrentActivity'
import { RecentLogs } from '@/components/dashboard/RecentLogs'
import { useWebSocketMessages } from '@/hooks/useWebSocket'
import { getDevices, getTasks, getLogs, syncNotionTasks, runTask } from '@/services/api'
import type { DeviceStatus } from '@/types/device'
import type { Task } from '@/types/task'
import type { Log } from '@/types/log'
import type { TaskProgress } from '@/types/task'
import { RiRefreshLine, RiPlayFill, RiNotionFill } from '@remixicon/react'

export function DashboardPage() {
  const [devices, setDevices] = useState<DeviceStatus[]>([])
  const [activeTask, setActiveTask] = useState<Task | null>(null)
  const [taskProgress, setTaskProgress] = useState<TaskProgress | null>(null)
  const [recentLogs, setRecentLogs] = useState<Log[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isSyncing, setIsSyncing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isInitialLoad, setIsInitialLoad] = useState(true)

  // Load initial data
  const loadData = useCallback(async (showSuccessToast = false) => {
    try {
      setIsLoading(true)
      setError(null) // Clear previous errors

      const [devicesData, tasksData, logsData] = await Promise.all([
        getDevices(),
        getTasks('Running', undefined, 1),
        getLogs({ limit: 10 }),
      ])

      setDevices(devicesData)
      setActiveTask(tasksData.length > 0 ? tasksData[0] : null)
      setRecentLogs(logsData)
      setIsInitialLoad(false)

      // Show success toast if requested
      if (showSuccessToast) {
        toast.success('Dashboard refreshed successfully', {
          icon: '🔄',
        })
      }
    } catch (error: any) {
      console.error('Error loading data:', error)
      const errorMessage = error?.response?.data?.error || error?.message || 'Failed to load data'
      setError(`Failed to load dashboard: ${errorMessage}`)

      // Show error toast
      toast.error(`Failed to load dashboard: ${errorMessage}`, {
        icon: '❌',
      })
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  // Handle Sync Notion button
  const handleSyncNotion = async () => {
    try {
      setIsSyncing(true)
      setError(null)
      const result = await syncNotionTasks(10)
      console.log('Synced tasks:', result)

      // Show success toast
      toast.success(`Successfully synced ${result.tasks_synced} task(s) from Notion`, {
        icon: '✅',
      })

      // Reload data
      await loadData()
    } catch (error: any) {
      console.error('Error syncing Notion:', error)
      const errorMessage = error?.response?.data?.error || error?.message || 'Failed to sync'

      // Show error toast
      toast.error(`Failed to sync Notion: ${errorMessage}`, {
        icon: '❌',
      })

      setError(`Failed to sync Notion tasks: ${errorMessage}`)
    } finally {
      setIsSyncing(false)
    }
  }

  // Handle Run Task button
  const handleRunTask = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const result = await runTask()
      console.log('Task started:', result)

      // Show success toast
      toast.success('Task started successfully!', {
        icon: '🚀',
      })

      // Reload data
      await loadData()
    } catch (error: any) {
      console.error('Error running task:', error)
      const errorMessage = error?.response?.data?.error || error?.message || 'Failed to run task'

      // Show error toast
      toast.error(`Failed to start task: ${errorMessage}`, {
        icon: '❌',
      })

      setError(`Failed to start task: ${errorMessage}`)
    } finally {
      setIsLoading(false)
    }
  }

  // WebSocket: Device status updates
  useWebSocketMessages('device_status_update', (message: any) => {
    setDevices((prev) =>
      prev.map((device) =>
        device.id === message.device_id
          ? { ...device, ...message.data }
          : device
      )
    )
  })

  // WebSocket: Task started
  useWebSocketMessages('task_started', async (_message: any) => {
    // Reload tasks to get the active one
    const tasksData = await getTasks('Running', undefined, 1)
    if (tasksData.length > 0) {
      setActiveTask(tasksData[0])
    }
  })

  // WebSocket: Task progress
  useWebSocketMessages('task_progress', (message: any) => {
    setTaskProgress({
      task_id: message.task_id,
      message: message.message,
      progress_percent: message.progress_percent,
    })
  })

  // WebSocket: Task completed
  useWebSocketMessages('task_completed', (_message: any) => {
    setActiveTask(null)
    setTaskProgress(null)

    // Show success toast
    toast.success('WhatsApp message sent successfully!', {
      icon: '✅',
      duration: 5000,
    })

    loadData() // Reload all data
  })

  // WebSocket: Task failed
  useWebSocketMessages('task_failed', (message: any) => {
    setActiveTask(null)
    setTaskProgress(null)

    // Show error toast
    const errorMsg = message?.error || 'Task execution failed'
    toast.error(`Task failed: ${errorMsg}`, {
      icon: '❌',
      duration: 6000,
    })

    loadData() // Reload all data
  })

  // WebSocket: New log entry
  useWebSocketMessages('log_entry', (message: any) => {
    setRecentLogs((prev) => [message.data, ...prev].slice(0, 10))
  })

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="mt-1 text-sm text-gray-500">
                Android Agent Platform - WhatsApp Automation
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Button
                variant="secondary"
                size="md"
                leftIcon={<RiNotionFill className="size-4" />}
                onClick={handleSyncNotion}
                isLoading={isSyncing}
              >
                Sync Notion
              </Button>
              <Button
                variant="primary"
                size="md"
                leftIcon={<RiPlayFill className="size-4" />}
                onClick={handleRunTask}
                isLoading={isLoading}
                disabled={activeTask !== null}
              >
                Run Task
              </Button>
              <Button
                variant="ghost"
                size="md"
                leftIcon={<RiRefreshLine className="size-4" />}
                onClick={() => loadData(true)}
              >
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="mt-1 text-sm text-red-700">{error}</p>
                <div className="mt-3">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      setError(null)
                      loadData(true)
                    }}
                  >
                    Try Again
                  </Button>
                </div>
              </div>
              <div className="ml-auto pl-3">
                <button
                  type="button"
                  className="inline-flex text-red-400 hover:text-red-500"
                  onClick={() => setError(null)}
                >
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {isInitialLoad && isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
              <p className="mt-4 text-sm text-gray-600">Loading dashboard...</p>
            </div>
          </div>
        )}

        {/* Empty State - No Devices */}
        {!isLoading && !error && devices.length === 0 && (
          <div className="text-center py-12">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No devices found</h3>
            <p className="mt-1 text-sm text-gray-500">
              Configure your devices in devices.yaml and restart the backend.
            </p>
            <div className="mt-6">
              <Button variant="primary" onClick={() => loadData(true)}>
                Retry
              </Button>
            </div>
          </div>
        )}

        {/* Content */}
        {!isInitialLoad && devices.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Devices */}
            <div className="lg:col-span-3">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Devices</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {devices.map((device) => (
                  <DeviceCard key={device.id} device={device} />
                ))}
              </div>
            </div>

            {/* Current Activity */}
            <div className="lg:col-span-1">
              <CurrentActivity task={activeTask} progress={taskProgress} />
            </div>

            {/* Recent Logs */}
            <div className="lg:col-span-2">
              <RecentLogs logs={recentLogs} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
