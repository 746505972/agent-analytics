<template>
  <div class="neural-network-config">
    <h3>神经网络配置</h3>
    
    <!-- 方法描述 -->
    <div class="method-description">
      <p>神经网络 (Neural Network) 是一种受生物神经系统启发的机器学习模型，由多个相互连接的节点(神经元)组成。多层感知机(MLP)是一种前馈神经网络，适用于分类和回归任务。</p>
      <p class="formula">前向传播: a<sup>(l+1)</sup> = σ(W<sup>(l+1)</sup>a<sup>(l)</sup> + b<sup>(l+1)</sup>)</p>
      <p class="formula-desc">其中a<sup>(l)</sup>是第l层的激活值，W是权重矩阵，b是偏置向量，σ是非线性激活函数</p>
      <h4>主要特点：</h4>
      <ul>
        <li>强大的表达能力：能拟合复杂的非线性关系</li>
        <li>自动特征提取：能够从原始数据中学习有用特征</li>
        <li>通用逼近器：理论上可以逼近任何连续函数</li>
        <li>适应性强：可用于分类、回归等多种任务</li>
      </ul>
    </div>
    
    <!-- 任务类型选择 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">任务类型</label>
        <select 
          v-model="localConfig.task_type" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="auto">自动判断</option>
          <option value="classification">分类</option>
          <option value="regression">回归</option>
        </select>
      </div>
    </div>

    <!-- Y列选择 -->
    <div class="config-section" v-if="columns && columns.length > 0">
      <div class="form-group">
        <label class="section-title">因变量 (Y列)</label>
        <select 
          v-model="localConfig.y_column" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="">请选择</option>
          <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
        </select>
      </div>
    </div>
    
    <!-- 隐藏层结构 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">隐藏层结构</label>
        <input 
          type="text" 
          v-model="hiddenLayerSizesInput" 
          @blur="parseHiddenLayerSizes"
          class="form-control"
          placeholder="例如: 100,50,25 (表示3层分别有100,50,25个节点)"
        />
        <p class="form-help-text">定义神经网络隐藏层的结构，每层节点数量用逗号分隔</p>
      </div>
    </div>

    <!-- 激活函数 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">激活函数</label>
        <select v-model="localConfig.activation" class="form-control" @change="updateConfig">
          <option value="relu">ReLU (修正线性单元)</option>
          <option value="tanh">Tanh (双曲正切)</option>
          <option value="logistic">Logistic/Sigmoid (逻辑斯蒂)</option>
          <option value="identity">Identity (恒等)</option>
        </select>
        <p class="form-help-text">激活函数引入非线性特性，帮助网络学习复杂模式。ReLU通常效果较好且计算快，Tanh输出范围为[-1,1]，Sigmoid适合二分类输出</p>
      </div>
    </div>

    <!-- 求解器 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">求解器</label>
        <select v-model="localConfig.solver" class="form-control" @change="updateConfig">
          <option value="adam">Adam (自适应矩估计)</option>
          <option value="lbfgs">L-BFGS (有限内存BFGS)</option>
          <option value="sgd">SGD (随机梯度下降)</option>
        </select>
        <p class="form-help-text">求解器用于优化网络权重。Adam适合大多数情况，L-BFGS适合小数据集，SGD简单但可能较慢</p>
      </div>
    </div>

    <!-- 模型参数配置 -->
    <div class="config-section">
      <h4>模型参数</h4>
      
      <div class="form-group">
        <label class="section-title">L2正则化参数 (alpha)</label>
        <input 
          type="number" 
          step="0.0001" 
          v-model.number="localConfig.alpha" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 0.0001"
        />
        <p class="form-help-text">L2正则化参数，控制权重衰减强度，防止过拟合。值越大正则化越强</p>
      </div>

      <div class="form-group">
        <label class="section-title">最大迭代次数</label>
        <input 
          type="number" 
          v-model.number="localConfig.max_iter" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 200"
        />
        <p class="form-help-text">算法收敛前的最大迭代次数。如果算法不能收敛，请增加此参数</p>
      </div>

      <div class="form-group">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="localConfig.early_stopping" 
            @change="updateConfig"
          />
          启用早停机制
        </label>
        <p class="form-help-text">当验证分数停止改善时提前停止训练，防止过拟合</p>
      </div>

      <div class="form-group" v-if="localConfig.early_stopping">
        <label class="section-title">验证集比例</label>
        <input 
          type="number" 
          step="0.01" 
          min="0.1" 
          max="0.5" 
          v-model.number="localConfig.validation_fraction" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 0.1"
        />
        <p class="form-help-text">用作验证集的数据比例，用于监控早停条件</p>
      </div>

      <div class="form-group">
        <label class="section-title">初始学习率</label>
        <input 
          type="number" 
          step="0.001" 
          v-model.number="localConfig.learning_rate_init" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 0.001"
        />
        <p class="form-help-text">优化算法的初始学习率。对于adaptive求解器，学习率会自适应调整</p>
      </div>

      <div class="form-group">
        <label class="section-title">随机种子</label>
        <input 
          type="number" 
          v-model.number="localConfig.random_state" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 42"
        />
        <p class="form-help-text">设置随机种子以确保结果可重现</p>
      </div>
    </div>

    <!-- 高级参数配置 -->
    <div class="config-section">
      <h4>高级参数</h4>

      <div class="form-group">
        <label class="section-title">批量大小 (batch_size)</label>
        <input 
          type="text" 
          v-model="localConfig.batch_size" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: auto"
        />
        <p class="form-help-text">每个批次的样本数量。'auto'表示为min(200, n_samples)。较小的批次可能提高泛化能力，较大的批次加快训练速度</p>
      </div>

      <div class="form-group">
        <label class="section-title">学习率调度策略</label>
        <select v-model="localConfig.learning_rate" class="form-control" @change="updateConfig">
          <option value="constant">常数 (constant)</option>
          <option value="invscaling">逆缩放 (invscaling)</option>
          <option value="adaptive">自适应 (adaptive)</option>
        </select>
        <p class="form-help-text">学习率如何随时间变化。'constant'保持初始学习率，'invscaling'逐步降低，'adaptive'在训练停滞时降低</p>
      </div>

      <div class="form-group">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="localConfig.shuffle" 
            @change="updateConfig"
          />
          是否打乱样本顺序
        </label>
        <p class="form-help-text">是否在每次迭代后打乱训练数据。通常建议启用以提高模型稳定性</p>
      </div>

      <div class="form-group">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="localConfig.verbose" 
            @change="updateConfig"
          />
          显示训练进度
        </label>
        <p class="form-help-text">是否在训练过程中输出详细信息。调试时有用，但可能影响性能</p>
      </div>

      <div class="form-group">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="localConfig.warm_start" 
            @change="updateConfig"
          />
          温启动
        </label>
        <p class="form-help-text">是否使用前一次训练结果作为初始化。对增量训练有用</p>
      </div>

      <div class="form-group" v-if="localConfig.solver === 'sgd' || localConfig.solver === 'adam'">
        <label class="section-title">动量系数 (momentum)</label>
        <input 
          type="number" 
          step="0.01" 
          min="0" 
          max="1" 
          v-model.number="localConfig.momentum" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 0.9"
        />
        <p class="form-help-text">SGD和Adam求解器的动量系数，用于加速收敛并减少震荡。仅在SGD和Adam求解器时有效</p>
      </div>

      <div class="form-group" v-if="localConfig.solver === 'sgd'">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="localConfig.nesterovs_momentum" 
            @change="updateConfig"
          />
          启用Nesterov动量
        </label>
        <p class="form-help-text">是否使用Nesterov动量法。仅在SGD求解器时有效</p>
      </div>

      <div class="form-group" v-if="localConfig.solver === 'adam'">
        <label class="section-title">Adam参数 β₁</label>
        <input 
          type="number" 
          step="0.01" 
          min="0" 
          max="1" 
          v-model.number="localConfig.beta_1" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 0.9"
        />
        <p class="form-help-text">Adam求解器中梯度平方指数衰减率。仅在Adam求解器时有效</p>
      </div>

      <div class="form-group" v-if="localConfig.solver === 'adam'">
        <label class="section-title">Adam参数 β₂</label>
        <input 
          type="number" 
          step="0.001" 
          min="0" 
          max="1" 
          v-model.number="localConfig.beta_2" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 0.999"
        />
        <p class="form-help-text">Adam求解器中梯度平方指数衰减率。仅在Adam求解器时有效</p>
      </div>

      <div class="form-group" v-if="localConfig.solver === 'adam'">
        <label class="section-title">Adam参数 ε (epsilon)</label>
        <input 
          type="number" 
          step="1e-9" 
          v-model.number="localConfig.epsilon" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 1e-8"
        />
        <p class="form-help-text">Adam求解器中用于数值稳定的小常数。仅在Adam求解器时有效</p>
      </div>

      <div class="form-group">
        <label class="section-title">无改善最大迭代次数</label>
        <input 
          type="number" 
          v-model.number="localConfig.n_iter_no_change" 
          class="form-control"
          @input="updateConfig"
          placeholder="默认: 10"
        />
        <p class="form-help-text">早停机制中，当验证分数不再改善时的最大迭代次数阈值</p>
      </div>

      <div class="form-group">
        <label class="section-title">其他神经网络参数 (JSON格式)</label>
        <textarea 
          v-model="localConfig.params" 
          class="form-control"
          placeholder='例如: {"power_t": 0.5, "eta0": 0.01}'
          @input="updateParams"
          rows="4"
        ></textarea>
        <p class="form-help-text">以JSON格式输入其他神经网络参数</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NeuralNetworkConfig',
  props: {
    config: {
      type: Object,
      required: true
    },
    columns: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:config'],
  data() {
    return {
      localConfig: { ...this.config },
      hiddenLayerSizesInput: this.config.hidden_layer_sizes.join(',')
    };
  },
  mounted() {
    this.parseHiddenLayerSizes();
  },
  methods: {
    parseHiddenLayerSizes() {
      try {
        const sizes = this.hiddenLayerSizesInput.split(',').map(s => parseInt(s.trim()));
        if (sizes.length > 0 && sizes.every(size => !isNaN(size) && size > 0)) {
          this.localConfig.hidden_layer_sizes = sizes;
          this.updateConfig();
        } else {
          console.warn('Invalid hidden layer sizes input');
        }
      } catch (e) {
        console.warn('Error parsing hidden layer sizes:', e);
      }
    },
    updateConfig() {
      // 更新隐藏层输入框
      this.hiddenLayerSizesInput = this.localConfig.hidden_layer_sizes.join(',');
      
      this.$emit('update:config', {
        ...this.localConfig,
        hidden_layer_sizes: [...this.localConfig.hidden_layer_sizes]
      });
    }
  },
  watch: {
    config: {
      handler(newConfig) {
        this.localConfig = { ...newConfig };
        this.hiddenLayerSizesInput = newConfig.hidden_layer_sizes.join(',');
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.neural-network-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.config-section {
  margin-bottom: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #606266;
}

.section-title {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #409eff;
}

.method-description {
  background-color: #f5f5f5;
  border-left: 4px solid #409eff;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.method-description p {
  margin: 0 0 5px 0;
}

.method-description .formula {
  font-family: 'Cambria Math', 'Arial Unicode MS', serif;
  margin: 5px 0;
}

.method-description .formula-desc {
  font-size: 12px;
  color: #888;
  margin: 0;
}

.method-description ul {
  margin: 5px 0;
  padding-left: 20px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin-right: 5px;
}

.form-help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}
</style>