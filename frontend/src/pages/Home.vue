<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-h5 text-center">Bienvenido al Torneo de Futbolín</v-card-title>
          <v-card-text>
            <p>
              Esta aplicación te permite gestionar jugadores, equipos y partidos de futbolín, ¡todo en un mismo lugar!
            </p>
            <v-btn color="primary" @click="goLogin">Iniciar sesión</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const goLogin = () => {
  router.push('/login');
};
</script>
