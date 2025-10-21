import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "notifications_group"

    async def connect(self):
        print("⌛ Intentando conexión WebSocket...")
        try:
            # Primero aceptar la conexión
            await self.accept()
            print("✅ Conexión WebSocket aceptada")

            # Luego unirse al grupo
            await self.channel_layer.group_add(
                self.GROUP_NAME,
                self.channel_name
            )
            print(f"✅ Cliente añadido al grupo {self.GROUP_NAME}")

            # Enviar mensaje de confirmación al cliente
            await self.send(text_data=json.dumps({
                "type": "connection_established",
                "message": "Conectado al servidor de notificaciones"
            }))
        except Exception as e:
            print(f"❌ Error en connect: {str(e)}")
            raise

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.GROUP_NAME,
                self.channel_name
            )
            print(f"❌ Cliente desconectado del grupo {self.GROUP_NAME}")
        except Exception as e:
            print(f"❌ Error en disconnect: {str(e)}")

    async def receive(self, text_data):
        print(f"📥 Mensaje recibido: {text_data}")
        try:
            data = json.loads(text_data)
            print(f"📦 Datos procesados: {data}")
        except Exception as e:
            print(f"❌ Error al procesar mensaje recibido: {str(e)}")

    async def send_notification(self, event):
        print(f"📤 Preparando envío de notificación: {event}")
        try:
            # El mensaje completo que llegó del channel layer
            message = event.get('message', {})
            print(f"📦 Contenido del mensaje: {message}")

            # Enviamos el mensaje al cliente WebSocket
            await self.send(text_data=json.dumps({
                "type": "notification",
                "data": message
            }))
            print("✅ Notificación enviada al cliente")
        except Exception as e:
            print(f"❌ Error al enviar notificación: {str(e)}")
