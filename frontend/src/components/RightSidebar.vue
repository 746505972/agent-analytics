<template>
  <div :class="['right-section', { collapsed: isCollapsed }]">
    <div class="collapse-toggle" @click="toggleCollapse">
      {{ isCollapsed ? '<' : '>' }}
    </div>
    <div v-show="!isCollapsed">
      <ChatAssistant 
        :selected-file="selectedFile"
        :files="files"
        @refresh-files="refreshFiles"
      />
    </div>
  </div>
</template>

<script>
import ChatAssistant from "@/components/ChatAssistant.vue";

export default {
  name: "RightSidebar",
  components: {
    ChatAssistant
  },
  props: {
    selectedFile: {
      type: String,
      default: null
    },
    files: {
      type: Array,
      default: () => []
    },
    isCollapsed: {
      type: Boolean,
      default: false
    }
  },
  emits: ['toggle-collapse', 'refresh-files'],
  methods: {
    toggleCollapse() {
      this.$emit('toggle-collapse');
    },
    refreshFiles() {
      this.$emit('refresh-files');
    }
  }
}
</script>

<style scoped>
.right-section {
  flex: 2 1 200px;
  padding-right: 10px;
  overflow-y: auto;
  max-height: 100%;
  position: relative;
  transition: all 0.3s ease;
}

.right-section.collapsed {
  flex: 0 0 20px;
  padding: 0;
}

.collapse-toggle {
  position: absolute;
  top: 25px;
  transform: translateY(-50%);
  width: 20px;
  height: 40px;
  background-color: #419fff;
  color: white;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  font-weight: bold;
}

@media (max-width: 768px) {
  .right-section {
    padding: 0 10px;
    max-height: none;
  }
}
</style>