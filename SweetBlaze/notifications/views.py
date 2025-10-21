from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Notification
from .serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

# Vista combinada para listar y crear notificaciones.
# - GET  /api/notifications/  -> lista
# - POST /api/notifications/  -> crea (acepta multipart/form-data)
class NotificationListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication required
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        logger.info(f"Recibida petición POST: {request.POST}")
        logger.info(f"FILES: {request.FILES}")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            notification = serializer.save()
            logger.info(f"💾 Notificación guardada: {notification}")

            # Preparar datos para WebSocket
            notification_data = NotificationSerializer(notification).data
            logger.info(f"📦 Datos serializados: {notification_data}")

            # Obtener channel layer y enviar
            channel_layer = get_channel_layer()
            if channel_layer is None:
                logger.error("❌ No se pudo obtener el channel layer")
                return

            logger.info("📡 Enviando a través del channel layer...")
            async_to_sync(channel_layer.group_send)(
                "notifications_group",  # Debe coincidir con GROUP_NAME en el consumer
                {
                    "type": "send_notification",
                    "message": notification_data,
                },
            )
            logger.info("✅ Mensaje enviado al grupo de WebSocket")
        except Exception as e:
            logger.error(f"❌ Error al procesar la notificación: {str(e)}")
