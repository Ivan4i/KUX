export interface WebSocketMessage {
  type: string
  timestamp: string
  [key: string]: any
}

export interface DeviceStatusUpdateMessage extends WebSocketMessage {
  type: 'device_status_update'
  device_id: string
  data: any
}

export interface TaskStartedMessage extends WebSocketMessage {
  type: 'task_started'
  task_id: number
  data: any
}

export interface TaskProgressMessage extends WebSocketMessage {
  type: 'task_progress'
  task_id: number
  message: string
  progress_percent: number | null
}

export interface TaskCompletedMessage extends WebSocketMessage {
  type: 'task_completed'
  task_id: number
  data: any
}

export interface TaskFailedMessage extends WebSocketMessage {
  type: 'task_failed'
  task_id: number
  error: string
  data: any
}

export interface LogEntryMessage extends WebSocketMessage {
  type: 'log_entry'
  data: any
}

export interface NotificationMessage extends WebSocketMessage {
  type: 'notification'
  level: 'info' | 'warning' | 'error' | 'success'
  message: string
  data: any
}
