<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="pa-4">
          <v-card-title class="text-h5">Perfil de {{ profile?.username }}</v-card-title>
          <v-card-text>
            <p><strong>Email:</strong> {{ profile?.email }}</p>
            <p><strong>ID:</strong> {{ profile?.id }}</p>
            <p><strong>Equipo:</strong> {{ profile?.team?.name || 'Sin equipo' }}</p>
            <!-- Más datos si el backend lo soporta -->
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api';

interface Team {
  id: number;
  name: string;
}

interface Profile {
  id: number;
  email: string;
  username: string;
  team?: Team;
}

const profile = ref<Profile | null>(null);

onMounted(async () => {
  await loadProfile();
});

async function loadProfile() {
  try {
    profile.value = await api.get('profile').json<Profile>();
  } catch (error) {
    console.error('Error cargando perfil:', error);
  }
}
</script>
