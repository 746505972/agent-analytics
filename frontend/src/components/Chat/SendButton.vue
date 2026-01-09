<template>
  <button 
    @click="onClick" 
    :disabled="disabled"
    class="send-button"
  >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 664 663">
      <path
        fill="none"
        d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
      ></path>
      <path
        stroke-linejoin="round"
        stroke-linecap="round"
        stroke-width="33.67"
        stroke="#6c6c6c"
        d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
      ></path>
    </svg>
  </button>
</template>

<script>
export default {
  name: "SendButton",
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onClick(event) {
      if (!this.disabled) {
        this.$emit('click', event);
      }
    }
  }
}
</script>

<style scoped>
.send-button {
  width: fit-content;
  height: 100%;
  background-color: transparent;
  outline: none;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  padding: 5px;
}

.send-button svg {
  height: 18px;
}

.send-button svg path {
  transition: all 0.3s;
  stroke: #606266;
}

.send-button:hover svg path {
  stroke: #409eff;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>