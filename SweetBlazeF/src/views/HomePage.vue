<template>
  <IonPage>
    <IonContent class="ion-padding">
      <form @submit.prevent="sendNotification">
        <IonItem>
          <IonLabel position="stacked">Título</IonLabel>
          <IonInput v-model="form.title" required />
        </IonItem>

        <IonItem>
          <IonLabel position="stacked">Mensaje</IonLabel>
          <IonInput v-model="form.message" required />
        </IonItem>

        <IonItem>
          <IonLabel position="stacked">Tipo</IonLabel>
          <IonInput v-model="form.type" required />
        </IonItem>

        <IonItem>
          <IonLabel position="stacked">Archivo</IonLabel>
          <input type="file" @change="handleFile" />
        </IonItem>

        <IonButton expand="block" type="submit" class="ion-margin-top">
          Enviar Notificación
        </IonButton>
      </form>

      <!-- Lista de Notificaciones Recibidas -->
      <div class="notifications-section ion-margin-top">
        <h2>Notificaciones Recientes</h2>
        <IonList>
          <IonItem v-for="notification in notifications" :key="notification.id">
            <div class="notification-item">
              <h3>{{ notification.title }}</h3>
              <p>{{ notification.message }}</p>
              <small>Tipo: {{ notification.type }}</small>
              <a v-if="notification.file_url" :href="notification.file_url" target="_blank">Ver archivo</a>
            </div>
          </IonItem>
        </IonList>
      </div>
    </IonContent>
  </IonPage>
</template>

<style scoped>
.notifications-section {
  margin-top: 2rem;
}

.notification-item {
  padding: 1rem 0;
}

.notification-item h3 {
  margin: 0;
  color: var(--ion-color-primary);
  font-size: 1.1rem;
}

.notification-item p {
  margin: 0.5rem 0;
  color: var(--ion-color-dark);
}

.notification-item small {
  color: var(--ion-color-medium);
  display: block;
  margin-top: 0.25rem;
}

.notification-item a {
  display: inline-block;
  margin-top: 0.5rem;
  color: var(--ion-color-primary);
  text-decoration: none;
}
</style>

<script setup>
import { ref, onMounted } from 'vue';
import { IonPage, IonContent, IonItem, IonLabel, IonInput, IonButton, IonList } from '@ionic/vue';
import axios from 'axios';
import { useWebSocket } from '../composables/useWebSocket';

// Inicializar WebSocket y obtener notifications
const { notifications, socket } = useWebSocket();

const form = ref({
  title: '',
  message: '',
  type: '',
  file: ''
});

// Monitorear estado del WebSocket
onMounted(() => {
  if (socket) {
    socket.onopen = () => {
      console.log('✅ WebSocket conectado en HomePage');
    };
    
    socket.onerror = (error) => {
      console.error('❌ Error de WebSocket en HomePage:', error);
    };
  }
});


const selectedFile = ref(null);

const handleFile = (event) => {
  selectedFile.value = event.target.files[0];
};

const sendNotification = async () => {
  const formData = new FormData();
  formData.append('title', form.value.title);
  formData.append('message', form.value.message);
  formData.append('type', form.value.type);

  if (selectedFile.value) {
    formData.append('file', selectedFile.value);
  }

  try {
    // No necesitamos establecer el Content-Type, axios lo hace automáticamente para FormData
    // API REST en puerto 8000 (Django)
    const response = await axios.post(
      'http://127.0.0.1:8000/api/notifications/',
      formData
    );
    console.log('Notificación enviada:', response.data);
    // Limpiar el formulario después de enviar
    form.value = {
      title: '',
      message: '',
      type: '',
      file: ''
    };
    selectedFile.value = null;
  } catch (error) {
    console.error('Error al enviar la notificación:', error.response ? error.response.data : error.message);
    alert('Error al enviar la notificación. Por favor, revisa la consola para más detalles.');
  }
};

</script>