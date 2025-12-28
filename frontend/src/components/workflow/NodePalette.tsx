import {
  RiNotionFill,
  RiTimeLine,
  RiWhatsappLine,
  RiMessage2Line,
  RiRobotLine,
  RiTelegramLine,
  RiSparklingLine,
  RiQuestionLine
} from '@remixicon/react'

interface PaletteItem {
  type: string
  label: string
  description: string
  icon: React.ComponentType<{ className?: string }>
  data: Record<string, any>
  color: string
}

const triggers: PaletteItem[] = [
  {
    type: 'trigger',
    label: 'Notion Trigger',
    description: 'Fetch leads from Notion',
    icon: RiNotionFill,
    data: { label: 'Fetch from Notion', description: 'Get pending leads', icon: 'notion' },
    color: 'bg-purple-500',
  },
  {
    type: 'trigger',
    label: 'Schedule',
    description: 'Run on schedule',
    icon: RiTimeLine,
    data: { label: 'Scheduled Run', description: 'CRON trigger', icon: 'schedule' },
    color: 'bg-purple-500',
  },
]

const actions: PaletteItem[] = [
  {
    type: 'action',
    label: 'Gemini AI',
    description: 'Analyze with LLM',
    icon: RiSparklingLine,
    data: { label: 'Analyze Lead', description: 'Generate personalized message', icon: 'gemini', agent: 'gemini' },
    color: 'bg-indigo-500',
  },
  {
    type: 'action',
    label: 'WhatsApp',
    description: 'Send WhatsApp message',
    icon: RiWhatsappLine,
    data: { label: 'Send WhatsApp', description: 'Send via WhatsApp', icon: 'whatsapp', agent: 'whatsapp' },
    color: 'bg-green-500',
  },
  {
    type: 'action',
    label: 'SMS',
    description: 'Send SMS message',
    icon: RiMessage2Line,
    data: { label: 'Send SMS', description: 'Send via SMS', icon: 'sms', agent: 'sms' },
    color: 'bg-blue-500',
  },
  {
    type: 'action',
    label: 'MAX',
    description: 'Send MAX message',
    icon: RiRobotLine,
    data: { label: 'Send MAX', description: 'Send via MAX app', icon: 'max', agent: 'max' },
    color: 'bg-orange-500',
  },
  {
    type: 'action',
    label: 'Telegram',
    description: 'Send Telegram message',
    icon: RiTelegramLine,
    data: { label: 'Send Telegram', description: 'Send via Telegram', icon: 'telegram', agent: 'telegram' },
    color: 'bg-sky-500',
  },
]

const conditions: PaletteItem[] = [
  {
    type: 'condition',
    label: 'Condition',
    description: 'Branch based on condition',
    icon: RiQuestionLine,
    data: { label: 'Check Condition', description: 'If/else branch' },
    color: 'bg-amber-500',
  },
]

function DraggableNode({ item }: { item: PaletteItem }) {
  const onDragStart = (event: React.DragEvent) => {
    event.dataTransfer.setData('application/reactflow', item.type)
    event.dataTransfer.setData('application/nodedata', JSON.stringify(item.data))
    event.dataTransfer.effectAllowed = 'move'
  }

  return (
    <div
      draggable
      onDragStart={onDragStart}
      className={`flex items-center gap-2 p-2 ${item.color} text-white rounded-lg cursor-grab active:cursor-grabbing hover:opacity-90 transition-opacity`}
    >
      <item.icon className="size-4" />
      <div className="text-xs">
        <div className="font-medium">{item.label}</div>
      </div>
    </div>
  )
}

export function NodePalette() {
  return (
    <div className="w-56 bg-white border-r border-gray-200 p-4 overflow-y-auto">
      <h3 className="text-sm font-semibold text-gray-900 mb-4">Node Palette</h3>
      <p className="text-xs text-gray-500 mb-4">Drag nodes to the canvas</p>

      {/* Triggers */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wider">Triggers</h4>
        <div className="space-y-2">
          {triggers.map((item) => (
            <DraggableNode key={item.label} item={item} />
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wider">Actions</h4>
        <div className="space-y-2">
          {actions.map((item) => (
            <DraggableNode key={item.label} item={item} />
          ))}
        </div>
      </div>

      {/* Conditions */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wider">Logic</h4>
        <div className="space-y-2">
          {conditions.map((item) => (
            <DraggableNode key={item.label} item={item} />
          ))}
        </div>
      </div>
    </div>
  )
}
