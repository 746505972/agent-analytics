<template>
  <div class="chat-container">
    <h1>LLM聊天分析</h1>
    <div class="chat-box">
      <div class="messages">
        <div class="message received">
          您好！我是您的数据分析助手，请告诉我您需要什么分析？
        </div>
      </div>
      <div class="input-area">
        <input 
          type="text" 
          placeholder="输入您的分析需求..." 
          v-model="userInput"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">发送</button>
      </div>
    </div>
    <div class="nav-links">
      <router-link to="/upload">上传文件</router-link> |
      <router-link to="/dashboard">返回首页</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Chat",
  data() {
    return {
      userInput: ""
    }
  },
  methods: {
    sendMessage() {
      if (this.userInput.trim() !== "") {
        // 这里应该调用后端API处理用户消息
        console.log("发送消息:", this.userInput)
        this.userInput = ""
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.chat-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 20px 0;
  height: 500px;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 4px;
}

.received {
  background-color: #f5f5f5;
  max-width: 80%;
}

.input-area {
  display: flex;
  padding: 20px;
  border-top: 1px solid #ddd;
}

.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.input-area button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.nav-links {
  text-align: center;
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