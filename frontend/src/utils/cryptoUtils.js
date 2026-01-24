import CryptoJS from 'crypto-js';

const SECRET_KEY = 'agent-analytics-secret-key'; // 实际应用中应该从环境变量或其他安全位置获取

/**
 * 加密密码
 * @param {string} password - 要加密的密码
 * @returns {string} - 加密后的密码（Base64编码）
 */
export function encryptPassword(password) {
  try {
    return CryptoJS.AES.encrypt(password, SECRET_KEY).toString();
  } catch (error) {
    console.error('密码加密失败:', error);
    throw error;
  }
}

/**
 * 解密密码
 * @param {string} encryptedPassword - 加密的密码
 * @returns {string} - 解密后的密码
 */
export function decryptPassword(encryptedPassword) {
  try {
    const decrypted = CryptoJS.AES.decrypt(encryptedPassword, SECRET_KEY);
    return decrypted.toString(CryptoJS.enc.Utf8);
  } catch (error) {
    console.error('密码解密失败:', error);
    throw error;
  }
}