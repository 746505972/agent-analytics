<template>
  <div class="file-upload-wrapper">
    <label>
      <svg @click="onAddClick" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 337 337">
        <circle
          stroke-width="20"
          stroke="#6c6c6c"
          fill="none"
          r="158.5"
          cy="168.5"
          cx="168.5"
        ></circle>
        <path
          stroke-linecap="round"
          stroke-width="25"
          stroke="#6c6c6c"
          d="M167.759 79V259"
        ></path>
        <path
          stroke-linecap="round"
          stroke-width="25"
          stroke="#6c6c6c"
          d="M79 167.138H259"
        ></path>
      </svg>
      <span class="tooltip">添加历史</span>
    </label>
  </div>
</template>

<script>
export default {
  name: "FileUploadWrapper",
  methods: {
    onAddClick(event) {
      event.stopPropagation(); // 防止事件冒泡
      this.$emit('add-click');
    }
  }
}
</script>

<style scoped>
.file-upload-wrapper {
  width: fit-content;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Arial, Helvetica, sans-serif;
  padding: 5px;
}

.file-upload-wrapper label {
  cursor: pointer;
  width: fit-content;
  height: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.file-upload-wrapper label svg {
  height: 18px;
}

.file-upload-wrapper label svg path {
  transition: all 0.3s;
  stroke: #606266;
}

.file-upload-wrapper label svg circle {
  transition: all 0.3s;
  stroke: #606266;
}

.file-upload-wrapper label:hover svg path {
  stroke: #409eff;
}

.file-upload-wrapper label:hover svg circle {
  stroke: #409eff;
  fill: #f5f7fa;
}

.file-upload-wrapper label:hover .tooltip {
  display: block;
  opacity: 1;
}

.tooltip {
  position: absolute;
  top: -40px;
  display: none;
  opacity: 0;
  font-size: 10px;
  text-wrap: nowrap;
  background-color: #ffffff;
  padding: 6px 10px;
  border-radius: 5px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.596);
  transition: all 0.3s;
}
</style>