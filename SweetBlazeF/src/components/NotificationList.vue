<template>
  <ion-card v-for="(notification, index) in notifications" :key="index">
    <ion-card-header>
      <ion-card-title>Notificación</ion-card-title>
    </ion-card-header>
    <ion-card-content>
      {{ notification.message }}
    </ion-card-content>
  </ion-card>
</template>

<script setup>
import { useWebSocket } from '../composables/useWebSocket.js'

const { notifications } = useWebSocket()

function isImage(url) {
  return /\.(jpg|jpeg|png|gif)$/i.test(url)
}
</script>

<style scoped>
ion-card {
  margin-bottom: 16px;
}
</style>