import { memo } from 'react'
import { Handle, Position, NodeProps } from 'reactflow'
import { RiNotionFill, RiTimeLine, RiWebhookLine } from '@remixicon/react'

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  notion: RiNotionFill,
  schedule: RiTimeLine,
  webhook: RiWebhookLine,
}

interface TriggerNodeData {
  label: string
  description?: string
  icon?: string
}

export const TriggerNode = memo(({ data, selected }: NodeProps<TriggerNodeData>) => {
  const Icon = data.icon ? iconMap[data.icon] || RiTimeLine : RiTimeLine

  return (
    <div
      className={`px-4 py-3 rounded-lg bg-purple-500 text-white min-w-[180px] shadow-lg ${
        selected ? 'ring-2 ring-purple-300 ring-offset-2' : ''
      }`}
    >
      <div className="flex items-center gap-2">
        <div className="p-1.5 bg-purple-400 rounded">
          <Icon className="size-4" />
        </div>
        <div>
          <div className="font-medium text-sm">{data.label}</div>
          {data.description && (
            <div className="text-xs text-purple-200">{data.description}</div>
          )}
        </div>
      </div>

      {/* Output handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        className="!w-3 !h-3 !bg-purple-300 !border-2 !border-purple-600"
      />
    </div>
  )
})

TriggerNode.displayName = 'TriggerNode'
