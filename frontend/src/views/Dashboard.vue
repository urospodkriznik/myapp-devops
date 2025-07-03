<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>Users by Role</v-card-title>
          <v-card-text>
            <v-chart :option="barOption" autoresize style="height:300px;" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="4">
        <v-card>
          <v-card-title>Items by Category</v-card-title>
          <v-card-text>
            <v-chart :option="pieOption" autoresize style="height:300px;" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="12" lg="4">
        <v-card>
          <v-card-title>Items Added Over Time</v-card-title>
          <v-card-text>
            <v-chart :option="lineOption" autoresize style="height:300px;" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="mt-8">
      <v-col cols="12">
        <v-card>
          <v-card-title>Top Cryptocurrencies (CoinGecko)</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="coins"
              :items-per-page="100"
              :items-per-page-options="[]"
              class="elevation-1"
              density="comfortable"
              hide-default-footer
              ref="tableRef"
            >
              <template #item.name="{ item }">
                <v-avatar size="20" class="mr-2" style="vertical-align: middle;">
                  <img :src="item.image" :alt="item.name" style="width: 20px; height: 20px; object-fit: contain;" />
                </v-avatar>
                <span style="vertical-align: middle;">{{ item.name }}</span>
              </template>
              <template #item.current_price="{ item }">
                {{ formatPrice(item.current_price) }}
              </template>
              <template #item.price_change_percentage_24h="{ item }">
                <span :class="item.price_change_percentage_24h >= 0 ? 'text-success' : 'text-error'">
                  {{ item.price_change_percentage_24h.toFixed(2) }}%
                </span>
              </template>
              <template #item.market_cap="{ item }">
                {{ formatBigNumber(item.market_cap) }}
              </template>
              <template #item.fully_diluted_valuation="{ item }">
                {{ formatBigNumber(item.fully_diluted_valuation) }}
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const barOption = ref({
  //title: { text: 'Users by Role' },
  tooltip: {},
  xAxis: { data: ['Admin', 'User'] },
  yAxis: {},
  series: [
    {
      name: 'Users',
      type: 'bar',
      data: [5, 42],
      itemStyle: { color: '#1976d2' }
    }
  ]
})

const pieOption = ref({
  //title: { text: 'Items by Category', left: 'center' },
  tooltip: { trigger: 'item' },
  legend: { orient: 'vertical', left: 'left' },
  series: [
    {
      name: 'Items',
      type: 'pie',
      radius: '60%',
      data: [
        { value: 10, name: 'Electronics' },
        { value: 15, name: 'Books' },
        { value: 8, name: 'Clothing' }
      ],
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
      }
    }
  ]
})

const lineOption = ref({
  //title: { text: 'Items Added Over Time' },
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May'] },
  yAxis: { type: 'value' },
  series: [
    {
      name: 'Items',
      type: 'line',
      data: [2, 5, 8, 6, 10],
      smooth: true,
      lineStyle: { color: '#43a047' },
      areaStyle: { color: 'rgba(67, 160, 71, 0.2)' }
    }
  ]
})

const coins = ref([])
const page = ref(1)
const itemsPerPage = 100
const totalCoins = 1000
const loading = ref(false)
const tableRef = ref(null)
const headers = [
  { title: 'Name', value: 'name' },
  { title: 'Symbol', value: 'symbol' },
  { title: 'Price (USD)', value: 'current_price', align: 'end' },
  { title: 'Market Cap (USD)', value: 'market_cap', align: 'end' },
  { title: 'FDV (USD)', value: 'fully_diluted_valuation', align: 'end' },
  { title: '24h Change', value: 'price_change_percentage_24h', align: 'end' },
]

async function fetchCoins(pageNum = 1) {
  if (loading.value) return
  loading.value = true
  const { data } = await axios.get('https://api.coingecko.com/api/v3/coins/markets', {
    params: {
      vs_currency: 'usd',
      order: 'market_cap_desc',
      per_page: itemsPerPage,
      page: pageNum,
      sparkline: false
    },
    withCredentials: false
  })
  coins.value = coins.value.concat(data)
  loading.value = false
}

function handleScroll() {
  const tableEl = tableRef.value?.$el || tableRef.value
  if (!tableEl) return
  const scrollContainer = tableEl.querySelector('.v-table__wrapper') || tableEl
  if (!scrollContainer) return
  const { scrollTop, scrollHeight, clientHeight } = scrollContainer
  if (scrollTop + clientHeight >= scrollHeight - 100 && !loading.value && coins.value.length < totalCoins) {
    page.value += 1
    fetchCoins(page.value)
  }
}

onMounted(async () => {
  await fetchCoins(page.value)
  await nextTick()
  const tableEl = tableRef.value?.$el || tableRef.value
  const scrollContainer = tableEl.querySelector('.v-table__wrapper') || tableEl
  if (scrollContainer) {
    scrollContainer.addEventListener('scroll', handleScroll)
  }
})

function formatBigNumber(num) {
  if (num === null || num === undefined) return '-';
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
  return num.toString();
}

function formatPrice(num) {
  if (num === null || num === undefined) return '-';
  return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
</script> 