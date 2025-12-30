import { useState } from 'react'
import { RiWhatsappLine, RiInstagramLine, RiLinkedinLine, RiTelegramLine, RiSaveLine, RiPlayFill, RiSettingsLine, RiCodeLine } from '@remixicon/react'
import toast from 'react-hot-toast'
import { Button } from '@/components/common/Button'
import type { AgentType } from '@/types/scenario'
import { AGENT_ACTIONS } from '@/types/scenario'

interface AgentConfig {
  type: AgentType
  name: string
  icon: React.ReactNode
  color: string
  bgColor: string
  description: string
  status: 'active' | 'inactive' | 'coming_soon'
  prompts: {
    key: string
    label: string
    description: string
    value: string
    placeholder: string
  }[]
  settings: {
    key: string
    label: string
    type: 'number' | 'boolean' | 'string' | 'select'
    value: any
    options?: { value: string; label: string }[]
    description?: string
  }[]
}

const DEFAULT_AGENTS: AgentConfig[] = [
  {
    type: 'whatsapp',
    name: 'WhatsApp',
    icon: <RiWhatsappLine className="w-8 h-8" />,
    color: 'text-green-500',
    bgColor: 'bg-green-100',
    description: 'Отправка сообщений WhatsApp с человеческим поведением',
    status: 'active',
    prompts: [
      {
        key: 'screen_analysis',
        label: 'Промпт анализа экрана',
        description: 'Промпт для анализа экранов WhatsApp',
        value: `Analyze this WhatsApp screenshot and identify:
1. Current screen type (home, chat, search, etc.)
2. Visible UI elements and their positions
3. Any error messages or dialogs
4. Suggested next action

Return JSON with screen_type, elements[], errors[], and suggested_action.`,
        placeholder: 'Введите промпт анализа экрана...',
      },
      {
        key: 'message_personalization',
        label: 'Промпт персонализации сообщений',
        description: 'Промпт для персонализации сообщений',
        value: `You are a friendly person sending a WhatsApp message.
Personalize the following message template for the recipient.
Keep it natural, casual, and appropriate for WhatsApp.

Recipient: {{recipient_name}}
Template: {{message_template}}
Context: {{context}}

Return ONLY the personalized message, nothing else.`,
        placeholder: 'Введите промпт персонализации...',
      },
      {
        key: 'element_location',
        label: 'Промпт поиска элементов',
        description: 'Промпт для поиска элементов интерфейса',
        value: `Find the UI element: "{{element_description}}"

Return JSON with:
{
  "found": true/false,
  "x": center_x_coordinate,
  "y": center_y_coordinate,
  "confidence": 0-100
}`,
        placeholder: 'Введите промпт поиска элементов...',
      },
    ],
    settings: [
      { key: 'max_retries', label: 'Макс. повторов', type: 'number', value: 3, description: 'Максимальное количество попыток на действие' },
      { key: 'typing_speed', label: 'Скорость набора', type: 'select', value: 'normal', options: [
        { value: 'slow', label: 'Медленно (как человек)' },
        { value: 'normal', label: 'Нормально' },
        { value: 'fast', label: 'Быстро' },
      ]},
      { key: 'add_typos', label: 'Добавлять опечатки', type: 'boolean', value: false, description: 'Добавлять и исправлять опечатки для реалистичности' },
      { key: 'warmup_enabled', label: 'Включить прогрев', type: 'boolean', value: true, description: 'Выполнять прогревающие действия перед задачами' },
      { key: 'warmup_duration', label: 'Длительность прогрева (сек)', type: 'number', value: 60 },
    ],
  },
  {
    type: 'instagram',
    name: 'Instagram',
    icon: <RiInstagramLine className="w-8 h-8" />,
    color: 'text-pink-500',
    bgColor: 'bg-pink-100',
    description: 'Автоматизация Instagram сообщений и взаимодействий',
    status: 'coming_soon',
    prompts: [],
    settings: [],
  },
  {
    type: 'linkedin',
    name: 'LinkedIn',
    icon: <RiLinkedinLine className="w-8 h-8" />,
    color: 'text-primary-600',
    bgColor: 'bg-blue-100',
    description: 'Отправка сообщений LinkedIn и запросов на подключение',
    status: 'coming_soon',
    prompts: [],
    settings: [],
  },
  {
    type: 'telegram',
    name: 'Telegram',
    icon: <RiTelegramLine className="w-8 h-8" />,
    color: 'text-blue-400',
    bgColor: 'bg-blue-50',
    description: 'Автоматизация сообщений Telegram',
    status: 'coming_soon',
    prompts: [],
    settings: [],
  },
]

