import { Card } from '@/components/common/Card'
import type { Log } from '@/types/log'
import { FaCheckCircle, FaExclamationTriangle, FaTimesCircle } from 'react-icons/fa'
import { formatDistanceToNow } from 'date-fns'

interface RecentLogsProps {
  logs: Log[]
}

export function RecentLogs({ logs }: RecentLogsProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <FaCheckCircle className="text-success-500" />
      case 'warning':
        return <FaExclamationTriangle className="text-warning-500" />
      case 'failed':
        return <FaTimesCircle className="text-error-500" />
      default:
        return null
    }
  }

  const getStatusBgColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'bg-success-50'
      case 'warning':
        return 'bg-warning-50'
      case 'failed':
        return 'bg-error-50'
      default:
        return 'bg-gray-50'
    }
  }

  if (logs.length === 0) {
    return (
      <Card title="Recent Logs" subtitle="Last 10 entries">
        <div className="py-12 text-center">
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
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No activity logs</h3>
          <p className="mt-1 text-sm text-gray-500">
            Logs will appear here when tasks are executed
          </p>
        </div>
      </Card>
    )
  }

  return (
    <Card title="Recent Logs" subtitle="Last 10 entries" padding="none">
      <div className="divide-y divide-gray-100">
        {logs.map((log) => (
          <div
            key={log.id}
            className="px-4 py-3 hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-start gap-3">
              {/* Status Icon */}
              <div className={`flex-shrink-0 w-8 h-8 rounded-lg ${getStatusBgColor(log.status)} flex items-center justify-center`}>
                {getStatusIcon(log.status)}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {log.action_type.replace(/_/g, ' ')}
                    </p>
                    <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">
                      {log.details}
                    </p>
                  </div>
                  <span className="text-xs text-gray-400 whitespace-nowrap">
                    {formatDistanceToNow(new Date(log.created_at), { addSuffix: true })}
                  </span>
                </div>

                {/* Device */}
                <div className="flex items-center gap-3 mt-1">
                  <span className="text-xs text-gray-500">
                    {log.device_id}
                  </span>
                  {log.task_id && (
                    <>
                      <span className="text-gray-300">•</span>
                      <span className="text-xs text-gray-500">
                        Task #{log.task_id}
                      </span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}
