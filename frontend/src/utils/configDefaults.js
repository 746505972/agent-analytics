export const getDefaultConfigs = () => ({
  interpolationConfig:{
    interpolationMethod: 'linear',
    fillValue: '',
    knnNeighbors: 5,
  },
  invalidSamplesConfig: {
    // 无效样本参数
    removeDuplicates: false,
    removeDuplicatesCols: false,
    removeConstantCols: false,
    rowMissingThreshold: 1,
    columnMissingThreshold: 1,
  },
  correlationMethod: 'pearson',
  wordcloudConfig: {
    color: ['#FF274B'],
    maxWords: 200,
    width: 630,
    height: 450,
    minFontSize: 12,
    maxFontSize: 60,
    wordGap: 20,
    rotateStep: 45,
    shape: "circle",
    stopwords: []
  },
  sentimentConfig: {
    stopwords: [],
    internetSlang: {}
  },
  tTestConfig: {
    testType: 'one_sample',
    alpha: 0.05,
    popmean: 0,
    groupCol: '',
    equalVar: true,
    normalityMethod: 'shapiro'
  },
  normalityTestConfig: {
    method: 'shapiro',
    alpha: 0.05,
    groupBy: ''
  },
  fTestConfig: {
    groupBy: '',
    alpha: 0.05
  },
  chiSquareTestConfig: {
    groupBy: '',
    alpha: 0.05
  },
  nonParametricTestConfig: {
    testType: 'mannwhitney',
    groupBy: '',
    alpha: 0.05,
    alternative: 'two-sided',
    distribution: 'norm'
  },
  linearRegressionConfig: {
    y_column: '',
    method: 'ols',
    alpha: 1.0,
    l1_ratio: 0.5,
    params: {
      max_iter: 1000,
      tol: 0.0001,
      fit_intercept: true
    }
  },
  logisticRegressionConfig: {
    y_column: '',
    method: 'logistic',
    solver: 'lbfgs',
    params: {
      C: 1.0,
      max_iter: 1000,
      tol: 0.0001,
      fit_intercept: true,
      class_weight: null
    }
  },
  clusteringConfig: {
    method: 'kmeans',
    n_clusters: 3,
    params: {
      standardize: true,
      init: 'k-means++',
      max_iter: 300,
      eps: 0.5,
      min_samples: 5,
      linkage: 'ward',
      covariance_type: 'full'
    }
  },
  xgboostConfig: {
    y_column: '',
    task_type: 'auto',
    objective: '',
    n_estimators: 100,
    max_depth: 6,
    learning_rate: 0.3,
    subsample: 1.0,
    colsample_bytree: 1.0,
    random_state: 42,
    params: {}
  },
  svmConfig: {
    y_column: '',
    task_type: 'classification',
    kernel: 'rbf',
    C: 1.0,
    gamma: 'scale',
    degree: 3,
    coef0: 0.0,
    shrinking: true,
    probability: true,
    tol: 0.001,
    max_iter: -1,
    params: {}
  },
  decisionTreeConfig: {
    y_column: '',
    task_type: 'auto',
    criterion: '',
    max_depth: null,
    min_samples_split: 2,
    min_samples_leaf: 1,
    max_features: '',
    random_state: 42,
    params: {}
  }
})