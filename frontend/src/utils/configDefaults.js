export const getDefaultConfigs = () => ({
  correlationMethod: 'pearson',
  wordcloudConfig: {
    color: ['#FF274B'],
    maxWords: 200,
    width: 1600,
    height: 900,
    backgroundColor: "#ffffff",
    maxFontSize: 200,
    minFontSize: 10,
    stopwords: [],
    maskShape: "default"
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
  }
})