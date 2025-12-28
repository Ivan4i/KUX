import axios from 'axios'
import type { DeviceStatus } from '@/types/device'
import type { Task } from '@/types/task'
import type { Log, LogsSummary } from '@/types/log'
import type {
  Scenario,
  ScenarioListItem,
  ScenarioStep,
  CreateScenarioRequest,
  UpdateScenarioRequest,
  CreateStepRequest,
  UpdateStepRequest,
  RunScenarioRequest,
} from '@/types/scenario'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Health check
export const healthCheck = async () => {
  const response = await api.get('/api/health')
  return response.data
}

// Devices API
export const getDevices = async (): Promise<DeviceStatus[]> => {
  const response = await api.get('/api/devices')
  return response.data
}

export const getDeviceStatus = async (deviceId: string): Promise<DeviceStatus> => {
  const response = await api.get(`/api/devices/${deviceId}/status`)
  return response.data
}

export const refreshDeviceStatus = async (deviceId: string): Promise<DeviceStatus> => {
  const response = await api.post(`/api/devices/${deviceId}/refresh`)
  return response.data
}

export const rebootDevice = async (deviceId: string) => {
  const response = await api.post(`/api/devices/${deviceId}/reboot`)
  return response.data
}

export const takeDeviceScreenshot = async (deviceId: string) => {
  const response = await api.get(`/api/devices/${deviceId}/screenshot`)
  return response.data
}

export const launchScrcpy = async (deviceId: string) => {
  const response = await api.post(`/api/devices/${deviceId}/scrcpy`)
  return response.data
}

// Tasks API
export const syncNotionTasks = async (limit: number = 10) => {
  const response = await api.post(`/api/tasks/sync-notion?limit=${limit}`)
  return response.data
}

export const runTask = async (taskId?: number) => {
  const url = taskId ? `/api/tasks/run?task_id=${taskId}` : '/api/tasks/run'
  const response = await api.post(url)
  return response.data
}

export const getTasks = async (
  status?: string,
  deviceId?: string,
  limit: number = 50
): Promise<Task[]> => {
  const params = new URLSearchParams()
  if (status) params.append('status', status)
  if (deviceId) params.append('device_id', deviceId)
  params.append('limit', limit.toString())

  const response = await api.get(`/api/tasks?${params.toString()}`)
  return response.data
}

export const getTask = async (taskId: number): Promise<Task> => {
  const response = await api.get(`/api/tasks/${taskId}`)
  return response.data
}

export const deleteTask = async (taskId: number) => {
  const response = await api.delete(`/api/tasks/${taskId}`)
  return response.data
}

// Logs API
export const getLogs = async (
  filters: {
    deviceId?: string
    taskId?: number
    status?: string
    actionType?: string
    hours?: number
    limit?: number
  } = {}
): Promise<Log[]> => {
  const params = new URLSearchParams()
  if (filters.deviceId) params.append('device_id', filters.deviceId)
  if (filters.taskId) params.append('task_id', filters.taskId.toString())
  if (filters.status) params.append('status', filters.status)
  if (filters.actionType) params.append('action_type', filters.actionType)
  if (filters.hours) params.append('hours', filters.hours.toString())
  if (filters.limit) params.append('limit', filters.limit.toString())

  const response = await api.get(`/api/logs?${params.toString()}`)
  return response.data
}

export const getLog = async (logId: number): Promise<Log> => {
  const response = await api.get(`/api/logs/${logId}`)
  return response.data
}

export const getLogsSummary = async (
  deviceId?: string,
  hours: number = 24
): Promise<LogsSummary> => {
  const params = new URLSearchParams()
  if (deviceId) params.append('device_id', deviceId)
  params.append('hours', hours.toString())

  const response = await api.get(`/api/logs/stats/summary?${params.toString()}`)
  return response.data
}

export const cleanupOldLogs = async (days: number = 30) => {
  const response = await api.delete(`/api/logs/cleanup?days=${days}`)
  return response.data
}

// ============================================================================
// Scenarios API
// ============================================================================

export const getScenarios = async (
  filters: {
    status?: string
    is_template?: boolean
    limit?: number
    offset?: number
  } = {}
): Promise<{ scenarios: ScenarioListItem[]; total: number }> => {
  const params = new URLSearchParams()
  if (filters.status) params.append('status', filters.status)
  if (filters.is_template !== undefined) params.append('is_template', filters.is_template.toString())
  if (filters.limit) params.append('limit', filters.limit.toString())
  if (filters.offset) params.append('offset', filters.offset.toString())

  const response = await api.get(`/api/scenarios?${params.toString()}`)
  return response.data
}

export const getScenario = async (scenarioId: string): Promise<Scenario> => {
  const response = await api.get(`/api/scenarios/${scenarioId}`)
  return response.data
}

export const createScenario = async (data: CreateScenarioRequest): Promise<Scenario> => {
  const response = await api.post('/api/scenarios', data)
  return response.data
}

export const updateScenario = async (scenarioId: string, data: UpdateScenarioRequest): Promise<Scenario> => {
  const response = await api.put(`/api/scenarios/${scenarioId}`, data)
  return response.data
}

