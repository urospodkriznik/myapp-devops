<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-6" elevation="2">
          <v-card-title class="text-h4 mb-4">
            <v-icon icon="mdi-home" class="mr-3" />
            Welcome to MyApp
          </v-card-title>
          
          <v-card-text class="text-body-1">
            <p class="mb-4">
              Hello <strong>{{ auth.user?.name }}</strong>! Welcome to your dashboard.
            </p>
            
            <p class="text-medium-emphasis">
              This is a full-stack application demonstrating modern DevOps practices, 
              security hardening, and monitoring capabilities.
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-package-variant" class="mr-2" />
            Items Management
          </v-card-title>
          
          <v-card-text>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Manage your inventory items with full CRUD operations.
            </p>
            
            <v-btn 
              color="primary" 
              to="/items"
              prepend-icon="mdi-arrow-right"
            >
              Go to Items
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-account-group" class="mr-2" />
            User Management
          </v-card-title>
          
          <v-card-text>
            <p class="text-body-2 text-medium-emphasis mb-3">
              Manage users and their permissions (Admin only).
            </p>
            
            <v-btn 
              color="primary" 
              to="/users"
              prepend-icon="mdi-arrow-right"
            >
              Go to Users
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-information" class="mr-2" />
            Application Features
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <div class="text-center pa-4">
                  <v-icon icon="mdi-shield-check" size="48" color="success" class="mb-2" />
                  <h3 class="text-h6 mb-2">Security</h3>
                  <p class="text-body-2 text-medium-emphasis">
                    JWT authentication, role-based access control, security headers, and HTTPS enforcement.
                  </p>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="text-center pa-4">
                  <v-icon icon="mdi-chart-line" size="48" color="info" class="mb-2" />
                  <h3 class="text-h6 mb-2">Monitoring</h3>
                  <p class="text-body-2 text-medium-emphasis">
                    Structured logging, Prometheus metrics, Grafana dashboards, and health checks.
                  </p>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="text-center pa-4">
                  <v-icon icon="mdi-docker" size="48" color="primary" class="mb-2" />
                  <h3 class="text-h6 mb-2">DevOps</h3>
                  <p class="text-body-2 text-medium-emphasis">
                    Docker containerization, CI/CD pipelines, environment management, and automated deployments.
                  </p>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script> 