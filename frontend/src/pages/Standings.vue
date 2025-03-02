<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Clasificación</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-simple-table>
          <thead>
          <tr>
            <th>#</th>
            <th>Equipo</th>
            <th>Puntos</th>
            <th>Partidos Jugados</th>
          </tr>
          </thead>
          <tbody>
          <tr
              v-for="(standing, index) in standings"
              :key="standing.team_id"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ standing.team_name }}</td>
            <td>{{ standing.points }}</td>
            <td>{{ standing.matches_played }}</td>
          </tr>
          </tbody>
        </v-simple-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api';

interface Standing {
  team_id: number;
  team_name: string;
  points: number;
  matches_played: number;
}

const standings = ref<Standing[]>([]);

onMounted(() => {
  loadStandings();
});

async function loadStandings() {
  try {
    standings.value = await api.get('standings').json<Standing[]>();
  } catch (error) {
    console.error('Error cargando standings:', error);
  }
}
</script>
