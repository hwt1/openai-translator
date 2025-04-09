<template>
  <div id="app" v-if="!isFullPage">
    <h1>{{ message }}</h1>
    <el-button type="primary" @click="fetchData">获取数据</el-button>
    <el-button type="primary" @click="toPage">页面跳转</el-button>
    <p v-if="data">{{ data }}</p>
  </div>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      message: '欢迎使用 Flask + Vue 项目',
      data: null
    };
  },
  computed: {
    isFullPage() {
      return this.$route.meta.fullPage;
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/data');
        const result = await response.json();
        this.data = result;
      } catch (error) {
        console.error('请求出错:', error);
      }
    },
    toPage(){
      this.$router.push('/translate');
    }
  }
};
</script>