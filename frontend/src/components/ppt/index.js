/**
 * PPT 组件统一导出
 */

import TitleSlide from './TitleSlide.vue'
import ThankYouSlide from './ThankYouSlide.vue'
import ResearchBackgroundSlide from './ResearchBackgroundSlide.vue'
import ResearchObjectivesSlide from './ResearchObjectivesSlide.vue'
import TechnologiesSlide from './TechnologiesSlide.vue'
import SystemArchitectureSlide from './SystemArchitectureSlide.vue'
import AgentMechanismSlide from './AgentMechanismSlide.vue'
import AnalysisToolsSlide from './AnalysisToolsSlide.vue'
// import ReportGenerationSlide from './ReportGenerationSlide.vue'
import ImplementationSlide from './ImplementationSlide.vue'
import ExperimentsSlide from './ExperimentsSlide.vue'
import LimitationsSlide from './LimitationsSlide.vue'
import ConclusionSlide from './ConclusionSlide.vue'
import StyleDemoSlide from './StyleDemoSlide.vue'

export { TitleSlide }
export { ThankYouSlide }
export { ResearchBackgroundSlide }
export { ResearchObjectivesSlide }
export { TechnologiesSlide }
export { SystemArchitectureSlide }
export { AgentMechanismSlide }
export { AnalysisToolsSlide }
// export { ReportGenerationSlide }
export { ImplementationSlide }
export { ExperimentsSlide }
export { LimitationsSlide }
export { ConclusionSlide }
export { StyleDemoSlide }

/**
 * PPT 幻灯片配置数组 - 按论文答辩框架组织
 * 共 12 页：封面 → 背景 → 目标→技术→架构→Agent 机制→工具→报告→实现→实验→局限→总结
 */
export const slidesConfig = [
  { component: TitleSlide, name: 'title' },                    // 1. 封面
  { component: ResearchBackgroundSlide, name: 'background' },  // 2. 研究背景与问题
  { component: ResearchObjectivesSlide, name: 'objectives' },  // 3. 研究目标与贡献
  { component: TechnologiesSlide, name: 'technologies' },      // 4. 相关技术
  { component: ImplementationSlide, name: 'implementation' },  // 9. 系统实现与界面
  { component: SystemArchitectureSlide, name: 'architecture' },// 5. 系统总体架构
  { component: AgentMechanismSlide, name: 'agent-mechanism' }, // 6. Agent 决策机制
  { component: AnalysisToolsSlide, name: 'tools' },            // 7. 数据分析工具设计
  // { component: ReportGenerationSlide, name: 'report-generation' }, // 8. 报告生成方法
  { component: ExperimentsSlide, name: 'experiments' },        // 10. 实验与效果分析
  { component: LimitationsSlide, name: 'limitations' },        // 11. 系统局限性
  { component: ConclusionSlide, name: 'conclusion' },          // 12. 总结与展望
  { component: ThankYouSlide, name: 'thank-you' }           // 13. 致谢
]
