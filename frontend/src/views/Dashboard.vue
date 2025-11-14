<template>
  <div class="dashboard">
    <h1>仪表板</h1>
    <p>欢迎来到 Agent-Analytics 系统</p>
    <div class="nav-links">
      <router-link to="/upload">上传文件</router-link> |
      <router-link to="/chat">聊天分析</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard"
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  text-align: center;
}

.nav-links {
  margin-top: 20px;
}

.nav-links a {
  margin: 0 10px;
  text-decoration: none;
  color: #409eff;
}

.nav-links a:hover {
  text-decoration: underline;
}
</style>