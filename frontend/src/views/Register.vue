<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-6" elevation="3">
          <v-card-title class="text-center text-h5 mb-4">
            <v-icon icon="mdi-account-plus" class="mr-2" />
            Create Account
          </v-card-title>
          
          <v-form @submit.prevent="submit" v-model="isValid">
            <v-text-field
              v-model="name"
              label="Full Name"
              :rules="nameRules"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              required
              :disabled="auth.loading"
            />
            
            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              :rules="emailRules"
              prepend-inner-icon="mdi-email"
              variant="outlined"
              required
              :disabled="auth.loading"
            />
            
            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              :rules="passwordRules"
              prepend-inner-icon="mdi-lock"
              variant="outlined"
              required
              :disabled="auth.loading"
              @keyup.enter="submit"
            />
            
            <v-text-field
              v-model="confirmPassword"
              label="Confirm Password"
              type="password"
              :rules="confirmPasswordRules"
              prepend-inner-icon="mdi-lock-check"
              variant="outlined"
              required
              :disabled="auth.loading"
              @keyup.enter="submit"
            />
            
            <v-btn
              type="submit"
              color="primary"
              size="large"
              block
              :loading="auth.loading"
              :disabled="!isValid || auth.loading"
              class="mt-4"
            >
              <v-icon icon="mdi-account-plus" class="mr-2" />
              {{ auth.loading ? 'Creating Account...' : 'Create Account' }}
            </v-btn>
          </v-form>
          
          <v-divider class="my-4" />
          
          <div class="text-center">
            <p class="text-body-2 text-medium-emphasis mb-2">
              Already have an account?
            </p>
            <v-btn
              variant="text"
              color="primary"
              to="/login"
              :disabled="auth.loading"
            >
              Sign In
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const isValid = ref(false)
const auth = useAuthStore()
const router = useRouter()

const nameRules = [
  (v: string) => !!v || 'Name is required',
  (v: string) => v.length >= 2 || 'Name must be at least 2 characters',
]

const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid',
]

const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 6 || 'Password must be at least 6 characters',
]

const confirmPasswordRules = [
  (v: string) => !!v || 'Please confirm your password',
  (v: string) => v === password.value || 'Passwords do not match',
]

const submit = async () => {
  if (!isValid.value) return
  
  const success = await auth.register(name.value, email.value, password.value)
  if (success) {
    router.push('/login')
  }
}
</script>