import { memo } from 'react'
import { Handle, Position, NodeProps } from 'reactflow'
import {
  RiWhatsappLine,
  RiMessage2Line,
  RiRobotLine,
  RiMailLine,
  RiTelegramLine,
  RiSparklingLine
} from '@remixicon/react'

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  whatsapp: RiWhatsappLine,
  sms: RiMessage2Line,
  max: RiRobotLine,
  email: RiMailLine,
  telegram: RiTelegramLine,
  gemini: RiSparklingLine,
}

const agentColors: Record<string, { bg: string; border: string; icon: string }> = {
  whatsapp: { bg: 'bg-green-500', border: 'border-green-600', icon: 'bg-green-400' },
  sms: { bg: 'bg-blue-500', border: 'border-blue-600', icon: 'bg-blue-400' },
  max: { bg: 'bg-orange-500', border: 'border-orange-600', icon: 'bg-orange-400' },
  telegram: { bg: 'bg-sky-500', border: 'border-sky-600', icon: 'bg-sky-400' },
  gemini: { bg: 'bg-indigo-500', border: 'border-indigo-600', icon: 'bg-indigo-400' },
  default: { bg: 'bg-gray-500', border: 'border-gray-600', icon: 'bg-gray-400' },
}

interface ActionNodeData {
  label: string
  description?: string
  icon?: string
  agent?: string
}

export const ActionNode = memo(({ data, selected }: NodeProps<ActionNodeData>) => {
  const Icon = data.icon ? iconMap[data.icon] || RiRobotLine : RiRobotLine
  const colors = agentColors[data.agent || 'default'] || agentColors.default

  return (
    <div
      className={`px-4 py-3 rounded-lg ${colors.bg} text-white min-w-[180px] shadow-lg ${
        selected ? 'ring-2 ring-blue-300 ring-offset-2' : ''
      }`}
    >
      {/* Input handle */}
      <Handle
        type="target"
        position={Position.Top}
        className={`!w-3 !h-3 !bg-white !${colors.border}`}
      />

      <div className="flex items-center gap-2">
        <div className={`p-1.5 ${colors.icon} rounded`}>
          <Icon className="size-4" />
        </div>
        <div>
          <div className="font-medium text-sm">{data.label}</div>
          {data.description && (
            <div className="text-xs opacity-80">{data.description}</div>
          )}
        </div>
      </div>

      {/* Output handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        className={`!w-3 !h-3 !bg-white !${colors.border}`}
      />
    </div>
  )
})

ActionNode.displayName = 'ActionNode'
