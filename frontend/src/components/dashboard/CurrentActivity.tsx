import { Card } from '@/components/common/Card'
import type { Task } from '@/types/task'
import type { TaskProgress } from '@/types/task'
import { RiWhatsappLine, RiLoader4Line } from '@remixicon/react'

interface CurrentActivityProps {
  task: Task | null
  progress: TaskProgress | null
}

export function CurrentActivity({ task, progress }: CurrentActivityProps) {
  if (!task) {
    return (
      <Card title="Current Activity">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-3">
            <RiWhatsappLine className="text-2xl text-gray-400" />
          </div>
          <h3 className="text-sm font-medium text-gray-900">No active tasks</h3>
          <p className="mt-1 text-sm text-gray-500">
            Click "Run Task" to start sending messages
          </p>
        </div>
      </Card>
    )
  }

  return (
    <Card
      title="Current Activity"
      subtitle={`Task #${task.id}`}
    >
      <div className="space-y-4">
        {/* Task Info */}
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-10 h-10 bg-success-100 rounded-lg flex items-center justify-center">
            <RiWhatsappLine className="text-success-600 text-xl" />
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-medium text-gray-900 truncate">
              {task.recipient_name}
            </h4>
            <p className="text-sm text-gray-500">{task.phone_number}</p>
            <p className="text-xs text-gray-400 mt-1 line-clamp-2">
              {task.message_content}
            </p>
          </div>
        </div>

        {/* Progress */}
        {progress && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600 flex items-center gap-2">
                <RiLoader4Line className="animate-spin" />
                {progress.message}
              </span>
              {progress.progress_percent !== null && (
                <span className="font-medium text-primary-600">
                  {progress.progress_percent}%
                </span>
              )}
            </div>

            {progress.progress_percent !== null && (
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress.progress_percent}%` }}
                />
              </div>
            )}
          </div>
        )}

        {/* Device */}
        {task.device_id && (
          <div className="pt-3 border-t border-gray-100">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Device</span>
              <span className="font-medium text-gray-900">{task.device_id}</span>
            </div>
          </div>
        )}
      </div>
    </Card>
  )
}
