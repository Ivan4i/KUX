export interface DeviceStatus {
  id: string
  name: string
  location: string
  current_status: 'online' | 'offline' | 'busy'
  battery_level: number
  temperature: number
  signal_strength: number
  last_heartbeat: string | null
  active_task_id: number | null
  tasks_completed_today: number
}

export interface Device {
  id: string
  name: string
  location: string
  timezone: string
  tailscale_ip: string
  adb_port: number
  active_hours: string
  max_tasks_per_day: number
}
