<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Partidos</h2>
        <v-btn color="primary" @click="createMatch">Crear Partido</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="match in matches" :key="match.id" cols="12" sm="6" md="4">
        <v-card class="ma-3">
          <v-card-title>
            Partido #{{ match.id }}: {{ match.team_a.name }} vs {{ match.team_b.name }}
          </v-card-title>
          <v-card-text>
            <p>Estado: {{ match.status }}</p>
            <p>Hora de inicio: {{ match.start_time }}</p>
            <p v-if="match.end_time">Hora de fin: {{ match.end_time }}</p>
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

interface Match {
  id: number;
  team_a: Team;
  team_b: Team;
  start_time?: string;
  end_time?: string;
  status?: string;
}

const matches = ref<Match[]>([]);

onMounted(() => {
  loadMatches();
});

async function loadMatches() {
  try {
    matches.value = await api.get('matches').json<Match[]>();
  } catch (error) {
    console.error('Error cargando partidos:', error);
  }
}

async function createMatch() {
  try {
    // Ejemplo de creación de partido con IDs 1 y 2
    const newMatch = await api
        .post('matches', {
          json: {
            team_a_id: 1,
            team_b_id: 2,
            score_team_a: 0,
            score_team_b: 0,
            match_date: '2025-02-22T10:00:00Z',
            start_time: '2025-02-22T10:00:00Z'
          }
        })
        .json<Match>();
    console.log('Partido creado:', newMatch);
    await loadMatches();
  } catch (error) {
    console.error('Error creando partido:', error);
  }
}
</script>
