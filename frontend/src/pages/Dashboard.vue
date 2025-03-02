<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Dashboard</h1>
        <p>Resumen general del Torneo de Futbolín.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
// Puedes usar tu store para cargar datos globales o algo similar
// import { useSomeStore } from '@/store/someStore';

onMounted(() => {
  // Lógica para cargar datos o estadíficas
});
</script>
