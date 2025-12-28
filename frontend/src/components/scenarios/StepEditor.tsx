import { useState, useEffect } from 'react'
import { FaTimes, FaWhatsapp, FaInstagram, FaLinkedin, FaTelegram } from 'react-icons/fa'
import { Button } from '@/components/common/Button'
import type { ScenarioStep, AgentType, CreateStepRequest, UpdateStepRequest } from '@/types/scenario'
import { AGENT_ACTIONS } from '@/types/scenario'

interface StepEditorProps {
  isOpen: boolean
  onClose: () => void
  onSave: (data: CreateStepRequest | UpdateStepRequest) => Promise<void>
  step?: ScenarioStep | null
  isLoading?: boolean
}

const AGENT_OPTIONS: { type: AgentType; label: string; icon: React.ReactNode }[] = [
  { type: 'whatsapp', label: 'WhatsApp', icon: <FaWhatsapp className="w-5 h-5 text-green-500" /> },
  { type: 'instagram', label: 'Instagram', icon: <FaInstagram className="w-5 h-5 text-pink-500" /> },
  { type: 'linkedin', label: 'LinkedIn', icon: <FaLinkedin className="w-5 h-5 text-primary-600" /> },
  { type: 'telegram', label: 'Telegram', icon: <FaTelegram className="w-5 h-5 text-blue-400" /> },
]

// Parameter definitions for each action
const ACTION_PARAMETERS: Record<string, { key: string; label: string; type: 'string' | 'number' | 'boolean' | 'json'; required?: boolean; placeholder?: string }[]> = {
  // WhatsApp
  'whatsapp:send_message': [
    { key: 'recipient', label: 'Phone Number', type: 'string', required: true, placeholder: '+66812345678' },
    { key: 'message', label: 'Message', type: 'string', required: true, placeholder: 'Hello!' },
    { key: 'recipient_name', label: 'Recipient Name', type: 'string', placeholder: 'John Doe' },
    { key: 'personalize', label: 'Personalize with AI', type: 'boolean' },
    { key: 'use_typos', label: 'Add Realistic Typos', type: 'boolean' },
  ],
  'whatsapp:warmup': [
    { key: 'duration_seconds', label: 'Duration (seconds)', type: 'number', placeholder: '60' },
  ],
  'whatsapp:send_batch_messages': [
    { key: 'recipients', label: 'Recipients (JSON)', type: 'json', required: true, placeholder: '[{"phone": "+66...", "name": "John", "message": "Hi!"}]' },
    { key: 'delay_between', label: 'Delay Between (seconds)', type: 'number', placeholder: '30' },
  ],
  'whatsapp:check_delivery': [
    { key: 'recipient', label: 'Phone Number', type: 'string', required: true, placeholder: '+66812345678' },
  ],
  // Instagram
  'instagram:send_dm': [
    { key: 'username', label: 'Username', type: 'string', required: true, placeholder: '@username' },
    { key: 'message', label: 'Message', type: 'string', required: true },
  ],
  'instagram:follow_user': [
    { key: 'username', label: 'Username', type: 'string', required: true, placeholder: '@username' },
  ],
  'instagram:like_post': [
    { key: 'post_url', label: 'Post URL', type: 'string', required: true },
  ],
  // LinkedIn
  'linkedin:send_message': [
    { key: 'profile_url', label: 'Profile URL', type: 'string', required: true },
    { key: 'message', label: 'Message', type: 'string', required: true },
  ],
  'linkedin:connect': [
    { key: 'profile_url', label: 'Profile URL', type: 'string', required: true },
    { key: 'note', label: 'Connection Note', type: 'string' },
  ],
  'linkedin:view_profile': [
    { key: 'profile_url', label: 'Profile URL', type: 'string', required: true },
  ],
  // Telegram
  'telegram:send_message': [
    { key: 'chat_id', label: 'Chat ID / Username', type: 'string', required: true },
    { key: 'message', label: 'Message', type: 'string', required: true },
  ],
  'telegram:join_group': [
    { key: 'group_link', label: 'Group Link', type: 'string', required: true },
  ],
}

