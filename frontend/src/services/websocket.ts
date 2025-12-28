import type { WebSocketMessage } from '@/types/websocket'

type MessageHandler = (message: WebSocketMessage) => void

class WebSocketService {
  private ws: WebSocket | null = null
  private url: string
  private reconnectInterval: number = 5000
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private messageHandlers: Set<MessageHandler> = new Set()
  private isIntentionallyClosed: boolean = false

  constructor() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = import.meta.env.VITE_WS_URL || 'localhost:8000'
    this.url = `${protocol}//${host}/ws`
  }

  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    this.isIntentionallyClosed = false
    console.log('Connecting to WebSocket:', this.url)

    try {
      this.ws = new WebSocket(this.url)

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected')
        if (this.reconnectTimer) {
          clearTimeout(this.reconnectTimer)
          this.reconnectTimer = null
        }
      }

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          console.log('📨 WebSocket message:', message.type)

          // Notify all handlers
          this.messageHandlers.forEach((handler) => handler(message))
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        this.ws = null

        // Reconnect if not intentionally closed
        if (!this.isIntentionallyClosed) {
          console.log(`Reconnecting in ${this.reconnectInterval / 1000}s...`)
          this.reconnectTimer = setTimeout(() => {
            this.connect()
          }, this.reconnectInterval)
        }
      }
    } catch (error) {
      console.error('Error creating WebSocket:', error)
    }
  }

  disconnect() {
    this.isIntentionallyClosed = true

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }

    if (this.ws) {
      this.ws.close()
      this.ws = null
    }

    console.log('WebSocket disconnected')
  }

  subscribe(handler: MessageHandler): () => void {
    this.messageHandlers.add(handler)

    // Return unsubscribe function
    return () => {
      this.messageHandlers.delete(handler)
    }
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected, cannot send message')
    }
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }
}

// Global WebSocket instance
export const wsService = new WebSocketService()
