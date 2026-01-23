from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import MD5
import base64


def decrypt_password(encrypted_base64, password = "agent-analytics-secret-key"):
    """
    解密 CryptoJS AES 加密的数据

    CryptoJS.AES.encrypt() 默认使用:
    - AES-256-CBC
    - EVP_BytesToKey 密钥派生（MD5，1次迭代）
    - PKCS7 填充
    - 随机盐和 IV
    """
    try:
        # 1. Base64 解码
        encrypted_bytes = base64.b64decode(encrypted_base64)

        # 2. 检查是否是 Salted__ 格式
        if not encrypted_bytes.startswith(b'Salted__'):
            raise ValueError("不是有效的 CryptoJS 加密格式")

        # 3. 提取盐（8字节）
        salt = encrypted_bytes[8:16]
        ciphertext = encrypted_bytes[16:]

        # 4. 使用 EVP_BytesToKey 派生密钥和 IV（与 CryptoJS 兼容）
        # CryptoJS 使用 MD5 哈希函数
        def evp_bytes_to_key(password, salt, key_len=32, iv_len=16):
            """
            EVP_BytesToKey 实现，与 CryptoJS 兼容
            """
            dtot = MD5.new(password + salt).digest()
            d = [dtot]
            while len(dtot) < (key_len + iv_len):
                d.append(MD5.new(d[-1] + password + salt).digest())
                dtot += d[-1]
            return dtot[:key_len], dtot[key_len:key_len + iv_len]

        # 5. 派生密钥和 IV
        key, iv = evp_bytes_to_key(password.encode('utf-8'), salt)

        # 6. 创建解密器
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # 7. 解密
        decrypted_padded = cipher.decrypt(ciphertext)

        # 8. 移除 PKCS7 填充
        pad_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-pad_len]

        return decrypted.decode('utf-8')

    except Exception as e:
        print(f"解密错误: {e}")
        raise
