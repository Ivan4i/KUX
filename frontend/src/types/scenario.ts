// Scenario types for KUX frontend

export type ScenarioStatus =
  | 'draft'
  | 'pending'
  | 'running'
  | 'paused'
  | 'completed'
  | 'failed'
  | 'cancelled'

export type StepStatus =
  | 'pending'
  | 'running'
  | 'completed'
  | 'failed'
  | 'skipped'

export type AgentType =
  | 'whatsapp'
  | 'instagram'
  | 'linkedin'
  | 'telegram'

export interface ScenarioStep {
  id: string
  scenario_id: string
  order_index: number
  name: string
  agent_type: AgentType
  action: string
  parameters: Record<string, any>
  condition?: string
  delay_before_seconds: number
  timeout_seconds: number
  max_retries: number
  status: StepStatus
  result?: Record<string, any>
  error_message?: string
  started_at?: string
  completed_at?: string
  created_at: string
}

export interface Scenario {
  id: string
  name: string
  description?: string
  status: ScenarioStatus
  is_template: boolean
  cron_expression?: string
  scheduled_at?: string
  current_step_index: number
  total_steps: number
  started_at?: string
  completed_at?: string
  result?: Record<string, any>
  error_message?: string
  created_by?: string
  created_at: string
  updated_at: string
  steps: ScenarioStep[]
}

export interface ScenarioListItem {
  id: string
  name: string
  description?: string
  status: ScenarioStatus
  is_template: boolean
  cron_expression?: string
  total_steps: number
  created_at: string
  updated_at: string
}

export interface CreateScenarioRequest {
  name: string
  description?: string
  is_template?: boolean
  cron_expression?: string
  scheduled_at?: string
}

export interface UpdateScenarioRequest {
  name?: string
  description?: string
  is_template?: boolean
  cron_expression?: string
  scheduled_at?: string
}

export interface CreateStepRequest {
  name: string
  agent_type: AgentType
  action: string
  parameters?: Record<string, any>
  condition?: string
  delay_before_seconds?: number
  timeout_seconds?: number
  max_retries?: number
}

export interface UpdateStepRequest {
  name?: string
  agent_type?: AgentType
  action?: string
  parameters?: Record<string, any>
  condition?: string
  delay_before_seconds?: number
  timeout_seconds?: number
  max_retries?: number
  order_index?: number
}

export interface RunScenarioRequest {
  device_id?: string
  skip_to_step?: number
  dry_run?: boolean
}

export interface ScenarioProgress {
  scenario_id: string
  status: ScenarioStatus
  current_step: number
  total_steps: number
  current_step_name?: string
  progress_percent: number
  message?: string
}

// Available actions per agent type
export const AGENT_ACTIONS: Record<AgentType, { action: string; label: string; description: string }[]> = {
  whatsapp: [
    { action: 'send_message', label: 'Send Message', description: 'Send WhatsApp message to a phone number' },
    { action: 'warmup', label: 'Warmup', description: 'Simulate natural app usage before main task' },
    { action: 'send_batch_messages', label: 'Batch Messages', description: 'Send messages to multiple recipients' },
    { action: 'check_delivery', label: 'Check Delivery', description: 'Check if a message was delivered' },
  ],
  instagram: [
    { action: 'send_dm', label: 'Send DM', description: 'Send direct message' },
    { action: 'follow_user', label: 'Follow User', description: 'Follow an Instagram user' },
    { action: 'like_post', label: 'Like Post', description: 'Like a post' },
  ],
  linkedin: [
    { action: 'send_message', label: 'Send Message', description: 'Send LinkedIn message' },
    { action: 'connect', label: 'Connect', description: 'Send connection request' },
    { action: 'view_profile', label: 'View Profile', description: 'View a LinkedIn profile' },
  ],
  telegram: [
    { action: 'send_message', label: 'Send Message', description: 'Send Telegram message' },
    { action: 'join_group', label: 'Join Group', description: 'Join a Telegram group' },
  ],
}

// Status colors and labels
export const STATUS_CONFIG: Record<ScenarioStatus, { color: string; bgColor: string; label: string }> = {
  draft: { color: 'text-gray-600', bgColor: 'bg-gray-100', label: 'Draft' },
  pending: { color: 'text-yellow-600', bgColor: 'bg-yellow-100', label: 'Pending' },
  running: { color: 'text-blue-600', bgColor: 'bg-blue-100', label: 'Running' },
  paused: { color: 'text-orange-600', bgColor: 'bg-orange-100', label: 'Paused' },
  completed: { color: 'text-green-600', bgColor: 'bg-green-100', label: 'Completed' },
  failed: { color: 'text-red-600', bgColor: 'bg-red-100', label: 'Failed' },
  cancelled: { color: 'text-gray-600', bgColor: 'bg-gray-100', label: 'Cancelled' },
}

export const STEP_STATUS_CONFIG: Record<StepStatus, { color: string; bgColor: string; label: string }> = {
  pending: { color: 'text-gray-600', bgColor: 'bg-gray-100', label: 'Pending' },
  running: { color: 'text-blue-600', bgColor: 'bg-blue-100', label: 'Running' },
  completed: { color: 'text-green-600', bgColor: 'bg-green-100', label: 'Completed' },
  failed: { color: 'text-red-600', bgColor: 'bg-red-100', label: 'Failed' },
  skipped: { color: 'text-gray-500', bgColor: 'bg-gray-50', label: 'Skipped' },
}
