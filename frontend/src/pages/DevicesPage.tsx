import { useState, useEffect, useCallback } from 'react'
import toast from 'react-hot-toast'
import { Button } from '@/components/common/Button'
import {
  RiRefreshLine,
  RiSmartphoneLine,
  RiBattery2ChargeLine,
  RiBatteryLine,
  RiBatteryLowLine,
  RiTempHotLine,
  RiSignalWifiLine,
  RiComputerLine,
  RiRestartLine,
  RiCameraLine,
  RiCheckboxCircleFill,
  RiTimeLine,
  RiMapPinLine,
  RiGlobalLine,
} from '@remixicon/react'
import {
  getDevices,
  refreshDeviceStatus,
  rebootDevice,
  takeDeviceScreenshot,
  launchScrcpy,
} from '@/services/api'
import type { DeviceStatus } from '@/types/device'

const STATUS_CONFIG = {
  online: {
    color: 'bg-success-500',
    textColor: 'text-success-600',
    bgColor: 'bg-success-100',
    label: 'Online',
  },
  offline: {
    color: 'bg-gray-400',
    textColor: 'text-gray-600',
    bgColor: 'bg-gray-100',
    label: 'Offline',
  },
  busy: {
    color: 'bg-warning-500',
    textColor: 'text-warning-600',
    bgColor: 'bg-warning-100',
    label: 'Busy',
  },
}

