import { useEffect, useCallback } from 'react'
import { wsService } from '@/services/websocket'
import type { WebSocketMessage } from '@/types/websocket'

type MessageHandler = (message: WebSocketMessage) => void

export function useWebSocket() {
  useEffect(() => {
    // Connect on mount
    wsService.connect()

    // Disconnect on unmount
    return () => {
      wsService.disconnect()
    }
  }, [])

  const subscribe = useCallback((handler: MessageHandler) => {
    return wsService.subscribe(handler)
  }, [])

  const send = useCallback((message: any) => {
    wsService.send(message)
  }, [])

  const isConnected = useCallback(() => {
    return wsService.isConnected()
  }, [])

  return {
    subscribe,
    send,
    isConnected,
  }
}

// Specialized hook for specific message types
export function useWebSocketMessages<T extends WebSocketMessage>(
  messageType: string,
  handler: (message: T) => void
) {
  const { subscribe } = useWebSocket()

  useEffect(() => {
    const unsubscribe = subscribe((message: WebSocketMessage) => {
      if (message.type === messageType) {
        handler(message as T)
      }
    })

    return unsubscribe
  }, [subscribe, messageType, handler])
}
