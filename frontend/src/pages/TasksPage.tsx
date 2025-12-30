import { useState, useEffect, useCallback } from 'react'
import toast from 'react-hot-toast'
import { RiRefreshLine, RiPlayFill, RiDeleteBinLine, RiFilterLine, RiCheckLine, RiCloseLine, RiTimeLine, RiLoader4Line } from '@remixicon/react'
import { Button } from '@/components/common/Button'
import { useWebSocketMessages } from '@/hooks/useWebSocket'
import { getTasks, runTask, deleteTask, syncNotionTasks } from '@/services/api'
import type { Task, TaskProgress } from '@/types/task'

type TaskStatus = 'Pending' | 'Running' | 'Sent' | 'Failed' | 'all'

const STATUS_CONFIG: Record<string, { color: string; bgColor: string; icon: React.ReactNode }> = {
  Pending: { color: 'text-yellow-600', bgColor: 'bg-yellow-100', icon: <RiTimeLine className="w-3 h-3" /> },
  Running: { color: 'text-primary-600', bgColor: 'bg-blue-100', icon: <RiLoader4Line className="w-3 h-3 animate-spin" /> },
  Sent: { color: 'text-green-600', bgColor: 'bg-green-100', icon: <RiCheckLine className="w-3 h-3" /> },
  Failed: { color: 'text-red-600', bgColor: 'bg-red-100', icon: <RiCloseLine className="w-3 h-3" /> },
}

