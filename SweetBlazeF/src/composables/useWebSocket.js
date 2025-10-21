import { ref } from 'vue'

export function useWebSocket() {
  const notifications = ref([])

  // WebSocket en puerto 8000 (Daphne ASGI)
  const socket = new WebSocket('ws://localhost:8000/ws/notifications/')

  socket.onopen = () => {
    console.log('✅ WebSocket conectado')
  }

  socket.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      console.log('📩 Mensaje WebSocket recibido:', message);

      // Si es un mensaje de notificación, procesarlo
      if (message.type === 'notification' && message.data) {
        console.log('📨 Nueva notificación:', message.data);
        notifications.value.unshift(message.data);
      } else {
        console.log('ℹ️ Otro tipo de mensaje:', message);
      }
    } catch (error) {
      console.error('❌ Error al procesar mensaje WebSocket:', error);
    }
  }

  socket.onerror = (error) => {
    console.error('❌ Error en WebSocket:', error)
  }

  socket.onclose = () => {
    console.log('🔌 WebSocket cerrado')
  }

  return {
    socket,
    notifications
  }
}