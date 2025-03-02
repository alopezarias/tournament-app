<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Equipos</h2>
        <v-btn color="primary" @click="createTeam">Crear Nuevo Equipo</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="team in teams" :key="team.id" cols="12" sm="6" md="4">
        <v-card class="ma-3">
          <v-card-title>{{ team.name }}</v-card-title>
          <v-card-text>
            <p>Miembros: {{ team.members?.length || 0 }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router';

interface Team {
  id: number;
  name: string;
  members?: any[];
}

const teams = ref<Team[]>([]);
const router = useRouter();

onMounted(async () => {
  await loadTeams();
});

async function loadTeams() {
  try {
    teams.value = await api.get('teams').json<Team[]>();
  } catch (error) {
    console.error('Error cargando equipos:', error);
  }
}

async function createTeam() {
  try {
    const newTeam = await api
        .post('teams', { json: { name: 'Equipo de prueba', image: '' } })
        .json<Team>();
    console.log('Equipo creado:', newTeam);
    // Recargar lista
    await loadTeams();
  } catch (error) {
    console.error('Error creando equipo:', error);
  }
}
</script>
