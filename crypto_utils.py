from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_data(data, key):
    """Encripta los datos usando AES-CBC."""
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext).decode()

def decrypt_data(encrypted_data, key):
    """Desencripta los datos usando AES-CBC."""
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size).decode()
    except (ValueError, KeyError) as e:
        # Retornamos None si la clave es incorrecta o los datos están corruptos
        return None
