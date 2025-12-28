import { useState } from 'react'
import toast from 'react-hot-toast'
import { Card } from '@/components/common/Card'
import { Button } from '@/components/common/Button'
import type { DeviceStatus } from '@/types/device'
import { FaBatteryFull, FaBatteryHalf, FaBatteryQuarter, FaTemperatureHigh, FaSignal, FaDesktop } from 'react-icons/fa'
import { launchScrcpy } from '@/services/api'

interface DeviceCardProps {
  device: DeviceStatus
}

export function DeviceCard({ device }: DeviceCardProps) {
  const [isLaunching, setIsLaunching] = useState(false)

  const handleLaunchScrcpy = async () => {
    try {
      setIsLaunching(true)
      await launchScrcpy(device.id)
      toast.success(`Screen mirror launched for ${device.name}`)
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to launch scrcpy')
    } finally {
      setIsLaunching(false)
    }
  }
  const statusColors = {
    online: 'bg-success-500',
    offline: 'bg-gray-400',
    busy: 'bg-warning-500',
  }

  const statusText = {
    online: 'Online',
    offline: 'Offline',
    busy: 'Busy',
  }

  const getBatteryIcon = (level: number) => {
    if (level > 66) return <FaBatteryFull className="text-success-600" />
    if (level > 33) return <FaBatteryHalf className="text-warning-600" />
    return <FaBatteryQuarter className="text-error-600" />
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

  return (
    <Card className="hover:shadow-md transition-shadow">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{device.name}</h3>
            <p className="text-sm text-gray-500">{device.location}</p>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${statusColors[device.current_status]}`} />
            <span className="text-sm font-medium text-gray-700">
              {statusText[device.current_status]}
            </span>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-3 gap-4">
          {/* Battery */}
          <div className="flex items-center gap-2">
            {getBatteryIcon(device.battery_level)}
            <div>
              <p className={`text-lg font-semibold ${getBatteryColor(device.battery_level)}`}>
                {device.battery_level}%
              </p>
              <p className="text-xs text-gray-500">Battery</p>
            </div>
          </div>

          {/* Temperature */}
          <div className="flex items-center gap-2">
            <FaTemperatureHigh className={getTemperatureColor(device.temperature)} />
            <div>
              <p className={`text-lg font-semibold ${getTemperatureColor(device.temperature)}`}>
                {device.temperature}°C
              </p>
              <p className="text-xs text-gray-500">Temp</p>
            </div>
          </div>

          {/* Signal */}
          <div className="flex items-center gap-2">
            <FaSignal className="text-gray-600" />
            <div>
              <p className="text-lg font-semibold text-gray-700">
                {device.signal_strength}%
              </p>
              <p className="text-xs text-gray-500">Signal</p>
            </div>
          </div>
        </div>

        {/* Tasks Today + Screen Button */}
        <div className="pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-sm text-gray-600">Tasks today: </span>
              <span className="text-sm font-semibold text-primary-600">
                {device.tasks_completed_today}
              </span>
            </div>
            <Button
              variant="secondary"
              size="sm"
              leftIcon={<FaDesktop />}
              onClick={handleLaunchScrcpy}
              isLoading={isLaunching}
              disabled={device.current_status === 'offline'}
            >
              Screen
            </Button>
          </div>
        </div>
      </div>
    </Card>
  )
}