export function DevicesPage() {
  const [devices, setDevices] = useState<DeviceStatus[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [actionInProgress, setActionInProgress] = useState<Record<string, string>>({})

  const loadDevices = useCallback(async (showToast = false) => {
    try {
      setIsRefreshing(true)
      const data = await getDevices()
      setDevices(data)
      if (showToast) {
        toast.success('Devices refreshed')
      }
    } catch (error) {
      console.error('Error loading devices:', error)
      toast.error('Failed to load devices')
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }, [])

  useEffect(() => {
    loadDevices()

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      loadDevices()
    }, 30000)

    return () => clearInterval(interval)
  }, [loadDevices])

  const handleRefreshDevice = async (deviceId: string) => {
    try {
      setActionInProgress((prev) => ({ ...prev, [deviceId]: 'refresh' }))
      const updatedStatus = await refreshDeviceStatus(deviceId)
      setDevices((prev) =>
        prev.map((d) => (d.id === deviceId ? updatedStatus : d))
      )
      toast.success('Device status refreshed')
    } catch (error) {
      console.error('Error refreshing device:', error)
      toast.error('Failed to refresh device status')
    } finally {
      setActionInProgress((prev) => {
        const { [deviceId]: _, ...rest } = prev
        return rest
      })
    }
  }

  const handleRebootDevice = async (deviceId: string, deviceName: string) => {
    if (!confirm(`Are you sure you want to reboot ${deviceName}? This will interrupt any running tasks.`)) {
      return
    }

    try {
      setActionInProgress((prev) => ({ ...prev, [deviceId]: 'reboot' }))
      await rebootDevice(deviceId)
      toast.success(`${deviceName} is rebooting...`)

      // Update device status to offline temporarily
      setDevices((prev) =>
        prev.map((d) =>
          d.id === deviceId ? { ...d, current_status: 'offline' as const } : d
        )
      )
    } catch (error) {
      console.error('Error rebooting device:', error)
      toast.error('Failed to reboot device')
    } finally {
      setActionInProgress((prev) => {
        const { [deviceId]: _, ...rest } = prev
        return rest
      })
    }
  }

  const handleTakeScreenshot = async (deviceId: string, _deviceName: string) => {
    try {
      setActionInProgress((prev) => ({ ...prev, [deviceId]: 'screenshot' }))
      const result = await takeDeviceScreenshot(deviceId)
      toast.success(`Screenshot saved: ${result.screenshot_path}`)
    } catch (error) {
      console.error('Error taking screenshot:', error)
      toast.error('Failed to take screenshot')
    } finally {
      setActionInProgress((prev) => {
        const { [deviceId]: _, ...rest } = prev
        return rest
      })
    }
  }

  const handleLaunchScrcpy = async (deviceId: string, deviceName: string) => {
    try {
      setActionInProgress((prev) => ({ ...prev, [deviceId]: 'scrcpy' }))
      await launchScrcpy(deviceId)
      toast.success(`Screen mirror launched for ${deviceName}`)
    } catch (error: any) {
      console.error('Error launching scrcpy:', error)
      toast.error(error?.response?.data?.detail || 'Failed to launch scrcpy')
    } finally {
      setActionInProgress((prev) => {
        const { [deviceId]: _, ...rest } = prev
        return rest
      })
    }
  }

  const getBatteryIcon = (level: number) => {
    if (level > 66) return <RiBattery2ChargeLine className="w-5 h-5 text-success-600" />
    if (level > 33) return <RiBatteryLine className="w-5 h-5 text-warning-600" />
    return <RiBatteryLowLine className="w-5 h-5 text-error-600" />
  }

  const getBatteryColor = (level: number) => {
    if (level > 66) return 'text-success-600'
    if (level > 33) return 'text-warning-600'
    return 'text-error-600'
  }

  const getTemperatureColor = (temp: number) => {
    if (temp > 40) return 'text-error-600'
    if (temp > 35) return 'text-warning-600'
    return 'text-gray-600'
  }

  const formatLastHeartbeat = (heartbeat: string | null) => {
    if (!heartbeat) return 'Never'
    const date = new Date(heartbeat)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffSec = Math.floor(diffMs / 1000)
    const diffMin = Math.floor(diffSec / 60)

    if (diffSec < 60) return `${diffSec}s ago`
    if (diffMin < 60) return `${diffMin}m ago`
    return date.toLocaleTimeString('ru-RU')
  }

  // Calculate stats
  const onlineCount = devices.filter((d) => d.current_status === 'online').length
  const busyCount = devices.filter((d) => d.current_status === 'busy').length
  const offlineCount = devices.filter((d) => d.current_status === 'offline').length
  const totalTasks = devices.reduce((sum, d) => sum + d.tasks_completed_today, 0)

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-sm text-gray-600">Loading devices...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Devices</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage and monitor your Android devices
              </p>
            </div>
            <Button
              variant="secondary"
              size="md"
              leftIcon={<RiRefreshLine />}
              onClick={() => loadDevices(true)}
              isLoading={isRefreshing}
            >
              Refresh All
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-success-100 rounded-lg">
                <RiCheckboxCircleFill className="w-5 h-5 text-success-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{onlineCount}</p>
                <p className="text-sm text-gray-500">Online</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-warning-100 rounded-lg">
                <RiTimeLine className="w-5 h-5 text-warning-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{busyCount}</p>
                <p className="text-sm text-gray-500">Busy</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gray-100 rounded-lg">
                <RiSmartphoneLine className="w-5 h-5 text-gray-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{offlineCount}</p>
                <p className="text-sm text-gray-500">Offline</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-100 rounded-lg">
                <RiCheckboxCircleFill className="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{totalTasks}</p>
                <p className="text-sm text-gray-500">Tasks Today</p>
              </div>
            </div>
          </div>
        </div>

        {/* Devices List */}
        {devices.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <RiSmartphoneLine className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900">No devices found</h3>
            <p className="mt-1 text-sm text-gray-500">
              Configure your devices in devices.yaml and restart the backend.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {devices.map((device) => {
              const statusConfig = STATUS_CONFIG[device.current_status]
              const isOnline = device.current_status !== 'offline'
              const currentAction = actionInProgress[device.id]

              return (
                <div
                  key={device.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between">
                      {/* Device Info */}
                      <div className="flex items-start gap-4">
                        <div className="p-3 bg-gray-100 rounded-xl">
                          <RiSmartphoneLine className="w-8 h-8 text-gray-600" />
                        </div>
                        <div>
                          <div className="flex items-center gap-3">
                            <h3 className="text-xl font-semibold text-gray-900">
                              {device.name}
                            </h3>
                            <span
                              className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${statusConfig.bgColor} ${statusConfig.textColor}`}
                            >
                              <span className={`w-1.5 h-1.5 rounded-full ${statusConfig.color}`} />
                              {statusConfig.label}
                            </span>
                          </div>
                          <div className="mt-2 flex items-center gap-4 text-sm text-gray-500">
                            <span className="flex items-center gap-1">
                              <RiMapPinLine className="w-3 h-3" />
                              {device.location}
                            </span>
                            <span className="flex items-center gap-1">
                              <RiTimeLine className="w-3 h-3" />
                              {formatLastHeartbeat(device.last_heartbeat)}
                            </span>
                            <span className="flex items-center gap-1">
                              <RiGlobalLine className="w-3 h-3" />
                              {device.id}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex items-center gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          leftIcon={<RiRefreshLine />}
                          onClick={() => handleRefreshDevice(device.id)}
                          isLoading={currentAction === 'refresh'}
                          disabled={!!currentAction}
                        >
                          Refresh
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          leftIcon={<RiCameraLine />}
                          onClick={() => handleTakeScreenshot(device.id, device.name)}
                          isLoading={currentAction === 'screenshot'}
                          disabled={!isOnline || !!currentAction}
                        >
                          Screenshot
                        </Button>
                        <Button
                          variant="secondary"
                          size="sm"
                          leftIcon={<RiComputerLine />}
                          onClick={() => handleLaunchScrcpy(device.id, device.name)}
                          isLoading={currentAction === 'scrcpy'}
                          disabled={!isOnline || !!currentAction}
                        >
                          Screen
                        </Button>
                        <Button
                          variant="danger"
                          size="sm"
                          leftIcon={<RiRestartLine />}
                          onClick={() => handleRebootDevice(device.id, device.name)}
                          isLoading={currentAction === 'reboot'}
                          disabled={!isOnline || !!currentAction}
                        >
                          Reboot
                        </Button>
                      </div>
                    </div>

                    {/* Metrics */}
                    <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
                      {/* Battery */}
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        {getBatteryIcon(device.battery_level)}
                        <div>
                          <p className={`text-lg font-semibold ${getBatteryColor(device.battery_level)}`}>
                            {device.battery_level}%
                          </p>
                          <p className="text-xs text-gray-500">Battery</p>
                        </div>
                      </div>

                      {/* Temperature */}
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <RiTempHotLine className={`w-5 h-5 ${getTemperatureColor(device.temperature)}`} />
                        <div>
                          <p className={`text-lg font-semibold ${getTemperatureColor(device.temperature)}`}>
                            {device.temperature}°C
                          </p>
                          <p className="text-xs text-gray-500">Temperature</p>
                        </div>
                      </div>

                      {/* Signal */}
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <RiSignalWifiLine className="w-5 h-5 text-gray-600" />
                        <div>
                          <p className="text-lg font-semibold text-gray-700">
                            {device.signal_strength}%
                          </p>
                          <p className="text-xs text-gray-500">Signal</p>
                        </div>
                      </div>

                      {/* Tasks Today */}
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <RiCheckboxCircleFill className="w-5 h-5 text-primary-600" />
                        <div>
                          <p className="text-lg font-semibold text-primary-600">
                            {device.tasks_completed_today}
                          </p>
                          <p className="text-xs text-gray-500">Tasks Today</p>
                        </div>
                      </div>

                      {/* Active Task */}
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <RiTimeLine className="w-5 h-5 text-warning-600" />
                        <div>
                          <p className="text-lg font-semibold text-gray-700">
                            {device.active_task_id ? `#${device.active_task_id}` : '-'}
                          </p>
                          <p className="text-xs text-gray-500">Active Task</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
