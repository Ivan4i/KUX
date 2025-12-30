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
    label: 'Notion триггер',
    description: 'Получить лиды из Notion',
    icon: RiNotionFill,
    data: { label: 'Загрузить из Notion', description: 'Получить ожидающие лиды', icon: 'notion' },
    color: 'bg-purple-500',
  },
  {
    type: 'trigger',
    label: 'Расписание',
    description: 'Запуск по расписанию',
    icon: RiTimeLine,
    data: { label: 'Запуск по расписанию', description: 'CRON триггер', icon: 'schedule' },
    color: 'bg-purple-500',
  },
]

const actions: PaletteItem[] = [
  {
    type: 'action',
    label: 'Gemini AI',
    description: 'Анализ через ИИ',
    icon: RiSparklingLine,
    data: { label: 'Анализ лида', description: 'Сгенерировать персональное сообщение', icon: 'gemini', agent: 'gemini' },
    color: 'bg-indigo-500',
  },
  {
    type: 'action',
    label: 'WhatsApp',
    description: 'Отправить сообщение WhatsApp',
    icon: RiWhatsappLine,
    data: { label: 'Отправить WhatsApp', description: 'Отправить через WhatsApp', icon: 'whatsapp', agent: 'whatsapp' },
    color: 'bg-green-500',
  },
  {
    type: 'action',
    label: 'SMS',
    description: 'Отправить SMS сообщение',
    icon: RiMessage2Line,
    data: { label: 'Отправить SMS', description: 'Отправить через SMS', icon: 'sms', agent: 'sms' },
    color: 'bg-blue-500',
  },
  {
    type: 'action',
    label: 'MAX',
    description: 'Отправить сообщение MAX',
    icon: RiRobotLine,
    data: { label: 'Отправить MAX', description: 'Отправить через MAX', icon: 'max', agent: 'max' },
    color: 'bg-orange-500',
  },
  {
    type: 'action',
    label: 'Telegram',
    description: 'Отправить сообщение Telegram',
    icon: RiTelegramLine,
    data: { label: 'Отправить Telegram', description: 'Отправить через Telegram', icon: 'telegram', agent: 'telegram' },
    color: 'bg-sky-500',
  },
]

const conditions: PaletteItem[] = [
  {
    type: 'condition',
    label: 'Условие',
    description: 'Ветвление по условию',
    icon: RiQuestionLine,
    data: { label: 'Проверка условия', description: 'Ветка если/иначе' },
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
      <h3 className="text-sm font-semibold text-gray-900 mb-4">Палитра узлов</h3>
      <p className="text-xs text-gray-500 mb-4">Перетащите узлы на холст</p>

      {/* Триггеры */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wider">Триггеры</h4>
        <div className="space-y-2">
          {triggers.map((item) => (
            <DraggableNode key={item.label} item={item} />
          ))}
        </div>
      </div>

      {/* Действия */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wider">Действия</h4>
        <div className="space-y-2">
          {actions.map((item) => (
            <DraggableNode key={item.label} item={item} />
          ))}
        </div>
      </div>

      {/* Логика */}
      <div className="mb-4">
        <h4 className="text-xs font-medium text-gray-600 mb-2 uppercase tracking-wider">Логика</h4>
        <div className="space-y-2">
          {conditions.map((item) => (
            <DraggableNode key={item.label} item={item} />
          ))}
        </div>
      </div>
    </div>
  )
}
