import { memo } from 'react'
import { Handle, Position, NodeProps } from 'reactflow'
import { RiQuestionLine } from '@remixicon/react'

interface ConditionNodeData {
  label: string
  description?: string
  condition?: string
}

export const ConditionNode = memo(({ data, selected }: NodeProps<ConditionNodeData>) => {
  return (
    <div
      className={`px-4 py-3 rounded-lg bg-amber-500 text-white min-w-[180px] shadow-lg ${
        selected ? 'ring-2 ring-amber-300 ring-offset-2' : ''
      }`}
    >
      {/* Input handle */}
      <Handle
        type="target"
        position={Position.Top}
        className="!w-3 !h-3 !bg-white !border-amber-600"
      />

      <div className="flex items-center gap-2">
        <div className="p-1.5 bg-amber-400 rounded">
          <RiQuestionLine className="size-4" />
        </div>
        <div>
          <div className="font-medium text-sm">{data.label}</div>
          {data.description && (
            <div className="text-xs text-amber-100">{data.description}</div>
          )}
        </div>
      </div>

      {/* Yes output handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="yes"
        className="!w-3 !h-3 !bg-green-400 !border-2 !border-green-600 !left-1/4"
        style={{ left: '30%' }}
      />

      {/* No output handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="no"
        className="!w-3 !h-3 !bg-red-400 !border-2 !border-red-600"
        style={{ left: '70%' }}
      />

      {/* Labels for handles */}
      <div className="flex justify-between text-[10px] mt-2 px-2">
        <span className="text-green-200">Да</span>
        <span className="text-red-200">Нет</span>
      </div>
    </div>
  )
})

ConditionNode.displayName = 'ConditionNode'
