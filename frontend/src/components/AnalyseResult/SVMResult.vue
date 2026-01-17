<template>
  <div class="svm-result-container" v-if="datasetDetails.resultMethod">
    <!-- 方法标题 -->
    <h3 class="method-title">
      {{
        datasetDetails.method === 'svm_classification' ? '支持向量机分类 (SVM Classification)' : '支持向量机回归 (SVM Regression)'
      }}
    </h3>

    <!-- 任务类型信息 -->
    <div class="info-section">
      <h4>任务信息</h4>
      <div class="info-grid">
        <div class="info-item">
          <label>任务类型:</label>
          <span>{{ datasetDetails.task_type }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.x_columns && datasetDetails.x_columns.length">
          <label>特征列:</label>
          <span>{{ datasetDetails.x_columns.join(', ') }}</span>
        </div>
        <div class="info-item">
          <label>目标列:</label>
          <span>{{ datasetDetails.y_column }}</span>
        </div>
        <div class="info-item">
          <label>样本数量:</label>
          <span>{{ datasetDetails.sample_size }}</span>
        </div>
      </div>
    </div>

    <!-- 模型参数信息 -->
    <div class="info-section">
      <h4>模型参数</h4>
      <div class="info-grid">
        <div class="info-item">
          <label>核函数:</label>
          <span>{{ datasetDetails.model_params.kernel }}</span>
        </div>
        <div class="info-item">
          <label>C (正则化参数):</label>
          <span>{{ datasetDetails.model_params.C }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.model_params.gamma">
          <label>Gamma:</label>
          <span>{{ datasetDetails.model_params.gamma }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.model_params.degree !== undefined">
          <label>多项式度数:</label>
          <span>{{ datasetDetails.model_params.degree }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.model_params.coef0 !== undefined">
          <label>Coefficient 0:</label>
          <span>{{ datasetDetails.model_params.coef0 }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.model_params.tol !== undefined">
          <label>容忍度:</label>
          <span>{{ datasetDetails.model_params.tol }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.model_params.max_iter !== undefined">
          <label>最大迭代次数:</label>
          <span>{{ datasetDetails.model_params.max_iter }}</span>
        </div>
      </div>
    </div>

    <!-- 分类特有信息 -->
    <div v-if="datasetDetails.method === 'svm_classification'" class="info-section">
      <h4>分类信息</h4>
      <div class="info-grid">
        <div class="info-item">
          <label>类别数量:</label>
          <span>{{ datasetDetails.n_classes }}</span>
        </div>
        <div class="info-item">
          <label>类别标签:</label>
          <span>{{ datasetDetails.class_labels ? datasetDetails.class_labels.join(', ') : '' }}</span>
        </div>
        <div class="info-item">
          <label>支持向量数量:</label>
          <span>{{ datasetDetails.support_vectors_count }}</span>
        </div>
        <div class="info-item" v-if="datasetDetails.n_support_vectors_per_class">
          <label>各类别支持向量数:</label>
          <span>{{ datasetDetails.n_support_vectors_per_class.join(', ') }}</span>
        </div>
      </div>
    </div>

    <!-- 回归特有信息 -->
    <div v-else-if="datasetDetails.method === 'svm_regression'" class="info-section">
      <h4>回归信息</h4>
      <div class="info-grid">
        <div class="info-item">
          <label>支持向量数量:</label>
          <span>{{ datasetDetails.support_vectors_count }}</span>
        </div>
      </div>
    </div>

    <!-- 评估指标 -->
    <div class="info-section">
      <h4>评估指标</h4>
      <div class="info-grid">
        <!-- 分类评估指标 -->
        <div v-if="datasetDetails.method === 'svm_classification'">
          <div class="info-item">
            <label>准确率 (Accuracy):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.accuracy) }}</span>
          </div>
          <div class="info-item">
            <label>精确率 (Precision):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.precision) }}</span>
          </div>
          <div class="info-item">
            <label>召回率 (Recall):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.recall) }}</span>
          </div>
          <div class="info-item">
            <label>F1分数:</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.f1_score) }}</span>
          </div>
          <div v-if="datasetDetails.evaluation_metrics.precision_micro !== null" class="info-item">
            <label>精确率 (Micro平均):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.precision_micro) }}</span>
          </div>
          <div v-if="datasetDetails.evaluation_metrics.recall_micro !== null" class="info-item">
            <label>召回率 (Micro平均):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.recall_micro) }}</span>
          </div>
          <div v-if="datasetDetails.evaluation_metrics.f1_micro !== null" class="info-item">
            <label>F1分数 (Micro平均):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.f1_micro) }}</span>
          </div>
        </div>
        <!-- 回归评估指标 -->
        <div v-else-if="datasetDetails.method === 'svm_regression'">
          <div class="info-item">
            <label>均方误差 (MSE):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.mse) }}</span>
          </div>
          <div class="info-item">
            <label>均方根误差 (RMSE):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.rmse) }}</span>
          </div>
          <div class="info-item">
            <label>R² 分数:</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.r2_score) }}</span>
          </div>
          <div class="info-item">
            <label>平均绝对误差 (MAE):</label>
            <span>{{ formatMetric(datasetDetails.evaluation_metrics.mae) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 模型解释 -->
    <div class="info-section">
      <h4>模型解释</h4>
      <div class="explanation">
        <p>
          <strong>SVM (支持向量机)</strong> 是一种监督学习模型，主要用于分类和回归分析。
          它通过寻找最优超平面来最大化不同类别之间的间隔，从而进行分类或回归预测。
        </p>
        <ul>
          <li>
            <strong>核函数</strong>: 决定了如何将输入空间映射到高维特征空间。
            <em>Linear</em> 适用于线性可分数据，<em>RBF</em> 适用于非线性数据。
          </li>
          <li>
            <strong>C参数</strong>: 控制对误分类的惩罚程度。较大的C值会减少误分类但可能导致过拟合。
          </li>
          <li>
            <strong>Gamma</strong>: 仅用于RBF/polynomial/sigmoid核，定义单个训练样本的影响范围。
          </li>
          <li>
            <strong>支持向量</strong>: 是最接近决策边界的训练样本点，它们决定了最终的决策边界。
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SVMResult',
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatMetric(value) {
      if (value === null || value === undefined) {
        return 'N/A';
      }
      // 如果是数字，格式化为保留4位小数
      if (typeof value === 'number') {
        return value.toFixed(4);
      }
      return value;
    }
  }
};
</script>

<style scoped>
.svm-result-container {
  padding: 20px;
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

.method-title {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.info-section {
  margin-bottom: 25px;
}

.info-section h4 {
  color: #34495e;
  margin-bottom: 15px;
  border-left: 4px solid #3498db;
  padding-left: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 12px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-weight: bold;
  color: #555;
  margin-bottom: 4px;
  font-size: 0.9em;
}

.info-item span {
  background-color: white;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
  color: #333;
}

.explanation {
  background-color: #e8f4fd;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.explanation p {
  margin: 0 0 10px 0;
}

.explanation ul {
  margin: 0;
  padding-left: 20px;
}

.explanation li {
  margin-bottom: 8px;
}

.explanation em {
  font-weight: bold;
  color: #2980b9;
}
</style>