<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <button @click="fetchData">获取数据</button>
    <p v-if="data">{{ data }}</p>
  </div>
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
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/data');
        const result = await response.json();
        this.data = result;
      } catch (error) {
        console.error('请求出错:', error);
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>