export function StepEditor({ isOpen, onClose, onSave, step, isLoading = false }: StepEditorProps) {
  const [name, setName] = useState('')
  const [agentType, setAgentType] = useState<AgentType>('whatsapp')
  const [action, setAction] = useState('')
  const [parameters, setParameters] = useState<Record<string, any>>({})
  const [delayBefore, setDelayBefore] = useState(0)
  const [timeout, setTimeout] = useState(300)
  const [maxRetries, setMaxRetries] = useState(3)
  const [condition, setCondition] = useState('')

  const isEditing = !!step

  // Initialize form when step changes
  useEffect(() => {
    if (step) {
      setName(step.name)
      setAgentType(step.agent_type)
      setAction(step.action)
      setParameters(step.parameters || {})
      setDelayBefore(step.delay_before_seconds)
      setTimeout(step.timeout_seconds)
      setMaxRetries(step.max_retries)
      setCondition(step.condition || '')
    } else {
      // Reset form for new step
      setName('')
      setAgentType('whatsapp')
      setAction('')
      setParameters({})
      setDelayBefore(0)
      setTimeout(300)
      setMaxRetries(3)
      setCondition('')
    }
  }, [step, isOpen])

  // Get available actions for selected agent
  const availableActions = AGENT_ACTIONS[agentType] || []

  // Get parameters for selected action
  const actionKey = `${agentType}:${action}`
  const parameterDefs = ACTION_PARAMETERS[actionKey] || []

  const handleAgentChange = (newAgent: AgentType) => {
    setAgentType(newAgent)
    setAction('')
    setParameters({})
  }

  const handleActionChange = (newAction: string) => {
    setAction(newAction)
    setParameters({})
  }

  const handleParameterChange = (key: string, value: any, type: string) => {
    let parsedValue = value

    if (type === 'number') {
      parsedValue = value === '' ? undefined : Number(value)
    } else if (type === 'boolean') {
      parsedValue = value === true || value === 'true'
    } else if (type === 'json') {
      try {
        parsedValue = JSON.parse(value)
      } catch {
        parsedValue = value // Keep as string if invalid JSON
      }
    }

    setParameters(prev => ({
      ...prev,
      [key]: parsedValue,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const data = {
      name: name || `${agentType} - ${action}`,
      agent_type: agentType,
      action,
      parameters,
      delay_before_seconds: delayBefore,
      timeout_seconds: timeout,
      max_retries: maxRetries,
      condition: condition || undefined,
    }

    await onSave(data)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black bg-opacity-50" onClick={onClose} />

      {/* Modal */}
      <div className="relative min-h-screen flex items-center justify-center p-4">
        <div className="relative bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              {isEditing ? 'Edit Step' : 'Add New Step'}
            </h2>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
            >
              <FaTimes className="w-5 h-5" />
            </button>
          </div>

          {/* Content */}
          <form onSubmit={handleSubmit} className="overflow-y-auto max-h-[calc(90vh-140px)]">
            <div className="px-6 py-4 space-y-6">
              {/* Step Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Step Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g., Send welcome message"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>

              {/* Agent Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Agent
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {AGENT_OPTIONS.map((agent) => (
                    <button
                      key={agent.type}
                      type="button"
                      onClick={() => handleAgentChange(agent.type)}
                      className={`
                        flex flex-col items-center gap-1 p-3 rounded-lg border-2 transition-all
                        ${agentType === agent.type
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-gray-300'
                        }
                      `}
                    >
                      {agent.icon}
                      <span className="text-xs font-medium">{agent.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Action */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Action
                </label>
                <select
                  value={action}
                  onChange={(e) => handleActionChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  required
                >
                  <option value="">Select an action...</option>
                  {availableActions.map((act) => (
                    <option key={act.action} value={act.action}>
                      {act.label} - {act.description}
                    </option>
                  ))}
                </select>
              </div>

              {/* Parameters */}
              {action && parameterDefs.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Parameters
                  </label>
                  <div className="space-y-3 p-4 bg-gray-50 rounded-lg">
                    {parameterDefs.map((param) => (
                      <div key={param.key}>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                          {param.label}
                          {param.required && <span className="text-red-500 ml-1">*</span>}
                        </label>

                        {param.type === 'boolean' ? (
                          <label className="flex items-center gap-2">
                            <input
                              type="checkbox"
                              checked={parameters[param.key] === true}
                              onChange={(e) => handleParameterChange(param.key, e.target.checked, param.type)}
                              className="w-4 h-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                            />
                            <span className="text-sm text-gray-600">Enable</span>
                          </label>
                        ) : param.type === 'json' ? (
                          <textarea
                            value={typeof parameters[param.key] === 'object' ? JSON.stringify(parameters[param.key], null, 2) : parameters[param.key] || ''}
                            onChange={(e) => handleParameterChange(param.key, e.target.value, param.type)}
                            placeholder={param.placeholder}
                            rows={4}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            required={param.required}
                          />
                        ) : param.type === 'number' ? (
                          <input
                            type="number"
                            value={parameters[param.key] ?? ''}
                            onChange={(e) => handleParameterChange(param.key, e.target.value, param.type)}
                            placeholder={param.placeholder}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            required={param.required}
                          />
                        ) : param.key === 'message' ? (
                          <textarea
                            value={parameters[param.key] || ''}
                            onChange={(e) => handleParameterChange(param.key, e.target.value, param.type)}
                            placeholder={param.placeholder}
                            rows={3}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            required={param.required}
                          />
                        ) : (
                          <input
                            type="text"
                            value={parameters[param.key] || ''}
                            onChange={(e) => handleParameterChange(param.key, e.target.value, param.type)}
                            placeholder={param.placeholder}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                            required={param.required}
                          />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Advanced Settings */}
              <details className="group">
                <summary className="flex items-center gap-2 cursor-pointer text-sm font-medium text-gray-700">
                  <span>Advanced Settings</span>
                  <span className="text-gray-400 group-open:rotate-90 transition-transform">▶</span>
                </summary>

                <div className="mt-4 space-y-4 p-4 bg-gray-50 rounded-lg">
                  {/* Delay Before */}
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Delay Before (seconds)
                    </label>
                    <input
                      type="number"
                      value={delayBefore}
                      onChange={(e) => setDelayBefore(Number(e.target.value))}
                      min={0}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <p className="mt-1 text-xs text-gray-500">Wait before executing this step</p>
                  </div>

                  {/* Timeout */}
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Timeout (seconds)
                    </label>
                    <input
                      type="number"
                      value={timeout}
                      onChange={(e) => setTimeout(Number(e.target.value))}
                      min={30}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>

                  {/* Max Retries */}
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Max Retries
                    </label>
                    <input
                      type="number"
                      value={maxRetries}
                      onChange={(e) => setMaxRetries(Number(e.target.value))}
                      min={0}
                      max={10}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>

                  {/* Condition */}
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Condition (optional)
                    </label>
                    <input
                      type="text"
                      value={condition}
                      onChange={(e) => setCondition(e.target.value)}
                      placeholder="e.g., previous_step.success == true"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <p className="mt-1 text-xs text-gray-500">
                      Python expression to evaluate. Step runs only if condition is true.
                    </p>
                  </div>
                </div>
              </details>
            </div>

            {/* Footer */}
            <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50">
              <Button variant="secondary" onClick={onClose} disabled={isLoading}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={isLoading} disabled={!action}>
                {isEditing ? 'Save Changes' : 'Add Step'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
