export interface Task {
  id: number
  notion_id: string | null
  recipient_name: string
  phone_number: string
  message_content: string
  status: 'Pending' | 'Running' | 'Sent' | 'Failed'
  device_id: string | null
  device_assignment: string
  priority: number
  created_date: string | null
  scheduled_send_time: string | null
  sent_date: string | null
  attempt_count: number
  notes: string
  created_at: string
  started_at: string | null
  completed_at: string | null
}

export interface TaskProgress {
  task_id: number
  message: string
  progress_percent: number | null
}
