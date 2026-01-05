<script>
export default {
  name: "DeleteHistoryItems"
}
</script>

<style scoped>
/* From Uiverse.io by cssbuttons-io */
button {
  width: 100px;
  height: 30px;
  cursor: pointer;
  display: flex;
  align-items: center;
  border: none;
  border-radius: 5px;
  box-shadow: 1px 1px 3px rgba(0,0,0,0.15);
  background: #ff6363;
  margin-right: 10px;
}

button, button span {
 transition: 200ms;
}

button .text {
 transform: translateX(10px);
 color: white;
 font-weight: bold;
}

button .icon {
 position: absolute;
 border-left: 1px solid #c41b1b;
 transform: translateX(70px);
 width: 30px;
 display: flex;
 align-items: center;
 justify-content: center;
}

button svg {
 width: 10px;
 fill: #eee;
}

button:hover {
 background: #ff4949;
}

button:hover .text {
 color: transparent;
}

button:hover .icon {
 width: 100px;
 border-left: none;
 transform: translateX(0);
}

button:focus {
 outline: none;
}

button:active .icon svg {
 transform: scale(0.8);
}
</style>

<template>
  <button class="noselect">
    <span class="text">分析历史</span>
    <span class="icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206 8.313 3.666 3.666 8.237-8.318 8.285 8.203z"></path></svg></span>
  </button>
</template>
