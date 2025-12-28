import { FaPlay, FaPause, FaStop, FaCopy, FaTrash, FaClock, FaEdit } from 'react-icons/fa'
import { Button } from '@/components/common/Button'
import type { ScenarioListItem } from '@/types/scenario'
import { STATUS_CONFIG } from '@/types/scenario'

interface ScenarioCardProps {
  scenario: ScenarioListItem
  onRun: (id: string) => void
  onPause: (id: string) => void
  onCancel: (id: string) => void
  onEdit: (id: string) => void
  onDuplicate: (id: string) => void
  onDelete: (id: string) => void
  isLoading?: boolean
}

export function ScenarioCard({
  scenario,
  onRun,
  onPause,
  onCancel,
  onEdit,
  onDuplicate,
  onDelete,
  isLoading = false,
}: ScenarioCardProps) {
  const statusConfig = STATUS_CONFIG[scenario.status]
  const isRunning = scenario.status === 'running'
  const isPaused = scenario.status === 'paused'
  const canRun = ['draft', 'completed', 'failed', 'cancelled'].includes(scenario.status)

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-semibold text-gray-900 truncate">
                {scenario.name}
              </h3>
              {scenario.is_template && (
                <span className="px-2 py-0.5 text-xs font-medium text-purple-600 bg-purple-100 rounded-full">
                  Template
                </span>
              )}
            </div>
            {scenario.description && (
              <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                {scenario.description}
              </p>
            )}
          </div>

          {/* Status Badge */}
          <span
            className={`px-2.5 py-1 text-xs font-medium rounded-full ${statusConfig.bgColor} ${statusConfig.color}`}
          >
            {statusConfig.label}
          </span>
        </div>

        {/* Info */}
        <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
          <span className="flex items-center gap-1">
            <span className="font-medium">{scenario.total_steps}</span> steps
          </span>

          {scenario.cron_expression && (
            <span className="flex items-center gap-1">
              <FaClock className="w-3 h-3" />
              <span className="font-mono text-xs">{scenario.cron_expression}</span>
            </span>
          )}

          <span className="text-gray-400">
            {formatDate(scenario.updated_at)}
          </span>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {canRun && (
            <Button
              variant="primary"
              size="sm"
              leftIcon={<FaPlay className="w-3 h-3" />}
              onClick={() => onRun(scenario.id)}
              isLoading={isLoading}
              disabled={scenario.total_steps === 0}
            >
              Run
            </Button>
          )}

          {isRunning && (
            <>
              <Button
                variant="secondary"
                size="sm"
                leftIcon={<FaPause className="w-3 h-3" />}
                onClick={() => onPause(scenario.id)}
                isLoading={isLoading}
              >
                Pause
              </Button>
              <Button
                variant="danger"
                size="sm"
                leftIcon={<FaStop className="w-3 h-3" />}
                onClick={() => onCancel(scenario.id)}
                isLoading={isLoading}
              >
                Cancel
              </Button>
            </>
          )}

          {isPaused && (
            <>
              <Button
                variant="primary"
                size="sm"
                leftIcon={<FaPlay className="w-3 h-3" />}
                onClick={() => onRun(scenario.id)}
                isLoading={isLoading}
              >
                Resume
              </Button>
              <Button
                variant="danger"
                size="sm"
                leftIcon={<FaStop className="w-3 h-3" />}
                onClick={() => onCancel(scenario.id)}
                isLoading={isLoading}
              >
                Cancel
              </Button>
            </>
          )}

          <div className="flex-1" />

          <Button
            variant="ghost"
            size="sm"
            leftIcon={<FaEdit className="w-3 h-3" />}
            onClick={() => onEdit(scenario.id)}
          >
            Edit
          </Button>

          <Button
            variant="ghost"
            size="sm"
            leftIcon={<FaCopy className="w-3 h-3" />}
            onClick={() => onDuplicate(scenario.id)}
          >
            Copy
          </Button>

          <Button
            variant="ghost"
            size="sm"
            leftIcon={<FaTrash className="w-3 h-3 text-red-500" />}
            onClick={() => onDelete(scenario.id)}
            className="text-red-500 hover:text-red-600 hover:bg-red-50"
          />
        </div>
      </div>

      {/* Progress bar for running scenarios */}
      {isRunning && (
        <div className="h-1 bg-gray-100 rounded-b-lg overflow-hidden">
          <div
            className="h-full bg-blue-500 animate-pulse"
            style={{ width: '60%' }}
          />
        </div>
      )}
    </div>
  )
}
