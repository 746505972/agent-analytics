<template>
  <form class="form" @submit.prevent="submitForm">
    <p class="title">数据库连接 </p>
    <p class="message">填写数据库连接信息以访问您的数据 </p>
    <label>
      <input
        v-model="dbConfig.host"
        class="input"
        type="text"
        placeholder=""
        required="">
      <span>主机地址</span>
    </label>

    <div class="flex">
      <label>
        <input
          v-model="dbConfig.port"
          class="input"
          type="text"
          placeholder=""
          required="">
        <span>端口</span>
      </label>

      <label>
        <input
          v-model="dbConfig.username"
          class="input"
          type="text"
          placeholder=""
          required="">
        <span>用户名</span>
      </label>
    </div>

    <label>
      <input
        v-model="dbConfig.password"
        class="input"
        type="password"
        placeholder=""
        required="">
      <span>密码</span>
    </label>

    <div class="flex">
      <label>
        <input
          v-model="dbConfig.database"
          class="input"
          type="text"
          placeholder=""
          required="">
        <span>数据库名称</span>
      </label>

      <label>
        <input
          v-model="dbConfig.table"
          class="input"
          type="text"
          placeholder=""
          required="">
        <span>表名</span>
      </label>
    </div>
    <button type="submit" class="submit">连接数据库</button>
    <p class="signin">需要重置表单? <a href="#" @click.prevent="resetForm">清空</a> </p>
  </form>
</template>

<script>
export default {
  name: "DBConnector",
  props: {
    dbConfig: {
      type: Object,
      required: true
    }
  },
  emits: ['update:dbConfig', 'connect-db'],
  methods: {
    submitForm() {
      this.$emit('connect-db', this.dbConfig);
    },
    resetForm() {
      const defaultConfig = {
        type: 'mysql',
        host: '',
        port: '',
        username: '',
        password: '',
        database: '',
        table: ''
      };
      this.$emit('update:dbConfig', defaultConfig);
    },
  },
  watch: {
    dbConfig: {
      handler(newVal) {
        this.$emit('update:dbConfig', newVal);
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 350px;
  padding: 20px;
  border-radius: 20px;
  position: relative;
  border: 1px solid rgba(144, 147, 153, 0.4);
}

.title {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -1px;
  position: relative;
  display: flex;
  align-items: center;
  padding-left: 30px;
  color: #00bfff;
}

.title::before {
  width: 18px;
  height: 18px;
}

.title::after {
  width: 18px;
  height: 18px;
  animation: pulse 1s linear infinite;
}

.title::before,
.title::after {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  border-radius: 50%;
  left: 0;
  background-color: #00bfff;
}

.message,
.signin {
  font-size: 14px;
}

.signin {
  text-align: center;
}

.signin a:hover {
  text-decoration: underline royalblue;
}

.signin a {
  color: #00bfff;
}

.flex {
  display: flex;
  width: 100%;
  gap: 6px;
}

.form label {
  position: relative;
}

.form label .input {
  width: 100%;
  padding: 20px 05px 05px 10px;
  outline: 0;
  border: 1px solid rgba(105, 105, 105, 0.397);
  border-radius: 10px;
}

.form label .input + span {
  position: absolute;
  left: 10px;
  top: 0;
  font-size: 0.9em;
  cursor: text;
  transition: 0.3s ease;
}

.form label .input:placeholder-shown + span {
  top: 12px;
  font-size: 0.9em;
}

.form label .input:focus + span,
.form label .input:valid + span {
  color: #00bfff;
  top: 0;
  font-size: 0.7em;
  font-weight: 600;
}

.input {
  font-size: medium;
}

.submit {
  border: none;
  outline: none;
  padding: 10px;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  transform: translateY(-1px);
  background-color: #00bfff;
}

.submit:hover {
  background-color: #00bfff96;
}

@keyframes pulse {
  from {
    transform: scale(0.9);
    opacity: 1;
  }

  to {
    transform: scale(1.8);
    opacity: 0;
  }
}
</style>
