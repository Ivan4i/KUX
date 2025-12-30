import { useState, useEffect, useCallback } from 'react'
import toast from 'react-hot-toast'
import { Button } from '@/components/common/Button'
import {
  RiRefreshLine,
  RiFilterLine,
  RiCheckboxCircleFill,
  RiAlertLine,
  RiCloseCircleFill,
  RiInformationLine,
  RiDeleteBinLine,
  RiSearchLine,
  RiArrowDownSLine,
  RiArrowUpSLine,
} from '@remixicon/react'
import { getLogs, getLogsSummary, cleanupOldLogs, getDevices } from '@/services/api'
import type { Log, LogsSummary } from '@/types/log'
import type { DeviceStatus } from '@/types/device'

const STATUS_CONFIG: Record<string, { icon: React.ReactNode; color: string; bgColor: string; label: string }> = {
  success: {
    icon: <RiCheckboxCircleFill className="w-4 h-4" />,
    color: 'text-success-600',
    bgColor: 'bg-success-100',
    label: 'Успешно',
  },
  warning: {
    icon: <RiAlertLine className="w-4 h-4" />,
    color: 'text-warning-600',
    bgColor: 'bg-warning-100',
    label: 'Внимание',
  },
  failed: {
    icon: <RiCloseCircleFill className="w-4 h-4" />,
    color: 'text-error-600',
    bgColor: 'bg-error-100',
    label: 'Ошибка',
  },
  info: {
    icon: <RiInformationLine className="w-4 h-4" />,
    color: 'text-primary-600',
    bgColor: 'bg-primary-100',
    label: 'Инфо',
  },
}

const ACTION_TYPES = [
  { value: '', label: 'Все действия' },
  { value: 'whatsapp_send', label: 'Отправка WhatsApp' },
  { value: 'device_check', label: 'Проверка устройства' },
  { value: 'app_restart', label: 'Перезапуск приложения' },
  { value: 'device_reboot', label: 'Перезагрузка устройства' },
  { value: 'screenshot', label: 'Скриншот' },
  { value: 'system', label: 'Система' },
]

const TIME_RANGES = [
  { value: 1, label: 'За час' },
  { value: 6, label: 'За 6 часов' },
  { value: 24, label: 'За 24 часа' },
  { value: 48, label: 'За 2 дня' },
  { value: 168, label: 'За неделю' },
  { value: 720, label: 'За месяц' },
]

