import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { RiDraggable, RiEditLine, RiDeleteBinLine, RiWhatsappLine, RiInstagramLine, RiLinkedinLine, RiTelegramLine } from '@remixicon/react'
import type { ScenarioStep, AgentType } from '@/types/scenario'
import { STEP_STATUS_CONFIG, AGENT_ACTIONS } from '@/types/scenario'

interface StepCardProps {
  step: ScenarioStep
  index: number
  onEdit: (step: ScenarioStep) => void
  onDelete: (stepId: string) => void
  isDragging?: boolean
}

const AGENT_ICONS: Record<AgentType, React.ReactNode> = {
  whatsapp: <RiWhatsappLine className="w-4 h-4 text-green-500" />,
  instagram: <RiInstagramLine className="w-4 h-4 text-pink-500" />,
  linkedin: <RiLinkedinLine className="w-4 h-4 text-blue-600" />,
  telegram: <RiTelegramLine className="w-4 h-4 text-blue-400" />,
}

const AGENT_COLORS: Record<AgentType, string> = {
  whatsapp: 'border-l-green-500',
  instagram: 'border-l-pink-500',
  linkedin: 'border-l-blue-600',
  telegram: 'border-l-blue-400',
}

export function StepCard({ step, index, onEdit, onDelete, isDragging = false }: StepCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: step.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  const statusConfig = STEP_STATUS_CONFIG[step.status]
  const agentActions = AGENT_ACTIONS[step.agent_type] || []
  const actionInfo = agentActions.find(a => a.action === step.action)

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`
        bg-white rounded-lg border-l-4 ${AGENT_COLORS[step.agent_type]}
        border border-gray-200 shadow-sm
        ${isDragging ? 'shadow-lg ring-2 ring-blue-500 ring-opacity-50' : ''}
        transition-shadow hover:shadow-md
      `}
    >
      <div className="p-3">
        <div className="flex items-start gap-3">
          {/* Drag Handle */}
          <button
            className="p-1 text-gray-400 hover:text-gray-600 cursor-grab active:cursor-grabbing"
            {...attributes}
            {...listeners}
          >
            <RiDraggable className="w-4 h-4" />
          </button>

          {/* Step Number */}
          <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
            <span className="text-xs font-semibold text-gray-600">{index + 1}</span>
          </div>

          {/* Agent Icon */}
          <div className="flex-shrink-0 mt-0.5">
            {AGENT_ICONS[step.agent_type]}
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h4 className="text-sm font-medium text-gray-900 truncate">
                {step.name}
              </h4>
              <span className={`px-1.5 py-0.5 text-xs rounded ${statusConfig.bgColor} ${statusConfig.color}`}>
                {statusConfig.label}
              </span>
            </div>

            <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
              <span className="font-medium capitalize">{step.agent_type}</span>
              <span>•</span>
              <span>{actionInfo?.label || step.action}</span>

              {step.delay_before_seconds > 0 && (
                <>
                  <span>•</span>
                  <span>Задержка: {step.delay_before_seconds}с</span>
                </>
              )}

              {step.condition && (
                <>
                  <span>•</span>
                  <span className="text-purple-600">Условно</span>
                </>
              )}
            </div>

            {/* Parameters Preview */}
            {step.parameters && Object.keys(step.parameters).length > 0 && (
              <div className="mt-2 p-2 bg-gray-50 rounded text-xs font-mono text-gray-600 truncate">
                {Object.entries(step.parameters).slice(0, 2).map(([key, value]) => (
                  <span key={key} className="mr-3">
                    {key}: {typeof value === 'string' ? value.substring(0, 30) : JSON.stringify(value).substring(0, 30)}
                    {(typeof value === 'string' && value.length > 30) ? '...' : ''}
                  </span>
                ))}
                {Object.keys(step.parameters).length > 2 && (
                  <span className="text-gray-400">+{Object.keys(step.parameters).length - 2} ещё</span>
                )}
              </div>
            )}

            {/* Error message if failed */}
            {step.status === 'failed' && step.error_message && (
              <div className="mt-2 p-2 bg-red-50 rounded text-xs text-red-600">
                {step.error_message}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-1">
            <button
              onClick={() => onEdit(step)}
              className="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded"
              title="Изменить шаг"
            >
              <RiEditLine className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onDelete(step.id)}
              className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded"
              title="Удалить шаг"
            >
              <RiDeleteBinLine className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// Draggable overlay version for when dragging
export function StepCardOverlay({ step, index }: { step: ScenarioStep; index: number }) {
  const statusConfig = STEP_STATUS_CONFIG[step.status]

  return (
    <div className={`
      bg-white rounded-lg border-l-4 ${AGENT_COLORS[step.agent_type]}
      border border-gray-200 shadow-xl opacity-90
    `}>
      <div className="p-3">
        <div className="flex items-start gap-3">
          <div className="p-1 text-gray-400">
            <RiDraggable className="w-4 h-4" />
          </div>

          <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
            <span className="text-xs font-semibold text-gray-600">{index + 1}</span>
          </div>

          <div className="flex-shrink-0 mt-0.5">
            {AGENT_ICONS[step.agent_type]}
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h4 className="text-sm font-medium text-gray-900 truncate">
                {step.name}
              </h4>
              <span className={`px-1.5 py-0.5 text-xs rounded ${statusConfig.bgColor} ${statusConfig.color}`}>
                {statusConfig.label}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
