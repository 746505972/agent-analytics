export async function checkServerStatus() {
      // 检查后端是否启动
      const maxRetries = 5; // 最大重试次数，最多等待60秒
      const retryInterval = 1000; // 重试间隔1000毫秒

      let retries = 0;

      while (this.isWaitingForServer && retries < maxRetries) {
        try {
          const response = await fetch('http://localhost:8000/', {
            method: 'GET',
            mode: 'cors', // 启用CORS
            cache: 'no-cache' // 不使用缓存
          });

          if (response.ok) {
            this.isWaitingForServer = false;
            break;
          }
        } catch (error) {
          console.debug('尝试连接后端服务...', error.message);
        }

        retries++;

        // 等待一段时间再重试
        await new Promise(resolve => setTimeout(resolve, retryInterval));
      }

      if (this.isWaitingForServer) {
        alert('警告：后端服务可能未启动或无法访问');
        // 即使后端未启动也允许继续，不阻塞UI
        this.isWaitingForServer = false;
      }
    }