export function LogsPage() {
  const [logs, setLogs] = useState<Log[]>([])
  const [summary, setSummary] = useState<LogsSummary | null>(null)
  const [devices, setDevices] = useState<DeviceStatus[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [isCleaning, setIsCleaning] = useState(false)

  // Filters
  const [deviceFilter, setDeviceFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [actionFilter, setActionFilter] = useState('')
  const [hoursFilter, setHoursFilter] = useState(24)
  const [searchQuery, setSearchQuery] = useState('')
  const [showFilters, setShowFilters] = useState(false)

  // Expanded log details
  const [expandedLogId, setExpandedLogId] = useState<number | null>(null)

  // Load data
  const loadData = useCallback(async (showToast = false) => {
    try {
      setIsRefreshing(true)
      const [logsData, summaryData, devicesData] = await Promise.all([
        getLogs({
          deviceId: deviceFilter || undefined,
          status: statusFilter || undefined,
          actionType: actionFilter || undefined,
          hours: hoursFilter,
          limit: 200,
        }),
        getLogsSummary(deviceFilter || undefined, hoursFilter),
        getDevices(),
      ])

      setLogs(logsData)
      setSummary(summaryData)
      setDevices(devicesData)

      if (showToast) {
        toast.success('Логи обновлены')
      }
    } catch (error) {
      console.error('Error loading logs:', error)
      toast.error('Не удалось загрузить логи')
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }, [deviceFilter, statusFilter, actionFilter, hoursFilter])

  useEffect(() => {
    loadData()
  }, [loadData])

  const handleCleanup = async () => {
    if (!confirm('Вы уверены, что хотите удалить логи старше 30 дней? Это действие нельзя отменить.')) {
      return
    }

    try {
      setIsCleaning(true)
      const result = await cleanupOldLogs(30)
      toast.success(`Удалено ${result.deleted_count} старых записей`)
      loadData()
    } catch (error) {
      console.error('Error cleaning logs:', error)
      toast.error('Не удалось очистить логи')
    } finally {
      setIsCleaning(false)
    }
  }

  // Filter logs by search query
  const filteredLogs = logs.filter((log) => {
    if (!searchQuery) return true
    const query = searchQuery.toLowerCase()
    return (
      log.device_id?.toLowerCase().includes(query) ||
      log.action_type?.toLowerCase().includes(query) ||
      log.details?.toLowerCase().includes(query) ||
      log.status?.toLowerCase().includes(query)
    )
  })

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  }

  const getDeviceName = (deviceId: string) => {
    const device = devices.find((d) => d.id === deviceId)
    return device?.name || deviceId
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-sm text-gray-600">Загрузка логов...</p>
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
              <h1 className="text-3xl font-bold text-gray-900">Журнал активности</h1>
              <p className="mt-1 text-sm text-gray-500">
                Просмотр и анализ системных логов
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="md"
                leftIcon={<RiDeleteBinLine />}
                onClick={handleCleanup}
                isLoading={isCleaning}
              >
                Очистка
              </Button>
              <Button
                variant="secondary"
                size="md"
                leftIcon={<RiRefreshLine />}
                onClick={() => loadData(true)}
                isLoading={isRefreshing}
              >
                Обновить
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
              <p className="text-sm text-gray-500">Всего логов</p>
              <p className="text-2xl font-bold text-gray-900">{summary.total_logs}</p>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
              <p className="text-sm text-gray-500">Успешно</p>
              <p className="text-2xl font-bold text-success-600">{summary.success_count}</p>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
              <p className="text-sm text-gray-500">Предупреждения</p>
              <p className="text-2xl font-bold text-warning-600">{summary.warning_count}</p>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
              <p className="text-sm text-gray-500">Ошибки</p>
              <p className="text-2xl font-bold text-error-600">{summary.failed_count}</p>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
              <p className="text-sm text-gray-500">Успешность</p>
              <p className="text-2xl font-bold text-primary-600">{summary.success_rate}%</p>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-6">
          <div
            className="px-4 py-3 flex items-center justify-between cursor-pointer"
            onClick={() => setShowFilters(!showFilters)}
          >
            <div className="flex items-center gap-2">
              <RiFilterLine className="w-4 h-4 text-gray-500" />
              <span className="font-medium text-gray-700">Фильтры</span>
              {(deviceFilter || statusFilter || actionFilter) && (
                <span className="px-2 py-0.5 text-xs bg-primary-100 text-primary-700 rounded-full">
                  Активны
                </span>
              )}
            </div>
            {showFilters ? (
              <RiArrowUpSLine className="w-4 h-4 text-gray-500" />
            ) : (
              <RiArrowDownSLine className="w-4 h-4 text-gray-500" />
            )}
          </div>

          {showFilters && (
            <div className="px-4 py-4 border-t border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Устройство
                  </label>
                  <select
                    value={deviceFilter}
                    onChange={(e) => setDeviceFilter(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="">Все устройства</option>
                    {devices.map((device) => (
                      <option key={device.id} value={device.id}>
                        {device.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Статус
                  </label>
                  <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="">Все статусы</option>
                    <option value="success">Успешно</option>
                    <option value="warning">Предупреждение</option>
                    <option value="failed">Ошибка</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Тип действия
                  </label>
                  <select
                    value={actionFilter}
                    onChange={(e) => setActionFilter(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    {ACTION_TYPES.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Период
                  </label>
                  <select
                    value={hoursFilter}
                    onChange={(e) => setHoursFilter(Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    {TIME_RANGES.map((range) => (
                      <option key={range.value} value={range.value}>
                        {range.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setDeviceFilter('')
                    setStatusFilter('')
                    setActionFilter('')
                    setHoursFilter(24)
                  }}
                >
                  Сбросить фильтры
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative">
            <RiSearchLine className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Поиск логов..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>

        {/* Logs Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {filteredLogs.length === 0 ? (
            <div className="p-12 text-center">
              <RiInformationLine className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900">Логи не найдены</h3>
              <p className="mt-1 text-sm text-gray-500">
                Попробуйте изменить фильтры или период
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Статус
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Время
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Устройство
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Действие
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Детали
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ID задачи
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredLogs.map((log) => {
                    const statusConfig = STATUS_CONFIG[log.status] || STATUS_CONFIG.info
                    const isExpanded = expandedLogId === log.id

                    return (
                      <>
                        <tr
                          key={log.id}
                          className="hover:bg-gray-50 cursor-pointer"
                          onClick={() => setExpandedLogId(isExpanded ? null : log.id)}
                        >
                          <td className="px-4 py-3 whitespace-nowrap">
                            <span
                              className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${statusConfig.bgColor} ${statusConfig.color}`}
                            >
                              {statusConfig.icon}
                              {statusConfig.label}
                            </span>
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                            {formatDate(log.created_at)}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                            {getDeviceName(log.device_id)}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                            <code className="px-2 py-0.5 bg-gray-100 rounded text-xs">
                              {log.action_type}
                            </code>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-500 max-w-xs truncate">
                            {log.details}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                            {log.task_id || '-'}
                          </td>
                        </tr>
                        {isExpanded && (
                          <tr key={`${log.id}-expanded`}>
                            <td colSpan={6} className="px-4 py-4 bg-gray-50">
                              <div className="space-y-3">
                                <div>
                                  <span className="text-xs font-medium text-gray-500 uppercase">
                                    Полные детали:
                                  </span>
                                  <p className="mt-1 text-sm text-gray-700 whitespace-pre-wrap">
                                    {log.details || 'Нет деталей'}
                                  </p>
                                </div>
                                {log.screenshot_path && (
                                  <div>
                                    <span className="text-xs font-medium text-gray-500 uppercase">
                                      Скриншот:
                                    </span>
                                    <p className="mt-1 text-sm text-primary-600 font-mono">
                                      {log.screenshot_path}
                                    </p>
                                  </div>
                                )}
                                <div className="grid grid-cols-4 gap-4 text-xs">
                                  <div>
                                    <span className="text-gray-500">ID лога:</span>
                                    <span className="ml-1 font-medium">{log.id}</span>
                                  </div>
                                  <div>
                                    <span className="text-gray-500">ID устройства:</span>
                                    <span className="ml-1 font-medium">{log.device_id}</span>
                                  </div>
                                  <div>
                                    <span className="text-gray-500">ID задачи:</span>
                                    <span className="ml-1 font-medium">{log.task_id || 'Н/Д'}</span>
                                  </div>
                                  <div>
                                    <span className="text-gray-500">Статус:</span>
                                    <span className={`ml-1 font-medium ${statusConfig.color}`}>
                                      {log.status}
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </td>
                          </tr>
                        )}
                      </>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}

          {filteredLogs.length > 0 && (
            <div className="px-4 py-3 bg-gray-50 border-t border-gray-200">
              <p className="text-sm text-gray-500">
                Показано {filteredLogs.length} из {logs.length} логов
                {searchQuery && ` (фильтр: "${searchQuery}")`}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
