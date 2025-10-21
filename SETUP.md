# 🚀 Guía de Configuración - SweetBlaze

## Estructura del Proyecto

- **Backend**: Django + Daphne (ASGI) + Channels (WebSocket) en puerto **8000**
- **Frontend**: Vue 3 + Vite en puerto **5173**

---

## ⚙️ Instalación

### Backend
```powershell
cd SweetBlaze
pip install -r requirements.txt
python run_api.py
```

Esto iniciará el servidor Daphne en `http://localhost:8000` con soporte para:
- ✅ API REST HTTP
- ✅ WebSocket

### Frontend
```powershell
cd SweetBlazeF
npm install
npm run dev
```

Accede a `http://localhost:5173`

---

## 🔌 Flujo de Notificaciones

### 1️⃣ Frontend: Crear Notificación
```javascript
// Envío HTTP a la API REST
fetch('http://localhost:8000/api/notifications/', {
  method: 'POST',
  body: formData
})
```

### 2️⃣ Backend: Procesar y Transmitir
```python
# views.py: perform_create()
# - Guarda la notificación en BD ✅
# - Serializa los datos 📦
# - Envía a través del WebSocket 📡
channel_layer.group_send("notifications_group", {
  "type": "send_notification",
  "message": notification_data
})
```

### 3️⃣ Backend: Consumer WebSocket
```python
# consumers.py: send_notification()
# - Recibe el mensaje del canal
# - Envía al cliente conectado ✅
await self.send(text_data=json.dumps({
  "type": "notification",
  "data": message
}))
```

### 4️⃣ Frontend: Recibir en WebSocket
```javascript
// useWebSocket.js: socket.onmessage
// - Conecta a ws://localhost:8000/ws/notifications/
// - Recibe la notificación 📩
// - Actualiza la lista local ✅
notifications.value.unshift(message.data)
```

---

## 🐛 Troubleshooting

### El WebSocket no recibe mensajes
**Causa**: El servidor no está usando Daphne

**Solución**: Ejecuta `python run_api.py` (NO `python manage.py runserver`)

### Error de CORS
**Solución**: Verifica que `localhost:5173` esté en `CORS_ALLOWED_ORIGINS` en `settings.py`

### Daphne no arranca
**Solución**: 
```powershell
pip install daphne channels asgiref
python run_api.py
```

---

## 📊 Ports

| Servicio | Puerto | Protocolo |
|----------|--------|-----------|
| Frontend (Vite) | 5173 | HTTP |
| Backend (Daphne) | 8000 | HTTP + WebSocket |

---

## 📝 Logs Útiles

**Backend** (Daphne):
```
[INFO] WebSocket conectado
[INFO] Notificación guardada
[INFO] Mensaje enviado al grupo
```

**Frontend** (DevTools):
```
✅ WebSocket conectado
📩 Mensaje WebSocket recibido
📨 Nueva notificación
```
