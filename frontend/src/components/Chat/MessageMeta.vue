<script>
import {formatTime} from "@/utils/formatTime";

export default {
  name: "MessageMeta",
  methods: {formatTime},
  props: {
    message: {
      type: Object,
      required: true
    }
  }
}
</script>

<template>
  <div class="message-meta-info">
    <div v-if="message.details && Array.isArray(message.details)" class="details-tags">
      <span
        v-for="(detail, index) in message.details"
        :key="index"
        class="detail-tag"
      >
        {{ detail }}
      </span>
    </div>
    <div v-else-if="message.details" class="details-text">
      {{ message.details }}
    </div>
    <div v-if="message.createdAt" class="time-info">{{ formatTime(message.createdAt) }}</div>
  </div>
</template>

<style scoped>
/* 消息元信息样式 */
.message-meta-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
  flex-wrap: wrap;
}

.details-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.detail-tag {
  background-color: #f0f2f5;
  border: 1px solid #dcdfe6;
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 12px;
  color: #606266;
  line-height: 1.2;
}

.time-info {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  background-color: #f5f7fa;
  border-radius: 12px;
  padding: 2px 8px;
}

.details-text {
  font-size: 12px;
  color: #606266;
  padding: 2px 8px 2px 0;
}
</style>