export function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [taskProgress, setTaskProgress] = useState<Record<number, TaskProgress>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [isInitialLoad, setIsInitialLoad] = useState(true)
  const [isSyncing, setIsSyncing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [filterStatus, setFilterStatus] = useState<TaskStatus>('all')
  const [selectedTasks, setSelectedTasks] = useState<Set<number>>(new Set())

  // Load tasks
  const loadTasks = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)

      const status = filterStatus === 'all' ? undefined : filterStatus
      const data = await getTasks(status, undefined, 100)
      setTasks(data)
      setIsInitialLoad(false)
    } catch (error: any) {
      console.error('Error loading tasks:', error)
      setError(error?.response?.data?.error || error?.message || 'Не удалось загрузить задачи')
      toast.error('Не удалось загрузить задачи')
    } finally {
      setIsLoading(false)
    }
  }, [filterStatus])

  useEffect(() => {
    loadTasks()
  }, [loadTasks])

  // WebSocket handlers
  useWebSocketMessages('task_started', (_message: any) => {
    loadTasks()
  })

  useWebSocketMessages('task_progress', (message: any) => {
    setTaskProgress(prev => ({
      ...prev,
      [message.task_id]: {
        task_id: message.task_id,
        message: message.message,
        progress_percent: message.progress_percent,
      }
    }))
  })

  useWebSocketMessages('task_completed', (_message: any) => {
    loadTasks()
    toast.success('Задача выполнена!')
  })

  useWebSocketMessages('task_failed', (message: any) => {
    loadTasks()
    toast.error(`Задача не выполнена: ${message.error || 'Неизвестная ошибка'}`)
  })

  // Actions
  const handleSyncNotion = async () => {
    try {
      setIsSyncing(true)
      const result = await syncNotionTasks(20)
      toast.success(`Синхронизировано ${result.tasks_synced} задач из Notion`)
      loadTasks()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Ошибка синхронизации Notion')
    } finally {
      setIsSyncing(false)
    }
  }

  const handleRunTask = async (taskId?: number) => {
    try {
      setIsLoading(true)
      await runTask(taskId)
      toast.success(taskId ? 'Задача запущена!' : 'Следующая задача запущена!')
      loadTasks()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Не удалось запустить задачу')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту задачу?')) return

    try {
      setIsLoading(true)
      await deleteTask(taskId)
      toast.success('Задача удалена')
      setTasks(prev => prev.filter(t => t.id !== taskId))
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Не удалось удалить задачу')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteSelected = async () => {
    if (selectedTasks.size === 0) return
    if (!window.confirm(`Удалить ${selectedTasks.size} выбранных задач?`)) return

    try {
      setIsLoading(true)
      for (const taskId of selectedTasks) {
        await deleteTask(taskId)
      }
      toast.success(`Удалено ${selectedTasks.size} задач`)
      setSelectedTasks(new Set())
      loadTasks()
    } catch (error: any) {
      toast.error(error?.response?.data?.error || 'Не удалось удалить задачи')
    } finally {
      setIsLoading(false)
    }
  }

  const toggleTaskSelection = (taskId: number) => {
    setSelectedTasks(prev => {
      const next = new Set(prev)
      if (next.has(taskId)) {
        next.delete(taskId)
      } else {
        next.add(taskId)
      }
      return next
    })
  }

  const toggleSelectAll = () => {
    if (selectedTasks.size === tasks.length) {
      setSelectedTasks(new Set())
    } else {
      setSelectedTasks(new Set(tasks.map(t => t.id)))
    }
  }

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  // Stats
  const stats = {
    total: tasks.length,
    pending: tasks.filter(t => t.status === 'Pending').length,
    running: tasks.filter(t => t.status === 'Running').length,
    sent: tasks.filter(t => t.status === 'Sent').length,
    failed: tasks.filter(t => t.status === 'Failed').length,
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Задачи</h1>
              <p className="mt-1 text-sm text-gray-500">
                Управление задачами WhatsApp сообщений
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Button
                variant="secondary"
                size="md"
                leftIcon={<RiRefreshLine />}
                onClick={handleSyncNotion}
                isLoading={isSyncing}
              >
                Синхр. Notion
              </Button>
              <Button
                variant="primary"
                size="md"
                leftIcon={<RiPlayFill />}
                onClick={() => handleRunTask()}
                isLoading={isLoading}
                disabled={stats.pending === 0}
              >
                Запустить
              </Button>
              <Button
                variant="ghost"
                size="md"
                leftIcon={<RiRefreshLine />}
                onClick={() => loadTasks()}
              >
                Обновить
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-5 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-xs text-gray-500">Всего</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
              <div className="text-xs text-gray-500">Ожидает</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">{stats.running}</div>
              <div className="text-xs text-gray-500">Выполняется</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.sent}</div>
              <div className="text-xs text-gray-500">Отправлено</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">{stats.failed}</div>
              <div className="text-xs text-gray-500">Ошибка</div>
            </div>
          </div>
        </div>
      </div>

      {/* Filters & Actions */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <RiFilterLine className="w-4 h-4 text-gray-400" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value as TaskStatus)}
                  className="text-sm border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="all">Все статусы</option>
                  <option value="Pending">Ожидает</option>
                  <option value="Running">Выполняется</option>
                  <option value="Sent">Отправлено</option>
                  <option value="Failed">Ошибка</option>
                </select>
              </div>

              {selectedTasks.size > 0 && (
                <Button
                  variant="danger"
                  size="sm"
                  leftIcon={<RiDeleteBinLine />}
                  onClick={handleDeleteSelected}
                >
                  Удалить ({selectedTasks.size})
                </Button>
              )}
            </div>

            <span className="text-sm text-gray-500">
              {tasks.length} задач
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Loading */}
        {isInitialLoad && isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
              <p className="mt-4 text-sm text-gray-600">Загрузка задач...</p>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!isLoading && tasks.length === 0 && (
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
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">Нет задач</h3>
            <p className="mt-1 text-sm text-gray-500">
              Синхронизируйте задачи из Notion или создайте вручную.
            </p>
            <div className="mt-6">
              <Button variant="primary" onClick={handleSyncNotion} isLoading={isSyncing}>
                <RiRefreshLine className="w-4 h-4 mr-2" />
                Синхронизировать из Notion
              </Button>
            </div>
          </div>
        )}

        {/* Tasks Table */}
        {!isInitialLoad && tasks.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left">
                    <input
                      type="checkbox"
                      checked={selectedTasks.size === tasks.length && tasks.length > 0}
                      onChange={toggleSelectAll}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Статус
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Получатель
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Сообщение
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Устройство
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Запланировано
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Действия
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {tasks.map((task) => {
                  const config = STATUS_CONFIG[task.status] || STATUS_CONFIG.Pending
                  const progress = taskProgress[task.id]

                  return (
                    <tr key={task.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <input
                          type="checkbox"
                          checked={selectedTasks.has(task.id)}
                          onChange={() => toggleTaskSelection(task.id)}
                          className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-full ${config.bgColor} ${config.color}`}>
                          {config.icon}
                          {task.status}
                        </span>
                        {progress && task.status === 'Running' && (
                          <div className="mt-1 text-xs text-gray-500">
                            {progress.message}
                            {progress.progress_percent !== null && (
                              <span className="ml-1">({progress.progress_percent}%)</span>
                            )}
                          </div>
                        )}
                      </td>
                      <td className="px-4 py-3">
                        <div className="text-sm font-medium text-gray-900">
                          {task.recipient_name}
                        </div>
                        <div className="text-xs text-gray-500 font-mono">
                          {task.phone_number}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="text-sm text-gray-700 max-w-xs truncate" title={task.message_content}>
                          {task.message_content}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <span className="text-sm text-gray-600">
                          {task.device_id || task.device_assignment || '-'}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span className="text-sm text-gray-600">
                          {formatDate(task.scheduled_send_time)}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          {task.status === 'Pending' && (
                            <button
                              onClick={() => handleRunTask(task.id)}
                              className="p-1.5 text-primary-600 hover:bg-blue-50 rounded"
                              title="Запустить"
                            >
                              <RiPlayFill className="w-3.5 h-3.5" />
                            </button>
                          )}
                          <button
                            onClick={() => handleDeleteTask(task.id)}
                            className="p-1.5 text-red-600 hover:bg-red-50 rounded"
                            title="Удалить"
                          >
                            <RiDeleteBinLine className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
