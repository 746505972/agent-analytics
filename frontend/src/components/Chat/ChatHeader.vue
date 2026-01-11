<script>
import clickOutside from "@/utils/clickOutside";

export default {
  name: "ChatHeader",
  directives: {clickOutside},
  props: {
    isShowingHistory: {
      type: Boolean,
      default: false
    },
    baseUrl: {
      type: String,
      default: ''
    },
    model: {
      type: String,
      default: ''
    }
  },
  emits: ['update:isShowingHistory', 'createNewSession', 'update:baseUrl', 'update:model'],
  data() {
    return {
      isShowingSetting: false,
    }
  },
  methods: {
    toggleHistoryView() {
      this.$emit('update:isShowingHistory', !this.isShowingHistory)
    },
    createNewSession() {
      this.$emit('createNewSession')
    },
    toggleSetting(){
      this.isShowingSetting = !this.isShowingSetting
    },
    onUrlChange(e) {
      this.$emit('update:baseUrl', e.target.value)
      localStorage.setItem('baseUrl', e.target.value);
    },
    onModelChange(e) {
      this.$emit('update:model', e.target.value)
      localStorage.setItem('model', e.target.value);
    },
    close() {
      this.isShowingSetting = false;
    }
  },
}
</script>

<template>
  <div class="chat-header">
    <div class="header-left">
      <h2>数据分析助手</h2>
    </div>
    <div class="header-right">
      <!-- 历史记录按钮 -->
      <button @click="toggleHistoryView" class="btn" title="查看历史记录">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
          <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
        </svg>
      </button>
      <button @click="createNewSession" class="btn" title="新建会话">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
        </svg>
      </button>
      <button @click="toggleSetting" class="btn" title="设置">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 30 30">
          <path d="M26.6,12.9l-2.9-0.3c-0.2-0.7-0.5-1.4-0.8-2l1.8-2.3c0.2-0.2,0.1-0.5,0-0.7l-2.2-2.2c-0.2-0.2-0.5-0.2-0.7,0  l-2.3,1.8c-0.6-0.4-1.3-0.6-2-0.8l-0.3-2.9C17,3.2,16.8,3,16.6,3h-3.1c-0.3,0-0.5,0.2-0.5,0.4l-0.3,2.9c-0.7,0.2-1.4,0.5-2,0.8  L8.3,5.4c-0.2-0.2-0.5-0.1-0.7,0L5.4,7.6c-0.2,0.2-0.2,0.5,0,0.7l1.8,2.3c-0.4,0.6-0.6,1.3-0.8,2l-2.9,0.3C3.2,13,3,13.2,3,13.4v3.1  c0,0.3,0.2,0.5,0.4,0.5l2.9,0.3c0.2,0.7,0.5,1.4,0.8,2l-1.8,2.3c-0.2,0.2-0.1,0.5,0,0.7l2.2,2.2c0.2,0.2,0.5,0.2,0.7,0l2.3-1.8  c0.6,0.4,1.3,0.6,2,0.8l0.3,2.9c0,0.3,0.2,0.4,0.5,0.4h3.1c0.3,0,0.5-0.2,0.5-0.4l0.3-2.9c0.7-0.2,1.4-0.5,2-0.8l2.3,1.8  c0.2,0.2,0.5,0.1,0.7,0l2.2-2.2c0.2-0.2,0.2-0.5,0-0.7l-1.8-2.3c0.4-0.6,0.6-1.3,0.8-2l2.9-0.3c0.3,0,0.4-0.2,0.4-0.5v-3.1  C27,13.2,26.8,13,26.6,12.9z M15,19c-2.2,0-4-1.8-4-4c0-2.2,1.8-4,4-4s4,1.8,4,4C19,17.2,17.2,19,15,19z"/>
        </svg>
      </button>
    </div>
  </div>
  <div v-if="isShowingSetting" class="setting" v-click-outside="close">
    <div class="setting-title">LLM服务设置</div>
    <div class="setting-item">
      <label for="baseUrlInput">API基础地址:</label>
      <input 
        id="baseUrlInput"
        :value="baseUrl"
        type="text" 
        placeholder="请输入API基础地址"
        class="setting-input"
        @input="onUrlChange"
      >
    </div>
    <div class="setting-item">
      <label for="modelInput">模型名称:</label>
      <input 
        id="modelInput"
        :value="model"
        type="text" 
        placeholder="请输入模型名称"
        class="setting-input"
        @input="onModelChange"
      >
    </div>
    <div class="setting-item">
      <label for="modelInput">API Key请设置为环境变量:</label>
      <h5>DASHSCOPE_API_KEY</h5>
    </div>
  </div>
</template>

<style scoped>
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.chat-header h2 {
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 20px;
  color: #303133;
}

/* 多会话UI样式 */
.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn{
  padding: 5px;
  background-color: #f0f0f0;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn:hover{
  background-color: #e6e6e6;
}

.setting {
  position: absolute;
  top: 60px;
  right: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 20px;
  width: 300px;
  z-index: 1000;
  background-color: #f8f9fa;
}

.setting-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #303133;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #dcdfe6;
}

.setting-item {
  margin-bottom: 15px;
}

.setting-item label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #606266;
}

.setting-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.setting-input:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

</style>