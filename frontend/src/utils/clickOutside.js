export default {
  mounted(el, binding, vnode) {
    // 确保元素已经被添加到DOM中
    setTimeout(() => {
      el.clickOutsideEvent = function(event) {
        // 检查点击的元素是否在当前元素内部
        if (!(el === event.target || el.contains(event.target))) {
          // 检查绑定的值是否为函数
          const handler = binding.value;
          if (typeof handler === 'function') {
            // 调用绑定的方法
            handler(event);
          }
        }
      };
      // 将事件监听器添加到 document 上
      document.addEventListener('click', el.clickOutsideEvent);
    }, 0);
  },
  unmounted(el) {
    // 解除事件监听器
    if (el.clickOutsideEvent) {
      document.removeEventListener('click', el.clickOutsideEvent);
    }
  }
};