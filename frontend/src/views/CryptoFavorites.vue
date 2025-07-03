<template>
  <v-container class="py-4" fluid>
    <v-row dense>
      <v-col cols="12" v-for="symbol in symbols" :key="symbol">
        <v-card elevation="1" class="pa-2">
          <v-card-title class="text-subtitle-2 py-1 px-2">{{ symbol }}</v-card-title>
          <div :id="'tv_chart_' + symbol" style="height:400px;"></div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

const symbols = ['BTC.D', 'ETHBTC', 'SOLBTC', 'SOLETH']

onMounted(() => {
  const script = document.createElement('script')
  script.src = 'https://s3.tradingview.com/tv.js'
  script.async = true
  script.onload = () => {
    symbols.forEach((s) => {
      new window.TradingView.widget({
        container_id: `tv_chart_${s}`,
        autosize: true,
        symbol: s,
        interval: "W",
        theme: "light",
        style: "1",
        locale: "en",
        toolbar_bg: "#f1f3f6",
        enable_publishing: false,
        allow_symbol_change: false,
        hide_top_toolbar: true,
        hide_legend: false,
        studies: ["RSI@tv-basicstudies"], // built-in RSI
      })
    })
  }
  document.body.appendChild(script)
})
</script>