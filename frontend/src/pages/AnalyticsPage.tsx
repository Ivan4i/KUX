import { useState, useEffect, useCallback } from 'react'
import toast from 'react-hot-toast'
import { Button } from '@/components/common/Button'
import {
  FaSync,
  FaChartLine,
  FaCheckCircle,
  FaExclamationTriangle,
  FaTimesCircle,
  FaMobileAlt,
  FaTasks,
  FaClock,
  FaCalendarAlt,
} from 'react-icons/fa'
import { getLogs, getLogsSummary, getDevices, getTasks } from '@/services/api'
import type { LogsSummary } from '@/types/log'
import type { DeviceStatus } from '@/types/device'
import type { Task } from '@/types/task'

interface TimeRangeStats {
  label: string
  hours: number
  stats: LogsSummary | null
}

export function AnalyticsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [devices, setDevices] = useState<DeviceStatus[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [timeRangeStats, setTimeRangeStats] = useState<TimeRangeStats[]>([
    { label: 'Last Hour', hours: 1, stats: null },
    { label: 'Last 24 Hours', hours: 24, stats: null },
    { label: 'Last Week', hours: 168, stats: null },
    { label: 'Last Month', hours: 720, stats: null },
  ])
  const [selectedRange, setSelectedRange] = useState(24)

  const loadData = useCallback(async (showToast = false) => {
    try {
      setIsRefreshing(true)

      // Load all data in parallel
      const [devicesData, tasksData, ...statsData] = await Promise.all([
        getDevices(),
        getTasks(undefined, undefined, 100),
        getLogsSummary(undefined, 1),
        getLogsSummary(undefined, 24),
        getLogsSummary(undefined, 168),
        getLogsSummary(undefined, 720),
      ])

      setDevices(devicesData)
      setTasks(tasksData)
      setTimeRangeStats([
        { label: 'Last Hour', hours: 1, stats: statsData[0] },
        { label: 'Last 24 Hours', hours: 24, stats: statsData[1] },
        { label: 'Last Week', hours: 168, stats: statsData[2] },
        { label: 'Last Month', hours: 720, stats: statsData[3] },
      ])

      if (showToast) {
        toast.success('Analytics refreshed')
      }
    } catch (error) {
      console.error('Error loading analytics:', error)
      toast.error('Failed to load analytics')
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  // Get current selected stats
  const currentStats = timeRangeStats.find((t) => t.hours === selectedRange)?.stats

  // Calculate device stats
  const onlineDevices = devices.filter((d) => d.current_status === 'online').length
  const totalDevices = devices.length
  const avgBattery = devices.length > 0
    ? Math.round(devices.reduce((sum, d) => sum + d.battery_level, 0) / devices.length)
    : 0
  const avgTemp = devices.length > 0
    ? (devices.reduce((sum, d) => sum + d.temperature, 0) / devices.length).toFixed(1)
    : '0'

  // Calculate task stats
  const completedTasks = tasks.filter((t) => t.status === 'Completed').length
  const failedTasks = tasks.filter((t) => t.status === 'Failed').length
  const pendingTasks = tasks.filter((t) => t.status === 'Pending').length
  const runningTasks = tasks.filter((t) => t.status === 'Running').length

  // Simple bar chart component
  const BarChart = ({ data, maxValue }: { data: { label: string; value: number; color: string }[]; maxValue: number }) => (
    <div className="space-y-3">
      {data.map((item, index) => (
        <div key={index}>
          <div className="flex items-center justify-between text-sm mb-1">
            <span className="text-gray-600">{item.label}</span>
            <span className="font-medium">{item.value}</span>
          </div>
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full ${item.color} rounded-full transition-all duration-500`}
              style={{ width: `${maxValue > 0 ? (item.value / maxValue) * 100 : 0}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  )

  // Success rate gauge
  const SuccessRateGauge = ({ rate }: { rate: number }) => {
    const getColor = () => {
      if (rate >= 90) return 'text-success-600'
      if (rate >= 70) return 'text-warning-600'
      return 'text-error-600'
    }

    const getStrokeColor = () => {
      if (rate >= 90) return '#10b981'
      if (rate >= 70) return '#f59e0b'
      return '#ef4444'
    }

    return (
      <div className="relative w-32 h-32 mx-auto">
        <svg className="transform -rotate-90 w-32 h-32">
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke="#e5e7eb"
            strokeWidth="12"
            fill="none"
          />
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke={getStrokeColor()}
            strokeWidth="12"
            fill="none"
            strokeDasharray={`${(rate / 100) * 352} 352`}
            strokeLinecap="round"
            className="transition-all duration-1000"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`text-2xl font-bold ${getColor()}`}>{rate}%</span>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-sm text-gray-600">Loading analytics...</p>
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
              <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
              <p className="mt-1 text-sm text-gray-500">
                Platform statistics and performance metrics
              </p>
            </div>
            <div className="flex items-center gap-4">
              {/* Time Range Selector */}
              <select
                value={selectedRange}
                onChange={(e) => setSelectedRange(Number(e.target.value))}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                {timeRangeStats.map((range) => (
                  <option key={range.hours} value={range.hours}>
                    {range.label}
                  </option>
                ))}
              </select>

              <Button
                variant="secondary"
                size="md"
                leftIcon={<FaSync />}
                onClick={() => loadData(true)}
                isLoading={isRefreshing}
              >
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary-100 rounded-xl">
                <FaChartLine className="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {currentStats?.total_logs || 0}
                </p>
                <p className="text-sm text-gray-500">Total Actions</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-success-100 rounded-xl">
                <FaCheckCircle className="w-6 h-6 text-success-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-success-600">
                  {currentStats?.success_count || 0}
                </p>
                <p className="text-sm text-gray-500">Successful</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-error-100 rounded-xl">
                <FaTimesCircle className="w-6 h-6 text-error-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-error-600">
                  {currentStats?.failed_count || 0}
                </p>
                <p className="text-sm text-gray-500">Failed</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-warning-100 rounded-xl">
                <FaExclamationTriangle className="w-6 h-6 text-warning-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-warning-600">
                  {currentStats?.warning_count || 0}
                </p>
                <p className="text-sm text-gray-500">Warnings</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Success Rate */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Success Rate</h3>
            <SuccessRateGauge rate={currentStats?.success_rate || 0} />
            <p className="text-center mt-4 text-sm text-gray-500">
              {currentStats?.success_count || 0} of {currentStats?.total_logs || 0} actions succeeded
            </p>
          </div>

          {/* Action Types */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions by Type</h3>
            {currentStats?.action_counts && Object.keys(currentStats.action_counts).length > 0 ? (
              <BarChart
                data={Object.entries(currentStats.action_counts).map(([key, value]) => ({
                  label: key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
                  value,
                  color: 'bg-primary-500',
                }))}
                maxValue={Math.max(...Object.values(currentStats.action_counts))}
              />
            ) : (
              <p className="text-gray-500 text-center py-8">No actions recorded</p>
            )}
          </div>

          {/* Tasks Overview */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Tasks Overview</h3>
            <BarChart
              data={[
                { label: 'Completed', value: completedTasks, color: 'bg-success-500' },
                { label: 'Running', value: runningTasks, color: 'bg-primary-500' },
                { label: 'Pending', value: pendingTasks, color: 'bg-warning-500' },
                { label: 'Failed', value: failedTasks, color: 'bg-error-500' },
              ]}
              maxValue={Math.max(completedTasks, runningTasks, pendingTasks, failedTasks, 1)}
            />
          </div>
        </div>

        {/* Device Stats */}
        <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Device Health */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Device Health</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <FaMobileAlt className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Online Devices</span>
                </div>
                <p className="text-2xl font-bold text-gray-900">
                  {onlineDevices} / {totalDevices}
                </p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <FaChartLine className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Avg Battery</span>
                </div>
                <p className={`text-2xl font-bold ${avgBattery > 50 ? 'text-success-600' : avgBattery > 20 ? 'text-warning-600' : 'text-error-600'}`}>
                  {avgBattery}%
                </p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <FaClock className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Avg Temperature</span>
                </div>
                <p className={`text-2xl font-bold ${Number(avgTemp) < 35 ? 'text-gray-900' : Number(avgTemp) < 40 ? 'text-warning-600' : 'text-error-600'}`}>
                  {avgTemp}°C
                </p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <FaTasks className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Tasks Today</span>
                </div>
                <p className="text-2xl font-bold text-primary-600">
                  {devices.reduce((sum, d) => sum + d.tasks_completed_today, 0)}
                </p>
              </div>
            </div>
          </div>

          {/* Time Range Comparison */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Over Time</h3>
            <div className="space-y-4">
              {timeRangeStats.map((range) => (
                <div
                  key={range.hours}
                  className={`p-4 rounded-lg border transition-colors ${
                    selectedRange === range.hours
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-gray-50 cursor-pointer hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedRange(range.hours)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <FaCalendarAlt className="w-4 h-4 text-gray-400" />
                      <span className="font-medium text-gray-900">{range.label}</span>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="text-gray-500">
                        {range.stats?.total_logs || 0} actions
                      </span>
                      <span
                        className={`font-medium ${
                          (range.stats?.success_rate || 0) >= 90
                            ? 'text-success-600'
                            : (range.stats?.success_rate || 0) >= 70
                            ? 'text-warning-600'
                            : 'text-error-600'
                        }`}
                      >
                        {range.stats?.success_rate || 0}% success
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
