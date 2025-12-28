export interface Log {
  id: number
  device_id: string
  task_id: number | null
  action_type: string
  status: 'success' | 'warning' | 'failed'
  details: string
  screenshot_path: string | null
  created_at: string
}

export interface LogsSummary {
  time_range_hours: number
  total_logs: number
  success_count: number
  warning_count: number
  failed_count: number
  success_rate: number
  action_counts: Record<string, number>
  device_id: string | null
}