export const deleteScenario = async (scenarioId: string): Promise<void> => {
  await api.delete(`/api/scenarios/${scenarioId}`)
}

export const duplicateScenario = async (scenarioId: string, newName?: string): Promise<Scenario> => {
  const params = newName ? `?new_name=${encodeURIComponent(newName)}` : ''
  const response = await api.post(`/api/scenarios/${scenarioId}/duplicate${params}`)
  return response.data
}

// Scenario execution
export const runScenario = async (scenarioId: string, data?: RunScenarioRequest): Promise<{ message: string; scenario_id: string }> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/run`, data || {})
  return response.data
}

export const pauseScenario = async (scenarioId: string): Promise<{ message: string }> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/pause`)
  return response.data
}

export const resumeScenario = async (scenarioId: string): Promise<{ message: string }> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/resume`)
  return response.data
}

export const cancelScenario = async (scenarioId: string): Promise<{ message: string }> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/cancel`)
  return response.data
}

// Scenario steps
export const addScenarioStep = async (scenarioId: string, data: CreateStepRequest): Promise<ScenarioStep> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/steps`, data)
  return response.data
}

export const updateScenarioStep = async (
  scenarioId: string,
  stepId: string,
  data: UpdateStepRequest
): Promise<ScenarioStep> => {
  const response = await api.put(`/api/scenarios/${scenarioId}/steps/${stepId}`, data)
  return response.data
}

export const deleteScenarioStep = async (scenarioId: string, stepId: string): Promise<void> => {
  await api.delete(`/api/scenarios/${scenarioId}/steps/${stepId}`)
}

export const reorderScenarioSteps = async (scenarioId: string, stepIds: string[]): Promise<{ message: string }> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/steps/reorder`, { step_ids: stepIds })
  return response.data
}

// Scheduler
export const scheduleScenario = async (
  scenarioId: string,
  data: { cron_expression?: string; scheduled_at?: string }
): Promise<{ message: string }> => {
  const response = await api.post(`/api/scenarios/${scenarioId}/schedule`, data)
  return response.data
}

export const unscheduleScenario = async (scenarioId: string): Promise<{ message: string }> => {
  const response = await api.delete(`/api/scenarios/${scenarioId}/schedule`)
  return response.data
}

// Queue status
export const getQueueStatus = async (): Promise<{
  queue_size: number
  processing_count: number
  items: Array<{ id: string; type: string; priority: number; status: string }>
}> => {
  const response = await api.get('/api/scenarios/queue/status')
  return response.data
}

export const getSchedulerStatus = async (): Promise<{
  running: boolean
  active_jobs: number
  jobs: Array<{ id: string; type: string; next_run: string; cron?: string }>
}> => {
  const response = await api.get('/api/scenarios/scheduler/status')
  return response.data
}

// ============================================================================
// Settings API
// ============================================================================

export interface IntegrationSettings {
  notion_api_key: string | null
  notion_database_id: string | null
  telegram_bot_token: string | null
  telegram_chat_id: string | null
  puter_api_key: string | null
  puter_api_url: string | null
  puter_default_model: string | null
}

export interface BehaviorSettings {
  min_typing_delay_ms: number
  max_typing_delay_ms: number
  min_action_delay_ms: number
  max_action_delay_ms: number
  typo_probability: number
  typo_fix_probability: number
  max_messages_per_hour: number
  max_messages_per_day: number
  cooldown_after_batch_min: number
}

export interface AppSettings {
  app_env: string
  app_debug: boolean
  log_level: string
}

export interface AllSettings {
  integrations: IntegrationSettings
  behavior: BehaviorSettings
  app: AppSettings
}

export interface ConfigStatus {
  integrations: {
    notion: { configured: boolean; api_key: boolean; database_id: boolean }
    telegram: { configured: boolean; bot_token: boolean; chat_id: boolean }
    puter: { configured: boolean; api_key: boolean }
  }
  env_file_exists: boolean
}

export const getSettings = async (): Promise<AllSettings> => {
  const response = await api.get('/api/settings')
  return response.data
}

export const getConfigStatus = async (): Promise<ConfigStatus> => {
  const response = await api.get('/api/settings/status')
  return response.data
}

export const updateIntegrationSettings = async (settings: Partial<IntegrationSettings>): Promise<{ success: boolean; message: string; updated: string[] }> => {
  const response = await api.put('/api/settings/integrations', settings)
  return response.data
}

export const updateBehaviorSettings = async (settings: BehaviorSettings): Promise<{ success: boolean; message: string }> => {
  const response = await api.put('/api/settings/behavior', settings)
  return response.data
}

export const updateAppSettings = async (settings: AppSettings): Promise<{ success: boolean; message: string }> => {
  const response = await api.put('/api/settings/app', settings)
  return response.data
}

export const testNotionConnection = async (): Promise<{ success: boolean; message: string; database_title?: string }> => {
  const response = await api.post('/api/settings/test/notion')
  return response.data
}

export const testTelegramConnection = async (): Promise<{ success: boolean; message: string }> => {
  const response = await api.post('/api/settings/test/telegram')
  return response.data
}

export default api
