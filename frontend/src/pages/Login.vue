<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-center text-h5">
            Inicio de Sesión
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                  v-model="email"
                  label="Email"
                  type="email"
                  required
              ></v-text-field>
              <v-text-field
                  v-model="password"
                  label="Contraseña"
                  type="password"
                  required
              ></v-text-field>
              <v-btn
                  type="submit"
                  color="primary"
                  block
                  :loading="loading"
              >
                Iniciar Sesión
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  try {
    await authStore.login({ email: email.value, password: password.value });
    router.push('/dashboard');
  } catch (error) {
    console.error('Error en el login:', error);
  } finally {
    loading.value = false;
  }
};
</script>
