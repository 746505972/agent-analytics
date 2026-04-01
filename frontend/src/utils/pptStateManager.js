/**
 * PPT 状态管理工具
 * 用于保存和恢复 PPT 演示页面的状态
 */

const STORAGE_KEY = 'ppt_presentation_state'

export const pptState = {
  /**
   * 保存当前幻灯片索引
   * @param {number} slideIndex - 当前幻灯片索引
   */
  saveState(slideIndex) {
    try {
      const state = {
        currentSlide: slideIndex,
        timestamp: Date.now()
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
    } catch (error) {
      console.error('Failed to save PPT state:', error)
    }
  },

  /**
   * 恢复保存的幻灯片索引
   * @returns {number} 保存的幻灯片索引，如果没有则返回 0
   */
  restoreState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const state = JSON.parse(saved)
        // 检查是否是今天的记录（可选）
        const lastVisit = new Date(state.timestamp)
        const now = new Date()
        
        // 如果是同一天，恢复状态
        if (lastVisit.toDateString() === now.toDateString()) {
          return state.currentSlide || 0
        }
      }
    } catch (error) {
      console.error('Failed to restore PPT state:', error)
    }
    return 0
  },

  /**
   * 清除保存的状态
   */
  clearState() {
    try {
      localStorage.removeItem(STORAGE_KEY)
    } catch (error) {
      console.error('Failed to clear PPT state:', error)
    }
  }
}