export function AgentsPage() {
  const [agents, setAgents] = useState<AgentConfig[]>(DEFAULT_AGENTS)
  const [selectedAgent, setSelectedAgent] = useState<AgentType | null>(null)
  const [activeTab, setActiveTab] = useState<'prompts' | 'settings' | 'actions'>('prompts')
  const [isLoading, setIsLoading] = useState(false)
  const [hasChanges, setHasChanges] = useState(false)

  const currentAgent = agents.find(a => a.type === selectedAgent)

  const handleAgentSelect = (type: AgentType) => {
    if (hasChanges) {
      if (!window.confirm('У вас есть несохранённые изменения. Отменить их?')) return
    }
    setSelectedAgent(type)
    setHasChanges(false)
  }

  const handlePromptChange = (key: string, value: string) => {
    if (!selectedAgent) return

    setAgents(prev => prev.map(agent => {
      if (agent.type !== selectedAgent) return agent
      return {
        ...agent,
        prompts: agent.prompts.map(p => p.key === key ? { ...p, value } : p),
      }
    }))
    setHasChanges(true)
  }

  const handleSettingChange = (key: string, value: any) => {
    if (!selectedAgent) return

    setAgents(prev => prev.map(agent => {
      if (agent.type !== selectedAgent) return agent
      return {
        ...agent,
        settings: agent.settings.map(s => s.key === key ? { ...s, value } : s),
      }
    }))
    setHasChanges(true)
  }

  const handleSave = async () => {
    setIsLoading(true)
    try {
      // TODO: Save to backend
      await new Promise(resolve => setTimeout(resolve, 500))
      toast.success('Настройки агента сохранены!')
      setHasChanges(false)
    } catch (error) {
      toast.error('Не удалось сохранить настройки')
    } finally {
      setIsLoading(false)
    }
  }

  const handleTestPrompt = async (promptKey: string) => {
    toast.success(`Тестирование промпта: ${promptKey}`)
    // TODO: Implement prompt testing
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Агенты</h1>
              <p className="mt-1 text-sm text-gray-500">
                Настройка ИИ агентов и их промптов
              </p>
            </div>

            {selectedAgent && hasChanges && (
              <Button
                variant="primary"
                leftIcon={<RiSaveLine />}
                onClick={handleSave}
                isLoading={isLoading}
              >
                Сохранить
              </Button>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Agent Selector */}
          <div className="col-span-3">
            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-200">
                <h2 className="text-sm font-semibold text-gray-900">Доступные агенты</h2>
              </div>
              <div className="divide-y divide-gray-100">
                {agents.map((agent) => (
                  <button
                    key={agent.type}
                    onClick={() => handleAgentSelect(agent.type)}
                    disabled={agent.status === 'coming_soon'}
                    className={`
                      w-full px-4 py-3 flex items-center gap-3 text-left transition-colors
                      ${selectedAgent === agent.type ? 'bg-blue-50 border-l-4 border-l-blue-500' : 'hover:bg-gray-50'}
                      ${agent.status === 'coming_soon' ? 'opacity-50 cursor-not-allowed' : ''}
                    `}
                  >
                    <div className={`p-2 rounded-lg ${agent.bgColor} ${agent.color}`}>
                      {agent.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-gray-900">{agent.name}</span>
                        {agent.status === 'active' && (
                          <span className="w-2 h-2 rounded-full bg-green-500" />
                        )}
                        {agent.status === 'coming_soon' && (
                          <span className="text-xs text-gray-400">Скоро</span>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 truncate">{agent.description}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Agent Configuration */}
          <div className="col-span-9">
            {!selectedAgent ? (
              <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                  <RiSettingsLine className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Выберите агента</h3>
                <p className="text-sm text-gray-500">
                  Выберите агента из боковой панели для настройки его промптов и параметров.
                </p>
              </div>
            ) : currentAgent ? (
              <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                {/* Agent Header */}
                <div className="px-6 py-4 border-b border-gray-200 flex items-center gap-4">
                  <div className={`p-3 rounded-lg ${currentAgent.bgColor} ${currentAgent.color}`}>
                    {currentAgent.icon}
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">Агент {currentAgent.name}</h2>
                    <p className="text-sm text-gray-500">{currentAgent.description}</p>
                  </div>
                </div>

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="flex px-6">
                    {[
                      { key: 'prompts', label: 'Промпты', icon: <RiCodeLine className="w-4 h-4" /> },
                      { key: 'settings', label: 'Настройки', icon: <RiSettingsLine className="w-4 h-4" /> },
                      { key: 'actions', label: 'Доступные действия', icon: <RiPlayFill className="w-4 h-4" /> },
                    ].map((tab) => (
                      <button
                        key={tab.key}
                        onClick={() => setActiveTab(tab.key as any)}
                        className={`
                          flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 -mb-px transition-colors
                          ${activeTab === tab.key
                            ? 'border-primary-500 text-primary-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                          }
                        `}
                      >
                        {tab.icon}
                        {tab.label}
                      </button>
                    ))}
                  </nav>
                </div>

                {/* Content */}
                <div className="p-6">
                  {/* Prompts Tab */}
                  {activeTab === 'prompts' && (
                    <div className="space-y-6">
                      {currentAgent.prompts.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                          Промпты для этого агента пока не настроены.
                        </div>
                      ) : (
                        currentAgent.prompts.map((prompt) => (
                          <div key={prompt.key} className="border border-gray-200 rounded-lg overflow-hidden">
                            <div className="bg-gray-50 px-4 py-3 flex items-center justify-between">
                              <div>
                                <h4 className="text-sm font-medium text-gray-900">{prompt.label}</h4>
                                <p className="text-xs text-gray-500">{prompt.description}</p>
                              </div>
                              <Button
                                variant="ghost"
                                size="sm"
                                leftIcon={<RiPlayFill className="w-3 h-3" />}
                                onClick={() => handleTestPrompt(prompt.key)}
                              >
                                Тест
                              </Button>
                            </div>
                            <textarea
                              value={prompt.value}
                              onChange={(e) => handlePromptChange(prompt.key, e.target.value)}
                              placeholder={prompt.placeholder}
                              rows={8}
                              className="w-full px-4 py-3 font-mono text-sm border-0 focus:ring-0 resize-y"
                            />
                          </div>
                        ))
                      )}
                    </div>
                  )}

                  {/* Settings Tab */}
                  {activeTab === 'settings' && (
                    <div className="space-y-6">
                      {currentAgent.settings.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                          Настройки для этого агента пока недоступны.
                        </div>
                      ) : (
                        currentAgent.settings.map((setting) => (
                          <div key={setting.key} className="flex items-start gap-4">
                            <div className="flex-1">
                              <label className="block text-sm font-medium text-gray-900">
                                {setting.label}
                              </label>
                              {setting.description && (
                                <p className="text-xs text-gray-500 mt-0.5">{setting.description}</p>
                              )}
                            </div>
                            <div className="w-48">
                              {setting.type === 'boolean' ? (
                                <label className="flex items-center">
                                  <input
                                    type="checkbox"
                                    checked={setting.value}
                                    onChange={(e) => handleSettingChange(setting.key, e.target.checked)}
                                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                                  />
                                  <span className="ml-2 text-sm text-gray-600">
                                    {setting.value ? 'Включено' : 'Выключено'}
                                  </span>
                                </label>
                              ) : setting.type === 'select' ? (
                                <select
                                  value={setting.value}
                                  onChange={(e) => handleSettingChange(setting.key, e.target.value)}
                                  className="w-full text-sm border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
                                >
                                  {setting.options?.map((opt) => (
                                    <option key={opt.value} value={opt.value}>
                                      {opt.label}
                                    </option>
                                  ))}
                                </select>
                              ) : setting.type === 'number' ? (
                                <input
                                  type="number"
                                  value={setting.value}
                                  onChange={(e) => handleSettingChange(setting.key, Number(e.target.value))}
                                  className="w-full text-sm border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
                                />
                              ) : (
                                <input
                                  type="text"
                                  value={setting.value}
                                  onChange={(e) => handleSettingChange(setting.key, e.target.value)}
                                  className="w-full text-sm border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
                                />
                              )}
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  )}

                  {/* Actions Tab */}
                  {activeTab === 'actions' && (
                    <div className="space-y-4">
                      {AGENT_ACTIONS[currentAgent.type]?.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                          Действия для этого агента пока недоступны.
                        </div>
                      ) : (
                        <div className="grid grid-cols-2 gap-4">
                          {AGENT_ACTIONS[currentAgent.type]?.map((action) => (
                            <div
                              key={action.action}
                              className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors"
                            >
                              <h4 className="text-sm font-medium text-gray-900">{action.label}</h4>
                              <p className="text-xs text-gray-500 mt-1">{action.description}</p>
                              <div className="mt-2">
                                <code className="text-xs bg-gray-100 px-2 py-1 rounded font-mono">
                                  {action.action}
                                </code>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  )
}
